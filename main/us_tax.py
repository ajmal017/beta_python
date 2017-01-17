import pandas as pd
import numpy as np
import json

from main import state_tax_engine
from main import tax_sheet
from main import test_tax_sheet as tst_tx

class FederalTax(object):
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


class StateTax(object):

    '''
    Most individual U.S. states collect a state income tax in addition to federal income tax.
    The two are separate entities. State income tax is imposed at a fixed or graduated rate on
    taxable income of individuals. The rates vary by state. Taxable income conforms closely to
    federal taxable income in most states, with limited modifications. Many states allow a standard
    deduction or some form of itemized deductions. 
    '''


    def __init__(self, state, filing_status, income):

        self.state = state
        self.filing_status = filing_status
        self.income = income


    def get_state_tax(self):
        '''
        return state tax for given state, income and filing_status
        '''
        self.set_tax_engine()
        idx = self.get_index()
        df = pd.DataFrame(index=idx)
        df['Rate'] = self.get_rates()
        df['Bracket'] = self.get_brackets()

        # Names could be improved ... am not familiar with the correct tax terminology
        # also, deductions are not included in calculation ...
        df['Is_Greater_Than'] = np.where(float(self.income) > df['Bracket'], 1, 0)
        df['Excess'] = self.income - df['Bracket']
        df['Bracket_Component'] = df['Rate'] * df['Excess'] * df['Is_Greater_Than']
        result = df['Bracket_Component'].sum()
        return result


    def set_tax_engine(self):
        '''
        sets json with tax_engine for state and filing status
        '''
        found = False
        for i in range(len(state_tax_engine.tax_engine)):
            json_st_tx = json.loads(state_tax_engine.tax_engine[i])
            if json_st_tx['state'] == self.state:
                json_state_tax = json_st_tx
                found = True

        if found:
            self.tax_engine = json_state_tax[self.filing_status]

        else:
            raise Exception('state not handled')


    def get_index(self):
        '''
        returns index for rates and brackets for state and filing status
        '''
        return [i for i in range(len(self.tax_engine))]
    

    def get_rates(self):
        '''
        returns list with rates for state and filing status
        '''
        return [self.tax_engine[i]["rate"] for i in range(len(self.tax_engine))]


    def get_brackets(self):
        '''
        returns list with brackets for state and filing status
        '''
        return [self.tax_engine[i]["bracket"] for i in range(len(self.tax_engine))]
        

FICA_RATE_SS_EMPLOYED = 0.062
FICA_RATE_SS_SELF_EMPLOYED = 0.124
FICA_RATE_MEDICARE_EMPLOYED = 0.0145
FICA_RATE_MEDICARE_SELF_EMPLOYED = 0.029
FICA_INC_CEILING_SS = 118500.

class Fica(object):

    '''
    Federal Insurance Contributions Act (FICA) tax is a United States
    federal payroll (or employment) tax imposed on both employees and employers
    to fund Social Security and Medicare
    '''


    def __init__(self, filing_status, total_income):

        self.filing_status = filing_status
        self.total_income = total_income



    def get_fica(self):
        '''
        FICA = Social Security contribution + Medicare contribution
        '''

        result = self.get_for_ss() + self.get_for_medicare()

        return result
    

    def get_for_ss(self):

        if self.filing_status == 'Employed':
            '''
            For social security = IF employment_status is employed then multiply wages,
            salaries, tips etc (Line 7 of Form 1040) up to a maximum amount of $118,500
            by 6.2%
            '''
            
            result = min(self.total_income, FICA_INC_CEILING_SS) * FICA_RATE_SS_EMPLOYED
            

        elif self.filing_status == 'Self_Employed':
            '''
            For social security = IF employment_status is self employed then multiply
            business income (Line 12 of Form 1040) less SE_tax  (Line 57 of Form 1040)
            up to a maximum amount of $118,500 by 12.4%
            '''            
            # NB - assuming here that 'business income (Line 12 of Form 1040) less SE_tax
            # (Line 57 of Form 1040)' is equal to total_income
            
            result = min(self.total_income, FICA_INC_CEILING_SS) * FICA_RATE_SS_SELF_EMPLOYED

        else:
            result = 0

        return result


    def get_for_medicare(self):

        if self.filing_status == 'Employed':
            '''
            For medicare = IF employment_status is employed then multiply wages, salaries,
            tips etc (Line 7 of Form 1040)  by 1.45%F
            '''
            
            result = self.total_income * FICA_RATE_MEDICARE_EMPLOYED
            

        elif self.filing_status == 'Self_Employed':
            '''
            For medicare = IF employment_status is self employed then multiply business
            income (Line 12 of Form 1040) less SE_tax  (Line 57 of Form 1040) by 2.9%
            '''
            # NB - assuming here that 'business income (Line 12 of Form 1040) less SE_tax
            # (Line 57 of Form 1040)' is equal to total_income
            
            result = self.total_income * FICA_RATE_MEDICARE_SELF_EMPLOYED

        else:
            result = 0

        return result







