""" PLT Calculator tests"""
# pylint: disable=line-too-long

import pandas as pd
from aggregationtools import plt_calculator, EPCurve, EPType
from aggregationtools.plt import PLT


def test_calculate_oep_curve():
    """ Test Calculate OEP Curve"""
    oep = plt_calculator.calculate_oep_curve(TEST_PLT, 5)
    assert isinstance(oep, EPCurve)
    assert oep.get_ep_type() == EPType.OEP
    assert oep.loss_at_a_given_return_period(5) == 900
    assert oep.loss_at_a_given_return_period(2.5) == 800
    assert oep.loss_at_a_given_return_period(5/3) == 300
    assert oep.loss_at_a_given_return_period(1.25) == 100
    assert oep.loss_at_a_given_return_period(1) == 0


def test_calculate_oep_curve_sample_plt():
    """ Test Calculate OEP Curve from Excel PLT example"""
    TEST_PLT = PLT(pd.read_csv(r'sample_plt/plt.csv'), number_of_simulations=50000)
    grouped_plt = plt_calculator.group_plts(TEST_PLT)
    oep = plt_calculator.calculate_oep_curve(grouped_plt.plt, grouped_plt.simulations)
    assert isinstance(oep, EPCurve)
    assert oep.get_ep_type() == EPType.OEP
    assert oep.loss_at_a_given_return_period(10) == 38559130.58
    assert oep.loss_at_a_given_return_period(25) == 105494369.44
    assert oep.loss_at_a_given_return_period(50) == 198673192.75
    assert oep.loss_at_a_given_return_period(100) == 339844342.61
    assert oep.loss_at_a_given_return_period(200) == 514043110.58
    assert oep.loss_at_a_given_return_period(250) == 580645121.6999999
    assert oep.loss_at_a_given_return_period(500) == 832353773.07


def test_calculate_aep_curve():
    """ Test Calculate AEP curve"""
    aep = plt_calculator.calculate_aep_curve(TEST_PLT, 5)
    assert isinstance(aep, EPCurve)
    assert aep.get_ep_type() == EPType.AEP
    assert aep.loss_at_a_given_return_period(5) == 3000
    assert aep.loss_at_a_given_return_period(2.5) == 900
    assert aep.loss_at_a_given_return_period(5/3) == 500
    assert aep.loss_at_a_given_return_period(1.25) == 100
    assert aep.loss_at_a_given_return_period(1) == 0


def test_group_plts():
    """Group PLTs"""
    d_1 = {
        "PeriodId": [1, 1, 2, 3, 4, 5, 6],
        "EventId": [123, 678, 124, 125, 126, 127, 128],
        "EventDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018],
        "Loss": [100, 102, 90, 110, 120, 80, 100],
        "LossDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018],
        "Weight": [1/5, 1/5, 1/5, 1/5, 1/5, 1/5, 1/5]

    }
    d_2 = {
        "PeriodId": [1, 1, 2, 3, 4, 5, 6],
        "EventId": [123, 678, 124, 125, 126, 127, 128],
        "EventDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018],
        "Loss": [100, 102, 90, 110, 120, 80, 100],
        "LossDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018],
        "Weight": [1/5, 1/5, 1/5, 1/5, 1/5, 1/5, 1/5]
    }
    grouped_plt = plt_calculator.group_plts(
        PLT(d_1), PLT(d_2)).plt

    assert grouped_plt.loc[grouped_plt['PeriodId'] == 1].Loss.sum() == 404


def test_group_plts_single_input():
    """Group PLTs"""
    d_1 = {
        "PeriodId": [1, 1, 2, 3, 4, 5, 6],
        "EventId": [123, 678, 124, 125, 126, 127, 128],
        "EventDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018],
        "Loss": [100, 102, 90, 110, 120, 80, 100],
        "LossDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018],
        "Weight": [1/5, 1/5, 1/5, 1/5, 1/5, 1/5, 1/5]
    }

    grouped_plt = plt_calculator.group_plts(
        PLT(d_1)).plt

    assert grouped_plt.loc[grouped_plt['PeriodId'] == 1].Loss.sum() == 202


def test_roll_up_plts():
    """Rollup PLTs"""
    d_1 = {
        "PeriodId": [1, 1, 2, 3, 4, 5, 6],
        "EventId": [123, 678, 124, 125, 126, 127, 128],
        "EventDate": [10 / 19 / 2018, 10 / 20 / 2018, 10 / 19 / 2018, 10 / 19 / 2018, 10 / 19 / 2018,
                      10 / 19 / 2018, 10 / 19 / 2018],
        "Loss": [100, 102, 90, 110, 120, 80, 100],
        "LossDate": [10 / 19 / 2018, 10 / 20 / 2018, 10 / 19 / 2018, 10 / 19 / 2018, 10 / 19 / 2018, 10 / 19 / 2018,
                     10 / 19 / 2018],
        "Weight": [1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5]
    }
    d_2 = {
        "PeriodId": [1, 1, 2, 3, 4, 5, 6],
        "EventId": [123, 678, 124, 125, 126, 127, 128],
        "EventDate": [10 / 19 / 2018, 10 / 20 / 2018, 10 / 19 / 2018, 10 / 19 / 2018, 10 / 19 / 2018,
                      10 / 19 / 2018, 10 / 19 / 2018],
        "Loss": [100, 102, 90, 110, 120, 80, 100],
        "LossDate": [10 / 19 / 2018, 10 / 20 / 2018, 10 / 19 / 2018, 10 / 19 / 2018, 10 / 19 / 2018, 10 / 19 / 2018,
                     10 / 19 / 2018],
        "Weight": [1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5]
    }
    rolled_up_plt = plt_calculator.roll_up_plts(
        PLT(d_1), PLT(d_2)).plt

    assert rolled_up_plt.loc[rolled_up_plt['PeriodId'] == 1].Loss.sum() == 404


DATA = [
    {
        "PeriodId": 1,
        "EventId": 3500016,
        "LossDate": "3/13/2016 12:00:00 AM",
        "EventDate": "03/10/2016 00:00",
        "Loss": 100
    },
    {
        "PeriodId": 3,
        "EventId": 3500129,
        "LossDate": "8/25/2016 12:00:00 AM",
        "EventDate": "8/24/2016 12:00:00 AM",
        "Loss": 200
    },
    {
        "PeriodId": 3,
        "EventId": 3500140,
        "LossDate": "01/01/2017 00:00",
        "EventDate": "12/29/2016 12:00:00 AM",
        "Loss": 300
    },
    {
        "PeriodId": 4,
        "EventId": 3500141,
        "LossDate": "01/10/2016 00:00",
        "EventDate": "01/09/2016 00:00",
        "Loss": 400
    },
    {
        "PeriodId": 4,
        "EventId": 3500141,
        "LossDate": "01/11/2016 00:00",
        "EventDate": "01/09/2016 00:00",
        "Loss": 500
    },
    {
        "PeriodId": 4,
        "EventId": 3500141,
        "LossDate": "1/13/2016 12:00:00 AM",
        "EventDate": "01/09/2016 00:00",
        "Loss": 600
    },
    {
        "PeriodId": 4,
        "EventId": 3500141,
        "LossDate": "1/14/2016 12:00:00 AM",
        "EventDate": "01/09/2016 00:00",
        "Loss": 700
    },
    {
        "PeriodId": 4,
        "EventId": 3500151,
        "LossDate": "8/19/2016 12:00:00 AM",
        "EventDate": "8/19/2016 12:00:00 AM",
        "Loss": 800
    },
    {
        "PeriodId": 5,
        "EventId": 3500166,
        "LossDate": "9/19/2016 12:00:00 AM",
        "EventDate": "9/19/2016 12:00:00 AM",
        "Loss": 900
    }
]

TEST_PLT = pd.DataFrame(DATA)
