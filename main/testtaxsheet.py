import pandas as pd
import inflation


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

filing_status = 'single'

retire_earn_at_fra = 3490.

retire_earn_under_fra = 1310.

total_income = 100000.

adj_gross = 140000.

other_income=40000.

after_tax_income = 110982.

federal_taxable_income = 109996.

federal_regular_tax = 20614.

state_tax_after_credits = 8404.

state_effective_rate_to_agi = 0.06

fica = 14581.

ss_fra_retirement = 7002.

paid_days = 2

ira_rmo_factor = 26.5

initial_401k_balance = 50000

inflation_level = inflation.inflation_level

risk_profile_over_cpi = 0.005

projected_income_growth = 0.01
