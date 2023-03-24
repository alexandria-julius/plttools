""" elt Calculator
ELT calculator functions
"""
import numpy
import math
import pandas as pd
import numpy as np
from scipy.fft import fft, ifft
from scipy.stats import beta
from aggregationtools import ELT, ep_curve


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
        elt.at[index] = row

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

