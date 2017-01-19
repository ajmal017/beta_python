import pandas as pd
from main import inflation
from main import abstract
from main import constants

'''
test settings to test TaxUser class in taxsheet.py (also used in projectedtax.py)
'''

name = "John Smith"

ssn  = "123456789" 

dob = pd.Timestamp('1969-03-03')

desired_retirement_age = 70.

retirement_lifestyle = 1.

reverse_mort = True

life_exp = 85.

house_value = 250000.

filing_status = abstract.PersonalData.CivilStatus['SINGLE']

retire_earn_at_fra = 3490.

retire_earn_under_fra = 1310.

total_income = 100000.

adj_gross = 140000.

other_income=40000.

after_tax_income = 110982.

federal_taxable_income = 109996.

federal_regular_tax = 20614.

ss_fra_retirement = 7002.

paid_days = 2

ira_rmd_factor = 26.5

initial_401k_balance = 50000

inflation_level = inflation.inflation_level

risk_profile_over_cpi = 0.005

projected_income_growth = 0.01

contrib_rate_employee_401k = 0.055

contrib_rate_employer_401k = 0.02

state = "CA"

employment_status = constants.EMPLOYMENT_STATUS_SELF_EMPLOYED


