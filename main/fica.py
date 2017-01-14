import pdb
from main import taxsheet
from main import testtaxsheet as tst_tx

FICA_RATE_SS_EMPLOYED = 0.062
FICA_RATE_SS_SELF_EMPLOYED = 0.124
FICA_RATE_MEDICARE_EMPLOYED = 0.0145
FICA_RATE_MEDICARE_SELF_EMPLOYED = 0.029

FICA_INC_CEILING_SS = 118500.

class FedInsContribsAct(object):

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


if __name__ == "__main__":

    filing_status = 'Self_Employed'
    total_income = 100000.

    tst_cls = FedInsContribsAct(filing_status,
                                total_income)

    fica = tst_cls.get_fica()
    pdb.set_trace()
