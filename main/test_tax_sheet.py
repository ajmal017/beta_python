import pandas as pd
from main import abstract
from main import constants
from datetime import date
#from retiresmartz.models import RetirementPlan
#from main.models import User, Advisor
#from client.models import Client
#from address.models import Address
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
retirement_age = 62
lifestyle = 3
income = 51078.
reverse_mortgage = False
desired_risk = 0.08
income_growth = 1.
paid_days = 0
retirement_postal_code = 19104

retirement_accounts = [{'cat': 3,
                             'employer_match_type': 'contributions',
                             'owner': 'self',
                             'contrib_period': 'monthly',
                             'contrib_amt': 28,
                             'employer_match': 0.5,
                             'balance_efdt': '2016-12-31',
                             'acc_type': 5,
                             'balance': 0,
                             'id': 1,
                             'name': 'Walmart 401k'},
                            {'cat': 4,
                             'employer_match_type': 'none',
                             'owner': 'self',
                             'contrib_period': 'yearly',
                             'contrib_amt': 13,
                             'employer_match': 0,
                             'balance_efdt': '2017-02-16',
                             'acc_type': 6,
                             'balance': 0,
                             'id': 2,
                             'name': 'Roth'}]

expenses = [{'cat': 11,
                  'amt': 24.083333333333332,
                  'id': 11,
                  'who': 'self',
                  'desc': 'Savings'},
                 {'cat': 13,
                  'amt': 18.666666666666668,
                  'id': 13,
                  'who': 'self',
                  'desc': 'Tobacco'},
                 {'cat': 14,
                  'amt': 289.4166666666667,
                  'id': 14,
                  'who': 'self',
                  'desc': 'Transportation'},
                 {'cat': 15,
                  'amt': 12.166666666666666,
                  'id': 15,
                  'who': 'self',
                  'desc': 'Miscellaneous'},
                 {'cat': 1,
                  'amt': 18.5,
                  'id': 1,
                  'who': 'self',
                  'desc': 'Alcoholic Beverage'},
                 {'cat': 2,
                  'amt': 66.91666666666667,
                  'id': 2,
                  'who': 'self',
                  'desc': 'Apparel & Services'},
                 {'cat': 3,
                  'amt': 52.5,
                  'id': 3,
                  'who': 'self',
                  'desc': 'Education'},
                 {'cat': 4,
                  'amt': 62.083333333333336,
                  'id': 4,
                  'who': 'self',
                  'desc': 'Entertainment'},
                 {'cat': 5,
                  'amt': 247.83333333333334,
                  'id': 5,
                  'who': 'self',
                  'desc': 'Food'},
                 {'cat': 6,
                  'amt': 64.08333333333333,
                  'id': 6,
                  'who': 'self',
                  'desc': 'Healthcare'},
                 {'cat': 7,
                  'amt': 696.9166666666666,
                  'id': 7,
                  'who': 'self',
                  'desc': 'Housing'},
                 {'cat': 8,
                  'amt': 93.41666666666667,
                  'id': 8,
                  'who': 'self',
                  'desc': 'Insuarance, Pensions & Social Security'},
                 {'cat': 9,
                  'amt': 24.5,
                  'id': 9,
                  'who': 'self',
                  'desc': 'Personal Care'},
                 {'cat': 10,
                  'amt': 2.4166666666666665,
                  'id': 10,
                  'who': 'self',
                  'desc': 'Reading'},
                 {'cat': 12,
                  'amt': 139,
                  'id': 12,
                  'who': 'self',
                  'desc': 'Taxes'}]

btc = 349.

# second, the client
regional_data = { "tax_transcript":"/media/sample_2012_pd4aUzv.pdf",
                  "ssn":"123-12-3412",
                  "tax_transcript_data_ex":{   "selfEmploymentTax":0,
                                               "otherRefundableCredits":0,
                                               "nonTaxableCombatPay":0,
                                               "excessSocialSecurity":0,
                                               "totalAdjustments":0,
                                               "isBlind":False,
                                               "filingStatus":1,
                                               "netPremiumCredit":0,
                                               "additionalChildTaxCredit":0,
                                               "isSpouseBlind":False,
                                               "taxableIncome":0,
                                               "adjustedGrossIncome":1370,
                                               "standardDeduction":0,
                                               "earnedIncomeCredit":0 },
                  "politically_exposed":False,
                  "tax_transcript_data":{'excess_ss_credit': 0,
                                         'total_tax': 0,
                                         'filing_status': 1,
                                         'tentative_tax': 0,
                                         'se_tax': 0,
                                         'SSN_spouse': '123-45-6789',
                                         'premium_tax_credit': 0,
                                         'earned_income_credit': 0,
                                         'refundable_credit': 0,
                                         'blind': False,
                                         'blind_spouse': False,
                                         'SSN': '123-12-3412',
                                         'total_adjustments': 0,
                                         'total_credits': 0,
                                         'combat_credit': 0,
                                         'total_income': 0,
                                         'exemptions': 3,
                                         'address': {'address1': '123 MAIN STREET',
                                                     'city': 'ANYWHERE',
                                                     'address2': '',
                                                     'post_code': '00001',
                                                     'state': 'USA'},
                                         'exemption_amount': 0,
                                         'adjusted_gross_income': 1370,
                                         'name_spouse': 'TAMARA B TAXPAYER',
                                         'tax_period': '2011-12-31',
                                         'std_deduction': 0,
                                         'name': 'THOMAS E TAXPAYER',
                                         'add_child_tax_credit': 0,
                                         'total_payments': 0,
                                         'taxable_income': 0}
                  }

date_of_birth = pd.Timestamp('1991-04-05')
home_value = 250000.
civil_status = abstract.PersonalData.CivilStatus['SINGLE'].value
employment_status = constants.EMPLOYMENT_STATUS_EMMPLOYED
ss_fra_todays = 2000.

# third, the rest
plans = []
life_exp = 79.
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

