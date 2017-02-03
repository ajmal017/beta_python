import pandas as pd
from main import abstract
from main import constants

'''
test settings to test TaxUser class in taxsheet.py (also used in projectedtax.py)
'''

dob = pd.Timestamp('1986-01-01')

desired_retirement_age = 70.

life_exp = 79.

retirement_lifestyle = 4

reverse_mort = True

house_value = 500000.

risk_profile_group = 0.005

filing_status = abstract.PersonalData.CivilStatus['SINGLE']

total_income = 100000.

adj_gross_income = 100000.

taxable_income = 0.

total_payments = 18219.

income_growth = 2

employment_status = constants.EMPLOYMENT_STATUS_EMMPLOYED

ss_fra_todays = 3300.

ss_fra_retirement = 9900.

paid_days = 1

contrib_rate_employer_401k = 0.02

contrib_rate_employee_401k = 0.055

initial_401k_balance = 0.

zip_code = 94213

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

