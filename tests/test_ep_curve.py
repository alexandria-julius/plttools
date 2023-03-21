""" EP Curve tests"""
# pylint: disable=too-many-lines
import pandas as pd
import pytest
from aggregationtools import EPCurve, EPType


def test_loss_at_a_given_return_period():
    """ Test losses at given return periods """
    oep_curve = EPCurve(DATA, ep_type=EPType.OEP)
    loss_10_year = oep_curve.loss_at_a_given_return_period(10)
    loss_100_year = oep_curve.loss_at_a_given_return_period(100)
    loss_1000_year = oep_curve.loss_at_a_given_return_period(1000)
    loss_1000000_year = oep_curve.loss_at_a_given_return_period(1000000)
    loss_800_year = oep_curve.loss_at_a_given_return_period(800)
    assert oep_curve.get_ep_type() == EPType.OEP
    assert loss_10_year == 9000
    assert loss_100_year == 9900
    assert loss_1000_year == 9990
    assert loss_1000000_year == 9990
    assert loss_800_year == 9987.5


def test_ep_curve_no_type_is_unknown():
    """ Test EP Curve is unknown when no type provided to init """
    unknown_ep_curve = EPCurve(DATA, None)
    assert unknown_ep_curve.get_ep_type() == EPType.UNKNOWN


def test_return_periods():
    """ Test that return periods list exists and is not empty """
    assert len(EPCurve.RETURN_PERIODS) > 0


def test_get_loss_at_given_return_period_negative_rp_throws_value_error():
    """Test that negative RP throws value error"""
    oep_curve = EPCurve(DATA, ep_type=EPType.OEP)
    with pytest.raises(ValueError):
        oep_curve.loss_at_a_given_return_period(-1)


def test_invalid_elt_data_throws_error():
    """ Test invalid ELT input data throws ValueError """
    invalid_ep_data = [{"probability":0.01, "los":100}, {"probability":0.02, "los":200}]
    with pytest.raises(ValueError,
                       match='Probability and Loss fields not in data. Check the spelling'):
        EPCurve(invalid_ep_data, None)


def test_get_standard_return_period_ep():
    """ Test get standard return period EP curve """
    oep_curve = EPCurve(DATA, ep_type=EPType.OEP)
    return_periods = EPCurve.RETURN_PERIODS
    standard_curve = oep_curve.get_standard_return_period_ep()
    test_ep_data = pd.DataFrame(DATA)
    for return_period in return_periods:
        probability = 1 / return_period
        assert probability in standard_curve
        # Sometimes not all probabilities exist in the input data
        if len(test_ep_data.loc[test_ep_data['Probability'] == probability]) > 0:
            assert standard_curve[probability] == test_ep_data.loc[
                test_ep_data['Probability'] == probability, 'Loss'].values[0]

DATA = [
    {
        "Probability": 0.001,
        "Loss": 9990
    },
    {
        "Probability": 0.002,
        "Loss": 9980
    },
    {
        "Probability": 0.003,
        "Loss": 9970
    },
    {
        "Probability": 0.004,
        "Loss": 9960
    },
    {
        "Probability": 0.005,
        "Loss": 9950
    },
    {
        "Probability": 0.006,
        "Loss": 9940
    },
    {
        "Probability": 0.007,
        "Loss": 9930
    },
    {
        "Probability": 0.008,
        "Loss": 9920
    },
    {
        "Probability": 0.009,
        "Loss": 9910
    },
    {
        "Probability": 0.01,
        "Loss": 9900
    },
    {
        "Probability": 0.011,
        "Loss": 9890
    },
    {
        "Probability": 0.012,
        "Loss": 9880
    },
    {
        "Probability": 0.013,
        "Loss": 9870
    },
    {
        "Probability": 0.014,
        "Loss": 9860
    },
    {
        "Probability": 0.015,
        "Loss": 9850
    },
    {
        "Probability": 0.016,
        "Loss": 9840
    },
    {
        "Probability": 0.017,
        "Loss": 9830
    },
    {
        "Probability": 0.018,
        "Loss": 9820
    },
    {
        "Probability": 0.019,
        "Loss": 9810
    },
    {
        "Probability": 0.02,
        "Loss": 9800
    },
    {
        "Probability": 0.021,
        "Loss": 9790
    },
    {
        "Probability": 0.022,
        "Loss": 9780
    },
    {
        "Probability": 0.023,
        "Loss": 9770
    },
    {
        "Probability": 0.024,
        "Loss": 9760
    },
    {
        "Probability": 0.025,
        "Loss": 9750
    },
    {
        "Probability": 0.026,
        "Loss": 9740
    },
    {
        "Probability": 0.027,
        "Loss": 9730
    },
    {
        "Probability": 0.028,
        "Loss": 9720
    },
    {
        "Probability": 0.029,
        "Loss": 9710
    },
    {
        "Probability": 0.03,
        "Loss": 9700
    },
    {
        "Probability": 0.031,
        "Loss": 9690
    },
    {
        "Probability": 0.032,
        "Loss": 9680
    },
    {
        "Probability": 0.033,
        "Loss": 9670
    },
    {
        "Probability": 0.034,
        "Loss": 9660
    },
    {
        "Probability": 0.035,
        "Loss": 9650
    },
    {
        "Probability": 0.036,
        "Loss": 9640
    },
    {
        "Probability": 0.037,
        "Loss": 9630
    },
    {
        "Probability": 0.038,
        "Loss": 9620
    },
    {
        "Probability": 0.039,
        "Loss": 9610
    },
    {
        "Probability": 0.04,
        "Loss": 9600
    },
    {
        "Probability": 0.041,
        "Loss": 9590
    },
    {
        "Probability": 0.042,
        "Loss": 9580
    },
    {
        "Probability": 0.043,
        "Loss": 9570
    },
    {
        "Probability": 0.044,
        "Loss": 9560
    },
    {
        "Probability": 0.045,
        "Loss": 9550
    },
    {
        "Probability": 0.046,
        "Loss": 9540
    },
    {
        "Probability": 0.047,
        "Loss": 9530
    },
    {
        "Probability": 0.048,
        "Loss": 9520
    },
    {
        "Probability": 0.049,
        "Loss": 9510
    },
    {
        "Probability": 0.05,
        "Loss": 9500
    },
    {
        "Probability": 0.051,
        "Loss": 9490
    },
    {
        "Probability": 0.052,
        "Loss": 9480
    },
    {
        "Probability": 0.053,
        "Loss": 9470
    },
    {
        "Probability": 0.054,
        "Loss": 9460
    },
    {
        "Probability": 0.055,
        "Loss": 9450
    },
    {
        "Probability": 0.056,
        "Loss": 9440
    },
    {
        "Probability": 0.057,
        "Loss": 9430
    },
    {
        "Probability": 0.058,
        "Loss": 9420
    },
    {
        "Probability": 0.059,
        "Loss": 9410
    },
    {
        "Probability": 0.06,
        "Loss": 9400
    },
    {
        "Probability": 0.061,
        "Loss": 9390
    },
    {
        "Probability": 0.062,
        "Loss": 9380
    },
    {
        "Probability": 0.063,
        "Loss": 9370
    },
    {
        "Probability": 0.064,
        "Loss": 9360
    },
    {
        "Probability": 0.065,
        "Loss": 9350
    },
    {
        "Probability": 0.066,
        "Loss": 9340
    },
    {
        "Probability": 0.067,
        "Loss": 9330
    },
    {
        "Probability": 0.068,
        "Loss": 9320
    },
    {
        "Probability": 0.069,
        "Loss": 9310
    },
    {
        "Probability": 0.07,
        "Loss": 9300
    },
    {
        "Probability": 0.071,
        "Loss": 9290
    },
    {
        "Probability": 0.072,
        "Loss": 9280
    },
    {
        "Probability": 0.073,
        "Loss": 9270
    },
    {
        "Probability": 0.074,
        "Loss": 9260
    },
    {
        "Probability": 0.075,
        "Loss": 9250
    },
    {
        "Probability": 0.076,
        "Loss": 9240
    },
    {
        "Probability": 0.077,
        "Loss": 9230
    },
    {
        "Probability": 0.078,
        "Loss": 9220
    },
    {
        "Probability": 0.079,
        "Loss": 9210
    },
    {
        "Probability": 0.08,
        "Loss": 9200
    },
    {
        "Probability": 0.081,
        "Loss": 9190
    },
    {
        "Probability": 0.082,
        "Loss": 9180
    },
    {
        "Probability": 0.083,
        "Loss": 9170
    },
    {
        "Probability": 0.084,
        "Loss": 9160
    },
    {
        "Probability": 0.085,
        "Loss": 9150
    },
    {
        "Probability": 0.086,
        "Loss": 9140
    },
    {
        "Probability": 0.087,
        "Loss": 9130
    },
    {
        "Probability": 0.088,
        "Loss": 9120
    },
    {
        "Probability": 0.089,
        "Loss": 9110
    },
    {
        "Probability": 0.09,
        "Loss": 9100
    },
    {
        "Probability": 0.091,
        "Loss": 9090
    },
    {
        "Probability": 0.092,
        "Loss": 9080
    },
    {
        "Probability": 0.093,
        "Loss": 9070
    },
    {
        "Probability": 0.094,
        "Loss": 9060
    },
    {
        "Probability": 0.095,
        "Loss": 9050
    },
    {
        "Probability": 0.096,
        "Loss": 9040
    },
    {
        "Probability": 0.097,
        "Loss": 9030
    },
    {
        "Probability": 0.098,
        "Loss": 9020
    },
    {
        "Probability": 0.099,
        "Loss": 9010
    },
    {
        "Probability": 0.1,
        "Loss": 9000
    },
    {
        "Probability": 0.101,
        "Loss": 8990
    },
    {
        "Probability": 0.102,
        "Loss": 8980
    },
    {
        "Probability": 0.103,
        "Loss": 8970
    },
    {
        "Probability": 0.104,
        "Loss": 8960
    },
    {
        "Probability": 0.105,
        "Loss": 8950
    },
    {
        "Probability": 0.106,
        "Loss": 8940
    },
    {
        "Probability": 0.107,
        "Loss": 8930
    },
    {
        "Probability": 0.108,
        "Loss": 8920
    },
    {
        "Probability": 0.109,
        "Loss": 8910
    },
    {
        "Probability": 0.11,
        "Loss": 8900
    },
    {
        "Probability": 0.111,
        "Loss": 8890
    },
    {
        "Probability": 0.112,
        "Loss": 8880
    },
    {
        "Probability": 0.113,
        "Loss": 8870
    },
    {
        "Probability": 0.114,
        "Loss": 8860
    },
    {
        "Probability": 0.115,
        "Loss": 8850
    },
    {
        "Probability": 0.116,
        "Loss": 8840
    },
    {
        "Probability": 0.117,
        "Loss": 8830
    },
    {
        "Probability": 0.118,
        "Loss": 8820
    },
    {
        "Probability": 0.119,
        "Loss": 8810
    },
    {
        "Probability": 0.12,
        "Loss": 8800
    },
    {
        "Probability": 0.121,
        "Loss": 8790
    },
    {
        "Probability": 0.122,
        "Loss": 8780
    },
    {
        "Probability": 0.123,
        "Loss": 8770
    },
    {
        "Probability": 0.124,
        "Loss": 8760
    },
    {
        "Probability": 0.125,
        "Loss": 8750
    },
    {
        "Probability": 0.126,
        "Loss": 8740
    },
    {
        "Probability": 0.127,
        "Loss": 8730
    },
    {
        "Probability": 0.128,
        "Loss": 8720
    },
    {
        "Probability": 0.129,
        "Loss": 8710
    },
    {
        "Probability": 0.13,
        "Loss": 8700
    },
    {
        "Probability": 0.131,
        "Loss": 8690
    },
    {
        "Probability": 0.132,
        "Loss": 8680
    },
    {
        "Probability": 0.133,
        "Loss": 8670
    },
    {
        "Probability": 0.134,
        "Loss": 8660
    },
    {
        "Probability": 0.135,
        "Loss": 8650
    },
    {
        "Probability": 0.136,
        "Loss": 8640
    },
    {
        "Probability": 0.137,
        "Loss": 8630
    },
    {
        "Probability": 0.138,
        "Loss": 8620
    },
    {
        "Probability": 0.139,
        "Loss": 8610
    },
    {
        "Probability": 0.14,
        "Loss": 8600
    },
    {
        "Probability": 0.141,
        "Loss": 8590
    },
    {
        "Probability": 0.142,
        "Loss": 8580
    },
    {
        "Probability": 0.143,
        "Loss": 8570
    },
    {
        "Probability": 0.144,
        "Loss": 8560
    },
    {
        "Probability": 0.145,
        "Loss": 8550
    },
    {
        "Probability": 0.146,
        "Loss": 8540
    },
    {
        "Probability": 0.147,
        "Loss": 8530
    },
    {
        "Probability": 0.148,
        "Loss": 8520
    },
    {
        "Probability": 0.149,
        "Loss": 8510
    },
    {
        "Probability": 0.15,
        "Loss": 8500
    },
    {
        "Probability": 0.151,
        "Loss": 8490
    },
    {
        "Probability": 0.152,
        "Loss": 8480
    },
    {
        "Probability": 0.153,
        "Loss": 8470
    },
    {
        "Probability": 0.154,
        "Loss": 8460
    },
    {
        "Probability": 0.155,
        "Loss": 8450
    },
    {
        "Probability": 0.156,
        "Loss": 8440
    },
    {
        "Probability": 0.157,
        "Loss": 8430
    },
    {
        "Probability": 0.158,
        "Loss": 8420
    },
    {
        "Probability": 0.159,
        "Loss": 8410
    },
    {
        "Probability": 0.16,
        "Loss": 8400
    },
    {
        "Probability": 0.161,
        "Loss": 8390
    },
    {
        "Probability": 0.162,
        "Loss": 8380
    },
    {
        "Probability": 0.163,
        "Loss": 8370
    },
    {
        "Probability": 0.164,
        "Loss": 8360
    },
    {
        "Probability": 0.165,
        "Loss": 8350
    },
    {
        "Probability": 0.166,
        "Loss": 8340
    },
    {
        "Probability": 0.167,
        "Loss": 8330
    },
    {
        "Probability": 0.168,
        "Loss": 8320
    },
    {
        "Probability": 0.169,
        "Loss": 8310
    },
    {
        "Probability": 0.17,
        "Loss": 8300
    },
    {
        "Probability": 0.171,
        "Loss": 8290
    },
    {
        "Probability": 0.172,
        "Loss": 8280
    },
    {
        "Probability": 0.173,
        "Loss": 8270
    },
    {
        "Probability": 0.174,
        "Loss": 8260
    },
    {
        "Probability": 0.175,
        "Loss": 8250
    },
    {
        "Probability": 0.176,
        "Loss": 8240
    },
    {
        "Probability": 0.177,
        "Loss": 8230
    },
    {
        "Probability": 0.178,
        "Loss": 8220
    },
    {
        "Probability": 0.179,
        "Loss": 8210
    },
    {
        "Probability": 0.18,
        "Loss": 8200
    },
    {
        "Probability": 0.181,
        "Loss": 8190
    },
    {
        "Probability": 0.182,
        "Loss": 8180
    },
    {
        "Probability": 0.183,
        "Loss": 8170
    },
    {
        "Probability": 0.184,
        "Loss": 8160
    },
    {
        "Probability": 0.185,
        "Loss": 8150
    },
    {
        "Probability": 0.186,
        "Loss": 8140
    },
    {
        "Probability": 0.187,
        "Loss": 8130
    },
    {
        "Probability": 0.188,
        "Loss": 8120
    },
    {
        "Probability": 0.189,
        "Loss": 8110
    },
    {
        "Probability": 0.19,
        "Loss": 8100
    },
    {
        "Probability": 0.191,
        "Loss": 8090
    },
    {
        "Probability": 0.192,
        "Loss": 8080
    },
    {
        "Probability": 0.193,
        "Loss": 8070
    },
    {
        "Probability": 0.194,
        "Loss": 8060
    },
    {
        "Probability": 0.195,
        "Loss": 8050
    },
    {
        "Probability": 0.196,
        "Loss": 8040
    },
    {
        "Probability": 0.197,
        "Loss": 8030
    },
    {
        "Probability": 0.198,
        "Loss": 8020
    },
    {
        "Probability": 0.199,
        "Loss": 8010
    },
    {
        "Probability": 0.2,
        "Loss": 8000
    },
    {
        "Probability": 0.201,
        "Loss": 7990
    },
    {
        "Probability": 0.202,
        "Loss": 7980
    },
    {
        "Probability": 0.203,
        "Loss": 7970
    },
    {
        "Probability": 0.204,
        "Loss": 7960
    },
    {
        "Probability": 0.205,
        "Loss": 7950
    },
    {
        "Probability": 0.206,
        "Loss": 7940
    },
    {
        "Probability": 0.207,
        "Loss": 7930
    },
    {
        "Probability": 0.208,
        "Loss": 7920
    },
    {
        "Probability": 0.209,
        "Loss": 7910
    },
    {
        "Probability": 0.21,
        "Loss": 7900
    },
    {
        "Probability": 0.211,
        "Loss": 7890
    },
    {
        "Probability": 0.212,
        "Loss": 7880
    },
    {
        "Probability": 0.213,
        "Loss": 7870
    },
    {
        "Probability": 0.214,
        "Loss": 7860
    },
    {
        "Probability": 0.215,
        "Loss": 7850
    },
    {
        "Probability": 0.216,
        "Loss": 7840
    },
    {
        "Probability": 0.217,
        "Loss": 7830
    },
    {
        "Probability": 0.218,
        "Loss": 7820
    },
    {
        "Probability": 0.219,
        "Loss": 7810
    },
    {
        "Probability": 0.22,
        "Loss": 7800
    },
    {
        "Probability": 0.221,
        "Loss": 7790
    },
    {
        "Probability": 0.222,
        "Loss": 7780
    },
    {
        "Probability": 0.223,
        "Loss": 7770
    },
    {
        "Probability": 0.224,
        "Loss": 7760
    },
    {
        "Probability": 0.225,
        "Loss": 7750
    },
    {
        "Probability": 0.226,
        "Loss": 7740
    },
    {
        "Probability": 0.227,
        "Loss": 7730
    },
    {
        "Probability": 0.228,
        "Loss": 7720
    },
    {
        "Probability": 0.229,
        "Loss": 7710
    },
    {
        "Probability": 0.23,
        "Loss": 7700
    },
    {
        "Probability": 0.231,
        "Loss": 7690
    },
    {
        "Probability": 0.232,
        "Loss": 7680
    },
    {
        "Probability": 0.233,
        "Loss": 7670
    },
    {
        "Probability": 0.234,
        "Loss": 7660
    },
    {
        "Probability": 0.235,
        "Loss": 7650
    },
    {
        "Probability": 0.236,
        "Loss": 7640
    },
    {
        "Probability": 0.237,
        "Loss": 7630
    },
    {
        "Probability": 0.238,
        "Loss": 7620
    },
    {
        "Probability": 0.239,
        "Loss": 7610
    },
    {
        "Probability": 0.24,
        "Loss": 7600
    },
    {
        "Probability": 0.241,
        "Loss": 7590
    },
    {
        "Probability": 0.242,
        "Loss": 7580
    },
    {
        "Probability": 0.243,
        "Loss": 7570
    },
    {
        "Probability": 0.244,
        "Loss": 7560
    },
    {
        "Probability": 0.245,
        "Loss": 7550
    },
    {
        "Probability": 0.246,
        "Loss": 7540
    },
    {
        "Probability": 0.247,
        "Loss": 7530
    },
    {
        "Probability": 0.248,
        "Loss": 7520
    },
    {
        "Probability": 0.249,
        "Loss": 7510
    },
    {
        "Probability": 0.25,
        "Loss": 7500
    },
    {
        "Probability": 0.251,
        "Loss": 7490
    },
    {
        "Probability": 0.252,
        "Loss": 7480
    },
    {
        "Probability": 0.253,
        "Loss": 7470
    },
    {
        "Probability": 0.254,
        "Loss": 7460
    },
    {
        "Probability": 0.255,
        "Loss": 7450
    },
    {
        "Probability": 0.256,
        "Loss": 7440
    },
    {
        "Probability": 0.257,
        "Loss": 7430
    },
    {
        "Probability": 0.258,
        "Loss": 7420
    },
    {
        "Probability": 0.259,
        "Loss": 7410
    },
    {
        "Probability": 0.26,
        "Loss": 7400
    },
    {
        "Probability": 0.261,
        "Loss": 7390
    },
    {
        "Probability": 0.262,
        "Loss": 7380
    },
    {
        "Probability": 0.263,
        "Loss": 7370
    },
    {
        "Probability": 0.264,
        "Loss": 7360
    },
    {
        "Probability": 0.265,
        "Loss": 7350
    },
    {
        "Probability": 0.266,
        "Loss": 7340
    },
    {
        "Probability": 0.267,
        "Loss": 7330
    },
    {
        "Probability": 0.268,
        "Loss": 7320
    },
    {
        "Probability": 0.269,
        "Loss": 7310
    },
    {
        "Probability": 0.27,
        "Loss": 7300
    },
    {
        "Probability": 0.271,
        "Loss": 7290
    },
    {
        "Probability": 0.272,
        "Loss": 7280
    },
    {
        "Probability": 0.273,
        "Loss": 7270
    },
    {
        "Probability": 0.274,
        "Loss": 7260
    },
    {
        "Probability": 0.275,
        "Loss": 7250
    },
    {
        "Probability": 0.276,
        "Loss": 7240
    },
    {
        "Probability": 0.277,
        "Loss": 7230
    },
    {
        "Probability": 0.278,
        "Loss": 7220
    },
    {
        "Probability": 0.279,
        "Loss": 7210
    },
    {
        "Probability": 0.28,
        "Loss": 7200
    },
    {
        "Probability": 0.281,
        "Loss": 7190
    },
    {
        "Probability": 0.282,
        "Loss": 7180
    },
    {
        "Probability": 0.283,
        "Loss": 7170
    },
    {
        "Probability": 0.284,
        "Loss": 7160
    },
    {
        "Probability": 0.285,
        "Loss": 7150
    },
    {
        "Probability": 0.286,
        "Loss": 7140
    },
    {
        "Probability": 0.287,
        "Loss": 7130
    },
    {
        "Probability": 0.288,
        "Loss": 7120
    },
    {
        "Probability": 0.289,
        "Loss": 7110
    },
    {
        "Probability": 0.29,
        "Loss": 7100
    },
    {
        "Probability": 0.291,
        "Loss": 7090
    },
    {
        "Probability": 0.292,
        "Loss": 7080
    },
    {
        "Probability": 0.293,
        "Loss": 7070
    },
    {
        "Probability": 0.294,
        "Loss": 7060
    },
    {
        "Probability": 0.295,
        "Loss": 7050
    },
    {
        "Probability": 0.296,
        "Loss": 7040
    },
    {
        "Probability": 0.297,
        "Loss": 7030
    },
    {
        "Probability": 0.298,
        "Loss": 7020
    },
    {
        "Probability": 0.299,
        "Loss": 7010
    },
    {
        "Probability": 0.3,
        "Loss": 7000
    },
    {
        "Probability": 0.301,
        "Loss": 6990
    },
    {
        "Probability": 0.302,
        "Loss": 6980
    },
    {
        "Probability": 0.303,
        "Loss": 6970
    },
    {
        "Probability": 0.304,
        "Loss": 6960
    },
    {
        "Probability": 0.305,
        "Loss": 6950
    },
    {
        "Probability": 0.306,
        "Loss": 6940
    },
    {
        "Probability": 0.307,
        "Loss": 6930
    },
    {
        "Probability": 0.308,
        "Loss": 6920
    },
    {
        "Probability": 0.309,
        "Loss": 6910
    },
    {
        "Probability": 0.31,
        "Loss": 6900
    },
    {
        "Probability": 0.311,
        "Loss": 6890
    },
    {
        "Probability": 0.312,
        "Loss": 6880
    },
    {
        "Probability": 0.313,
        "Loss": 6870
    },
    {
        "Probability": 0.314,
        "Loss": 6860
    },
    {
        "Probability": 0.315,
        "Loss": 6850
    },
    {
        "Probability": 0.316,
        "Loss": 6840
    },
    {
        "Probability": 0.317,
        "Loss": 6830
    },
    {
        "Probability": 0.318,
        "Loss": 6820
    },
    {
        "Probability": 0.319,
        "Loss": 6810
    },
    {
        "Probability": 0.32,
        "Loss": 6800
    },
    {
        "Probability": 0.321,
        "Loss": 6790
    },
    {
        "Probability": 0.322,
        "Loss": 6780
    },
    {
        "Probability": 0.323,
        "Loss": 6770
    },
    {
        "Probability": 0.324,
        "Loss": 6760
    },
    {
        "Probability": 0.325,
        "Loss": 6750
    },
    {
        "Probability": 0.326,
        "Loss": 6740
    },
    {
        "Probability": 0.327,
        "Loss": 6730
    },
    {
        "Probability": 0.328,
        "Loss": 6720
    },
    {
        "Probability": 0.329,
        "Loss": 6710
    },
    {
        "Probability": 0.33,
        "Loss": 6700
    },
    {
        "Probability": 0.331,
        "Loss": 6690
    },
    {
        "Probability": 0.332,
        "Loss": 6680
    },
    {
        "Probability": 0.333,
        "Loss": 6670
    },
    {
        "Probability": 0.334,
        "Loss": 6660
    },
    {
        "Probability": 0.335,
        "Loss": 6650
    },
    {
        "Probability": 0.336,
        "Loss": 6640
    },
    {
        "Probability": 0.337,
        "Loss": 6630
    },
    {
        "Probability": 0.338,
        "Loss": 6620
    },
    {
        "Probability": 0.339,
        "Loss": 6610
    },
    {
        "Probability": 0.34,
        "Loss": 6600
    },
    {
        "Probability": 0.341,
        "Loss": 6590
    },
    {
        "Probability": 0.342,
        "Loss": 6580
    },
    {
        "Probability": 0.343,
        "Loss": 6570
    },
    {
        "Probability": 0.344,
        "Loss": 6560
    },
    {
        "Probability": 0.345,
        "Loss": 6550
    },
    {
        "Probability": 0.346,
        "Loss": 6540
    },
    {
        "Probability": 0.347,
        "Loss": 6530
    },
    {
        "Probability": 0.348,
        "Loss": 6520
    },
    {
        "Probability": 0.349,
        "Loss": 6510
    },
    {
        "Probability": 0.35,
        "Loss": 6500
    },
    {
        "Probability": 0.351,
        "Loss": 6490
    },
    {
        "Probability": 0.352,
        "Loss": 6480
    },
    {
        "Probability": 0.353,
        "Loss": 6470
    },
    {
        "Probability": 0.354,
        "Loss": 6460
    },
    {
        "Probability": 0.355,
        "Loss": 6450
    },
    {
        "Probability": 0.356,
        "Loss": 6440
    },
    {
        "Probability": 0.357,
        "Loss": 6430
    },
    {
        "Probability": 0.358,
        "Loss": 6420
    },
    {
        "Probability": 0.359,
        "Loss": 6410
    },
    {
        "Probability": 0.36,
        "Loss": 6400
    },
    {
        "Probability": 0.361,
        "Loss": 6390
    },
    {
        "Probability": 0.362,
        "Loss": 6380
    },
    {
        "Probability": 0.363,
        "Loss": 6370
    },
    {
        "Probability": 0.364,
        "Loss": 6360
    },
    {
        "Probability": 0.365,
        "Loss": 6350
    },
    {
        "Probability": 0.366,
        "Loss": 6340
    },
    {
        "Probability": 0.367,
        "Loss": 6330
    },
    {
        "Probability": 0.368,
        "Loss": 6320
    },
    {
        "Probability": 0.369,
        "Loss": 6310
    },
    {
        "Probability": 0.37,
        "Loss": 6300
    },
    {
        "Probability": 0.371,
        "Loss": 6290
    },
    {
        "Probability": 0.372,
        "Loss": 6280
    },
    {
        "Probability": 0.373,
        "Loss": 6270
    },
    {
        "Probability": 0.374,
        "Loss": 6260
    },
    {
        "Probability": 0.375,
        "Loss": 6250
    },
    {
        "Probability": 0.376,
        "Loss": 6240
    },
    {
        "Probability": 0.377,
        "Loss": 6230
    },
    {
        "Probability": 0.378,
        "Loss": 6220
    },
    {
        "Probability": 0.379,
        "Loss": 6210
    },
    {
        "Probability": 0.38,
        "Loss": 6200
    },
    {
        "Probability": 0.381,
        "Loss": 6190
    },
    {
        "Probability": 0.382,
        "Loss": 6180
    },
    {
        "Probability": 0.383,
        "Loss": 6170
    },
    {
        "Probability": 0.384,
        "Loss": 6160
    },
    {
        "Probability": 0.385,
        "Loss": 6150
    },
    {
        "Probability": 0.386,
        "Loss": 6140
    },
    {
        "Probability": 0.387,
        "Loss": 6130
    },
    {
        "Probability": 0.388,
        "Loss": 6120
    },
    {
        "Probability": 0.389,
        "Loss": 6110
    },
    {
        "Probability": 0.39,
        "Loss": 6100
    },
    {
        "Probability": 0.391,
        "Loss": 6090
    },
    {
        "Probability": 0.392,
        "Loss": 6080
    },
    {
        "Probability": 0.393,
        "Loss": 6070
    },
    {
        "Probability": 0.394,
        "Loss": 6060
    },
    {
        "Probability": 0.395,
        "Loss": 6050
    },
    {
        "Probability": 0.396,
        "Loss": 6040
    },
    {
        "Probability": 0.397,
        "Loss": 6030
    },
    {
        "Probability": 0.398,
        "Loss": 6020
    },
    {
        "Probability": 0.399,
        "Loss": 6010
    },
    {
        "Probability": 0.4,
        "Loss": 6000
    },
    {
        "Probability": 0.401,
        "Loss": 5990
    },
    {
        "Probability": 0.402,
        "Loss": 5980
    },
    {
        "Probability": 0.403,
        "Loss": 5970
    },
    {
        "Probability": 0.404,
        "Loss": 5960
    },
    {
        "Probability": 0.405,
        "Loss": 5950
    },
    {
        "Probability": 0.406,
        "Loss": 5940
    },
    {
        "Probability": 0.407,
        "Loss": 5930
    },
    {
        "Probability": 0.408,
        "Loss": 5920
    },
    {
        "Probability": 0.409,
        "Loss": 5910
    },
    {
        "Probability": 0.41,
        "Loss": 5900
    },
    {
        "Probability": 0.411,
        "Loss": 5890
    },
    {
        "Probability": 0.412,
        "Loss": 5880
    },
    {
        "Probability": 0.413,
        "Loss": 5870
    },
    {
        "Probability": 0.414,
        "Loss": 5860
    },
    {
        "Probability": 0.415,
        "Loss": 5850
    },
    {
        "Probability": 0.416,
        "Loss": 5840
    },
    {
        "Probability": 0.417,
        "Loss": 5830
    },
    {
        "Probability": 0.418,
        "Loss": 5820
    },
    {
        "Probability": 0.419,
        "Loss": 5810
    },
    {
        "Probability": 0.42,
        "Loss": 5800
    },
    {
        "Probability": 0.421,
        "Loss": 5790
    },
    {
        "Probability": 0.422,
        "Loss": 5780
    },
    {
        "Probability": 0.423,
        "Loss": 5770
    },
    {
        "Probability": 0.424,
        "Loss": 5760
    },
    {
        "Probability": 0.425,
        "Loss": 5750
    },
    {
        "Probability": 0.426,
        "Loss": 5740
    },
    {
        "Probability": 0.427,
        "Loss": 5730
    },
    {
        "Probability": 0.428,
        "Loss": 5720
    },
    {
        "Probability": 0.429,
        "Loss": 5710
    },
    {
        "Probability": 0.43,
        "Loss": 5700
    },
    {
        "Probability": 0.431,
        "Loss": 5690
    },
    {
        "Probability": 0.432,
        "Loss": 5680
    },
    {
        "Probability": 0.433,
        "Loss": 5670
    },
    {
        "Probability": 0.434,
        "Loss": 5660
    },
    {
        "Probability": 0.435,
        "Loss": 5650
    },
    {
        "Probability": 0.436,
        "Loss": 5640
    },
    {
        "Probability": 0.437,
        "Loss": 5630
    },
    {
        "Probability": 0.438,
        "Loss": 5620
    },
    {
        "Probability": 0.439,
        "Loss": 5610
    },
    {
        "Probability": 0.44,
        "Loss": 5600
    },
    {
        "Probability": 0.441,
        "Loss": 5590
    },
    {
        "Probability": 0.442,
        "Loss": 5580
    },
    {
        "Probability": 0.443,
        "Loss": 5570
    },
    {
        "Probability": 0.444,
        "Loss": 5560
    },
    {
        "Probability": 0.445,
        "Loss": 5550
    },
    {
        "Probability": 0.446,
        "Loss": 5540
    },
    {
        "Probability": 0.447,
        "Loss": 5530
    },
    {
        "Probability": 0.448,
        "Loss": 5520
    },
    {
        "Probability": 0.449,
        "Loss": 5510
    },
    {
        "Probability": 0.45,
        "Loss": 5500
    },
    {
        "Probability": 0.451,
        "Loss": 5490
    },
    {
        "Probability": 0.452,
        "Loss": 5480
    },
    {
        "Probability": 0.453,
        "Loss": 5470
    },
    {
        "Probability": 0.454,
        "Loss": 5460
    },
    {
        "Probability": 0.455,
        "Loss": 5450
    },
    {
        "Probability": 0.456,
        "Loss": 5440
    },
    {
        "Probability": 0.457,
        "Loss": 5430
    },
    {
        "Probability": 0.458,
        "Loss": 5420
    },
    {
        "Probability": 0.459,
        "Loss": 5410
    },
    {
        "Probability": 0.46,
        "Loss": 5400
    },
    {
        "Probability": 0.461,
        "Loss": 5390
    },
    {
        "Probability": 0.462,
        "Loss": 5380
    },
    {
        "Probability": 0.463,
        "Loss": 5370
    },
    {
        "Probability": 0.464,
        "Loss": 5360
    },
    {
        "Probability": 0.465,
        "Loss": 5350
    },
    {
        "Probability": 0.466,
        "Loss": 5340
    },
    {
        "Probability": 0.467,
        "Loss": 5330
    },
    {
        "Probability": 0.468,
        "Loss": 5320
    },
    {
        "Probability": 0.469,
        "Loss": 5310
    },
    {
        "Probability": 0.47,
        "Loss": 5300
    },
    {
        "Probability": 0.471,
        "Loss": 5290
    },
    {
        "Probability": 0.472,
        "Loss": 5280
    },
    {
        "Probability": 0.473,
        "Loss": 5270
    },
    {
        "Probability": 0.474,
        "Loss": 5260
    },
    {
        "Probability": 0.475,
        "Loss": 5250
    },
    {
        "Probability": 0.476,
        "Loss": 5240
    },
    {
        "Probability": 0.477,
        "Loss": 5230
    },
    {
        "Probability": 0.478,
        "Loss": 5220
    },
    {
        "Probability": 0.479,
        "Loss": 5210
    },
    {
        "Probability": 0.48,
        "Loss": 5200
    },
    {
        "Probability": 0.481,
        "Loss": 5190
    },
    {
        "Probability": 0.482,
        "Loss": 5180
    },
    {
        "Probability": 0.483,
        "Loss": 5170
    },
    {
        "Probability": 0.484,
        "Loss": 5160
    },
    {
        "Probability": 0.485,
        "Loss": 5150
    },
    {
        "Probability": 0.486,
        "Loss": 5140
    },
    {
        "Probability": 0.487,
        "Loss": 5130
    },
    {
        "Probability": 0.488,
        "Loss": 5120
    },
    {
        "Probability": 0.489,
        "Loss": 5110
    },
    {
        "Probability": 0.49,
        "Loss": 5100
    },
    {
        "Probability": 0.491,
        "Loss": 5090
    },
    {
        "Probability": 0.492,
        "Loss": 5080
    },
    {
        "Probability": 0.493,
        "Loss": 5070
    },
    {
        "Probability": 0.494,
        "Loss": 5060
    },
    {
        "Probability": 0.495,
        "Loss": 5050
    },
    {
        "Probability": 0.496,
        "Loss": 5040
    },
    {
        "Probability": 0.497,
        "Loss": 5030
    },
    {
        "Probability": 0.498,
        "Loss": 5020
    },
    {
        "Probability": 0.499,
        "Loss": 5010
    },
    {
        "Probability": 0.5,
        "Loss": 5000
    },
    {
        "Probability": 0.501,
        "Loss": 4990
    },
    {
        "Probability": 0.502,
        "Loss": 4980
    },
    {
        "Probability": 0.503,
        "Loss": 4970
    },
    {
        "Probability": 0.504,
        "Loss": 4960
    },
    {
        "Probability": 0.505,
        "Loss": 4950
    },
    {
        "Probability": 0.506,
        "Loss": 4940
    },
    {
        "Probability": 0.507,
        "Loss": 4930
    },
    {
        "Probability": 0.508,
        "Loss": 4920
    },
    {
        "Probability": 0.509,
        "Loss": 4910
    },
    {
        "Probability": 0.51,
        "Loss": 4900
    },
    {
        "Probability": 0.511,
        "Loss": 4890
    },
    {
        "Probability": 0.512,
        "Loss": 4880
    },
    {
        "Probability": 0.513,
        "Loss": 4870
    },
    {
        "Probability": 0.514,
        "Loss": 4860
    },
    {
        "Probability": 0.515,
        "Loss": 4850
    },
    {
        "Probability": 0.516,
        "Loss": 4840
    },
    {
        "Probability": 0.517,
        "Loss": 4830
    },
    {
        "Probability": 0.518,
        "Loss": 4820
    },
    {
        "Probability": 0.519,
        "Loss": 4810
    },
    {
        "Probability": 0.52,
        "Loss": 4800
    },
    {
        "Probability": 0.521,
        "Loss": 4790
    },
    {
        "Probability": 0.522,
        "Loss": 4780
    },
    {
        "Probability": 0.523,
        "Loss": 4770
    },
    {
        "Probability": 0.524,
        "Loss": 4760
    },
    {
        "Probability": 0.525,
        "Loss": 4750
    },
    {
        "Probability": 0.526,
        "Loss": 4740
    },
    {
        "Probability": 0.527,
        "Loss": 4730
    },
    {
        "Probability": 0.528,
        "Loss": 4720
    },
    {
        "Probability": 0.529,
        "Loss": 4710
    },
    {
        "Probability": 0.53,
        "Loss": 4700
    },
    {
        "Probability": 0.531,
        "Loss": 4690
    },
    {
        "Probability": 0.532,
        "Loss": 4680
    },
    {
        "Probability": 0.533,
        "Loss": 4670
    },
    {
        "Probability": 0.534,
        "Loss": 4660
    },
    {
        "Probability": 0.535,
        "Loss": 4650
    },
    {
        "Probability": 0.536,
        "Loss": 4640
    },
    {
        "Probability": 0.537,
        "Loss": 4630
    },
    {
        "Probability": 0.538,
        "Loss": 4620
    },
    {
        "Probability": 0.539,
        "Loss": 4610
    },
    {
        "Probability": 0.54,
        "Loss": 4600
    },
    {
        "Probability": 0.541,
        "Loss": 4590
    },
    {
        "Probability": 0.542,
        "Loss": 4580
    },
    {
        "Probability": 0.543,
        "Loss": 4570
    },
    {
        "Probability": 0.544,
        "Loss": 4560
    },
    {
        "Probability": 0.545,
        "Loss": 4550
    },
    {
        "Probability": 0.546,
        "Loss": 4540
    },
    {
        "Probability": 0.547,
        "Loss": 4530
    },
    {
        "Probability": 0.548,
        "Loss": 4520
    },
    {
        "Probability": 0.549,
        "Loss": 4510
    },
    {
        "Probability": 0.55,
        "Loss": 4500
    },
    {
        "Probability": 0.551,
        "Loss": 4490
    },
    {
        "Probability": 0.552,
        "Loss": 4480
    },
    {
        "Probability": 0.553,
        "Loss": 4470
    },
    {
        "Probability": 0.554,
        "Loss": 4460
    },
    {
        "Probability": 0.555,
        "Loss": 4450
    },
    {
        "Probability": 0.556,
        "Loss": 4440
    },
    {
        "Probability": 0.557,
        "Loss": 4430
    },
    {
        "Probability": 0.558,
        "Loss": 4420
    },
    {
        "Probability": 0.559,
        "Loss": 4410
    },
    {
        "Probability": 0.56,
        "Loss": 4400
    },
    {
        "Probability": 0.561,
        "Loss": 4390
    },
    {
        "Probability": 0.562,
        "Loss": 4380
    },
    {
        "Probability": 0.563,
        "Loss": 4370
    },
    {
        "Probability": 0.564,
        "Loss": 4360
    },
    {
        "Probability": 0.565,
        "Loss": 4350
    },
    {
        "Probability": 0.566,
        "Loss": 4340
    },
    {
        "Probability": 0.567,
        "Loss": 4330
    },
    {
        "Probability": 0.568,
        "Loss": 4320
    },
    {
        "Probability": 0.569,
        "Loss": 4310
    },
    {
        "Probability": 0.57,
        "Loss": 4300
    },
    {
        "Probability": 0.571,
        "Loss": 4290
    },
    {
        "Probability": 0.572,
        "Loss": 4280
    },
    {
        "Probability": 0.573,
        "Loss": 4270
    },
    {
        "Probability": 0.574,
        "Loss": 4260
    },
    {
        "Probability": 0.575,
        "Loss": 4250
    },
    {
        "Probability": 0.576,
        "Loss": 4240
    },
    {
        "Probability": 0.577,
        "Loss": 4230
    },
    {
        "Probability": 0.578,
        "Loss": 4220
    },
    {
        "Probability": 0.579,
        "Loss": 4210
    },
    {
        "Probability": 0.58,
        "Loss": 4200
    },
    {
        "Probability": 0.581,
        "Loss": 4190
    },
    {
        "Probability": 0.582,
        "Loss": 4180
    },
    {
        "Probability": 0.583,
        "Loss": 4170
    },
    {
        "Probability": 0.584,
        "Loss": 4160
    },
    {
        "Probability": 0.585,
        "Loss": 4150
    },
    {
        "Probability": 0.586,
        "Loss": 4140
    },
    {
        "Probability": 0.587,
        "Loss": 4130
    },
    {
        "Probability": 0.588,
        "Loss": 4120
    },
    {
        "Probability": 0.589,
        "Loss": 4110
    },
    {
        "Probability": 0.59,
        "Loss": 4100
    },
    {
        "Probability": 0.591,
        "Loss": 4090
    },
    {
        "Probability": 0.592,
        "Loss": 4080
    },
    {
        "Probability": 0.593,
        "Loss": 4070
    },
    {
        "Probability": 0.594,
        "Loss": 4060
    },
    {
        "Probability": 0.595,
        "Loss": 4050
    },
    {
        "Probability": 0.596,
        "Loss": 4040
    },
    {
        "Probability": 0.597,
        "Loss": 4030
    },
    {
        "Probability": 0.598,
        "Loss": 4020
    },
    {
        "Probability": 0.599,
        "Loss": 4010
    },
    {
        "Probability": 0.6,
        "Loss": 4000
    },
    {
        "Probability": 0.601,
        "Loss": 3990
    },
    {
        "Probability": 0.602,
        "Loss": 3980
    },
    {
        "Probability": 0.603,
        "Loss": 3970
    },
    {
        "Probability": 0.604,
        "Loss": 3960
    },
    {
        "Probability": 0.605,
        "Loss": 3950
    },
    {
        "Probability": 0.606,
        "Loss": 3940
    },
    {
        "Probability": 0.607,
        "Loss": 3930
    },
    {
        "Probability": 0.608,
        "Loss": 3920
    },
    {
        "Probability": 0.609,
        "Loss": 3910
    },
    {
        "Probability": 0.61,
        "Loss": 3900
    },
    {
        "Probability": 0.611,
        "Loss": 3890
    },
    {
        "Probability": 0.612,
        "Loss": 3880
    },
    {
        "Probability": 0.613,
        "Loss": 3870
    },
    {
        "Probability": 0.614,
        "Loss": 3860
    },
    {
        "Probability": 0.615,
        "Loss": 3850
    },
    {
        "Probability": 0.616,
        "Loss": 3840
    },
    {
        "Probability": 0.617,
        "Loss": 3830
    },
    {
        "Probability": 0.618,
        "Loss": 3820
    },
    {
        "Probability": 0.619,
        "Loss": 3810
    },
    {
        "Probability": 0.62,
        "Loss": 3800
    },
    {
        "Probability": 0.621,
        "Loss": 3790
    },
    {
        "Probability": 0.622,
        "Loss": 3780
    },
    {
        "Probability": 0.623,
        "Loss": 3770
    },
    {
        "Probability": 0.624,
        "Loss": 3760
    },
    {
        "Probability": 0.625,
        "Loss": 3750
    },
    {
        "Probability": 0.626,
        "Loss": 3740
    },
    {
        "Probability": 0.627,
        "Loss": 3730
    },
    {
        "Probability": 0.628,
        "Loss": 3720
    },
    {
        "Probability": 0.629,
        "Loss": 3710
    },
    {
        "Probability": 0.63,
        "Loss": 3700
    },
    {
        "Probability": 0.631,
        "Loss": 3690
    },
    {
        "Probability": 0.632,
        "Loss": 3680
    },
    {
        "Probability": 0.633,
        "Loss": 3670
    },
    {
        "Probability": 0.634,
        "Loss": 3660
    },
    {
        "Probability": 0.635,
        "Loss": 3650
    },
    {
        "Probability": 0.636,
        "Loss": 3640
    },
    {
        "Probability": 0.637,
        "Loss": 3630
    },
    {
        "Probability": 0.638,
        "Loss": 3620
    },
    {
        "Probability": 0.639,
        "Loss": 3610
    },
    {
        "Probability": 0.64,
        "Loss": 3600
    },
    {
        "Probability": 0.641,
        "Loss": 3590
    },
    {
        "Probability": 0.642,
        "Loss": 3580
    },
    {
        "Probability": 0.643,
        "Loss": 3570
    },
    {
        "Probability": 0.644,
        "Loss": 3560
    },
    {
        "Probability": 0.645,
        "Loss": 3550
    },
    {
        "Probability": 0.646,
        "Loss": 3540
    },
    {
        "Probability": 0.647,
        "Loss": 3530
    },
    {
        "Probability": 0.648,
        "Loss": 3520
    },
    {
        "Probability": 0.649,
        "Loss": 3510
    },
    {
        "Probability": 0.65,
        "Loss": 3500
    },
    {
        "Probability": 0.651,
        "Loss": 3490
    },
    {
        "Probability": 0.652,
        "Loss": 3480
    },
    {
        "Probability": 0.653,
        "Loss": 3470
    },
    {
        "Probability": 0.654,
        "Loss": 3460
    },
    {
        "Probability": 0.655,
        "Loss": 3450
    },
    {
        "Probability": 0.656,
        "Loss": 3440
    },
    {
        "Probability": 0.657,
        "Loss": 3430
    },
    {
        "Probability": 0.658,
        "Loss": 3420
    },
    {
        "Probability": 0.659,
        "Loss": 3410
    },
    {
        "Probability": 0.66,
        "Loss": 3400
    },
    {
        "Probability": 0.661,
        "Loss": 3390
    },
    {
        "Probability": 0.662,
        "Loss": 3380
    },
    {
        "Probability": 0.663,
        "Loss": 3370
    },
    {
        "Probability": 0.664,
        "Loss": 3360
    },
    {
        "Probability": 0.665,
        "Loss": 3350
    },
    {
        "Probability": 0.666,
        "Loss": 3340
    },
    {
        "Probability": 0.667,
        "Loss": 3330
    },
    {
        "Probability": 0.668,
        "Loss": 3320
    },
    {
        "Probability": 0.669,
        "Loss": 3310
    },
    {
        "Probability": 0.67,
        "Loss": 3300
    },
    {
        "Probability": 0.671,
        "Loss": 3290
    },
    {
        "Probability": 0.672,
        "Loss": 3280
    },
    {
        "Probability": 0.673,
        "Loss": 3270
    },
    {
        "Probability": 0.674,
        "Loss": 3260
    },
    {
        "Probability": 0.675,
        "Loss": 3250
    },
    {
        "Probability": 0.676,
        "Loss": 3240
    },
    {
        "Probability": 0.677,
        "Loss": 3230
    },
    {
        "Probability": 0.678,
        "Loss": 3220
    },
    {
        "Probability": 0.679,
        "Loss": 3210
    },
    {
        "Probability": 0.68,
        "Loss": 3200
    },
    {
        "Probability": 0.681,
        "Loss": 3190
    },
    {
        "Probability": 0.682,
        "Loss": 3180
    },
    {
        "Probability": 0.683,
        "Loss": 3170
    },
    {
        "Probability": 0.684,
        "Loss": 3160
    },
    {
        "Probability": 0.685,
        "Loss": 3150
    },
    {
        "Probability": 0.686,
        "Loss": 3140
    },
    {
        "Probability": 0.687,
        "Loss": 3130
    },
    {
        "Probability": 0.688,
        "Loss": 3120
    },
    {
        "Probability": 0.689,
        "Loss": 3110
    },
    {
        "Probability": 0.69,
        "Loss": 3100
    },
    {
        "Probability": 0.691,
        "Loss": 3090
    },
    {
        "Probability": 0.692,
        "Loss": 3080
    },
    {
        "Probability": 0.693,
        "Loss": 3070
    },
    {
        "Probability": 0.694,
        "Loss": 3060
    },
    {
        "Probability": 0.695,
        "Loss": 3050
    },
    {
        "Probability": 0.696,
        "Loss": 3040
    },
    {
        "Probability": 0.697,
        "Loss": 3030
    },
    {
        "Probability": 0.698,
        "Loss": 3020
    },
    {
        "Probability": 0.699,
        "Loss": 3010
    },
    {
        "Probability": 0.7,
        "Loss": 3000
    },
    {
        "Probability": 0.701,
        "Loss": 2990
    },
    {
        "Probability": 0.702,
        "Loss": 2980
    },
    {
        "Probability": 0.703,
        "Loss": 2970
    },
    {
        "Probability": 0.704,
        "Loss": 2960
    },
    {
        "Probability": 0.705,
        "Loss": 2950
    },
    {
        "Probability": 0.706,
        "Loss": 2940
    },
    {
        "Probability": 0.707,
        "Loss": 2930
    },
    {
        "Probability": 0.708,
        "Loss": 2920
    },
    {
        "Probability": 0.709,
        "Loss": 2910
    },
    {
        "Probability": 0.71,
        "Loss": 2900
    },
    {
        "Probability": 0.711,
        "Loss": 2890
    },
    {
        "Probability": 0.712,
        "Loss": 2880
    },
    {
        "Probability": 0.713,
        "Loss": 2870
    },
    {
        "Probability": 0.714,
        "Loss": 2860
    },
    {
        "Probability": 0.715,
        "Loss": 2850
    },
    {
        "Probability": 0.716,
        "Loss": 2840
    },
    {
        "Probability": 0.717,
        "Loss": 2830
    },
    {
        "Probability": 0.718,
        "Loss": 2820
    },
    {
        "Probability": 0.719,
        "Loss": 2810
    },
    {
        "Probability": 0.72,
        "Loss": 2800
    },
    {
        "Probability": 0.721,
        "Loss": 2790
    },
    {
        "Probability": 0.722,
        "Loss": 2780
    },
    {
        "Probability": 0.723,
        "Loss": 2770
    },
    {
        "Probability": 0.724,
        "Loss": 2760
    },
    {
        "Probability": 0.725,
        "Loss": 2750
    },
    {
        "Probability": 0.726,
        "Loss": 2740
    },
    {
        "Probability": 0.727,
        "Loss": 2730
    },
    {
        "Probability": 0.728,
        "Loss": 2720
    },
    {
        "Probability": 0.729,
        "Loss": 2710
    },
    {
        "Probability": 0.73,
        "Loss": 2700
    },
    {
        "Probability": 0.731,
        "Loss": 2690
    },
    {
        "Probability": 0.732,
        "Loss": 2680
    },
    {
        "Probability": 0.733,
        "Loss": 2670
    },
    {
        "Probability": 0.734,
        "Loss": 2660
    },
    {
        "Probability": 0.735,
        "Loss": 2650
    },
    {
        "Probability": 0.736,
        "Loss": 2640
    },
    {
        "Probability": 0.737,
        "Loss": 2630
    },
    {
        "Probability": 0.738,
        "Loss": 2620
    },
    {
        "Probability": 0.739,
        "Loss": 2610
    },
    {
        "Probability": 0.74,
        "Loss": 2600
    },
    {
        "Probability": 0.741,
        "Loss": 2590
    },
    {
        "Probability": 0.742,
        "Loss": 2580
    },
    {
        "Probability": 0.743,
        "Loss": 2570
    },
    {
        "Probability": 0.744,
        "Loss": 2560
    },
    {
        "Probability": 0.745,
        "Loss": 2550
    },
    {
        "Probability": 0.746,
        "Loss": 2540
    },
    {
        "Probability": 0.747,
        "Loss": 2530
    },
    {
        "Probability": 0.748,
        "Loss": 2520
    },
    {
        "Probability": 0.749,
        "Loss": 2510
    },
    {
        "Probability": 0.75,
        "Loss": 2500
    },
    {
        "Probability": 0.751,
        "Loss": 2490
    },
    {
        "Probability": 0.752,
        "Loss": 2480
    },
    {
        "Probability": 0.753,
        "Loss": 2470
    },
    {
        "Probability": 0.754,
        "Loss": 2460
    },
    {
        "Probability": 0.755,
        "Loss": 2450
    },
    {
        "Probability": 0.756,
        "Loss": 2440
    },
    {
        "Probability": 0.757,
        "Loss": 2430
    },
    {
        "Probability": 0.758,
        "Loss": 2420
    },
    {
        "Probability": 0.759,
        "Loss": 2410
    },
    {
        "Probability": 0.76,
        "Loss": 2400
    },
    {
        "Probability": 0.761,
        "Loss": 2390
    },
    {
        "Probability": 0.762,
        "Loss": 2380
    },
    {
        "Probability": 0.763,
        "Loss": 2370
    },
    {
        "Probability": 0.764,
        "Loss": 2360
    },
    {
        "Probability": 0.765,
        "Loss": 2350
    },
    {
        "Probability": 0.766,
        "Loss": 2340
    },
    {
        "Probability": 0.767,
        "Loss": 2330
    },
    {
        "Probability": 0.768,
        "Loss": 2320
    },
    {
        "Probability": 0.769,
        "Loss": 2310
    },
    {
        "Probability": 0.77,
        "Loss": 2300
    },
    {
        "Probability": 0.771,
        "Loss": 2290
    },
    {
        "Probability": 0.772,
        "Loss": 2280
    },
    {
        "Probability": 0.773,
        "Loss": 2270
    },
    {
        "Probability": 0.774,
        "Loss": 2260
    },
    {
        "Probability": 0.775,
        "Loss": 2250
    },
    {
        "Probability": 0.776,
        "Loss": 2240
    },
    {
        "Probability": 0.777,
        "Loss": 2230
    },
    {
        "Probability": 0.778,
        "Loss": 2220
    },
    {
        "Probability": 0.779,
        "Loss": 2210
    },
    {
        "Probability": 0.78,
        "Loss": 2200
    },
    {
        "Probability": 0.781,
        "Loss": 2190
    },
    {
        "Probability": 0.782,
        "Loss": 2180
    },
    {
        "Probability": 0.783,
        "Loss": 2170
    },
    {
        "Probability": 0.784,
        "Loss": 2160
    },
    {
        "Probability": 0.785,
        "Loss": 2150
    },
    {
        "Probability": 0.786,
        "Loss": 2140
    },
    {
        "Probability": 0.787,
        "Loss": 2130
    },
    {
        "Probability": 0.788,
        "Loss": 2120
    },
    {
        "Probability": 0.789,
        "Loss": 2110
    },
    {
        "Probability": 0.79,
        "Loss": 2100
    },
    {
        "Probability": 0.791,
        "Loss": 2090
    },
    {
        "Probability": 0.792,
        "Loss": 2080
    },
    {
        "Probability": 0.793,
        "Loss": 2070
    },
    {
        "Probability": 0.794,
        "Loss": 2060
    },
    {
        "Probability": 0.795,
        "Loss": 2050
    },
    {
        "Probability": 0.796,
        "Loss": 2040
    },
    {
        "Probability": 0.797,
        "Loss": 2030
    },
    {
        "Probability": 0.798,
        "Loss": 2020
    },
    {
        "Probability": 0.799,
        "Loss": 2010
    },
    {
        "Probability": 0.8,
        "Loss": 2000
    },
    {
        "Probability": 0.801,
        "Loss": 1990
    },
    {
        "Probability": 0.802,
        "Loss": 1980
    },
    {
        "Probability": 0.803,
        "Loss": 1970
    },
    {
        "Probability": 0.804,
        "Loss": 1960
    },
    {
        "Probability": 0.805,
        "Loss": 1950
    },
    {
        "Probability": 0.806,
        "Loss": 1940
    },
    {
        "Probability": 0.807,
        "Loss": 1930
    },
    {
        "Probability": 0.808,
        "Loss": 1920
    },
    {
        "Probability": 0.809,
        "Loss": 1910
    },
    {
        "Probability": 0.81,
        "Loss": 1900
    },
    {
        "Probability": 0.811,
        "Loss": 1890
    },
    {
        "Probability": 0.812,
        "Loss": 1880
    },
    {
        "Probability": 0.813,
        "Loss": 1870
    },
    {
        "Probability": 0.814,
        "Loss": 1860
    },
    {
        "Probability": 0.815,
        "Loss": 1850
    },
    {
        "Probability": 0.816,
        "Loss": 1840
    },
    {
        "Probability": 0.817,
        "Loss": 1830
    },
    {
        "Probability": 0.818,
        "Loss": 1820
    },
    {
        "Probability": 0.819,
        "Loss": 1810
    },
    {
        "Probability": 0.82,
        "Loss": 1800
    },
    {
        "Probability": 0.821,
        "Loss": 1790
    },
    {
        "Probability": 0.822,
        "Loss": 1780
    },
    {
        "Probability": 0.823,
        "Loss": 1770
    },
    {
        "Probability": 0.824,
        "Loss": 1760
    },
    {
        "Probability": 0.825,
        "Loss": 1750
    },
    {
        "Probability": 0.826,
        "Loss": 1740
    },
    {
        "Probability": 0.827,
        "Loss": 1730
    },
    {
        "Probability": 0.828,
        "Loss": 1720
    },
    {
        "Probability": 0.829,
        "Loss": 1710
    },
    {
        "Probability": 0.83,
        "Loss": 1700
    },
    {
        "Probability": 0.831,
        "Loss": 1690
    },
    {
        "Probability": 0.832,
        "Loss": 1680
    },
    {
        "Probability": 0.833,
        "Loss": 1670
    },
    {
        "Probability": 0.834,
        "Loss": 1660
    },
    {
        "Probability": 0.835,
        "Loss": 1650
    },
    {
        "Probability": 0.836,
        "Loss": 1640
    },
    {
        "Probability": 0.837,
        "Loss": 1630
    },
    {
        "Probability": 0.838,
        "Loss": 1620
    },
    {
        "Probability": 0.839,
        "Loss": 1610
    },
    {
        "Probability": 0.84,
        "Loss": 1600
    },
    {
        "Probability": 0.841,
        "Loss": 1590
    },
    {
        "Probability": 0.842,
        "Loss": 1580
    },
    {
        "Probability": 0.843,
        "Loss": 1570
    },
    {
        "Probability": 0.844,
        "Loss": 1560
    },
    {
        "Probability": 0.845,
        "Loss": 1550
    },
    {
        "Probability": 0.846,
        "Loss": 1540
    },
    {
        "Probability": 0.847,
        "Loss": 1530
    },
    {
        "Probability": 0.848,
        "Loss": 1520
    },
    {
        "Probability": 0.849,
        "Loss": 1510
    },
    {
        "Probability": 0.85,
        "Loss": 1500
    },
    {
        "Probability": 0.851,
        "Loss": 1490
    },
    {
        "Probability": 0.852,
        "Loss": 1480
    },
    {
        "Probability": 0.853,
        "Loss": 1470
    },
    {
        "Probability": 0.854,
        "Loss": 1460
    },
    {
        "Probability": 0.855,
        "Loss": 1450
    },
    {
        "Probability": 0.856,
        "Loss": 1440
    },
    {
        "Probability": 0.857,
        "Loss": 1430
    },
    {
        "Probability": 0.858,
        "Loss": 1420
    },
    {
        "Probability": 0.859,
        "Loss": 1410
    },
    {
        "Probability": 0.86,
        "Loss": 1400
    },
    {
        "Probability": 0.861,
        "Loss": 1390
    },
    {
        "Probability": 0.862,
        "Loss": 1380
    },
    {
        "Probability": 0.863,
        "Loss": 1370
    },
    {
        "Probability": 0.864,
        "Loss": 1360
    },
    {
        "Probability": 0.865,
        "Loss": 1350
    },
    {
        "Probability": 0.866,
        "Loss": 1340
    },
    {
        "Probability": 0.867,
        "Loss": 1330
    },
    {
        "Probability": 0.868,
        "Loss": 1320
    },
    {
        "Probability": 0.869,
        "Loss": 1310
    },
    {
        "Probability": 0.87,
        "Loss": 1300
    },
    {
        "Probability": 0.871,
        "Loss": 1290
    },
    {
        "Probability": 0.872,
        "Loss": 1280
    },
    {
        "Probability": 0.873,
        "Loss": 1270
    },
    {
        "Probability": 0.874,
        "Loss": 1260
    },
    {
        "Probability": 0.875,
        "Loss": 1250
    },
    {
        "Probability": 0.876,
        "Loss": 1240
    },
    {
        "Probability": 0.877,
        "Loss": 1230
    },
    {
        "Probability": 0.878,
        "Loss": 1220
    },
    {
        "Probability": 0.879,
        "Loss": 1210
    },
    {
        "Probability": 0.88,
        "Loss": 1200
    },
    {
        "Probability": 0.881,
        "Loss": 1190
    },
    {
        "Probability": 0.882,
        "Loss": 1180
    },
    {
        "Probability": 0.883,
        "Loss": 1170
    },
    {
        "Probability": 0.884,
        "Loss": 1160
    },
    {
        "Probability": 0.885,
        "Loss": 1150
    },
    {
        "Probability": 0.886,
        "Loss": 1140
    },
    {
        "Probability": 0.887,
        "Loss": 1130
    },
    {
        "Probability": 0.888,
        "Loss": 1120
    },
    {
        "Probability": 0.889,
        "Loss": 1110
    },
    {
        "Probability": 0.89,
        "Loss": 1100
    },
    {
        "Probability": 0.891,
        "Loss": 1090
    },
    {
        "Probability": 0.892,
        "Loss": 1080
    },
    {
        "Probability": 0.893,
        "Loss": 1070
    },
    {
        "Probability": 0.894,
        "Loss": 1060
    },
    {
        "Probability": 0.895,
        "Loss": 1050
    },
    {
        "Probability": 0.896,
        "Loss": 1040
    },
    {
        "Probability": 0.897,
        "Loss": 1030
    },
    {
        "Probability": 0.898,
        "Loss": 1020
    },
    {
        "Probability": 0.899,
        "Loss": 1010
    },
    {
        "Probability": 0.9,
        "Loss": 1000
    },
    {
        "Probability": 0.901,
        "Loss": 990
    },
    {
        "Probability": 0.902,
        "Loss": 980
    },
    {
        "Probability": 0.903,
        "Loss": 970
    },
    {
        "Probability": 0.904,
        "Loss": 960
    },
    {
        "Probability": 0.905,
        "Loss": 950
    },
    {
        "Probability": 0.906,
        "Loss": 940
    },
    {
        "Probability": 0.907,
        "Loss": 930
    },
    {
        "Probability": 0.908,
        "Loss": 920
    },
    {
        "Probability": 0.909,
        "Loss": 910
    },
    {
        "Probability": 0.91,
        "Loss": 900
    },
    {
        "Probability": 0.911,
        "Loss": 890
    },
    {
        "Probability": 0.912,
        "Loss": 880
    },
    {
        "Probability": 0.913,
        "Loss": 870
    },
    {
        "Probability": 0.914,
        "Loss": 860
    },
    {
        "Probability": 0.915,
        "Loss": 850
    },
    {
        "Probability": 0.916,
        "Loss": 840
    },
    {
        "Probability": 0.917,
        "Loss": 830
    },
    {
        "Probability": 0.918,
        "Loss": 820
    },
    {
        "Probability": 0.919,
        "Loss": 810
    },
    {
        "Probability": 0.92,
        "Loss": 800
    },
    {
        "Probability": 0.921,
        "Loss": 790
    },
    {
        "Probability": 0.922,
        "Loss": 780
    },
    {
        "Probability": 0.923,
        "Loss": 770
    },
    {
        "Probability": 0.924,
        "Loss": 760
    },
    {
        "Probability": 0.925,
        "Loss": 750
    },
    {
        "Probability": 0.926,
        "Loss": 740
    },
    {
        "Probability": 0.927,
        "Loss": 730
    },
    {
        "Probability": 0.928,
        "Loss": 720
    },
    {
        "Probability": 0.929,
        "Loss": 710
    },
    {
        "Probability": 0.93,
        "Loss": 700
    },
    {
        "Probability": 0.931,
        "Loss": 690
    },
    {
        "Probability": 0.932,
        "Loss": 680
    },
    {
        "Probability": 0.933,
        "Loss": 670
    },
    {
        "Probability": 0.934,
        "Loss": 660
    },
    {
        "Probability": 0.935,
        "Loss": 650
    },
    {
        "Probability": 0.936,
        "Loss": 640
    },
    {
        "Probability": 0.937,
        "Loss": 630
    },
    {
        "Probability": 0.938,
        "Loss": 620
    },
    {
        "Probability": 0.939,
        "Loss": 610
    },
    {
        "Probability": 0.94,
        "Loss": 600
    },
    {
        "Probability": 0.941,
        "Loss": 590
    },
    {
        "Probability": 0.942,
        "Loss": 580
    },
    {
        "Probability": 0.943,
        "Loss": 570
    },
    {
        "Probability": 0.944,
        "Loss": 560
    },
    {
        "Probability": 0.945,
        "Loss": 550
    },
    {
        "Probability": 0.946,
        "Loss": 540
    },
    {
        "Probability": 0.947,
        "Loss": 530
    },
    {
        "Probability": 0.948,
        "Loss": 520
    },
    {
        "Probability": 0.949,
        "Loss": 510
    },
    {
        "Probability": 0.95,
        "Loss": 500
    },
    {
        "Probability": 0.951,
        "Loss": 490
    },
    {
        "Probability": 0.952,
        "Loss": 480
    },
    {
        "Probability": 0.953,
        "Loss": 470
    },
    {
        "Probability": 0.954,
        "Loss": 460
    },
    {
        "Probability": 0.955,
        "Loss": 450
    },
    {
        "Probability": 0.956,
        "Loss": 440
    },
    {
        "Probability": 0.957,
        "Loss": 430
    },
    {
        "Probability": 0.958,
        "Loss": 420
    },
    {
        "Probability": 0.959,
        "Loss": 410
    },
    {
        "Probability": 0.96,
        "Loss": 400
    },
    {
        "Probability": 0.961,
        "Loss": 390
    },
    {
        "Probability": 0.962,
        "Loss": 380
    },
    {
        "Probability": 0.963,
        "Loss": 370
    },
    {
        "Probability": 0.964,
        "Loss": 360
    },
    {
        "Probability": 0.965,
        "Loss": 350
    },
    {
        "Probability": 0.966,
        "Loss": 340
    },
    {
        "Probability": 0.967,
        "Loss": 330
    },
    {
        "Probability": 0.968,
        "Loss": 320
    },
    {
        "Probability": 0.969,
        "Loss": 310
    },
    {
        "Probability": 0.97,
        "Loss": 300
    },
    {
        "Probability": 0.971,
        "Loss": 290
    },
    {
        "Probability": 0.972,
        "Loss": 280
    },
    {
        "Probability": 0.973,
        "Loss": 270
    },
    {
        "Probability": 0.974,
        "Loss": 260
    },
    {
        "Probability": 0.975,
        "Loss": 250
    },
    {
        "Probability": 0.976,
        "Loss": 240
    },
    {
        "Probability": 0.977,
        "Loss": 230
    },
    {
        "Probability": 0.978,
        "Loss": 220
    },
    {
        "Probability": 0.979,
        "Loss": 210
    },
    {
        "Probability": 0.98,
        "Loss": 200
    },
    {
        "Probability": 0.981,
        "Loss": 190
    },
    {
        "Probability": 0.982,
        "Loss": 180
    },
    {
        "Probability": 0.983,
        "Loss": 170
    },
    {
        "Probability": 0.984,
        "Loss": 160
    },
    {
        "Probability": 0.985,
        "Loss": 150
    },
    {
        "Probability": 0.986,
        "Loss": 140
    },
    {
        "Probability": 0.987,
        "Loss": 130
    },
    {
        "Probability": 0.988,
        "Loss": 120
    },
    {
        "Probability": 0.989,
        "Loss": 110
    },
    {
        "Probability": 0.99,
        "Loss": 100
    },
    {
        "Probability": 0.991,
        "Loss": 90
    },
    {
        "Probability": 0.992,
        "Loss": 80
    },
    {
        "Probability": 0.993,
        "Loss": 70
    },
    {
        "Probability": 0.994,
        "Loss": 60
    },
    {
        "Probability": 0.995,
        "Loss": 50
    },
    {
        "Probability": 0.996,
        "Loss": 40
    },
    {
        "Probability": 0.997,
        "Loss": 30
    },
    {
        "Probability": 0.998,
        "Loss": 20
    },
    {
        "Probability": 0.999,
        "Loss": 10
    }
]
