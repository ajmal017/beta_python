import pdb
import logging
import math
import pandas as pd
import numpy as np
from main import inflation
from main import projectedfedtax as fedtax
from main import statetax as state
from main import fica
from main import testtaxsheet as tst_tx

#from client.models import Client
#from retirementsmartz.models import RetirementPlan
#from main.abstract import PersonalData


from dateutil.relativedelta import relativedelta

logger = logging.getLogger('taxsheet')

class TaxUser(object):

    '''
    Contains a list of inputs and functions for Andrew's Excel tax sheet (Retirement Modelling v4.xlsx).
    '''

    def __init__(self,name,
                 ssn,
                 dob,
                 desired_retirement_age,
                 life_exp,
                 retirement_lifestyle,
                 reverse_mort,
                 house_value,
                 filing_status,
                 retire_earn_at_fra,
                 retire_earn_under_fra,
                 total_income,
                 adj_gross,
                 federal_taxable_income,
                 federal_regular_tax,
                 after_tax_income,
                 other_income,
                 ss_fra_retirement,
                 paid_days,
                 ira_rmd_factor,
                 initial_401k_balance,
                 inflation_level,
                 risk_profile_over_cpi,
                 projected_income_growth,
                 contrib_rate_employee_401k,
                 contrib_rate_employer_401k,
                 state,
                 employment_status):

        '''
        set variables
        '''
        self.name = name
        self.ssn = ssn
        self.dob = dob
        self.desired_retirement_age = desired_retirement_age
        self.life_exp = life_exp
        self.retirement_lifestyle = retirement_lifestyle
        self.reverse_mort = reverse_mort
        self.house_value = house_value
        self.filing_status = filing_status
        self.risk_profile_over_cpi = risk_profile_over_cpi
        self.retire_earn_at_fra = retire_earn_at_fra
        self.retire_earn_under_fra = retire_earn_under_fra
        self.total_income = total_income
        self.adj_gross = adj_gross
        self.federal_taxable_income = federal_taxable_income
        self.federal_regular_tax = federal_regular_tax
        self.after_tax_income = after_tax_income
        self.fica = fica
        self.ss_fra_retirement = ss_fra_retirement
        self.paid_days = paid_days
        self.ira_rmd_factor = ira_rmd_factor
        self.initial_401k_balance = initial_401k_balance
        self.projected_income_growth = projected_income_growth
        self.other_income = other_income
        self.contrib_rate_employee_401k = contrib_rate_employee_401k
        self.contrib_rate_employer_401k = contrib_rate_employer_401k
        self.state = state
        self.employment_status = employment_status


        '''
        age
        '''
        self.age = ((pd.Timestamp('today')-dob).days)/365.

        '''
        retirememt period
        '''
        self.pre_retirement_end = math.floor((self.desired_retirement_age - self.age) * 12)  # i.e. last period in which TaxUser is younger than desired retirement age
                                                                                            # NB this period has index self.pre_retirement_end - 1
                                                                                            
        self.retirement_start = self.pre_retirement_end + 1                                 # i.e. first period in which TaxUser is older than desired retirement age
                                                                                            # NB this period has index self.retirement_start - 1

        '''
        years
        '''
        self.start_year = pd.Timestamp('today').year
        self.years_to_project = round(self.life_exp - self.age)
        self.retirement_years = round(self.life_exp - self.desired_retirement_age)
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
        self.inflation_level = inflation_level
        self.annual_inflation = [self.inflation_level[11 + (i * 12)] for i in range(self.years_to_project)]

        '''
        data frame indices
        '''
        self.dateind = [pd.Timestamp('today').date() + relativedelta(months=1) + relativedelta(months=+i) for i in range(self.total_rows)]
        self.dateind_pre = [pd.Timestamp('today').date() + relativedelta(months=1) + relativedelta(months=+i) for i in range(self.pre_retirement_end)]
        self.dateind_post = [self.dateind_pre[len(self.dateind_pre)-1]
                             + relativedelta(months=1)
                             + relativedelta(months=+i) for i in range(self.total_rows - self.pre_retirement_end)]
        
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
    

    def create_maindf(self):
        '''
        create the main data frame
        '''
        
        self.maindf['Person_Age'] = [self.age + (1./12.)*(i+1) for i in range(self.total_rows)]


        # MONTHLY GROWTH RATE ASSUMPTIONS

        self.port_return = self.risk_profile_over_cpi/12.

        self.pre_proj_inc_growth_monthly = [self.projected_income_growth/12. for i in range(self.pre_retirement_end)]
        self.post_proj_inc_growth_monthly = [0. for i in range(self.total_rows - self.pre_retirement_end)]
        self.maindf['Proj_Inc_Growth_Monthly'] = self.set_full_series(self.pre_proj_inc_growth_monthly, self.post_proj_inc_growth_monthly)

        self.maindf['Proj_Inflation_Rate'] = [self.inflation_level[i]/12. for i in range(self.total_rows)]
        self.pre_proj_inflation_rate = [self.inflation_level[i]/12. for i in range(self.pre_retirement_end)] 
        self.post_proj_inflation_rate = [self.inflation_level[self.retirement_start + i]/12. for i in range(self.total_rows - self.pre_retirement_end)] 

        self.maindf['Portfolio_Return'] = self.maindf['Proj_Inflation_Rate'] + self.risk_profile_over_cpi/12.
        self.pre_portfolio_return = [self.inflation_level[i]/12. + self.risk_profile_over_cpi/12. for i in range(self.pre_retirement_end)]
        self.post_portfolio_return = [self.inflation_level[self.retirement_start
                                                           + i]/12. + self.risk_profile_over_cpi/12.
                                      for i in range(self.total_rows - self.pre_retirement_end)]

        self.maindf['Retire_Work_Inc_Daily_Rate'] = [116*(1+self.projected_income_growth/12.)**i for i in range(self.total_rows)]

        '''
        get the 'flators'
        '''
        
        self.pre_deflator = [0. for i in range(self.pre_retirement_end)]
        self.pre_deflator[self.pre_retirement_end - 1] = 1. * (1 - self.pre_proj_inflation_rate[self.pre_retirement_end - 1])                                                                                          
        for i in range (1, self.pre_retirement_end):
            self.pre_deflator[self.pre_retirement_end - 1 - i] = self.pre_deflator[self.pre_retirement_end - 1 - i + 1] * (1 - self.pre_proj_inflation_rate[self.pre_retirement_end - 1 - i])                                                                                         

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

        self.pre_fed_regular_tax = self.federal_regular_tax/12. * self.pre_df['Inf_Inflator_Pre']
        self.post_fed_regular_tax  = [0. for i in range(self.total_rows - self.pre_retirement_end)]
        self.maindf['Fed_Regular_Tax'] = self.set_full_series(self.pre_fed_regular_tax, self.post_fed_regular_tax)
        
        self.maindf['Fed_Taxable_Income'] = self.maindf['Adj_Gross_Income'] - self.maindf['Fed_Regular_Tax']

        self.state_tax = state.StateTax(self.state, self.filing_status, self.total_income)
        self.state_tax_after_credits = self.state_tax.get_state_tax()
        self.state_effective_rate_to_agi = self.state_tax_after_credits/self.total_income

        self.pre_state_tax_after_credits = self.state_tax_after_credits/12. * self.pre_df['Inf_Inflator_Pre']      
        self.post_state_tax_after_credits = [0. for i in range(self.total_rows - self.pre_retirement_end)] 
        self.maindf['State_Tax_After_Credits'] = self.set_full_series(self.pre_state_tax_after_credits, self.post_state_tax_after_credits)
            
        self.maindf['After_Tax_Income'] = self.maindf['Adj_Gross_Income'] - self.maindf['Fed_Regular_Tax'] - self.maindf['State_Tax_After_Credits']
        pdb.set_trace()
        fc = fica.Fica(self.employment_status,self.total_income)
        self.fica = fc.get_fica()
        pdb.set_trace()
        
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

        self.contrib_rate_employee_ira = 0.015
        self.maindf['Ira_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_ira

        self.contrib_rate_employee_roth_ira = 0.015
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

        self.starting_balance_ira = 10000
        self.capital_growth_pension, self.balance_pension = self.get_capital_growth_and_balance_series(self.total_rows, 'Ira', self.starting_balance_ira )
        self.maindf['Ira_Capital_Growth'] = self.capital_growth_pension
        self.maindf['Ira_Balance'] = self.balance_pension

        self.starting_balance_roth_ira = 10000
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
        self.starting_balance_401k = 50000
        self.pre_401k_capital_growth, self.pre_401k_balance = self.get_capital_growth_and_balance_series(self.pre_retirement_end, '401k', self.starting_balance_401k )        

        self.post_401k_balance = [self.pre_401k_balance[self.pre_retirement_end - 1] for i in range(self.total_rows - self.pre_retirement_end)]
        self.post_401k_capital_growth = [0. for i in range(self.total_rows - self.pre_retirement_end)]
        self.post_total_tax_distrib = [0. for i in range(self.total_rows - self.pre_retirement_end)]
                
        for i in range(1, self.total_rows - self.pre_retirement_end): # **** NEED to add in 'total of taxable distribution'
            self.post_401k_capital_growth[i] = self.post_portfolio_return[i] * self.post_401k_balance[i - 1]

            if (self.contrib_rate_employee_401k + self.contrib_rate_employer_401k) * self.post_total_income[i] + self.post_401k_capital_growth[i] + self.post_401k_balance[i - 1] - self.post_total_tax_distrib[i - 1] > 0:
                self.post_401k_balance[i] = (self.contrib_rate_employee_401k + (self.contrib_rate_employer_401k) * self.post_total_income[i]) + self.post_401k_capital_growth[i] + self.post_401k_balance[i - 1] - self.post_total_tax_distrib[i - 1]
            else:
                self.post_401k_balance[i] = 0.

        self.maindf['401k_Capital_Growth'] = self.set_full_series(self.pre_401k_capital_growth, self.post_401k_capital_growth)
        self.maindf['401k_Balance'] = self.set_full_series(self.pre_401k_balance, self.post_401k_balance)
        '''
        glad to have got that out of the way ...
        '''

        # TAXABLE ACCOUNTS

        self.maindf['Taxable_Accounts'] = self.maindf['Pension_Balance'] \
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

                                            
        # RETIREMENT PERIOD INCOME

        self.pre_des_ret_inc_pre_tax = self.retirement_lifestyle * self.maindf['Adj_Gross_Income'][0:self.pre_retirement_end]
        self.post_des_ret_inc_pre_tax = [self.pre_des_ret_inc_pre_tax[len(self.pre_des_ret_inc_pre_tax) - 1] for i in range(self.total_rows - self.pre_retirement_end)] 
        self.maindf['Des_Ret_Inc_Pre_Tax_Post_Nominal'] = self.set_full_series(self.pre_des_ret_inc_pre_tax, self.post_des_ret_inc_pre_tax)
        self.maindf['Des_Ret_Inc_Pre_Tax'] = self.maindf['Des_Ret_Inc_Pre_Tax_Post_Nominal'] * self.maindf['Inflator']

        if self.maindf['Person_Age'][self.retirement_start -1] < 66:
            self.tax_exempt_amount = self.retire_earn_under_fra
        else:
            self.tax_exempt_amount = self.retire_earn_at_fra
        self.maindf['Soc_Sec_Ret_Ear_Tax_Exempt'] = self.tax_exempt_amount  * (1+self.maindf['Proj_Inflation_Rate']).cumprod()

        '''
        use the 'flators'
        '''
        self.maindf['Nominal_Soc_Sec_Benefit'] = [self.ss_fra_retirement for i in range(self.total_rows)]
        self.maindf['Soc_Sec_Benefit'] = self.maindf['Flator'] * self.maindf['Nominal_Soc_Sec_Benefit']

        self.maindf['Nominal_Ret_Working_Inc'] = np.where(self.maindf['Person_Age'] < 80, self.maindf['Retire_Work_Inc_Daily_Rate'] * 4 * self.paid_days, 0)
        self.maindf['Ret_Working_Inc'] = self.maindf['Deflator'] * self.maindf['Nominal_Ret_Working_Inc']
        
        self.maindf['Nominal_Pension_Payments'] = [0. for i in range(self.total_rows)]
        self.maindf['Pension_Payments'] = self.maindf['Deflator'] * self.maindf['Nominal_Pension_Payments']

        self.maindf['Nominal_Annuity_Payments'] = [0. for i in range(self.total_rows)]
        self.maindf['Annuity_Payments'] = self.maindf['Deflator'] * self.maindf['Nominal_Annuity_Payments']
        
        self.post_reverse_mortgage = np.where(self.age > 0,
                                                   np.where(self.maindf['Total_Income'] == 0
                                                            , self.maindf['Home_Value'][self.retirement_start - 1] * (0.9/(self.retirement_years * 12.))
                                                            , 0)
                                                   , 0)[self.pre_retirement_end:]
        self.pre_reverse_mortage = [self.post_reverse_mortgage[0] for i in range (self.pre_retirement_end)]
        self.maindf['Reverse_Mortgage_Nominal'] = self.set_full_series(self.pre_reverse_mortage, self.post_reverse_mortgage)
        self.maindf['Reverse_Mortgage'] = self.maindf['Deflator'] * self.maindf['Reverse_Mortgage_Nominal']
        
        self.maindf['Certain_Ret_Inc'] = self.get_full_post_retirement_and_pre_deflated(self.maindf['Soc_Sec_Benefit']
                                                                                        + self.maindf['Ret_Working_Inc']
                                                                                        + self.maindf['Pension_Payments']
                                                                                        + self.maindf['Annuity_Payments']
                                                                                        + self.maindf['Reverse_Mortgage'])

        
        self.maindf['Ret_Certain_Inc_Gap'] = self.get_full_post_retirement_and_pre_deflated(self.maindf['Des_Ret_Inc_Pre_Tax']
                                                                                            - self.maindf['Certain_Ret_Inc'])

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

        taxFed = fedtax.TaxFederal(self.years, self.annual_inflation, self.annual_taxable_income)
        taxFed.create_tax_engine()
        taxFed.create_tax_projected()

        self.annual_projected_tax = taxFed.tax_projected['Single']
        
        self.post_projected_tax = pd.Series()
        
        for i in range(len(self.years_post) - 1):
            self.post_projected_tax = self.post_projected_tax.append(pd.Series([self.annual_projected_tax.iloc[self.pre_retirement_years - 1 + 1 + i]/12.,
                                                                                self.annual_projected_tax.iloc[self.pre_retirement_years - 1 + 1 + i]/12.,
                                                                                self.annual_projected_tax.iloc[self.pre_retirement_years - 1 + 1 + i]/12.,
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
        

if __name__ == "__main__":

    tst_cls = TaxUser(tst_tx.name,
                      tst_tx.ssn,
                      tst_tx.dob,
                      tst_tx.desired_retirement_age,
                      tst_tx.life_exp,
                      tst_tx.retirement_lifestyle,
                      tst_tx.reverse_mort,
                      tst_tx.house_value,
                      tst_tx.filing_status,
                      tst_tx.retire_earn_at_fra,
                      tst_tx.retire_earn_under_fra,
                      tst_tx.total_income,
                      tst_tx.adj_gross,
                      tst_tx.federal_taxable_income,
                      tst_tx.federal_regular_tax,
                      tst_tx.after_tax_income,
                      tst_tx.other_income,
                      tst_tx.ss_fra_retirement,
                      tst_tx.paid_days,
                      tst_tx.ira_rmd_factor,
                      tst_tx.initial_401k_balance,
                      tst_tx.inflation_level,
                      tst_tx.risk_profile_over_cpi,
                      tst_tx.projected_income_growth,
                      tst_tx.contrib_rate_employee_401k,
                      tst_tx.contrib_rate_employer_401k,
                      tst_tx.state,
                      tst_tx.employment_status)
    
    tst_cls.create_maindf()

        
