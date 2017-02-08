import pandas as pd
from main import abstract
from main import constants
from datetime import date

'''
test settings to test TaxUser class in taxsheet.py (also used in projectedtax.py)
'''

dob = pd.Timestamp('1991-04-05')

desired_retirement_age = 66.

life_exp = 79.

retirement_lifestyle = 3

total_income = 121908.

reverse_mort = False

house_value = 1.0

risk_profile_group = 0.17391

filing_status = abstract.PersonalData.CivilStatus['SINGLE']

regional_data = {"tax_transcript_data":None}
'''
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
                  "tax_transcript_data":{   "se_tax":0,
                                            "premium_tax_credit":0,
                                            "exemption_amount":0,
                                            "total_credits":0,
                                            "exemptions":3,
                                            "SSN_spouse":"123-45-6789\n987-65-4321",
                                            "blind":False,
                                            "adjusted_gross_income":1370,
                                            "taxable_income":0,
                                            "total_payments":0,                                            
                                            "add_child_tax_credit":0,
                                            "name":"THOMAS E TAXPAYER",
                                            "address":{     "address2":"",
                                                            "state":"USA",
                                                            "post_code":"00001",
                                                            "city":"ANYWHERE",
                                                            "address1":"123 MAIN STREET"   },
                                            "tax_period":"2011-12-31",
                                            "total_income":0,
                                            "excess_ss_credit":0,
                                            "earned_income_credit":0,
                                            "total_adjustments":0,
                                            "total_tax":0,
                                            "blind_spouse":False,
                                            "refundable_credit":0,
                                            "std_deduction":0,
                                            "SSN":"123-12-3412",
                                            "filing_status":1,
                                            "combat_credit":0,
                                            "tentative_tax":0,
                                            "name_spouse":"TAMARA B TAXPAYER" }
                  }
'''

#external_income = {'amount':0, 'begin_date': date(2020, 1, 1)}

external_income = {None}

income_growth = 1.0

employment_status = constants.EMPLOYMENT_STATUS_EMMPLOYED

ss_fra_todays = 1078.

paid_days = 0

retirement_accounts = [{'owner': 'self', 'contrib_period': 'monthly', 'balance': 1500, 'balance_efdt': '2016-12-31', 'acc_type': 5, 'employer_match_type': 'contributions', 'contrib_amt': 150, 'name': 'Walmart 401k', 'employer_match': 0.5, 'id': 1, 'cat': 3}]
 
'''
retirement_accounts = [{'employer_match_type': 'contributions', 'id': 1, 'owner': 'self', 'balance_efdt': '2017-02-02', 'name': '401K', 'employer_match': 0.49, 'contrib_amt': 250, 'balance': 25000, 'acc_type': 5, 'cat': 2, 'contrib_period': 'monthly'},
                       {'employer_match_type': 'contributions', 'id': 1, 'owner': 'self', 'balance_efdt': '2017-02-02', 'name': '401K', 'employer_match': 0.49, 'contrib_amt': 250, 'balance': 25000, 'acc_type': 5, 'cat': 2, 'contrib_period': 'monthly'},
                       {'employer_match_type': 'income', 'id': 1, 'owner': 'self', 'balance_efdt': '2017-02-02', 'name': 'Roth', 'employer_match': 0.07, 'contrib_amt': 100, 'balance': 3000, 'acc_type': 6, 'cat': 1, 'contrib_period': 'yearly'},
                       {'employer_match_type': 'none', 'id': 1, 'owner': 'self', 'balance_efdt': '2017-02-02', 'name': 'IRA', 'employer_match': 0, 'contrib_amt': 25, 'balance': 10, 'acc_type': 7, 'cat': 1, 'contrib_period': 'monthly'},
                       {'employer_match_type': 'contributions', 'id': 1, 'owner': 'self', 'balance_efdt': '2017-02-02', 'name': 'Roth IRA', 'employer_match': 0.09, 'contrib_amt': 20, 'balance': 15, 'acc_type': 8, 'cat': 1, 'contrib_period': 'monthly'},
                       {'employer_match_type': 'contributions', 'id': 1, 'owner': 'self', 'balance_efdt': '2017-02-02', 'name': 'SEP IRA', 'employer_match': 0.82, 'contrib_amt': 12, 'balance': 7, 'acc_type': 9, 'cat': 1, 'contrib_period': 'yearly'},
                       {'employer_match_type': 'none', 'id': 1, 'owner': 'self', 'balance_efdt': '2017-02-02', 'name': 'Simple IRA', 'employer_match': 0, 'contrib_amt': 6, 'balance': 12, 'acc_type': 11, 'cat': 2, 'contrib_period': 'monthly'},
                       {'employer_match_type': 'contributions', 'id': 1, 'owner': 'self', 'balance_efdt': '2017-02-02', 'name': 'SARSEP', 'employer_match': 1, 'contrib_amt': 24, 'balance': 24, 'acc_type': 12, 'cat': 2, 'contrib_period': 'yearly'},
                       {'employer_match_type': 'income', 'id': 1, 'owner': 'self', 'balance_efdt': '2017-02-02', 'name': 'MPA', 'employer_match': 0.57, 'contrib_amt': 10, 'balance': 300, 'acc_type': 16, 'cat': 6, 'contrib_period': 'monthly'},
                       {'employer_match_type': 'contributions', 'id': 1, 'owner': 'self', 'balance_efdt': '2017-02-02', 'name': 'Profit sharing', 'employer_match': 1, 'contrib_amt': 10, 'balance': 36, 'acc_type': 14, 'cat': 2, 'contrib_period': 'monthly'},
                       {'employer_match_type': 'income', 'id': 1, 'owner': 'self', 'balance_efdt': '2017-02-02', 'name': 'ESOP', 'employer_match': 0.27, 'contrib_amt': 10, 'balance': 50, 'acc_type': 17, 'cat': 7, 'contrib_period': 'monthly'}]
'''
#retirement_accounts = []

zip_code = 19104

expenses = [{'who': 'self', 'amt': 24, 'desc': 'Savings', 'id': 11, 'cat': 11}, {'who': 'self', 'amt': 66, 'desc': 'Tobacco', 'id': 13, 'cat': 13}, {'who': 'self', 'amt': 1150, 'desc': 'Transportation', 'id': 14, 'cat': 14}, {'who': 'self', 'amt': 53, 'desc': 'Miscellaneous', 'id': 15, 'cat': 15}, {'who': 'self', 'amt': 66, 'desc': 'Alcoholic Beverage', 'id': 1, 'cat': 1}, {'who': 'self', 'amt': 257, 'desc': 'Apparel & Services', 'id': 2, 'cat': 2}, {'who': 'self', 'amt': 205, 'desc': 'Education', 'id': 3, 'cat': 3}, {'who': 'self', 'amt': 240, 'desc': 'Entertainment', 'id': 4, 'cat': 4}, {'who': 'self', 'amt': 984, 'desc': 'Food', 'id': 5, 'cat': 5}, {'who': 'self', 'amt': 249, 'desc': 'Healthcare', 'id': 6, 'cat': 6}, {'who': 'self', 'amt': 2757, 'desc': 'Housing', 'id': 7, 'cat': 7}, {'who': 'self', 'amt': 93, 'desc': 'Insuarance, Pensions & Social Security', 'id': 8, 'cat': 8}, {'who': 'self', 'amt': 105, 'desc': 'Personal Care', 'id': 9, 'cat': 9}, {'who': 'self', 'amt': 9, 'desc': 'Reading', 'id': 10, 'cat': 10}, {'who': 'self', 'amt': 151, 'desc': 'Taxes', 'id': 12, 'cat': 12}]

btc = 45000.



