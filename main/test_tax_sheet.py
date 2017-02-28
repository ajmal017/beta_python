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
retirement_age = 56
lifestyle = 3
income = 60000.
reverse_mortgage = False
desired_risk = 0.45
income_growth = 3.
paid_days = 0
retirement_postal_code = 10052

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

expenses = [{'cat': 11, 'amt': 56, 'who': 'self', 'id': 11, 'desc': 'Savings'},
            {'cat': 13, 'amt': 26, 'who': 'self', 'id': 13, 'desc': 'Tobacco'},
            {'cat': 14, 'amt': 940, 'who': 'self', 'id': 14, 'desc': 'Transportation'},
            {'cat': 15, 'amt': 48, 'who': 'self', 'id': 15, 'desc': 'Miscellaneous'},
            {'cat': 1, 'amt': 53, 'who': 'self', 'id': 1, 'desc': 'Alcoholic Beverage'},
            {'cat': 2, 'amt': 133, 'who': 'self', 'id': 2, 'desc': 'Apparel & Services'},
            {'cat': 3, 'amt': 93, 'who': 'self', 'id': 3, 'desc': 'Education'},
            {'cat': 4, 'amt': 211, 'who': 'self', 'id': 4, 'desc': 'Entertainment'},
            {'cat': 5, 'amt': 596, 'who': 'self', 'id': 5, 'desc': 'Food'},
            {'cat': 6, 'amt': 281, 'who': 'self', 'id': 6, 'desc': 'Healthcare'},
            {'cat': 7, 'amt': 1258, 'who': 'self', 'id': 7, 'desc': 'Housing'},
            {'cat': 8, 'amt': 412, 'who': 'self', 'id': 8, 'desc': 'Insuarance, Pensions & Social Security'},
            {'cat': 9, 'amt': 54, 'who': 'self', 'id': 9, 'desc': 'Personal Care'},
            {'cat': 10, 'amt': 6, 'who': 'self', 'id': 10, 'desc': 'Reading'},
            {'cat': 12, 'amt': 698.4725578065284, 'who': 'self', 'id': 12, 'desc': 'Taxes'}]


btc = 1596.

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
                  "tax_transcript_data":{'SSN': '123-45-6789',
                                         'filing_status': 0}

                  }

date_of_birth = pd.Timestamp('1989-06-01')
home_value = 250000.
civil_status = abstract.PersonalData.CivilStatus['SINGLE'].value
employment_status = constants.EMPLOYMENT_STATUS_EMMPLOYED
ss_fra_todays = 1.

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

