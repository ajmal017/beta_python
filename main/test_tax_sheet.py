import pandas as pd
from main import abstract
from main import constants

'''
test settings to test TaxUser class in taxsheet.py (also used in projectedtax.py)
'''

dob = pd.Timestamp('1986-01-01')

desired_retirement_age = 64.

life_exp = 89.

retirement_lifestyle = 1

reverse_mort = False

house_value = 500000.

risk_profile_group = 0.005

filing_status = abstract.PersonalData.CivilStatus['SINGLE']

total_income = 100000.

adj_gross_income = 100.

taxable_income = 0.

total_payments = 18219.

income_growth = 0.02

employment_status = constants.EMPLOYMENT_STATUS_EMMPLOYED

ss_fra_todays = 3300.

ss_fra_retirement = 9900.

paid_days = 1

contrib_rate_employer_401k = 0.02

contrib_rate_employee_401k = 0.055

initial_401k_balance = 0.

zip_code = 94213


