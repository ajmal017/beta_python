import pandas as pd
from main import abstract
from main import constants
from datetime import date
from retiresmartz.models import RetirementPlan

'''
test settings to test TaxUser class in taxsheet.py (also used in projectedtax.py)
'''

dob = pd.Timestamp('1991-04-05')

desired_retirement_age = 65.

life_exp = 82.

retirement_lifestyle = 4

total_income = 51078.

reverse_mort = False

house_value = 1.0

risk_profile_group = 0.13

filing_status = abstract.PersonalData.CivilStatus['SINGLE']

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
                  "tax_transcript_data":None
                  }

external_income = []

income_growth = 1.0

employment_status = constants.EMPLOYMENT_STATUS_EMMPLOYED

ss_fra_todays = 2000.

paid_days = 0

retirement_accounts = [{'owner': 'self', 'id': 1, 'contrib_amt': 28, 'balance': 15000, 'employer_match_type': 'contributions', 'cat': 3, 'name': 'Walmart 401k', 'balance_efdt': '2016-12-31', 'acc_type': 5, 'contrib_period': 'monthly', 'employer_match': 0.5}, {'owner': 'self', 'id': 2, 'contrib_amt': 13, 'balance': 1200, 'employer_match_type': 'none', 'cat': 4, 'name': 'Roth IRA', 'balance_efdt': '2017-02-01', 'acc_type': 8, 'contrib_period': 'yearly', 'employer_match': 0}]

zip_code = 19104

expenses = [{'id': 11, 'desc': 'Savings', 'who': 'self', 'amt': 55, 'cat': 11}, {'id': 13, 'desc': 'Tobacco', 'who': 'self', 'amt': 46, 'cat': 13}, {'id': 14, 'desc': 'Transportation', 'who': 'self', 'amt': 718, 'cat': 14}, {'id': 15, 'desc': 'Miscellaneous', 'who': 'self', 'amt': 30, 'cat': 15}, {'id': 1, 'desc': 'Alcoholic Beverage', 'who': 'self', 'amt': 45, 'cat': 1}, {'id': 2, 'desc': 'Apparel & Services', 'who': 'self', 'amt': 166, 'cat': 2}, {'id': 3, 'desc': 'Education', 'who': 'self', 'amt': 129, 'cat': 3}, {'id': 4, 'desc': 'Entertainment', 'who': 'self', 'amt': 154, 'cat': 4}, {'id': 5, 'desc': 'Food', 'who': 'self', 'amt': 614, 'cat': 5}, {'id': 6, 'desc': 'Healthcare', 'who': 'self', 'amt': 158, 'cat': 6}, {'id': 7, 'desc': 'Housing', 'who': 'self', 'amt': 1729, 'cat': 7}, {'id': 8, 'desc': 'Insuarance, Pensions & Social Security', 'who': 'self', 'amt': 215, 'cat': 8}, {'id': 12, 'desc': 'Taxes', 'who': 'self', 'amt': 154.1006810700825, 'cat': 12}]


btc = 349.


