import pdb
import pandas as pd
import numpy as np
from main import taxsheet
from main import testtaxsheet as tst_tx

class TaxFederal(object):
    '''
    Model for projected federal tax calculation; based on 'Projected Federal Tax Calc' tab in 'Retirement Modelling v3.xlsx' 
    '''

    def __init__(self, years, inflation, taxable_income):


        '''
        checks
        '''
        if len(inflation) != len(years):
            raise Exception('len(inflation) != len(years)')
        
        if len(taxable_income) != len(years):
            raise Exception('len(taxable_income) != len(years)')
        
        '''
        variables
        '''
        self.years              = years
        self.inflation          = inflation
        self.taxable_income     = taxable_income

        
    def create_tax_engine(self):

        '''
        tax engine
        '''

        self.tax_user_type =    ['Single',
                                 'Married_Fil_Joint',
                                 'Married_Fil_Sep',
                                 'Head_Of_House',
                                 'Qual_Widow_Dep_Child',
                                 'Married_Fil_Sep_Live_Apart']
        
        self.tax_bracket = [0., 0.1, 0.15, 0.25, 0.28, 0.33, 0.35, 0.396]

        self.tax_engine = pd.DataFrame(index=self.tax_bracket[1:])
        
        self.tax_engine['Bracket_Rate_Differential'] = [self.tax_bracket[i] - self.tax_bracket[i - 1] for i in range(1, len(self.tax_bracket))]
        
        self.tax_engine['Single']                        = [0.       , 9225.    , 37450.    , 90750.    , 189300.   , 411500.   , 413200.   ]
        self.tax_engine['Married_Fil_Joint']             = [0.       , 18450.   , 74900.    , 151200.   , 230450.   , 411500.   , 464850.   ]    
        self.tax_engine['Married_Fil_Sep']               = [0.       , 9225.    , 37450.    , 75600.    , 115225.   , 205750.   , 232425.   ]  
        self.tax_engine['Head_Of_House']                 = [0.       , 13150.   , 50200.    , 129600.   , 209850.   , 411500.   , 439000    ]   
        self.tax_engine['Qual_Widow_Dep_Child']          = [0.       , 18450.   , 74900.    , 151200.   , 230450.   , 411500.   , 464850    ]   
        self.tax_engine['Married_Fil_Sep_Live_Apart']    = [0.       , 9225.    , 37450.    , 90750.    , 189300.   , 411500.   , 413200.   ]   

        self.stand_deduct = {'Single':                      6300. ,
                             'Married_Fil_Joint':           12600. ,
                             'Married_Fil_Sep':             6300. ,
                             'Head_Of_House':               9250. ,
                             'Qual_Widow_Dep_Child':        12600. ,
                             'Married_Fil_Sep_Live_Apart':  6300. }


    def get_federal_tax(self, inflation, income, tax_user):
        '''
        returns federal tax for given income, inflation amd tax user type 
        '''
        # Names could be improved ... am not familiar with the correct tax terminology
        # also, deductions are not included in calculation ...
        self.tax_engine['Is_Greater_Than_' + tax_user] = np.where(float(income) > (self.tax_engine[tax_user]  * (1 + inflation)), 1, 0)
        self.tax_engine['Excess_' + tax_user] = income - self.tax_engine[tax_user]  * (1 + inflation)
        self.tax_engine['Bracket_Component_' + tax_user] = self.tax_engine['Bracket_Rate_Differential'] * self.tax_engine['Excess_' + tax_user] * self.tax_engine['Is_Greater_Than_' + tax_user]
        result = self.tax_engine['Bracket_Component_' + tax_user].sum()
        return result
    

    def create_tax_projected(self):
        '''
        projected federal tax
        '''
        self.tax_projected = pd.DataFrame(index = self.years)
        self.tax_projected['Ann_Avg_Inflation'] = self.inflation
        self.tax_projected['Annual_Taxable_Income'] = self.taxable_income

        for user in self.tax_user_type:
            self.tax_projected[user] = [self.get_federal_tax(self.tax_projected['Ann_Avg_Inflation'].iloc[j],
                                                                           self.tax_projected['Annual_Taxable_Income'].iloc[j],
                                                                           user) for j in range(len(self.years))]

        

if __name__ == "__main__":

    tst_tx_cls = taxsheet.TaxUser(tst_tx.name,
                                  tst_tx.ssn,
                                  tst_tx.dob,
                                  tst_tx.desired_retirement_age,
                                  tst_tx.life_exp,
                                  tst_tx.retirement_lifestyle,
                                  tst_tx.reverse_mort,
                                  tst_tx.house_value,
                                  tst_tx.filing_status,
                                  tst_tx.retire_earn_at_fra,
                                  tst_tx.retire_earn_under_fra,
                                  tst_tx.total_income,
                                  tst_tx.adj_gross,
                                  tst_tx.federal_taxable_income,
                                  tst_tx.federal_regular_tax,
                                  tst_tx.after_tax_income,
                                  tst_tx.other_income,
                                  tst_tx.ss_fra_retirement,
                                  tst_tx.paid_days,
                                  tst_tx.ira_rmo_factor,
                                  tst_tx.initial_401k_balance,
                                  tst_tx.inflation_level,
                                  tst_tx.risk_profile_over_cpi,
                                  tst_tx.projected_income_growth,
                                  tst_tx.state,
                                  tst_tx.employment_status)

    tst_tx_cls.create_maindf()

    tst_cls = TaxFederal(tst_tx_cls.years, tst_tx_cls.annual_inflation, tst_tx_cls.annual_taxable_income)
    tst_cls.create_tax_engine()
    tst_cls.create_tax_projected()
    pdb.set_trace()
    







