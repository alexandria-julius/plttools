""" ELT """
import pandas as pd
import numpy


class ELT:
    """ Event Loss Table (ELT)
        Structure of a ELT is as follows:
        AccgrpId (int - optional),
        LocName	(string - optional),
        LOB (string - optional),
        EventId (int),
        Rate (float),
        Loss (float),
        StdDevI (float),
        StdDevC (float),
        ExpValue (float)
    """

    REQUIRED_COLUMNS = ["EventId", "Rate", "Loss", "StdDevI", "StdDevC"]

    def __init__(self, data: list):
        """ Type initialiser for ELT

        Parameters
        ----------
        data:
            type(list)
            Contains a list of Event Losses

        Returns
        -------
        """
        elt_data = pd.DataFrame(data)
        if all(column in list(elt_data.columns.values) for column in ELT.REQUIRED_COLUMNS):
            if 'StandardDev' not in list(elt_data.columns.values):
                elt_data['StandardDev'] = elt_data['StdDevI'] + elt_data['StdDevC']
            elt_data['mu'] = elt_data['Loss'] / elt_data['ExpValue']
            elt_data['sigma'] = elt_data['StandardDev'] / elt_data['ExpValue']
            elt_data['alpha'] = ((elt_data['mu'] ** 2 * (1 - elt_data['mu'])) / elt_data['sigma'] ** 2) - elt_data['mu']
            elt_data['alpha'] = numpy.where(elt_data['alpha'] <= 0, 0.000001, elt_data['alpha'])
            elt_data['beta'] = (elt_data['alpha'] * (1 - elt_data['mu'])) / elt_data['mu']
            elt_data['beta'] = numpy.where(elt_data['beta'] <= 0, 0.000001, elt_data['beta'])

            self.elt = elt_data
        else:
            raise ValueError(
                "{0} field(s) not in data. Check the spelling".format(
                    ', '.join(set(ELT.REQUIRED_COLUMNS).difference(elt_data.columns))))

    def get_aal(self):
        """ Retrieves the AAL for the ELT
            Parameters
            ----------

            Returns
            -------
            float :
                The average annual loss = total annual losses / number of simulations
        """
        event_loss = self.elt['Loss'] * self.elt['Rate']
        aal = event_loss.sum()
        return aal

    def get_standard_deviation(self):
        """ Retrieves the Standard Deviation for the losses of the annual losses for the ELT
            ----------

            Returns
            -------
            float :
                The standard deviation of the annual losses for the ELT
        """
        self.elt['StdDev'] = self.elt['StdDevI'] + self.elt['StdDevC']
        self.elt['CV'] = self.elt['StdDev'] / self.elt['Loss']
        self.elt['stddev_calc'] = self.elt['Loss'] * self.elt['Loss'] * self.elt['Rate'] * (
                    1 + self.elt['CV'] * self.elt['CV'])
        stddev = numpy.sqrt(self.elt['stddev_calc'].sum())
        return stddev

    def get_covvar(self):
        """ Retrieves the CV for the ELT
            ----------

            Returns
            -------
            float :
                The CV of the annual losses for the ELT
        """
        covvar = self.get_standard_deviation() / self.get_aal()
        return covvar

    def get_lambda(self):
        """ Retrieves the lambda for the ELT
            ----------

            Returns
            -------
            float :
                The lambda for the ELT
        """
        elt_lambda = self.elt['Rate'].sum()

        return elt_lambda
