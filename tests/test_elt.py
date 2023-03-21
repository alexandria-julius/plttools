""" Tests PLT """
import pytest
from aggregationtools import ELT


def test_get_aal():
    """ Test Get AAL from ELT """
    my_elt = ELT(DATA)
    assert my_elt.get_aal() == pytest.approx(151.30, 0.1)


def test_get_standard_deviation():
    """ Test Get Standard Deviation from ELT """
    my_elt = ELT(DATA)
    assert my_elt.get_standard_deviation() == pytest.approx(4791, 0.1)


def test_get_cv():
    """ Test Get CV from ELT """
    my_elt = ELT(DATA)
    assert my_elt.get_covvar() == pytest.approx(31.64, 0.1)


def test_invalid_elt_columns_raises_value_error():
    """ Test invalid ELT data raises value error """
    bad_elt_data = [{
        "PeriodId": 526,
        "Loss": 44536,
        "StdDevI": 7441,
        "StdDevC": 22090,
        "ExpValue": 300000,
        "Rate": 0.000729
    }]
    with pytest.raises(ValueError):
        ELT(bad_elt_data)


DATA = [
    {
        "EventId": 100,
        "Loss": 68094,
        "StdDevI": 26950.83592,
        "StdDevC": 85533,
        "ExpValue": 300000,
        "Rate": 0.000018
    },
    {
        "EventId": 200,
        "Loss": 50713,
        "StdDevI": 16961.56092,
        "StdDevC": 18734,
        "ExpValue": 300000,
        "Rate": 0.00021
    },
    {
        "EventId": 300,
        "Loss": 3281,
        "StdDevI": 6019,
        "StdDevC": 12004,
        "ExpValue": 50000,
        "Rate": 0.000305
    },
    {
        "EventId": 350,
        "Loss": 27540,
        "StdDevI": 48962,
        "StdDevC": 17761,
        "ExpValue": 210000,
        "Rate": 0.000411
    },
    {
        "EventId": 400,
        "Loss": 98367,
        "StdDevI": 16085.91583,
        "StdDevC": 53815,
        "ExpValue": 120000,
        "Rate": 0.000912
    },
    {
        "EventId": 500,
        "Loss": 19025,
        "StdDevI": 75853,
        "StdDevC": 58268,
        "ExpValue": 500000,
        "Rate": 0.000078
    },
    {
        "EventId": 526,
        "Loss": 44536,
        "StdDevI": 7441,
        "StdDevC": 22090,
        "ExpValue": 300000,
        "Rate": 0.000729
    },
    {
        "EventId": 600,
        "Loss": 84287,
        "StdDevI": 62429,
        "StdDevC": 181382,
        "ExpValue": 200000,
        "Rate": 0.000042
    }
]
