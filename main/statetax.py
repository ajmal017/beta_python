from main import statetaxengine as state

import json
import pandas as pd
import numpy as np

#zip_codes = pd.read_csv('zipcode_list.csv')

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
        for i in range(len(state.tax_engine)):
            json_st_tx = json.loads(state.tax_engine[i])
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
        
            
if __name__ == "__main__":

    tst_tx_cls = StateTax('CA', 'Single', 100000.)
    tst = self.set_tax_engine()
    pdb.set_trace()
