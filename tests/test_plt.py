""" Tests PLT """
import pytest
from aggregationtools import PLT


def test_get_aal():
    """ Test Get AAL from PLT """
    my_plt = PLT(DATA, 5)
    assert my_plt.get_aal() == 900


def test_no_simulations_set_sets_to_max_period():
    """ Test that if no simulations are set, then the sim periods set to max period id"""
    my_plt = PLT(DATA)
    assert my_plt.simulations == 5


def test_get_standard_deviation():
    """ Test Get Standard Deviation from PLT """
    my_plt = PLT(DATA, 5)
    assert my_plt.get_standard_deviation() == pytest.approx(489.9, 0.1)


def test_invalid_plt_columns_raises_value_error():
    """ Test invalid PLT data raises value error """
    bad_plt_data = [{
        "periodId": 1,
        "eventId": 3500016,
        "lossDate": "3/13/2016 12:00:00 AM",
        "eventDate": "03/10/2016 00:00",
        "loss": 100
    }]
    with pytest.raises(ValueError):
        PLT(bad_plt_data)


DATA = [
    {
        "PeriodId": 1,
        "EventId": 3500016,
        "LossDate": "3/13/2016 12:00:00 AM",
        "EventDate": "03/10/2016 00:00",
        "Loss": 100,
        "Weight": 1/5
    },
    {
        "PeriodId": 3,
        "EventId": 3500129,
        "LossDate": "8/25/2016 12:00:00 AM",
        "EventDate": "8/24/2016 12:00:00 AM",
        "Loss": 200,
        "Weight": 1/5
    },
    {
        "PeriodId": 3,
        "EventId": 3500140,
        "LossDate": "01/01/2017 00:00",
        "EventDate": "12/29/2016 12:00:00 AM",
        "Loss": 300,
        "Weight": 1/5
    },
    {
        "PeriodId": 4,
        "EventId": 3500141,
        "LossDate": "01/10/2016 00:00",
        "EventDate": "01/09/2016 00:00",
        "Loss": 400,
        "Weight": 1/5
    },
    {
        "PeriodId": 4,
        "EventId": 3500141,
        "LossDate": "01/11/2016 00:00",
        "EventDate": "01/09/2016 00:00",
        "Loss": 500,
        "Weight": 1/5
    },
    {
        "PeriodId": 4,
        "EventId": 3500141,
        "LossDate": "1/13/2016 12:00:00 AM",
        "EventDate": "01/09/2016 00:00",
        "Loss": 600,
        "Weight": 1/5
    },
    {
        "PeriodId": 4,
        "EventId": 3500141,
        "LossDate": "1/14/2016 12:00:00 AM",
        "EventDate": "01/09/2016 00:00",
        "Loss": 700,
        "Weight": 1/5
    },
    {
        "PeriodId": 4,
        "EventId": 3500151,
        "LossDate": "8/19/2016 12:00:00 AM",
        "EventDate": "8/19/2016 12:00:00 AM",
        "Loss": 800,
        "Weight": 1/5
    },
    {
        "PeriodId": 5,
        "EventId": 3500166,
        "LossDate": "9/19/2016 12:00:00 AM",
        "EventDate": "9/19/2016 12:00:00 AM",
        "Loss": 900,
        "Weight": 1/5
    }
]
