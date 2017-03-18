import pandas as pd
from main import abstract
from main import constants
from datetime import date
import pdb


# define the objects needed
class TestClient(object):
    
    def __init__(self,
                 regional_data,
                 date_of_birth,
                 home_value,
                 civil_status,
                 employment_status,
                 ss_fra_todays):
        
        self.regional_data = regional_data
        self.date_of_birth = date_of_birth
        self.home_value = home_value
        self.civil_status = civil_status
        self.employment_status = employment_status
        self.ss_fra_todays = ss_fra_todays

class TestPlan(object):
    
    def __init__(self,
                 regional_data,
                 date_of_birth,
                 home_value,
                 civil_status,
                 employment_status,
                 ss_fra_todays,
                 retirement_age,
                 lifestyle,
                 income,
                 reverse_mortgage,
                 desired_risk,
                 income_growth,
                 paid_days,
                 retirement_postal_code,
                 retirement_accounts,
                 expenses,
                 btc):

        self.client = TestClient(regional_data,
                                 date_of_birth,
                                 home_value,
                                 civil_status,
                                 employment_status,
                                 ss_fra_todays)

        self.retirement_age = retirement_age
        self.lifestyle = lifestyle
        self.income = income
        self.reverse_mortgage = reverse_mortgage
        self.desired_risk = desired_risk
        self.income_growth = income_growth
        self.paid_days = paid_days
        self.retirement_postal_code = retirement_postal_code
        self.retirement_accounts = retirement_accounts
        self.expenses = expenses
        self.btc = btc

# first, the plan
retirement_age = 67
lifestyle = 2
income = 123456
reverse_mortgage = False
desired_risk = 0.32
income_growth = 1.0
paid_days = 0
retirement_postal_code = 1

retirement_accounts = [{'cat': 5, 'owner': 'self', 'contrib_period': 'monthly', 'id': 1, 'employer_match_type': 'income', 'name': '401K', 'balance': 1234, 'employer_match': 0.05, 'contrib_amt': 300, 'acc_type': 5, 'balance_efdt': '2017-02-06'}]

expenses = [{'cat': 1, 'who': 'self', 'desc': 'Alcoholic Beverage', 'amt': 98, 'id': 1}, {'cat': 2, 'who': 'self', 'desc': 'Apparel & Services', 'amt': 315, 'id': 2}, {'cat': 3, 'who': 'self', 'desc': 'Education', 'amt': 154, 'id': 3}, {'cat': 4, 'who': 'self', 'desc': 'Entertainment', 'amt': 406, 'id': 4}, {'cat': 5, 'who': 'self', 'desc': 'Food', 'amt': 989, 'id': 5}, {'cat': 6, 'who': 'self', 'desc': 'Healthcare', 'amt': 411, 'id': 6}, {'cat': 7, 'who': 'self', 'desc': 'Housing', 'amt': 2770, 'id': 7}, {'cat': 8, 'who': 'self', 'desc': 'Insuarance, Pensions & Social Security', 'amt': 1094, 'id': 8}, {'cat': 9, 'who': 'self', 'desc': 'Personal Care', 'amt': 97, 'id': 9}, {'cat': 10, 'who': 'self', 'desc': 'Reading', 'amt': 13, 'id': 10}, {'cat': 11, 'who': 'self', 'desc': 'Savings', 'amt': 162, 'id': 11}, {'cat': 13, 'who': 'self', 'desc': 'Tobacco', 'amt': 21, 'id': 13}, {'cat': 14, 'who': 'self', 'desc': 'Transportation', 'amt': 1281, 'id': 14}, {'cat': 15, 'who': 'self', 'desc': 'Miscellaneous', 'amt': 136, 'id': 15}, {'cat': 12, 'who': 'self', 'desc': 'Taxes', 'amt': 2040.2788727697182, 'id': 12}]

btc = 3600

# second, the client
regional_data =  {'tax_transcript_data' : {'se_tax': 0, 'total_tax': 0, 'SSN': '134-12-3413', 'std_deduction': 0, 'address': {'address2': '', 'post_code': '00001', 'state': 'USA', 'address1': '123 MAIN STREET', 'city': 'ANYWHERE'}, 'total_adjustments': 0, 'taxable_income': 0, 'combat_credit': 0, 'filing_status': 1, 'total_income': 0, 'earned_income_credit': 0, 'excess_ss_credit': 0, 'SSN_spouse': '123-45-6789\n987-65-4321', 'tentative_tax': 0, 'blind': False, 'exemption_amount': 0, 'add_child_tax_credit': 0, 'premium_tax_credit': 0, 'adjusted_gross_income': 1376, 'refundable_credit': 0, 'blind_spouse': False, 'total_credits': 0, 'name': 'THOMAS E TAXPAYER', 'total_payments': 0, 'tax_period': '2011-12-31', 'name_spouse': 'TAMARA B TAXPAYER', 'exemptions': 3}}

date_of_birth = pd.Timestamp('1990-12-21')
home_value = 1234.0
civil_status = abstract.PersonalData.CivilStatus['SINGLE'].value
employment_status = constants.EMPLOYMENT_STATUS_UNEMPLOYED
ss_fra_todays = 1078.0

# third, the rest
plans = []
life_exp = 85
is_partner = False

# now set up the plan
plan = TestPlan(regional_data,
                 date_of_birth,
                 home_value,
                 civil_status,
                 employment_status,
                 ss_fra_todays,
                 retirement_age,
                 lifestyle,
                 income,
                 reverse_mortgage,
                 desired_risk,
                 income_growth,
                 paid_days,
                 retirement_postal_code,
                 retirement_accounts,
                 expenses,
                 btc)

