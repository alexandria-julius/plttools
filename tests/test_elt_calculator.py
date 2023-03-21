""" elt Calculator tests"""
# pylint: disable=line-too-long
import pandas as pd

from aggregationtools import elt_calculator, EPCurve, EPType
from aggregationtools.elt import ELT
import pytest
import numpy


def test_group_elts():
    """Group ELTs"""
    d_1 = {
        "EventId": [100, 200, 300, 400, 500, 600],
        "Loss": [51765, 30931, 3281, 21980, 19025, 84287],
        "StdDevI": [2591, 10482, 6019, 15272, 75853, 62429],
        "StdDevC": [67373, 13942, 12004, 49023, 58268, 181382],
        "ExpValue": [200000, 200000, 50000, 50000, 500000, 200000],
        "Rate": [0.000018, 0.00021, 0.000305, 0.000912, 0.000078, 0.000042]
    }
    d_2 = {
        "EventId": [100, 200, 350, 400, 526],
        "Loss": [16329, 19782, 27540, 76387, 44536],
        "StdDevI": [26826, 13335, 48962, 5052, 7441],
        "StdDevC": [18160, 4792, 17761, 4792, 22090],
        "ExpValue": [100000, 100000, 210000, 70000, 300000],
        "Rate": [0.000018, 0.00021, 0.000411, 0.000912, 0.000729]
    }
    grouped_elt = elt_calculator.group_elts(
        ELT(d_1), ELT(d_2)).elt

    assert grouped_elt.loc[grouped_elt['EventId'] == 100].Loss.sum() == 68094


def test_group_elts_single_input():
    """Group elts"""
    d_1 = {
        "EventId": [100, 200, 300, 400, 500, 600, 100, 200, 350, 400, 526],
        "Loss": [51765, 30931, 3281, 21980, 19025, 84287, 16329, 19782, 27540, 76387, 44536],
        "StdDevI": [2591, 10482, 6019, 15272, 75853, 62429, 26826, 13335, 48962, 5052, 7441],
        "StdDevC": [67373, 13942, 12004, 49023, 58268, 181382, 18160, 4792, 17761, 4792, 22090],
        "ExpValue": [200000, 200000, 50000, 50000, 500000, 200000, 100000, 100000, 210000, 70000, 300000],
        "Rate": [0.000018, 0.00021, 0.000305, 0.000912, 0.000078, 0.000042, 0.000018, 0.00021, 0.000411, 0.000912, 0.000729]
    }

    grouped_elt = elt_calculator.group_elts(
        ELT(d_1)).elt

    assert grouped_elt.loc[grouped_elt['EventId'] == 100].Loss.sum() == 68094


def test_calculate_frequency_distribution():
    frequency_distribution = elt_calculator.calculate_frequency_distribution(ELT(TEST_ELT).elt)
    assert frequency_distribution[0] == pytest.approx(0.90484, 0.0001)


def test_calculate_severity_distribution():
    severity_distribution, severity_density_function = elt_calculator.calculate_severity_distribution(
        ELT(TEST_ELT).elt, grid_size=2**2, max_loss_factor=1)
    assert severity_distribution.iloc[1]['CEP'] == pytest.approx(0.73726, 0.00001)
    assert severity_density_function.iloc[0]['CEP'] == pytest.approx(0.26274, 0.0001)


def test_calculate_oep_curve():
    oep = elt_calculator.calculate_oep_curve(ELT(TEST_ELT).elt, grid_size=2**2, max_loss_factor=1)
    assert isinstance(oep, EPCurve)
    assert oep.get_ep_type() == EPType.OEP
    assert oep.loss_at_a_given_return_period(1/0.025307395866947635) == pytest.approx(10000000, 0.01)
    assert oep.loss_at_a_given_return_period(1/0.051289727305568245) == pytest.approx(5000000, 0.1)
    assert oep.loss_at_a_given_return_period(1/0.09516258196404048) == pytest.approx(0, 0.01)


def test_calculate_aep_curve():
    aep = elt_calculator.calculate_aep_curve(ELT(TEST_ELT).elt, grid_size=2**2, max_loss_factor=1)
    assert isinstance(aep, EPCurve)
    assert aep.get_ep_type() == EPType.AEP
    assert aep.loss_at_a_given_return_period(1/0.02618) == pytest.approx(10000000, 0.01)


DATA = [
  {
    "EventId": 1,
    "Rate": 0.01,
    "Loss": 1500000,
    "StdDevI": "",
    "StdDevC": "",
    "StandardDev": 800000,
    "ExpValue": 5500000
  },
  {
    "EventId": 2,
    "Rate": 0.01,
    "Loss": 3000000,
    "StdDevI": "",
    "StdDevC": "",
    "StandardDev": 2000000,
    "ExpValue": 15000000
  },
  {
    "EventId": 3,
    "Rate": 0.02,
    "Loss": 6500000,
    "StdDevI": "",
    "StdDevC": "",
    "StandardDev": 5000000,
    "ExpValue": 50000000
  },
  {
    "EventId": 4,
    "Rate": 0.03,
    "Loss": 8000000,
    "StdDevI": "",
    "StdDevC": "",
    "StandardDev": 6000000,
    "ExpValue": 90000000
  },
  {
    "EventId": 5,
    "Rate": 0.03,
    "Loss": 10000000,
    "StdDevI": "",
    "StdDevC": "",
    "StandardDev": 7000000,
    "ExpValue": 95000000
  }
]

TEST_ELT = pd.DataFrame(DATA)