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

retirement_accounts = """[{"owner":"self", "acc_type":5, "balance":2500}]"""

