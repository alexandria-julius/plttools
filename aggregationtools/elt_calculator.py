""" elt Calculator
ELT calculator functions
"""
import logging

import numpy
import math
import pandas as pd
import numpy as np
# import tensorflow as tf
# import tensorflow_probability as tfp

from scipy.fft import fft, ifft
from scipy.stats import beta
from aggregationtools import ELT, ep_curve

logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)

def calculate_oep_curve(elt, grid_size=2**14, max_loss_factor=5):
    """ This function calculates the OEP of a given ELT
    ----------
    elt : pandas dataframe containing PLT
    grid_size: grid size used for ep calculations
    max_loss_factor: factor used to extimate max loss

    Returns
    -------
    EPCurve :
         exceedance probability curve

    """
    elt_lambda = ELT(elt).get_lambda()
    severity_distribution, severity_density_function = calculate_severity_distribution(elt, grid_size, max_loss_factor)
    severity_distribution['OEP'] = 1 - numpy.exp(-elt_lambda * severity_distribution['CEP'])
    oep = severity_distribution.rename(columns={'OEP': 'Probability', 'threshold': 'Loss'})

    return ep_curve.EPCurve(oep, ep_type=ep_curve.EPType.OEP)


def calculate_tce_oep_curve(oep):
    """ This function calculates the TCE OEP of a given ELT
    ----------
    oep : OEP curve, this is part of the new calculation provided by the functional team, the oep needs to be calculated using calculate_oep_curve_new function

    Returns
    -------
    EPCurve :
         exceedance probability curve

    """
    tce_oep = oep.curve.reset_index().rename(columns={'Probability': 'ep', 'Loss': 'oep_loss'}).sort_values(by='ep')
    tce_oep['delta'] = -0.5 * (tce_oep['oep_loss'] - tce_oep['oep_loss'].shift(1)) * (tce_oep['ep'] + tce_oep['ep'].shift(1))
    tce_oep['delta'] = tce_oep['delta'].fillna(0)
    tce_oep['sigma_delta'] = tce_oep['delta'].cumsum()
    tce_oep['loss'] = (tce_oep['sigma_delta'] / tce_oep['ep']) + tce_oep['oep_loss']
    tce_oep = tce_oep[['ep', 'loss']].rename(columns={'ep': 'Probability', 'loss': 'Loss'})

    return ep_curve.EPCurve(tce_oep, ep_type=ep_curve.EPType.TCE_OEP)

def calculate_oep_curve_new(elt):
    """ This function calculates the OEP of a given ELT, this new calculation provided by the funtional team based on the Risk Modeler output
    ----------
    elt : pandas dataframe containing ELT

    Returns
    -------
    EPCurve :
         exceedance probability curve

    """
    logger.info('Starting OEP curve calculation')
    elt_lambda = ELT(elt).get_lambda()
    elt = elt.rename(columns={'Loss': 'Mean'}).sort_values(by='Mean', ascending=False)
    elt['aal'] = elt['Mean'] * elt['Rate']
    elt['wtd_mu'] = elt['aal'] * elt['mu']
    elt['agg_var'] = elt['Rate'] * (elt['Mean'] ** 2 + elt['StandardDev'] ** 2)

    elt['alpha'] = (1 - elt['mu']) / (elt['StandardDev'] / elt['Mean']) ** 2 - elt['mu']
    elt['alpha'] = numpy.where(elt['alpha'] <= 0, 0.000001, elt['alpha'])

    elt['alpha'] = np.where(elt['beta'] == 0.000001, np.where(elt['Mean'] / elt['ExpValue'] > 0.999999,
                                          0.00999999, (elt['mu'] * elt['beta']) / (1 - elt['mu'])), elt['alpha'])

    elt['sev_skew'] = (2 * (elt['beta'] - elt['alpha'])) / ((2 * elt['alpha']) + elt['beta']) * np.sqrt((elt['alpha'] + elt['beta'] + 1) / (elt['alpha'] * elt['beta']))
    elt['agg_skew'] = elt['Rate'] * (((elt['StandardDev'] ** 3) * elt['sev_skew']) + (3 * elt['Mean'] * elt['StandardDev'] ** 2) + elt['Mean'] ** 3)

    aal = elt['aal'].sum()
    agg_var = elt['agg_var'].sum()
    agg_cv = np.sqrt(agg_var) / aal
    agg_skew = elt['agg_skew'].sum() / agg_var ** 1.5

    wtd_mu = elt['wtd_mu'].sum()

    if -10 ** -8 < agg_skew < 0:
        agg_skew = -10 ** -8
    elif 0 <= agg_skew < 10 ** -8:
        agg_skew = 10 ** -8

    positive_agg_skew = max(agg_skew, 10 ** -8)

    oal = 0
    diff_means = [_calculate_mean_diff(e, elt) for e in range(len(elt) - 1)]
    oal += sum(diff_means)
    oal += elt.iloc[-1]['Mean'] * (1 - np.exp(-elt_lambda))
    logger.info('Calculating first oep threshold')
    elt_oep = _oep_calculation(elt, elt['ExpValue'].max())
    logger.info('Finished first oep threshold calculation')

    rp_50k = np.interp(1 / 50000, elt_oep['oep'], elt_oep['perspvalue'])
    rp_50k = max(rp_50k, 10e-6)
    y_add = 0.324 * np.log(elt_lambda) + 20.494 * ((aal - oal) / rp_50k) + 1.922 * wtd_mu + 1.908 * np.log(agg_cv) - (0.430 / agg_skew) + 0.209
    max_add = max(1.1, y_add)
    y_mult = (elt_lambda ** - 0.057) * (((aal - oal) / rp_50k) ** 0.227) * (wtd_mu ** 0.135) * (agg_cv ** 0.149) * (positive_agg_skew ** 0.0158) * 12.126
    max_mult = max(1.1, y_mult)

    max_loss = min(max_add, max_mult) * rp_50k
    logger.info('Calculating second oep threshold')
    oep_curve = _oep_calculation(elt, max_loss)
    oep = oep_curve[['oep', 'perspvalue']].rename(columns={'oep': 'Probability', 'perspvalue': 'Loss'})
    logger.info('Finished OEP curve calculation')
    return ep_curve.EPCurve(oep, ep_type=ep_curve.EPType.OEP)

def _calculate_mean_diff(index, elt):
    diff_mean = elt.iloc[index]['Mean'] - elt.iloc[index + 1]['Mean']
    sum_rate = elt.iloc[:index + 1]['Rate'].sum()
    return diff_mean * (1 - np.exp(-sum_rate))

def _oep_calculation(elt, max_loss):
    """ This function calculates the OEP of a given ELT
    ----------
    elt : pandas dataframe containing ELT
    max_loss : maximum loss

    Returns
    -------
    out :
        exceedance probability curve
    """
    logger.info('_oep_calculation 1')
    thd = np.concatenate([np.linspace(0, max_loss * 1e-5, 1001)[:1000], np.linspace(max_loss * 1e-5, max_loss, 29000)])
    logger.info('_oep_calculation 2')
    thd = np.sort(thd)[::-1]

    logger.info('_oep_calculation 3')
    elt['alpha'] = ((elt['mu'] ** 2 * (1 - elt['mu'])) / elt['sigma'] ** 2) - elt['mu']
    logger.info('_oep_calculation 4')
    elt.loc[elt['alpha'] < 0, 'alpha'] = 10e-6
    logger.info('_oep_calculation 5')
    elt['beta'] = ((1 - elt['mu']) * elt['alpha']) / elt['mu']
    logger.info('_oep_calculation 6')
    elt.loc[elt['beta'] < 0, 'beta'] = 10e-6

    logger.info('_oep_calculation 7')
    x_subset = elt[elt['ExpValue'] >= thd.min()]
    logger.info('_oep_calculation 8')
    # temp = np.ndarray(shape=(30000,elt.shape[0]), dtype=float)

    thd_x = (thd[:, None] / x_subset['ExpValue'].values).astype(np.float32)
    logger.info('_oep_calculation 8.1')
    temp = beta.cdf(thd_x, x_subset['alpha'].values.astype(np.float32), x_subset['beta'].values.astype(np.float32))

    # use tensorflow to calculate the cdf
    # beta_dist = tfp.distributions.Beta(x_subset['alpha'].values, x_subset['beta'].values)
    # temp = beta_dist.cdf(thd[:, None] / x_subset['ExpValue'].values)

    logger.info('_oep_calculation 9')
    oep_value = 1 - np.exp(-np.sum((1 - temp) * x_subset['Rate'].values, axis=1))
    logger.info('_oep_calculation 10')
    oep = pd.DataFrame({'perspvalue': thd, 'oep': oep_value})
    logger.info('_oep_calculation 11')
    oep = oep.sort_values(by='perspvalue', ascending=False)
    return oep

def calculate_aep_curve(elt, grid_size=2**14, max_loss_factor=5):
    """ This function calculates the OEP of a given ELT
    ----------
    elt : pandas dataframe containing PLT
    grid_size: grid size used for ep calculations
    max_loss_factor: factor used to extimate max loss

    Returns
    -------
    EPCurve :
         exceedance probability curve

    """
    elt_lambda = ELT(elt).get_lambda()
    max_loss = _max_loss(elt, max_loss_factor)
    dx = max_loss / grid_size
    xx = np.arange(1, grid_size + 1) * dx

    severity_distribution, severity_density_function = calculate_severity_distribution(elt, grid_size, max_loss_factor)

    elt['dx'] = dx / elt['ExpValue']
    elt['xx'] = ''
    elt['FX'] = ''
    elt['FX2'] = ''
    fx2 = [0] * grid_size
    for index, row in elt.iterrows():
        row['xx'] = np.true_divide(xx, row['ExpValue'])
        row['FX'] = beta.cdf(row['xx'], row['alpha'], row['beta'])
        row['FX2'] = beta.cdf(row['xx'][0] - row['dx'] / 2, row['alpha'], row['beta'])
        cdf2 = beta.cdf(row['xx'][:-1] + row['dx'] / 2, row['alpha'], row['beta'])
        cdf1 = beta.cdf(row['xx'][:-1] - row['dx'] / 2, row['alpha'], row['beta'])
        row['FX2'] = np.insert(cdf2 - cdf1, 0, row['FX2'])
        fx2 = fx2 + (row['Rate'] / elt_lambda) * row['FX2']
        elt[index] = row

    fx_hat = fft(fx2)
    fs_hat = numpy.exp(-elt_lambda*(1 - fx_hat))
    fs = numpy.real(ifft(fs_hat, norm="forward") / grid_size)
    fs_cum = numpy.cumsum(fs)
    severity_density_function['AEP'] = 1 - fs_cum
    aep = severity_density_function.rename(columns={'AEP': 'Probability', 'threshold': 'Loss'})

    return ep_curve.EPCurve(aep, ep_type=ep_curve.EPType.AEP)


def calculate_frequency_distribution(elt):
    """ This function calculates the frequency distribution or the probability of having
    exactly n occurences in a year
    ----------
    elt : pandas dataframe containing ELT

    Returns
    -------
    frequency_distribution
    """
    elt_lambda = ELT(elt).get_lambda()
    max_freq = max(3, 1 + _poisson_inv(1 - 1 / 20000, elt_lambda))
    frequency_distribution = [_poisson_pdf(n, elt_lambda) for n in range(0, max_freq+1)]
    return frequency_distribution


def calculate_severity_distribution(elt, grid_size=2**14, max_loss_factor=5):
    """ This function calculates the severity distribution or the distribution
    of the size of losses, given that an event has occurred
    ----------
    elt : pandas dataframe containing ELT

    Returns
    -------
    severity_distribution
    """
    max_loss = _max_loss(elt, max_loss_factor=max_loss_factor)
    loss_thresholds = numpy.linspace(0, max_loss, num=grid_size+1)
    probability = {}
    CEP = {}

    for threshold in loss_thresholds:
        probability[threshold] = 1 - beta.cdf(threshold/elt['ExpValue'], elt['alpha'], elt['beta'])
        probability[threshold] = np.nan_to_num(probability[threshold])
        CEP[threshold] = sum(elt['Rate'] * probability[threshold]) / ELT(elt).get_lambda()

    severity_distribution = pd.DataFrame(CEP.items(), columns=['threshold', 'CEP'])
    severity_density_function = severity_distribution.copy(deep=True)
    severity_density_function['shift_CEP'] = severity_density_function['CEP'].shift(1)
    severity_density_function = severity_density_function[1:]
    severity_density_function['CEP'] = severity_density_function['shift_CEP'] - severity_density_function['CEP']
    severity_density_function.drop('shift_CEP', axis=1, inplace=True)

    return severity_distribution, severity_density_function


def group_elts(elt1, elt2=None):
    """ This function groups two elts together
    Parameters
    ----------
    elt1 : pandas dataframe containing ELT
    elt2 : pandas dataframe containing elt

    Returns
    -------
    elt :
        A pandas dataframe containing a elt

    """
    if elt2 is None:
        grouped_elt = elt1.elt
    else:
        grouped_elt = pd.concat([elt1.elt, elt2.elt], axis=0)

    elt_unique = grouped_elt[['EventId','Rate','Loss','StdDevI','StdDevC','ExpValue']].loc[~grouped_elt.duplicated(subset='EventId', keep=False), :]
    elt_matches = grouped_elt[['EventId','Rate','Loss','StdDevI','StdDevC','ExpValue']].loc[grouped_elt.duplicated(subset='EventId', keep=False), :]
    elt_matches = elt_matches.groupby(['EventId', 'Rate']).agg({
                             'Loss': 'sum',
                             'StdDevC': 'sum',
                             'ExpValue': 'sum',
                             'StdDevI': lambda x: np.sqrt((x*x).sum())}
            ).reset_index()
    concatenated_elt = pd.concat([elt_unique, elt_matches]).reset_index(drop=True)

    return ELT(concatenated_elt)


def _poisson_inv(pct, elt_lambda):
    if (elt_lambda <= 0) | (pct >= 1):
        return
    n = 0
    Pssn = 0
    while Pssn <= pct:
        Pssn = Pssn + _poisson_pdf(n, elt_lambda)
        n = n + 1
    return n - 1


def _poisson_pdf(n, elt_lambda):
    poisson_pdf = (math.exp(-elt_lambda)*elt_lambda**n)/math.factorial(n)
    return poisson_pdf


def _max_loss(elt, max_loss_factor=5):
    max_loss = max_loss_factor*elt['Loss'].max()
    return max_loss

