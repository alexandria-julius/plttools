""" PLT """
import pandas as pd
import numpy


class PLT:

    """ Period Loss Table (PLT)
        Structure of a PLT is as follows:
        PeriodId (int),
        Weight (float),
        EventId (int),
        LossDate (datetime),
        EventDate (datetime),
        Loss (float),
        LossType (string - optional),
        Peril (string - optional),
        LOB (string - optional)
        Admin1 (string - optional)
        Country (string - optional)
        CedantId (string - optional)
        AccgrpId (int)
        LocName	(string)
    """

    REQUIRED_COLUMNS = ["PeriodId", "Loss", "Weight"]

    def __init__(self, data: list, number_of_simulations: int = None):
        """ Type initialiser for PLT

        Parameters
        ----------
        data:
            type(list)
            Contains a list of Period Losses [{"PeriodId": 1, "EventId":1,
            "EventDate":8/25/2016 12:00:00 AM, "LossDate":"3/13/2016 12:00:00 AM", "Loss":1000}]
        number_of_simulations:
            type(int)
            Number of simulation periods. Will default to the max period of the PLT if None

        Returns
        -------
        """
        plt_data = pd.DataFrame(data)
        if all(column in list(plt_data.columns.values) for column in PLT.REQUIRED_COLUMNS):
            self.plt = plt_data
            if number_of_simulations is None:
                self.simulations = self.plt[['PeriodId']].max().PeriodId
            else:
                self.simulations = number_of_simulations
        else:
            raise ValueError(
                "{0} field(s) not in data. Check the spelling".format(
                    ', '.join(set(PLT.REQUIRED_COLUMNS).difference(plt_data.columns))))

    def get_aal(self):
        """ Retrieves the AAL for the PLT
            Parameters
            ----------

            Returns
            -------
            float :
                The average annual loss = total annual losses / number of simulations
        """
        annual_losses = self.plt[['PeriodId', 'Loss']
                                 ].groupby('PeriodId').sum()
        total_annual_losses = annual_losses[['Loss']].sum()
        aal = total_annual_losses.Loss / self.simulations
        return aal

    def get_standard_deviation(self):
        """ Retrieves the Standard Deviation for the losses of the annual losses for the PLT
            Parameters for RM
            ----------

            Returns
            -------
            float :
                The standard deviation of the annual losses for the PLT
        """

        self.plt['variance'] = self.plt['Weight'] * self.plt['Loss'] * self.plt['Loss']
        variance = abs(self.plt['variance'].sum() - (self.get_aal() ** 2))
        stddev = numpy.sqrt(variance)
        return stddev

    def get_covvar(self):
        """ Retrieves the CV for the losses of the annual losses for the PLT
            Parameters for RM
            ----------

            Returns
            -------
            float :
                The CV of the annual losses for the PLT
        """
        # Calculate CV
        mean = (self.plt['Weight'] * self.plt['Loss']).sum()
        covvar = self.get_standard_deviation() / mean
        return covvar
