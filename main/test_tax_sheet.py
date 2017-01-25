import pandas as pd
from main import abstract
from main import constants

'''
test settings to test TaxUser class in taxsheet.py (also used in projectedtax.py)
'''

name = "John Adams"
 
ssn  = "234-45-6654" 

dob = pd.Timestamp('1986-01-01')

desired_retirement_age = 66.

life_exp = 79.3

retirement_lifestyle = 2

reverse_mort = True

house_value = 0.

risk_profile_group = 0.005

filing_status = abstract.PersonalData.CivilStatus['SINGLE']

total_income = 100000.

adj_gross_income = 100000.

taxable_income = 0.

total_payments = 18219.

after_tax_income = 110982.

income_growth = 0.02

employment_status = constants.EMPLOYMENT_STATUS_EMMPLOYED

ss_fra_todays = 3311.

ss_fra_retirement = 9773.

paid_days = 1

ira_rmd_factor = 26.5

contrib_rate_employer_401k = 0.02

contrib_rate_employee_401k = 0.055

initial_401k_balance = 0.

state = "CA"


