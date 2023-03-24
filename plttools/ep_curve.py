""" EP Curve module for the representation of an EP Curve"""
from enum import Enum
import pandas as pd
import numpy as np


class EPType(Enum):
    """ EP Type Enum representing type of EP Curve """
    OEP = 1
    AEP = 2
    UNKNOWN = 3


class EPCurve:
    """EP Curve"""

    RETURN_PERIODS = [2, 5, 10, 25, 50, 100, 200, 250, 500, 1000, 5000, 10000, 50000]
    REQUIRED_COLUMNS = ["Probability", "Loss"]

    def __init__(self, data: list, ep_type: EPType):
        """ Type initialiser for EP Curve

        Parameters
        ----------
        data:
            type(list)
            Contains a list of Probability and Loss pairs [{"Probability":0.01, "Loss":1000}
            ,{"Probability":0.02, "Loss":2000}]
        ep_type:
            type(EPType)
            Enum representing the type of EP Curve that this is (AEP or OEP)

        Returns
        -------
        """
        curve_data = pd.DataFrame(data)
        if all(column in list(curve_data.columns.values) for column in EPCurve.REQUIRED_COLUMNS):
            self.curve = curve_data

            max_loss_probability = [{"Probability": np.finfo(
                float).tiny, "Loss": self.curve.max().Loss}]
            self.curve = self.curve.append(pd.DataFrame(max_loss_probability))
            self.curve = self.curve.set_index('Probability')

            if ep_type is None:
                self.ep_type = EPType.UNKNOWN
            else:
                self.ep_type = ep_type
        else:
            raise ValueError(
                "Probability and Loss fields not in data. Check the spelling")

    def loss_at_a_given_return_period(self, return_period: float):
        """ Get a loss from EP curve

        Parameters
        ----------
        return_period:
            type(float)
            Non-Negative number representing the return period (reciprocal of the probability)

        Returns
        -------
        type(float) Return Period Loss
        """
        if return_period <= 0:
            raise ValueError(
                "return_period: {0} supplied is not positive".format(return_period))

        probability = 1 / return_period
        if probability in self.curve.index:
            loss = self.curve.loc[probability].Loss
        else:
            probability_array = [probability]
            self.curve = self.curve.reindex(self.curve.index.union(probability_array)).sort_index(
                ascending=True).interpolate(method='index')
            loss = self.curve.loc[probability].Loss
        return loss

    def get_ep_type(self):
        """ Get the type of EP Curve

        Parameters
        ----------

        Returns
        -------
        EPType
        """
        return self.ep_type

    def get_standard_return_period_ep(self):
        """ Calculates standard EP return periods and returns the overall curve

        Parameters
        ----------

        Returns
        -------
        type(dict) The following structure [{"Probability":0.01, "Loss":1000},
        {"Probability":0.02, "Loss":2000}]
        """
        return_periods = EPCurve.RETURN_PERIODS
        probabilities = list(map(lambda x: 1/x, return_periods))
        self.curve = self.curve[~self.curve.index.duplicated(keep='first')]
        self.curve = self.curve.reindex(self.curve.index.union(probabilities)).sort_index(
            ascending=True).interpolate(method='index')
        return self.curve.to_dict()['Loss']
