import logging
import math
import pandas as pd
import numpy as np
from main import inflation
from main import us_tax
from main import test_tax_sheet as tst_tx
from main import abstract
from main import constants
from dateutil.relativedelta import relativedelta
from main import inflation
from main import zip2state
import pdb

logger = logging.getLogger('taxsheet')
inflation_level = inflation.inflation_level

class TaxUser(object):

    '''
    Contains a list of inputs and functions for Andrew's Excel tax sheet (Retirement Modelling v4.xlsx).
    '''

    def __init__(self,
                 dob,
                 desired_retirement_age,
                 life_exp,
                 retirement_lifestyle,
                 reverse_mort,
                 house_value,
                 desired_risk,
                 filing_status,
                 total_income,
                 other_income,
                 taxable_income,
                 total_payments,
                 income_growth,
                 employment_status,
                 ss_fra_todays,
                 ss_fra_retirement,
                 paid_days,
                 contrib_rate_employer_401k,
                 contrib_rate_employee_401k,
                 initial_401k_balance,
                 zip_code):

        '''
        checks
        '''
        self.debug = True
        
        if (self.debug):
            self.show_inputs(dob,
                             desired_retirement_age,
                             life_exp,
                             retirement_lifestyle,
                             reverse_mort,
                             house_value,
                             desired_risk,
                             filing_status,
                             total_income,
                             other_income,
                             taxable_income,
                             total_payments,
                             income_growth,
                             employment_status,
                             ss_fra_todays,
                             ss_fra_retirement,
                             paid_days,
                             contrib_rate_employer_401k,
                             contrib_rate_employee_401k,
                             initial_401k_balance,
                             inflation_level,
                             zip_code)

            
        if not other_income:
            other_income = 0.
            
        if not house_value:
            house_value = 0.
            
        if not ss_fra_todays:
            ss_fra_todays = 0.
            
        if not ss_fra_retirement:
            ss_fra_retirement = 0.
            
        self.validate_inputs(dob,
                             desired_retirement_age,
                             life_exp,
                             retirement_lifestyle,
                             reverse_mort,
                             house_value,
                             desired_risk,
                             filing_status,
                             total_income,
                             other_income,
                             taxable_income,
                             total_payments,
                             income_growth,
                             employment_status,
                             ss_fra_todays,
                             ss_fra_retirement,
                             paid_days,
                             contrib_rate_employer_401k,
                             contrib_rate_employee_401k,
                             initial_401k_balance,
                             inflation_level,
                             zip_code)
        
        '''
        set variables
        '''
        self.dob = dob
        self.desired_retirement_age = desired_retirement_age
        self.life_exp = life_exp
        self.retirement_lifestyle = retirement_lifestyle
        self.reverse_mort = reverse_mort
        self.house_value = house_value
        self.desired_risk = desired_risk
        self.filing_status = abstract.PersonalData.CivilStatus(filing_status)
        self.total_income = total_income
        #self.adj_gross_income = max(adj_gross_income, total_income) #adj_gross_income must be at least as big as total_income
        self.taxable_income = taxable_income
        self.total_payments = total_payments
        self.other_income = other_income
        self.income_growth = income_growth/100.
        self.employment_status = constants.EMPLOYMENT_STATUSES[employment_status]
        self.ss_fra_todays = ss_fra_todays
        self.ss_fra_retirement = ss_fra_retirement
        self.paid_days = paid_days
        self.contrib_rate_employee_401k = contrib_rate_employee_401k
        self.contrib_rate_employer_401k = contrib_rate_employer_401k
        self.initial_401k_balance = initial_401k_balance
        self.ira_rmd_factor = 26.5
        self.state = zip2state.get_state(zip_code)


        '''
        age
        '''
        self.age = ((pd.Timestamp('today')-self.dob).days)/365.25
        self.validate_age()

        '''
        retirememt period
        '''
        self.validate_life_exp_and_des_retire_age()
        self.pre_retirement_end = math.ceil((self.desired_retirement_age - self.age) * 12)  # i.e. last period in which TaxUser is younger than desired retirement age
                                                                                             # NB this period has index self.pre_retirement_end - 1
                                                                                            
        self.retirement_start = self.pre_retirement_end + 1                                 # i.e. first period in which TaxUser is older than desired retirement age
                                                                                            # NB this period has index self.retirement_start - 1

        '''
        years
        '''
        self.start_year = pd.Timestamp('today').year
        self.years_to_project = round(math.ceil(self.life_exp) - self.age) # i.e. assume user dies at the start of the year of their life expectancy, rather than at the ...
        self.retirement_years = round(math.ceil(self.life_exp) - self.desired_retirement_age)
        self.pre_retirement_years = round(self.desired_retirement_age - self.age)
        self.years = [i for i in range(self.start_year, self.start_year + self.years_to_project)]
        self.years_pre = [i for i in range(self.start_year, self.start_year + self.pre_retirement_years)]
        self.years_post = [i for i in range(self.start_year + self.pre_retirement_years, self.start_year + self.years_to_project)]

        '''
        remenant

        period to retirement may not be a whole number of years.
        'remenant' = periods representing this 'gap'
        '''
        self.remenant_periods = self.pre_retirement_end - (12 * len(self.years_pre))   
        self.remenant_start_index = (self.pre_retirement_years * 12) - 1 + 1 # i.e. we need the period AFTER the last pre-retirement period (so +1)
 
        '''
        rows
        '''
        self.total_rows = self.pre_retirement_end + (self.retirement_years * 12)
        
        '''
        inflation
        '''
        self.indices_for_inflation = [(11 + (i * 12)) for i in range(self.years_to_project)]
        if len(inflation_level) < len(self.indices_for_inflation):
            raise Exception("supplied inflation data does not cover the full period required")
        
        self.annual_inflation = [sum(inflation_level[j*12:(j*12)+12])/12. for j in range(len(self.indices_for_inflation))]

        '''
        data frame indices
        '''
        self.dateind = [pd.Timestamp('today').date() + relativedelta(months=1) + relativedelta(months=+i) for i in range(self.total_rows)]
        self.dateind_pre = [pd.Timestamp('today').date() + relativedelta(months=1) + relativedelta(months=+i) for i in range(self.pre_retirement_end)]
        self.dateind_post = [self.dateind_pre[len(self.dateind_pre)-1]
                             + relativedelta(months=1)
                             + relativedelta(months=+i) for i in range(self.total_rows - len(self.dateind_pre))]
        
        '''
        data frame
        '''
        self.maindf = pd.DataFrame(index=self.dateind)


    def set_full_series(self, series_pre, series_post):
        '''
        returns full series by appending pre-retirement and post-retirement series
        '''
        full_pre = pd.Series(series_pre, index=self.dateind_pre)
        full_post = pd.Series(series_post, index=self.dateind_post)
        result = full_pre.append(full_post)
        return result

    
    def set_full_series_with_indices(self, series_pre, series_post, index_pre, index_post):
        '''
        returns full series by appending pre-retirement series (with index2) and post-retirement
        series (with index2) 
        '''       
        full_pre = pd.Series(series_pre, index_pre)
        full_post = pd.Series(series_post, index_post)
        result = full_pre.append(full_post)
        return result


    def get_full_post_retirement_and_pre_deflated(self, temp_df_column):
        '''
        returns data frame column having 'real' (c.f. 'nominal') vales, where post retirement is calculated
        from other columns, and pre-retirement is the deflated retirement value
        '''
        nominal_pre = [temp_df_column[self.pre_retirement_end - 1] for i in range(self.pre_retirement_end)]
        real_post = [temp_df_column[self.retirement_start - 1 + i] for i in range(self.total_rows - self.pre_retirement_end)]
        result = self.maindf['Deflator'] * self.set_full_series(nominal_pre, real_post)
        return result
    

    def get_full_post_retirement_and_pre_set_zero(self, temp_df_column):
        '''
        returns data frame column having 'real' (c.f. 'nominal') values, where post retirement is calculated
        from other columns, and pre-retirement is set to zero
        '''
        nominal_pre = [0. for i in range(self.pre_retirement_end)]
        real_post = [temp_df_column[self.retirement_start - 1 + i] for i in range(self.total_rows - self.pre_retirement_end)]
        result = self.set_full_series(nominal_pre, real_post)
        return result
    

    def get_full_pre_retirement_and_post_set_zero(self, temp_df_column):
        '''
        returns data frame column having 'real' (c.f. 'nominal') values, where pre retirement is calculated
        from other columns, and post-retirement is set to zero
        '''
        nominal_pre = [temp_df_column[self.pre_retirement_end - 1] for i in range(self.pre_retirement_end)]
        real_post = [0. for i in range(self.total_rows - self.pre_retirement_end)]
        result = self.set_full_series(nominal_pre, real_post)
        return result


    def get_capital_growth_and_balance_series(self, period, account_type, starting_balance):
        '''
        returns capital growth and balance series over period for account_type
        '''
        '''
        for now can't think of a more 'pythonic' way to do this next bit ... may need re-write ...
        '''
        balance = [starting_balance for i in range(period)]
        capital_growth = [0. for i in range(period)]
        for i in range(1, period):
            capital_growth[i] = self.maindf['Portfolio_Return'][i] * balance[i - 1]
            balance[i] = self.maindf[account_type + '_Employee'][i] + self.maindf[account_type + '_Employer'][i] + capital_growth[i] + balance[i - 1]
        return capital_growth, balance


    def get_projected_fed_tax(self):
        '''
        returns projected federal tax for given filing status, years, annual inflation, and annual taxable income 
        '''

        taxFed = us_tax.FederalTax(self.years, self.annual_inflation, self.annual_taxable_income)
        taxFed.create_tax_engine()
        taxFed.create_tax_projected()
        self.annual_projected_tax = taxFed.tax_projected['Projected_Fed_Tax']


    def get_soc_sec_factor(self):
        '''
        returns factor by which to multiply ss_fra_retirement based on desired retirement age
        '''

        if self.desired_retirement_age <= 62:
            factor = 0.75

        elif self.desired_retirement_age > 62 and self.desired_retirement_age <= 63:
            factor = 0.80

        elif self.desired_retirement_age > 63 and self.desired_retirement_age <= 64:
            factor = 0.867

        elif self.desired_retirement_age > 64 and self.desired_retirement_age <= 65:
            factor = 0.933

        elif self.desired_retirement_age > 65 and self.desired_retirement_age <= 66:
            factor = 1.0

        elif self.desired_retirement_age > 66 and self.desired_retirement_age <= 67:
            factor = 1.08

        elif self.desired_retirement_age > 67 and self.desired_retirement_age <= 68:
            factor = 1.16

        elif self.desired_retirement_age > 68 and self.desired_retirement_age <= 69:
            factor = 1.24

        elif self.desired_retirement_age > 69:
            factor = 1.32

        return factor


    def get_portfolio_return_above_cpi(self):
        return self.desired_risk * 10.0 * 0.005
    

    def create_maindf(self):
        '''
        create the main data frame
        '''
        self.maindf['Person_Age'] = [self.age + (1./12.)*(i+1) for i in range(self.total_rows)]


        # MONTHLY GROWTH RATE ASSUMPTIONS

        self.pre_proj_inc_growth_monthly = [self.income_growth/12. for i in range(self.pre_retirement_end)]
        self.post_proj_inc_growth_monthly = [0. for i in range(self.total_rows - self.pre_retirement_end)]
        self.maindf['Proj_Inc_Growth_Monthly'] = self.set_full_series(self.pre_proj_inc_growth_monthly, self.post_proj_inc_growth_monthly)

        self.maindf['Proj_Inflation_Rate'] = [inflation_level[i]/12. for i in range(self.total_rows)]
        self.pre_proj_inflation_rate = [inflation_level[i]/12. for i in range(self.pre_retirement_end)] 
        self.post_proj_inflation_rate = [inflation_level[self.retirement_start + i]/12. for i in range(self.total_rows - self.pre_retirement_end)] 

        self.maindf['Portfolio_Return'] = self.maindf['Proj_Inflation_Rate'] + self.get_portfolio_return_above_cpi()/12.
        self.pre_portfolio_return = [inflation_level[i]/12. + self.get_portfolio_return_above_cpi()/12. for i in range(self.pre_retirement_end)]
        self.post_portfolio_return = [inflation_level[self.retirement_start + i]/12. + self.get_portfolio_return_above_cpi()/12.
                                      for i in range(self.total_rows - self.pre_retirement_end)]

        self.maindf['Retire_Work_Inc_Daily_Rate'] = [116*(1+self.income_growth/12.)**i for i in range(self.total_rows)]

        '''
        get the 'flators'
        '''
        self.pre_deflator = [0. for i in range(self.pre_retirement_end)]
        self.pre_deflator[self.pre_retirement_end - 1] = 1. * (1 - self.pre_proj_inflation_rate[self.pre_retirement_end - 1])                                                                                          
        for i in range (1, self.pre_retirement_end):
            self.pre_deflator[self.pre_retirement_end - 1 - i] = self.pre_deflator[self.pre_retirement_end - 1 - i + 1] * (1 - self.pre_proj_inflation_rate[self.pre_retirement_end - 1 - i])                                                                                         

        self.pre_inflator = [0. for i in range(self.pre_retirement_end)]
        self.pre_inflator[0] = 1. * (1 + self.pre_proj_inflation_rate[0])
        for i in range (1, self.pre_retirement_end):
            self.pre_inflator[i] = self.pre_inflator[i-1] * (1 + self.pre_proj_inflation_rate[i])

        self.post_inflator = [0. for i in range(self.total_rows - self.pre_retirement_end)]
        self.post_inflator[0] = 1. * (1 + self.post_proj_inflation_rate[0])
        for i in range (1, self.total_rows - self.pre_retirement_end):
            self.post_inflator[i] = self.post_inflator[i - 1] * (1 + self.post_proj_inflation_rate[i])
        
        self.maindf['Deflator'] = self.set_full_series(self.pre_deflator, [1. for i in range(self.total_rows - self.pre_retirement_end)])     # for pre-retirement
        self.maindf['Inflator'] = self.set_full_series([1. for i in range(self.pre_retirement_end)], self.post_inflator)                      # for post-retirement
        self.maindf['Flator'] = self.maindf['Deflator'] * self.maindf['Inflator']                                                             # deserves a pat on the back


        # INCOME RELATED - WORKING PERIOD

        '''
        get pre-retirement  income flator
        '''
        self.pre_df = pd.DataFrame(index=self.dateind_pre)
        self.pre_df['Inc_Growth_Monthly_Pre'] = self.maindf['Proj_Inc_Growth_Monthly'][0:self.pre_retirement_end]
        self.pre_df['Inc_Inflator_Pre'] = (1 + self.pre_df['Inc_Growth_Monthly_Pre']).cumprod()
        
        '''
        get pre-retirement inflation flator
        '''
        self.pre_df['Proj_Inflation_Rate_Pre'] = self.maindf['Proj_Inflation_Rate'][0:self.pre_retirement_end]
        self.pre_df['Inf_Inflator_Pre'] = (1 + self.pre_df['Proj_Inflation_Rate_Pre']).cumprod()
        '''
        ---
        '''

        self.pre_total_income = self.total_income/12. * self.pre_df['Inc_Inflator_Pre']
        self.post_total_income  = [0. for i in range(self.total_rows - self.pre_retirement_end)]
        self.maindf['Total_Income'] = self.set_full_series(self.pre_total_income, self.post_total_income)
        
        self.pre_other_income = self.other_income/12. * self.pre_df['Inf_Inflator_Pre']
        self.post_other_income  = [0. for i in range(self.total_rows - self.pre_retirement_end)]
        self.maindf['Other_Income'] = self.set_full_series(self.pre_other_income, self.post_other_income)                                

        self.maindf['Adj_Gross_Income'] = self.maindf['Total_Income'] + self.maindf['Other_Income']
        
        self.pre_fed_regular_tax = self.total_payments/12. * self.pre_df['Inf_Inflator_Pre']
        self.post_fed_regular_tax  = [0. for i in range(self.total_rows - self.pre_retirement_end)]
        self.maindf['Fed_Regular_Tax_Est'] = self.set_full_series(self.pre_fed_regular_tax, self.post_fed_regular_tax)
        
        self.maindf['Fed_Taxable_Income'] = self.maindf['Adj_Gross_Income'] - self.maindf['Fed_Regular_Tax_Est']
        
        self.state_tax = us_tax.StateTax(self.state, self.filing_status, self.total_income)
        self.state_tax_after_credits = self.state_tax.get_state_tax()
        self.state_effective_rate_to_agi = self.state_tax_after_credits/self.total_income

        self.pre_state_tax_after_credits = self.state_tax_after_credits/12. * self.pre_df['Inf_Inflator_Pre']      
        self.post_state_tax_after_credits = [0. for i in range(self.total_rows - self.pre_retirement_end)]

        self.maindf['State_Tax_After_Credits'] = self.set_full_series(self.pre_state_tax_after_credits, self.post_state_tax_after_credits)
            
        self.maindf['After_Tax_Income_Est'] = self.maindf['Adj_Gross_Income'] - self.maindf['Fed_Regular_Tax_Est'] - self.maindf['State_Tax_After_Credits']
    
        fica_tx = us_tax.Fica(self.employment_status, self.total_income)
        self.fica = fica_tx.get_fica()
        
        self.pre_fica = self.fica/12. * self.pre_df['Inf_Inflator_Pre']       
        self.post_fica = [0. for i in range(self.total_rows - self.pre_retirement_end)] 
        self.maindf['FICA'] = self.set_full_series(self.pre_fica, self.post_fica)

        self.maindf['Home_Value'] = self.house_value * (1+self.maindf['Proj_Inflation_Rate']).cumprod()


        # INCOME RELATED - EMPLOYEE CONTRIBUTIONS

        self.contrib_rate_employee_pension = 0.0
        self.maindf['Pension_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_pension

        self.maindf['401k_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_401k

        self.contrib_rate_employee_profit_sharing = 0.0
        self.maindf['Profit_Sharing_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_profit_sharing

        self.contrib_rate_employee_money_purchase = 0.0
        self.maindf['Money_Purchase_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_money_purchase
        
        self.contrib_rate_employee_esop = 0.0
        self.maindf['Esop_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_esop
        
        self.contrib_rate_employee_roth_401k = 0.0
        self.maindf['Roth_401k_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_roth_401k

        self.contrib_rate_employee_individual_401k = 0.0
        self.maindf['Individual_401k_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_individual_401k
      
        self.contrib_rate_employee_ind_roth_401k = 0.0
        self.maindf['Ind_Roth_401k_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_ind_roth_401k

        self.contrib_rate_employee_401a_Keogh = 0.0
        self.maindf['401a_Keogh_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_401a_Keogh

        self.contrib_rate_employee_qual_np = 0.0
        self.maindf['Qual_Np_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_qual_np

        self.contrib_rate_employee_qual_priv_457 = 0.0
        self.maindf['Qual_Priv_457_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_qual_priv_457
 
        self.contrib_rate_employee_457 = 0.0
        self.maindf['457_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_457

        self.contrib_rate_employee_qual_np_roth = 0.0
        self.maindf['Qual_Np_Roth_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_qual_np_roth

        self.contrib_rate_employee_ira = 0.0
        self.maindf['Ira_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_ira

        self.contrib_rate_employee_roth_ira = 0.0
        self.maindf['Roth_Ira_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_roth_ira

        self.contrib_rate_employee_simple_ira = 0.0
        self.maindf['Simple_Ira_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_simple_ira

        self.contrib_rate_employee_sar_sep_ira = 0.0
        self.maindf['Sar_Sep_Ira_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_sar_sep_ira
 
        self.contrib_rate_employee_sep_ira = 0.0
        self.maindf['Sep_Ira_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_sep_ira

        self.contrib_rate_employee_qual_annuity = 0.0
        self.maindf['Qual_Annuity_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_qual_annuity

        self.contrib_rate_employee_tax_def_annuity = 0.0
        self.maindf['Tax_Def_Annuity_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_tax_def_annuity


        # INCOME RELATED - EMPLOYER CONTRIBUTIONS

        self.contrib_rate_employer_pension = 0.0
        self.maindf['Pension_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_pension

        self.maindf['401k_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_401k

        self.contrib_rate_employer_profit_sharing = 0.0
        self.maindf['Profit_Sharing_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_profit_sharing

        self.contrib_rate_employer_money_purchase = 0.0
        self.maindf['Money_Purchase_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_money_purchase

        self.contrib_rate_employer_esop = 0.0
        self.maindf['Esop_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_esop

        self.contrib_rate_employer_roth_401k = 0.0
        self.maindf['Roth_401k_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_roth_401k

        self.contrib_rate_employer_individual_401k = 0.0
        self.maindf['Individual_401k_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_individual_401k

        self.contrib_rate_employer_ind_roth_401k = 0.0
        self.maindf['Ind_Roth_401k_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_ind_roth_401k

        self.contrib_rate_employer_401a_Keogh = 0.0
        self.maindf['401a_Keogh_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_401a_Keogh

        self.contrib_rate_employer_qual_np = 0.0
        self.maindf['Qual_Np_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_qual_np

        self.contrib_rate_employer_qual_priv_457 = 0.0
        self.maindf['Qual_Priv_457_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_qual_priv_457

        self.contrib_rate_employer_457 = 0.0 
        self.maindf['457_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_457

        self.contrib_rate_employer_qual_np_roth = 0.0
        self.maindf['Qual_Np_Roth_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_qual_np_roth

        self.contrib_rate_employer_ira = 0.0
        self.maindf['Ira_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_ira

        self.contrib_rate_employer_roth_ira = 0.0
        self.maindf['Roth_Ira_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_roth_ira

        self.contrib_rate_employer_simple_ira = 0.0
        self.maindf['Simple_Ira_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_simple_ira

        self.contrib_rate_employer_sar_sep_ira = 0.0
        self.maindf['Sar_Sep_Ira_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_sar_sep_ira

        self.contrib_rate_employer_sep_ira = 0.0
        self.maindf['Sep_Ira_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_sep_ira

        self.contrib_rate_employer_qual_annuity = 0.0
        self.maindf['Qual_Annuity_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_qual_annuity

        self.contrib_rate_employer_tax_def_annuity = 0.0
        self.maindf['Tax_Def_Annuity_Employer'] = self.maindf['Total_Income'] * self.contrib_rate_employer_tax_def_annuity


        # ACCOUNT CAPITAL GROWTH AND ACCOUNT BALANCE

        self.starting_balance_pension = 0.0
        self.capital_growth_pension, self.balance_pension = self.get_capital_growth_and_balance_series(self.total_rows, 'Pension', self.starting_balance_pension )
        self.maindf['Pension_Capital_Growth'] = self.capital_growth_pension
        self.maindf['Pension_Balance'] = self.balance_pension

        self.starting_balance_profit_sharing = 0.0
        self.capital_growth_profit_sharing, self.balance_profit_sharing = self.get_capital_growth_and_balance_series(self.total_rows, 'Profit_Sharing', self.starting_balance_profit_sharing )
        self.maindf['Profit_Sharing_Capital_Growth'] = self.capital_growth_profit_sharing
        self.maindf['Profit_Sharing_Balance'] = self.balance_profit_sharing

        self.starting_balance_money_purchase = 0.0
        self.capital_growth_money_purchase, self.balance_money_purchase = self.get_capital_growth_and_balance_series(self.total_rows, 'Money_Purchase', self.starting_balance_money_purchase )
        self.maindf['Money_Purchase_Capital_Growth'] = self.capital_growth_money_purchase
        self.maindf['Money_Purchase_Balance'] = self.balance_money_purchase

        self.starting_balance_esop = 0.0
        self.capital_growth_esop, self.balance_esop = self.get_capital_growth_and_balance_series(self.total_rows, 'Esop', self.starting_balance_esop )
        self.maindf['Esop_Capital_Growth'] = self.capital_growth_money_purchase
        self.maindf['Esop_Balance'] = self.balance_esop

        self.starting_balance_roth_401k = 0.0
        self.capital_growth_roth_401k, self.balance_roth_401k = self.get_capital_growth_and_balance_series(self.total_rows, 'Roth_401k', self.starting_balance_roth_401k )
        self.maindf['Roth_401k_Capital_Growth'] = self.capital_growth_roth_401k
        self.maindf['Roth_401k_Balance'] = self.balance_roth_401k

        self.starting_balance_individual_401k = 0.0
        self.capital_growth_individual_401k, self.balance_individual_401k = self.get_capital_growth_and_balance_series(self.total_rows, 'Individual_401k', self.starting_balance_individual_401k )
        self.maindf['Individual_401k_Capital_Growth'] = self.capital_growth_individual_401k
        self.maindf['Individual_401k_Balance'] = self.balance_individual_401k

        self.starting_balance_ind_roth_401k = 0.0
        self.capital_growth_ind_roth_401k, self.balance_ind_roth_401k = self.get_capital_growth_and_balance_series(self.total_rows, 'Ind_Roth_401k', self.starting_balance_ind_roth_401k )
        self.maindf['Ind_Roth_401k_Capital_Growth'] = self.capital_growth_ind_roth_401k
        self.maindf['Ind_Roth_401k_Balance'] = self.balance_ind_roth_401k

        self.starting_balance_401a_Keogh = 0.0
        self.capital_growth_401a_Keogh, self.balance_401a_Keogh = self.get_capital_growth_and_balance_series(self.total_rows, '401a_Keogh', self.starting_balance_401a_Keogh )
        self.maindf['401a_Keogh_Capital_Growth'] = self.capital_growth_401a_Keogh
        self.maindf['401a_Keogh_Balance'] = self.balance_401a_Keogh

        self.starting_balance_qual_np = 0.0
        self.capital_growth_qual_np, self.balance_qual_np = self.get_capital_growth_and_balance_series(self.total_rows, 'Qual_Np', self.starting_balance_qual_np )
        self.maindf['Qual_Np_Capital_Growth'] = self.capital_growth_qual_np
        self.maindf['Qual_Np_Balance'] = self.balance_qual_np

        self.starting_balance_qual_priv_457 = 0.0
        self.capital_growth_qual_priv_457, self.balance_qual_priv_457 = self.get_capital_growth_and_balance_series(self.total_rows, 'Qual_Priv_457', self.starting_balance_qual_priv_457 )
        self.maindf['Qual_Priv_457_Capital_Growth'] = self.capital_growth_qual_priv_457
        self.maindf['Qual_Priv_457_Balance'] = self.balance_qual_priv_457

        self.starting_balance_457 = 0.0
        self.capital_growth_457, self.balance_457 = self.get_capital_growth_and_balance_series(self.total_rows, '457', self.starting_balance_457 )
        self.maindf['457_Capital_Growth'] = self.capital_growth_457
        self.maindf['457_Balance'] = self.balance_457

        self.starting_balance_qual_np_roth = 0.0
        self.capital_growth_qual_np_roth, self.balance_qual_np_roth = self.get_capital_growth_and_balance_series(self.total_rows, 'Qual_Np_Roth', self.starting_balance_qual_np_roth )
        self.maindf['Qual_Np_Roth_Capital_Growth'] = self.capital_growth_qual_np_roth
        self.maindf['Qual_Np_Roth_Balance'] = self.balance_qual_np_roth

        self.starting_balance_ira = 0.0
        self.capital_growth_ira, self.balance_ira = self.get_capital_growth_and_balance_series(self.total_rows, 'Ira', self.starting_balance_ira )
        self.maindf['Ira_Capital_Growth'] = self.capital_growth_ira
        self.maindf['Ira_Balance'] = self.balance_ira

        self.starting_balance_roth_ira = 0.0
        self.capital_growth_roth_ira, self.balance_roth_ira = self.get_capital_growth_and_balance_series(self.total_rows, 'Roth_Ira', self.starting_balance_roth_ira )
        self.maindf['Roth_Ira_Capital_Growth'] = self.capital_growth_roth_ira
        self.maindf['Roth_Ira_Balance'] = self.balance_roth_ira

        self.starting_balance_simple_ira = 0.0
        self.capital_growth_simple_ira, self.balance_simple_ira = self.get_capital_growth_and_balance_series(self.total_rows, 'Simple_Ira', self.starting_balance_simple_ira )
        self.maindf['Simple_Ira_Capital_Growth'] = self.capital_growth_simple_ira
        self.maindf['Simple_Ira_Balance'] = self.balance_simple_ira

        self.starting_balance_sar_sep_ira = 0.0
        self.capital_growth_sar_sep_ira, self.balance_sar_sep_ira = self.get_capital_growth_and_balance_series(self.total_rows, 'Sar_Sep_Ira', self.starting_balance_sar_sep_ira )
        self.maindf['Sar_Sep_Ira_Capital_Growth'] = self.capital_growth_sar_sep_ira
        self.maindf['Sar_Sep_Ira_Balance'] = self.balance_sar_sep_ira

        self.starting_balance_sep_ira = 0.0
        self.capital_growth_sep_ira, self.balance_sep_ira = self.get_capital_growth_and_balance_series(self.total_rows, 'Sep_Ira', self.starting_balance_sep_ira )
        self.maindf['Sep_Ira_Capital_Growth'] = self.capital_growth_sep_ira
        self.maindf['Sep_Ira_Balance'] = self.balance_sep_ira

        self.starting_balance_qual_annuity = 0.0
        self.capital_growth_qual_annuity, self.balance_qual_annuity = self.get_capital_growth_and_balance_series(self.total_rows, 'Qual_Annuity', self.starting_balance_qual_annuity )
        self.maindf['Qual_Annuity_Capital_Growth'] = self.capital_growth_qual_annuity
        self.maindf['Qual_Annuity_Balance'] = self.balance_qual_annuity

        self.starting_balance_tax_def_annuity = 0.0
        self.capital_growth_tax_def_annuity, self.balance_tax_def_annuity = self.get_capital_growth_and_balance_series(self.total_rows, 'Tax_Def_Annuity', self.starting_balance_tax_def_annuity )
        self.maindf['Tax_Def_Annuity_Capital_Growth'] = self.capital_growth_tax_def_annuity
        self.maindf['Tax_Def_Annuity_Balance'] = self.balance_tax_def_annuity
        
        self.maindf['Nontaxable_Accounts'] = np.where(self.maindf['Roth_401k_Balance'] + self.maindf['Ind_Roth_401k_Balance'] + self.maindf['Roth_Ira_Balance'] > 0,
                                                      self.maindf['Roth_401k_Balance'] + self.maindf['Ind_Roth_401k_Balance'] + self.maindf['Roth_Ira_Balance'],
                                                      0)


        # 401K
        
        '''
        for now can't think of a more 'pythonic' way to do this next bit ... may need re-write ...
        ''' 
        self.pre_401k_capital_growth, self.pre_401k_balance = self.get_capital_growth_and_balance_series(self.pre_retirement_end, '401k', self.initial_401k_balance )        

        self.post_401k_balance = [self.pre_401k_balance[self.pre_retirement_end - 1] for i in range(self.total_rows - self.pre_retirement_end)]
        self.post_401k_capital_growth = [0. for i in range(self.total_rows - self.pre_retirement_end)]
                
        for i in range(1, self.total_rows - self.pre_retirement_end): 
            self.post_401k_capital_growth[i] = ((self.contrib_rate_employee_401k + self.contrib_rate_employer_401k) * self.post_total_income[i]) + (self.post_portfolio_return[i] * self.post_401k_balance[i - 1]) 

            if (self.contrib_rate_employee_401k + self.contrib_rate_employer_401k) * self.post_total_income[i] + self.post_401k_capital_growth[i] + self.post_401k_balance[i - 1] > 0:
                self.post_401k_balance[i] = self.post_401k_capital_growth[i] + self.post_401k_balance[i - 1]
            else:
                self.post_401k_balance[i] = 0.

        self.maindf['401k_Capital_Growth'] = self.set_full_series(self.pre_401k_capital_growth, self.post_401k_capital_growth)
        self.maindf['401k_Balance'] = self.set_full_series(self.pre_401k_balance, self.post_401k_balance)
        '''
        glad to have got that out of the way ...
        '''

        # CERTAIN INCOME
        if self.retirement_lifestyle == 1:
            self.lifestyle_factor = 0.66

        elif self.retirement_lifestyle == 2:
            self.lifestyle_factor = 0.81

        elif self.retirement_lifestyle == 3:
            self.lifestyle_factor = 1

        elif self.retirement_lifestyle == 4:
            self.lifestyle_factor = 1.5

        
        self.pre_des_ret_inc_pre_tax = self.lifestyle_factor * self.maindf['Adj_Gross_Income'][0:self.pre_retirement_end]
        self.post_des_ret_inc_pre_tax = [self.pre_des_ret_inc_pre_tax[len(self.pre_des_ret_inc_pre_tax) - 1] for i in range(self.total_rows - self.pre_retirement_end)] 
        self.maindf['Des_Ret_Inc_Pre_Tax_Post_Nominal'] = self.set_full_series(self.pre_des_ret_inc_pre_tax, self.post_des_ret_inc_pre_tax)
        self.maindf['Des_Ret_Inc_Pre_Tax'] = self.maindf['Des_Ret_Inc_Pre_Tax_Post_Nominal'] * self.maindf['Inflator']


        '''
        use the 'flators'
        '''
        self.inflated_ss_fra_todays = self.ss_fra_todays * self.pre_inflator[self.pre_retirement_end - 1]
        self.nominal_soc_sec_benefit_pre = [self.inflated_ss_fra_todays for i in range(self.pre_retirement_end)]
        self.nominal_soc_sec_benefit_post = [(self.ss_fra_retirement * self.get_soc_sec_factor()) for i in range(self.total_rows - self.pre_retirement_end)]
        
        self.maindf['Nominal_Soc_Sec_Benefit'] = self.set_full_series(self.nominal_soc_sec_benefit_pre, self.nominal_soc_sec_benefit_post)
        self.maindf['Soc_Sec_Benefit'] = self.maindf['Flator'] * self.maindf['Nominal_Soc_Sec_Benefit']
        self.maindf['Soc_Sec_Ret_Ear_Tax_Exempt'] = self.maindf['Soc_Sec_Benefit']

        self.maindf['Nominal_Ret_Working_Inc'] = np.where(self.maindf['Person_Age'] < 80, self.maindf['Retire_Work_Inc_Daily_Rate'] * 4 * self.paid_days, 0)
        self.maindf['Ret_Working_Inc'] = self.maindf['Deflator'] * self.maindf['Nominal_Ret_Working_Inc']
        
        self.maindf['Nominal_Pension_Payments'] = [0. for i in range(self.total_rows)]
        self.maindf['Pension_Payments'] = self.maindf['Deflator'] * self.maindf['Nominal_Pension_Payments']

        self.maindf['Nominal_Annuity_Payments'] = [0. for i in range(self.total_rows)]
        self.maindf['Annuity_Payments'] = self.maindf['Deflator'] * self.maindf['Nominal_Annuity_Payments']

        if self.reverse_mort:
            self.post_reverse_mortgage = np.where(self.age > 0,
                                                        np.where(self.maindf['Total_Income'] == 0,
                                                                 np.where(self.maindf['Person_Age'] > 62,
                                                                          self.maindf['Home_Value'][self.retirement_start - 1] * (0.9/(self.retirement_years * 12.)),
                                                                          0),
                                                                 0),
                                                        0)[self.pre_retirement_end:]

        else:
            self.post_reverse_mortgage = [0. for i in range(self.total_rows - self.pre_retirement_end)]
            
        self.pre_reverse_mortgage = [self.post_reverse_mortgage[0] for i in range (self.pre_retirement_end)]
        self.maindf['Reverse_Mortgage_Nominal'] = self.set_full_series(self.pre_reverse_mortgage, self.post_reverse_mortgage)
        self.maindf['Reverse_Mortgage'] = self.maindf['Deflator'] * self.maindf['Reverse_Mortgage_Nominal']
        
        self.maindf['Certain_Ret_Inc'] = self.get_full_post_retirement_and_pre_deflated(self.maindf['Soc_Sec_Benefit']
                                                                                        + self.maindf['Ret_Working_Inc']
                                                                                        + self.maindf['Pension_Payments']
                                                                                        + self.maindf['Annuity_Payments']
                                                                                        + self.maindf['Reverse_Mortgage'])

        # TAXABLE ACCOUNTS

        self.maindf['Taxable_Accounts_Pre_Deccumulation'] = self.maindf['Pension_Balance'] \
                                                        + self.maindf['401k_Balance'] \
                                                        + self.maindf['Profit_Sharing_Balance'] \
                                                        + self.maindf['Money_Purchase_Balance'] \
                                                        + self.maindf['Esop_Balance'] \
                                                        + self.maindf['Roth_401k_Balance'] \
                                                        + self.maindf['Individual_401k_Balance'] \
                                                        + self.maindf['Ind_Roth_401k_Balance'] \
                                                        + self.maindf['401a_Keogh_Balance'] \
                                                        + self.maindf['Qual_Np_Balance'] \
                                                        + self.maindf['Qual_Priv_457_Balance'] \
                                                        + self.maindf['457_Balance'] \
                                                        + self.maindf['Qual_Np_Roth_Balance'] \
                                                        + self.maindf['Ira_Balance'] \
                                                        + self.maindf['Roth_Ira_Balance'] \
                                                        + self.maindf['Simple_Ira_Balance'] \
                                                        + self.maindf['Sar_Sep_Ira_Balance'] \
                                                        + self.maindf['Sep_Ira_Balance'] \
                                                        + self.maindf['Qual_Annuity_Balance'] \
                                                        + self.maindf['Tax_Def_Annuity_Balance'] \
                                                        - self.maindf['Nontaxable_Accounts']
        
                                            
        # DECCUMULATION

        self.maindf['Ret_Certain_Inc_Gap'] = self.get_full_post_retirement_and_pre_deflated(self.maindf['Des_Ret_Inc_Pre_Tax']
                                                                                            - self.maindf['Certain_Ret_Inc'])

        '''
        for now can't think of a more 'pythonic' way to do this next bit ... may need re-write ...
        ''' 
        self.pre_deccumulation_capital_growth = [0. for i in range(self.pre_retirement_end)]
        self.pre_deccumulation_balance = [0. for i in range(self.pre_retirement_end)]      

        self.post_deccumulation_balance = [0. for i in range(self.total_rows - self.pre_retirement_end)]
        self.post_deccumulation_capital_growth = [0. for i in range(self.total_rows - self.pre_retirement_end)]
                
        for i in range(1, self.total_rows - self.pre_retirement_end): 
            self.post_deccumulation_capital_growth[i] = self.post_portfolio_return[i] * self.post_deccumulation_balance[i - 1] - self.maindf['Ret_Certain_Inc_Gap'].iloc[self.pre_retirement_end + i]
            self.post_deccumulation_balance[i] = self.post_deccumulation_capital_growth[i] + self.post_deccumulation_balance[i - 1]

        self.maindf['Deccumulation_Capital_Growth'] = self.set_full_series(self.pre_deccumulation_capital_growth, self.post_deccumulation_capital_growth)
        self.maindf['Deccumulation_Balance'] = self.set_full_series(self.pre_deccumulation_balance, self.post_deccumulation_balance)

        self.maindf['Taxable_Accounts'] = np.where(self.maindf['Taxable_Accounts_Pre_Deccumulation'] + self.maindf['Deccumulation_Balance'] > 0,
                                                   self.maindf['Taxable_Accounts_Pre_Deccumulation'] + self.maindf['Deccumulation_Balance'], 0)

        self.maindf['Reqd_Min_Dist'] = np.where(self.maindf['Person_Age'] > 70.5, self.maindf['Taxable_Accounts'] /(self.ira_rmd_factor * 12.), 0)

        self.maindf['Tot_Non_Taxable_Dist'] = self.get_full_post_retirement_and_pre_set_zero(np.where(self.maindf['Ret_Certain_Inc_Gap'] > self.maindf['Reqd_Min_Dist'],
                                                                                                      np.where(self.maindf['Nontaxable_Accounts'] > 0
                                                                                                               , self.maindf['Ret_Certain_Inc_Gap'] - self.maindf['Reqd_Min_Dist'], 0)
                                                                                                      , 0))    

        self.maindf['Tot_Taxable_Dist'] = self.get_full_post_retirement_and_pre_set_zero(np.where(self.maindf['Reqd_Min_Dist'] > 0,
                                                                                                   self.maindf['Ret_Certain_Inc_Gap'] - self.maindf['Tot_Non_Taxable_Dist'],
                                                                                                   np.where(self.maindf['Reqd_Min_Dist'] - self.maindf['Tot_Non_Taxable_Dist'] > 0,
                                                                                                            self.maindf['Reqd_Min_Dist'] - self.maindf['Tot_Non_Taxable_Dist'],
                                                                                                            0)))

        self.maindf['Ret_Inc_Gap'] = self.get_full_post_retirement_and_pre_set_zero(self.maindf['Ret_Certain_Inc_Gap']
                                                                                     - self.maindf['Tot_Non_Taxable_Dist']
                                                                                     - self.maindf['Tot_Taxable_Dist'])

        
        # CALCULATION OF AFTER TAX INCOME

        self.maindf['Non_Taxable_Inc'] = self.maindf['Tot_Non_Taxable_Dist'] + self.maindf['Reverse_Mortgage']
        
        self.maindf['Taxable_Soc_Sec'] = self.get_full_post_retirement_and_pre_set_zero(self.maindf['Soc_Sec_Benefit']
                                                                                        + self.maindf['Ret_Working_Inc']
                                                                                        + self.maindf['Pension_Payments']
                                                                                        + self.maindf['Annuity_Payments']
                                                                                        + self.maindf['Tot_Taxable_Dist']
                                                                                        - self.maindf['Soc_Sec_Ret_Ear_Tax_Exempt'])

        self.maindf['Tot_Inc'] = self.get_full_post_retirement_and_pre_set_zero(self.maindf['Non_Taxable_Inc']
                                                                                + self.maindf['Tot_Taxable_Dist']
                                                                                + self.maindf['Annuity_Payments']
                                                                                + self.maindf['Pension_Payments']
                                                                                + self.maindf['Ret_Working_Inc']
                                                                                + self.maindf['Soc_Sec_Benefit'])

        self.taxable_inc_pre = (self.maindf['Soc_Sec_Benefit']
                                + self.maindf['Ret_Working_Inc']
                                + self.maindf['Pension_Payments']
                                + self.maindf['Annuity_Payments']
                                + self.maindf['Tot_Taxable_Dist'])[:self.pre_retirement_end]

        self.taxable_inc_post = (self.maindf['Taxable_Soc_Sec']
                                 + self.maindf['Ret_Working_Inc']
                                 + self.maindf['Pension_Payments']
                                 + self.maindf['Annuity_Payments']
                                 + self.maindf['Tot_Taxable_Dist'])[self.pre_retirement_end:]
        
        self.maindf['Taxable_Inc'] = self.set_full_series(self.taxable_inc_pre, self.taxable_inc_post)

        self.maindf['Adj_Gross_Inc'] = self.maindf['Tot_Inc']

        '''
        federal tax
        '''
        self.maindf['Fed_Taxable_Inc'] = self.set_full_series([0. for i in range(self.pre_retirement_end)], self.maindf['Taxable_Inc'][self.pre_retirement_end:])

        self.annual_taxable_income_pre = [self.maindf['Fed_Taxable_Income'][(i * 12)]
                                          + self.maindf['Fed_Taxable_Income'][(i * 12) + 1]
                                          + self.maindf['Fed_Taxable_Income'][(i * 12) + 2]
                                          + self.maindf['Fed_Taxable_Income'][(i * 12) + 3]
                                          + self.maindf['Fed_Taxable_Income'][(i * 12) + 4]
                                          + self.maindf['Fed_Taxable_Income'][(i * 12) + 5]
                                          + self.maindf['Fed_Taxable_Income'][(i * 12) + 6]
                                          + self.maindf['Fed_Taxable_Income'][(i * 12) + 7]
                                          + self.maindf['Fed_Taxable_Income'][(i * 12) + 8]
                                          + self.maindf['Fed_Taxable_Income'][(i * 12) + 9]
                                          + self.maindf['Fed_Taxable_Income'][(i * 12) + 10]
                                          + self.maindf['Fed_Taxable_Income'][(i * 12) + 11] for i in range(self.pre_retirement_years)]

        for i in range(self.remenant_periods):
            self.annual_taxable_income_pre = self.maindf['Fed_Taxable_Income'][self.remenant_start_index -1 + i]
        
        self.annual_taxable_income_post = [self.maindf['Taxable_Inc'][self.retirement_start - 1 + (i * 12)]
                                           + self.maindf['Taxable_Inc'][self.retirement_start - 1 + (i * 12) + 1]
                                           + self.maindf['Taxable_Inc'][self.retirement_start - 1 + (i * 12) + 2]
                                           + self.maindf['Taxable_Inc'][self.retirement_start - 1 + (i * 12) + 3]
                                           + self.maindf['Taxable_Inc'][self.retirement_start - 1 + (i * 12) + 4]
                                           + self.maindf['Taxable_Inc'][self.retirement_start - 1 + (i * 12) + 5]
                                           + self.maindf['Taxable_Inc'][self.retirement_start - 1 + (i * 12) + 6]
                                           + self.maindf['Taxable_Inc'][self.retirement_start - 1 + (i * 12) + 7]
                                           + self.maindf['Taxable_Inc'][self.retirement_start - 1 + (i * 12) + 8]
                                           + self.maindf['Taxable_Inc'][self.retirement_start - 1 + (i * 12) + 9]
                                           + self.maindf['Taxable_Inc'][self.retirement_start - 1 + (i * 12) + 10]
                                           + self.maindf['Taxable_Inc'][self.retirement_start - 1 + (i * 12) + 11] for i in range(self.retirement_years)]
       
        self.annual_taxable_income = self.set_full_series_with_indices(self.annual_taxable_income_pre,
                                                                       self.annual_taxable_income_post,
                                                                       self.years_pre,
                                                                       self.years_post)

        taxFed = us_tax.FederalTax(self.filing_status,
                                   self.years,
                                   self.annual_inflation,
                                   self.annual_taxable_income)
        taxFed.create_tax_engine()
        taxFed.create_tax_projected()

        self.annual_projected_tax = taxFed.tax_projected['Projected_Fed_Tax']
        
        self.post_projected_tax = pd.Series()
        
        for i in range(len(self.years_post)):
            self.post_projected_tax = self.post_projected_tax.append(pd.Series([self.annual_projected_tax.iloc[self.pre_retirement_years - 1  + 1 + i]/12.,
                                                                                self.annual_projected_tax.iloc[self.pre_retirement_years - 1  + 1 + i]/12.,
                                                                                self.annual_projected_tax.iloc[self.pre_retirement_years - 1  + 1 + i]/12.,
                                                                                self.annual_projected_tax.iloc[self.pre_retirement_years- 1 + 1 + i]/12.,
                                                                                self.annual_projected_tax.iloc[self.pre_retirement_years - 1 + 1 + i]/12.,
                                                                                self.annual_projected_tax.iloc[self.pre_retirement_years - 1 + 1 + i]/12.,
                                                                                self.annual_projected_tax.iloc[self.pre_retirement_years- 1 + 1 + i]/12.,
                                                                                self.annual_projected_tax.iloc[self.pre_retirement_years - 1 + 1 + i]/12.,
                                                                                self.annual_projected_tax.iloc[self.pre_retirement_years - 1 + 1 + i]/12.,
                                                                                self.annual_projected_tax.iloc[self.pre_retirement_years - 1 + 1 + i]/12.,
                                                                                self.annual_projected_tax.iloc[self.pre_retirement_years - 1 + 1 + i]/12.,
                                                                                self.annual_projected_tax.iloc[self.pre_retirement_years - 1 + 1 + i]/12.],
                                                                               index = [self.dateind_post[i * 12],
                                                                               self.dateind_post[(i * 12) + 1],
                                                                               self.dateind_post[(i * 12) + 2],
                                                                               self.dateind_post[(i * 12) + 3],
                                                                               self.dateind_post[(i * 12) + 4],
                                                                               self.dateind_post[(i * 12) + 5],
                                                                               self.dateind_post[(i * 12) + 6],
                                                                               self.dateind_post[(i * 12) + 7],
                                                                               self.dateind_post[(i * 12) + 8],
                                                                               self.dateind_post[(i * 12) + 9],
                                                                               self.dateind_post[(i * 12) + 10],
                                                                               self.dateind_post[(i * 12) + 11]]))

        
        full_post = pd.Series(self.post_projected_tax, index=self.dateind_post) 
        self.maindf['Fed_Regular_Tax'] = self.set_full_series([0. for i in range(self.pre_retirement_end)], self.post_projected_tax )
        
        self.maindf['State_Tax_After_Credits'] = self.maindf['Adj_Gross_Inc'] * self.state_effective_rate_to_agi

        self.maindf['After_Tax_Income'] = self.maindf['Adj_Gross_Inc'] - self.maindf['Fed_Regular_Tax'] - self.maindf['State_Tax_After_Credits']

        # Actual income
        self.maindf['Actual_Inc'] = self.maindf['Total_Income'] + self.maindf['Tot_Inc']

        # Desired income
        self.pre_0 = [0 for i in range(self.pre_retirement_end)]
        self.maindf['Desired_Inc'] = self.set_full_series(self.pre_0, self.post_des_ret_inc_pre_tax) * self.maindf['Inflator']

        if(self.debug):
            self.show_outputs()
        
        
    def validate_inputs(self,
                         dob,
                         desired_retirement_age,
                         life_exp,
                         retirement_lifestyle,
                         reverse_mort,
                         house_value,
                         desired_risk,
                         filing_status,
                         total_income,
                         other_income,
                         taxable_income,
                         total_payments,
                         income_growth,
                         employment_status,
                         ss_fra_todays,
                         ss_fra_retirement,
                         paid_days,
                         contrib_rate_employer_401k,
                         contrib_rate_employee_401k,
                         initial_401k_balance,
                         inflation_level,
                         zip_code):
        
        # Null checks
        if not dob:
            raise Exception('dob not provided')

        if not desired_retirement_age:
            raise Exception('desired_retirement_age not provided')

        if not life_exp:
            pdb.set_trace()
            raise Exception('life_exp no provided')

        if not retirement_lifestyle:
            raise Exception('retirement_lifestyle not provided')

        if not desired_risk:
            raise Exception('desired_risk not provided')

        if not inflation_level:
            raise Exception('inflation_level not provided')

        if not zip_code:
            raise Exception('state not provided')

        # other checks
        if desired_retirement_age < 0:
            raise Exception('desired_retirement_age less than 0')

        if life_exp < 0:
            raise Exception('life_exp less than 0')

        if life_exp < desired_retirement_age:
            raise Exception('life_exp less than desired_retirement_age')

        if retirement_lifestyle != 1 and retirement_lifestyle != 2 and retirement_lifestyle != 3 and retirement_lifestyle != 4:
            raise Exception('unhandled value of retirement_lifestyle')

        if desired_risk < 0 or desired_risk > 1:
            raise Exception('desired_risk outside 0 <= desired_risk <= 1')

        if house_value < 0:
            raise Exception('house_value less than 0')

        if ss_fra_todays < 0:
            raise Exception('ss_fra_todays less than 0')

        if ss_fra_retirement < 0:
            raise Exception('ss_underfra_todays less than 0')

        if total_income < 0:
            raise Exception('total_income less than 0')

        if other_income < 0:
            raise Exception('other_income less than 0')

        if taxable_income < 0:
            raise Exception('taxable_income less than 0')

        if total_payments < 0:
            raise Exception('total_payments less than 0')

        if paid_days < 0:
            raise Exception('paid_days less than 0')

        if paid_days > 30:
            raise Exception('paid_days greater than 30 per month')

        if initial_401k_balance < 0:
            raise Exception('initial_401k_balance less than 0')

        if contrib_rate_employer_401k < 0:
            raise Exception('contrib_rate_employer_401k less than 0')

        if contrib_rate_employer_401k > 1:
            raise Exception('contrib_rate_employer_401k greater than 1 (i.e. > 100%)')

        if contrib_rate_employee_401k < 0:
            raise Exception('contrib_rate_employee_401k less than 0')

        if contrib_rate_employee_401k > 1:
            raise Exception('contrib_rate_employee_401k greater than 1 (i.e. > 100%)')

        if type(zip_code) != int:
            raise Exception("zip_code must be integer")
        '''
        if zip_code < 10000 or zip_code > 99999:
            raise Exception("zip_code not of correct form")
        ''' 


    def validate_age(self):
        if self.age >= self.desired_retirement_age:
            raise Exception("age greater than or equal to desired retirement age")

        if self.age <= 0:
            raise Exception("age less than or equal to 0")


    def validate_life_exp_and_des_retire_age(self):
        if self.life_exp == self.desired_retirement_age:
            self.life_exp = self.life_exp + 1


    def show_inputs(self,
                     dob,
                     desired_retirement_age,
                     life_exp,
                     retirement_lifestyle,
                     reverse_mort,
                     house_value,
                     desired_risk,
                     filing_status,
                     total_income,
                     other_income,
                     taxable_income,
                     total_payments,
                     income_growth,
                     employment_status,
                     ss_fra_todays,
                     ss_fra_retirement,
                     paid_days,
                     contrib_rate_employer_401k,
                     contrib_rate_employee_401k,
                     initial_401k_balance,
                     inflation_level,
                     zip_code):
        print("-----------------------------Retirement model INPUTS -------------------")
        print('dob:                         ' + str(dob))
        print('desired_retirement_age:       ' + str(desired_retirement_age))
        print('life_exp:                    ' + str(life_exp))
        print('retirement_lifestyle:        ' + str(retirement_lifestyle))
        print('reverse_mort:                ' + str(reverse_mort))
        print('house_value:                 ' + str(house_value))
        print('desired_risk:                ' + str(desired_risk))
        print('filing_status:               ' + str(filing_status))
        print('total_income:                ' + str(total_income))
        print('other_income:                ' + str(other_income))
        print('taxable_income:              ' + str(taxable_income))
        print('total_payments:              ' + str(total_payments))
        print('income_growth:               ' + str(income_growth))
        print('employment_status:           ' + str(employment_status))
        print('ss_fra_todays:               ' + str(ss_fra_todays))
        print('ss_fra_retirement:           ' + str(ss_fra_retirement))
        print('paid_days:                   ' + str(paid_days))
        print('contrib_rate_employer_401k:  ' + str(contrib_rate_employer_401k))
        print('contrib_rate_employee_401k:  ' + str(contrib_rate_employee_401k))
        print('initial_401k_balance:        ' + str(initial_401k_balance))
        print('zip_code:                    ' + str(zip_code))
        print("[Set self.debug=False to hide these]")
        

    def show_outputs(self):
        print("--------------------------------------Retirement model OUTPUTS -------------------")
        print("--------------------------------------Taxable_Accounts ---------------------------")
        print(self.maindf['Taxable_Accounts'])
        print("--------------------------------------Actual_Inc ---------------------------")
        print(self.maindf['Actual_Inc'])
        print("--------------------------------------Desired_Inc ---------------------------")
        print(self.maindf['Desired_Inc'])
        print("[Set self.debug=False to hide these]")
        
        
