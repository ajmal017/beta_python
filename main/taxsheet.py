import pdb
import pandas as pd
import numpy as np
import inflation
import testtaxsheet as tst_tx

from dateutil.relativedelta import relativedelta



TOTALROWS = 12*50



class TaxUser(object):

    '''

    Contains a list of inputs and functions for Andrew's Excel tax sheet (Retirement Modelling v3.xlsx).

    '''



    def __init__(self,name,ssn,dob,desired_retirement_age,life_exp,retirement_lifestyle,reverse_mort,house_value,filing_status,retire_earn_at_fra,retire_earn_under_fra,total_income,adj_gross,federal_taxable_income,
                 federal_regular_tax,state_tax_after_credits,state_effective_rate_to_agi, after_tax_income,fica, other_income, ss_fra_retirement, paid_days, ira_rmo_factor, initial_401k_balance, inflation_level,
                 projected_income_growth=0.01, risk_profile_over_cpi=0.01):

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
        self.state_tax_after_credits = state_tax_after_credits
        self.state_effective_rate_to_agi = state_effective_rate_to_agi
        self.after_tax_income = after_tax_income
        self.fica = fica
        self.ss_fra_retirement = ss_fra_retirement
        self.paid_days = paid_days
        self.ira_rmo_factor = ira_rmo_factor
        self.initial_401k_balance = initial_401k_balance
        self.projected_income_growth = projected_income_growth
        self.other_income = other_income


        '''
        age
        '''
        self.age = ((pd.Timestamp('today')-dob).days)/365.

        '''
        retirememt period
        '''
        self.retirement_start = round((self.desired_retirement_age - self.age) * 12)
       
        '''
        data frame indices
        '''
        self.dateind = [pd.Timestamp('today').date() + relativedelta(months=+i) for i in range(TOTALROWS)]
        self.dateind_pre = [pd.Timestamp('today').date() + relativedelta(months=+i) for i in range(self.retirement_start)]
        self.dateind_post = [self.dateind_pre[len(self.dateind_pre)-1] + relativedelta(months=1) + relativedelta(months=+i) for i in range(TOTALROWS - self.retirement_start)]

        '''
        data frame
        '''
        self.maindf = pd.DataFrame(index=self.dateind)

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
        inflation
        '''
        self.inflation_level = inflation_level
        self.annual_inflation = [self.inflation_level[11 + (i * 12)] for i in range(self.years_to_project)]


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
        nominal_pre = [temp_df_column[self.retirement_start] for i in range(self.retirement_start)]
        real_post = [temp_df_column[self.retirement_start + i] for i in range(TOTALROWS - self.retirement_start)]
        result = self.maindf['Deflator'] * self.set_full_series(nominal_pre, real_post)
        return result
    

    def get_full_post_retirement_and_pre_set_zero(self, temp_df_column):
        '''
        returns data frame column having 'real' (c.f. 'nominal') values, where post retirement is calculated
        from other columns, and pre-retirement is set to zero
        '''
        nominal_pre = [0. for i in range(self.retirement_start)]
        real_post = [temp_df_column[self.retirement_start + i] for i in range(TOTALROWS - self.retirement_start)]
        result = self.set_full_series(nominal_pre, real_post)
        return result
    

    def get_full_pre_retirement_and_post_set_zero(self, temp_df_column):
        '''
        returns data frame column having 'real' (c.f. 'nominal') values, where pre retirement is calculated
        from other columns, and post-retirement is set to zero
        '''
        nominal_pre = [temp_df_column[self.retirement_start] for i in range(self.retirement_start)]
        real_post = [0. for i in range(TOTALROWS - self.retirement_start)]
        result = self.set_full_series(nominal_pre, real_post)
        return result
    

    def create_maindf(self):
        '''
        create the main data frame
        '''
        
        self.maindf['Person_Age'] = [self.age + (1./12.)*i for i in range(TOTALROWS)]


        # MONTHLY GROWTH RATE ASSUMPTIONS

        self.port_return = self.risk_profile_over_cpi/12.

        self.pre_proj_inc_growth_monthly = [self.projected_income_growth/12. for i in range(self.retirement_start)]
        self.post_proj_inc_growth_monthly = [0. for i in range(TOTALROWS - self.retirement_start)]
        self.maindf['Proj_Inc_Growth_Monthly'] = self.set_full_series(self.pre_proj_inc_growth_monthly, self.post_proj_inc_growth_monthly)

        self.maindf['Proj_Inflation_Rate'] = [self.inflation_level[i]/12. for i in range(TOTALROWS)]
        self.pre_proj_inflation_rate = [self.inflation_level[i]/12. for i in range(self.retirement_start)] 
        self.post_proj_inflation_rate = [self.inflation_level[self.retirement_start + i]/12. for i in range(TOTALROWS - self.retirement_start)] 

        self.maindf['Portfolio_Return'] = self.maindf['Proj_Inflation_Rate'] + self.risk_profile_over_cpi/12.
        self.pre_portfolio_return = [self.inflation_level[i]/12. + self.risk_profile_over_cpi/12. for i in range(self.retirement_start)]
        self.post_portfolio_return = [self.inflation_level[self.retirement_start + i]/12. + self.risk_profile_over_cpi/12. for i in range(TOTALROWS - self.retirement_start)]

        self.maindf['Retire_Work_Inc_Daily_Rate'] = [116*(1+self.projected_income_growth/12.)**i for i in range(TOTALROWS)]


        '''
        get the 'flators'
        '''
        
        self.pre_deflator = [0. for i in range(self.retirement_start)]  
        self.pre_deflator[self.retirement_start - 1] = 1. * (1 - self.pre_proj_inflation_rate[self.retirement_start -1])                                                                                            
        for i in range (1, self.retirement_start - 1):
            self.pre_deflator[self.retirement_start -1 - i] = self.pre_deflator[self.retirement_start -1 - i + 1] * (1 - self.pre_proj_inflation_rate[self.retirement_start -1 - i])                                                                                         

        self.post_inflator = [0. for i in range(TOTALROWS - self.retirement_start)]
        self.post_inflator[0] = 1.                                                                                           
        for i in range (1, TOTALROWS - self.retirement_start):
            self.post_inflator[i] = self.post_inflator[i - 1] * (1 - self.post_proj_inflation_rate[i])

        self.maindf['Deflator'] = self.set_full_series(self.pre_deflator, [1. for i in range(TOTALROWS - self.retirement_start)])   # for pre-retirement
        self.maindf['Inflator'] = self.set_full_series([1. for i in range(self.retirement_start)], self.post_inflator)              # for post-retirement
        self.maindf['Flator'] = self.maindf['Deflator'] * self.maindf['Inflator']                                                   # deserves a pat (or 'flat'?) on the back


        # INCOME RELATED - WORKING PERIOD

        self.pre_total_income = self.total_income/12. * (1+pd.Series(self.pre_proj_inc_growth_monthly, index=self.dateind_pre).cumprod())
        self.post_total_income  = [0. for i in range(TOTALROWS - self.retirement_start)]
        self.maindf['Total_Income'] = self.set_full_series(self.pre_total_income, self.post_total_income)
        
        self.pre_other_income = self.other_income/12. * (1+pd.Series(self.pre_proj_inflation_rate, index=self.dateind_pre).cumprod())
        self.post_other_income  = [0. for i in range(TOTALROWS - self.retirement_start)]
        self.maindf['Other_Income'] = self.set_full_series(self.pre_other_income, self.post_other_income)                                

        self.maindf['Adj_Gross_Income'] = self.maindf['Total_Income'] + self.maindf['Other_Income']
        
        self.pre_fed_regular_tax = self.federal_regular_tax/12. * (1+pd.Series(self.pre_proj_inflation_rate, index=self.dateind_pre).cumprod())
        self.post_fed_regular_tax  = [0. for i in range(TOTALROWS - self.retirement_start)]
        self.maindf['Fed_Regular_Tax'] = self.set_full_series(self.pre_fed_regular_tax, self.post_fed_regular_tax)
        
        self.maindf['Fed_Taxable_Income'] = self.maindf['Adj_Gross_Income'] - self.maindf['Fed_Regular_Tax']
  
        self.pre_state_tax_after_credits = self.state_tax_after_credits/12. * (1+pd.Series(self.pre_proj_inflation_rate, index=self.dateind_pre).cumprod())      
        self.post_state_tax_after_credits = [0. for i in range(TOTALROWS - self.retirement_start)] 
        self.maindf['State_Tax_After_Credits'] = self.set_full_series(self.pre_state_tax_after_credits, self.post_state_tax_after_credits)
            
        self.maindf['After_Tax_Income'] = self.maindf['Adj_Gross_Income'] - self.maindf['Fed_Regular_Tax'] - self.maindf['State_Tax_After_Credits']
        
        self.pre_fica = self.fica/12. * (1+pd.Series(self.pre_proj_inflation_rate, index=self.dateind_pre).cumprod())        
        self.post_fica = [0. for i in range(TOTALROWS - self.retirement_start)] 
        self.maindf['FICA'] = self.set_full_series(self.pre_fica, self.post_fica)

        self.maindf['Home_Value'] = self.house_value * (1+self.maindf['Proj_Inflation_Rate']).cumprod()


        # INCOME RELATED - EMPLOYEE CONTRIBUTIONS

        self.contrib_rate_employee_pension = 0.0
        self.maindf['Pension_Employee'] = self.maindf['Total_Income'] * self.contrib_rate_employee_pension

        self.contrib_rate_employee_401k = 0.055 
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

        self.contrib_rate_employer_401k = 0.02
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


        # ACCOUNT CAPITAL GROWTH

        self.starting_balance_pension = 0.0
        self.maindf['Pension_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_pension

        self.starting_balance_profit_sharing = 0.0
        self.maindf['Profit_Sharing_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_profit_sharing

        self.starting_balance_money_purchase = 0.0
        self.maindf['Money_Purchase_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_money_purchase

        self.starting_balance_esop = 0.0
        self.maindf['Esop_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_esop

        self.starting_balance_roth_401k = 0.0
        self.maindf['Roth_401k_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_roth_401k

        self.starting_balance_individual_401k = 0.0
        self.maindf['Individual_401k_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_individual_401k

        self.starting_balance_ind_roth_401k = 0.0
        self.maindf['Ind_Roth_401k_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_ind_roth_401k

        self.starting_balance_401a_Keogh = 0.0
        self.maindf['401a_Keogh_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_401a_Keogh

        self.starting_balance_qual_np = 0.0
        self.maindf['Qual_Np_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_qual_np

        self.starting_balance_qual_priv_457 = 0.0
        self.maindf['Qual_Priv_457_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_qual_priv_457

        self.starting_balance_457 = 0.0
        self.maindf['457_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_457

        self.starting_balance_qual_np_roth = 0.0
        self.maindf['Qual_Np_Roth_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_qual_np_roth

        self.starting_balance_ira = 10000
        self.maindf['Ira_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_ira

        self.starting_balance_roth_ira = 10000
        self.maindf['Roth_Ira_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_roth_ira

        self.starting_balance_simple_ira = 0.0
        self.maindf['Simple_Ira_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_simple_ira

        self.starting_balance_sar_sep_ira = 0.0
        self.maindf['Sar_Sep_Ira_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_sar_sep_ira

        self.starting_balance_sep_ira = 0.0
        self.maindf['Sep_Ira_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_sep_ira

        self.starting_balance_qual_annuity = 0.0
        self.maindf['Qual_Annuity_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_qual_annuity

        self.starting_balance_tax_def_annuity = 0.0
        self.maindf['Tax_Def_Annuity_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_tax_def_annuity

        
        # ACCOUNT BALANCE

        self.maindf['Pension_Balance'] = self.maindf['Pension_Employee'] \
                                         + self.maindf['Pension_Employer'] \
                                         + self.maindf['Pension_Capital_Growth'] \
                                         + self.starting_balance_pension

        self.maindf['Profit_Sharing_Balance'] = self.maindf['Profit_Sharing_Employee'] \
                                                + self.maindf['Profit_Sharing_Employer'] \
                                                + self.maindf['Profit_Sharing_Capital_Growth'] \
                                                + self.starting_balance_profit_sharing

        self.maindf['Money_Purchase_Balance'] = self.maindf['Money_Purchase_Employee'] \
                                                + self.maindf['Money_Purchase_Employer'] \
                                                + self.maindf['Money_Purchase_Capital_Growth'] \
                                                + self.starting_balance_money_purchase

        self.maindf['Esop_Balance'] = self.maindf['Esop_Employee'] \
                                      + self.maindf['Esop_Employer'] \
                                      + self.maindf['Esop_Capital_Growth'] \
                                      + self.starting_balance_esop

        self.maindf['Roth_401k_Balance'] = self.maindf['Roth_401k_Employee'] \
                                           + self.maindf['Roth_401k_Employer'] \
                                           + self.maindf['Roth_401k_Capital_Growth'] \
                                           + self.starting_balance_roth_401k

        self.maindf['Individual_401k_Balance'] = self.maindf['Individual_401k_Employee'] \
                                                 + self.maindf['Individual_401k_Employer'] \
                                                 + self.maindf['Individual_401k_Capital_Growth'] \
                                                 + self.starting_balance_individual_401k

        self.maindf['Ind_Roth_401k_Balance'] = self.maindf['Ind_Roth_401k_Employee'] \
                                               + self.maindf['Ind_Roth_401k_Employer'] \
                                               + self.maindf['Ind_Roth_401k_Capital_Growth'] \
                                               + self.starting_balance_ind_roth_401k

        self.maindf['401a_Keogh_Balance'] = self.maindf['401a_Keogh_Employee'] \
                                            + self.maindf['401a_Keogh_Employer'] \
                                            + self.maindf['401a_Keogh_Capital_Growth'] \
                                            + self.starting_balance_401a_Keogh

        self.maindf['Qual_Np_Balance'] = self.maindf['Qual_Np_Employee'] \
                                         + self.maindf['Qual_Np_Employer'] \
                                         + self.maindf['Qual_Np_Capital_Growth'] \
                                         + self.starting_balance_qual_np

        self.maindf['Qual_Priv_457_Balance'] = self.maindf['Qual_Priv_457_Employee'] \
                                               + self.maindf['Qual_Priv_457_Employer'] \
                                               + self.maindf['Qual_Priv_457_Capital_Growth'] \
                                               + self.starting_balance_qual_priv_457

        self.maindf['457_Balance'] = self.maindf['457_Employee'] \
                                     + self.maindf['457_Employer'] \
                                     + self.maindf['457_Capital_Growth'] \
                                     + self.starting_balance_457

        self.maindf['Qual_Np_Roth_Balance'] = self.maindf['Qual_Np_Roth_Employee'] \
                                              + self.maindf['Qual_Np_Roth_Employer'] \
                                              + self.maindf['Qual_Np_Roth_Capital_Growth'] \
                                              + self.starting_balance_qual_np_roth

        self.maindf['Ira_Balance'] = self.maindf['Ira_Employee'] \
                                     + self.maindf['Ira_Employer'] \
                                     + self.maindf['Ira_Capital_Growth'] \
                                     + self.starting_balance_ira

        self.maindf['Roth_Ira_Balance'] = self.maindf['Roth_Ira_Employee'] \
                                          + self.maindf['Roth_Ira_Employer'] \
                                          + self.maindf['Roth_Ira_Capital_Growth'] \
                                          + self.starting_balance_roth_ira

        self.maindf['Simple_Ira_Balance'] = self.maindf['Simple_Ira_Employee'] \
                                            + self.maindf['Simple_Ira_Employer'] \
                                            + self.maindf['Simple_Ira_Capital_Growth'] \
                                            + self.starting_balance_simple_ira

        self.maindf['Sar_Sep_Ira_Balance'] = self.maindf['Sar_Sep_Ira_Employee'] \
                                             + self.maindf['Sar_Sep_Ira_Employer'] \
                                             + self.maindf['Sar_Sep_Ira_Capital_Growth'] \
                                             + self.starting_balance_sar_sep_ira

        self.maindf['Sep_Ira_Balance'] = self.maindf['Sep_Ira_Employee'] \
                                         + self.maindf['Sep_Ira_Employer'] \
                                         + self.maindf['Sep_Ira_Capital_Growth'] \
                                         + self.starting_balance_sep_ira

        self.maindf['Qual_Annuity_Balance'] = self.maindf['Qual_Annuity_Employee'] \
                                              + self.maindf['Qual_Annuity_Employer'] \
                                              + self.maindf['Qual_Annuity_Capital_Growth'] \
                                              + self.starting_balance_qual_annuity

        self.maindf['Tax_Def_Annuity_Balance'] = self.maindf['Tax_Def_Annuity_Employee'] \
                                                 + self.maindf['Tax_Def_Annuity_Employer'] \
                                                 + self.maindf['Tax_Def_Annuity_Capital_Growth'] \
                                                 + self.starting_balance_tax_def_annuity

        self.maindf['Nontaxable_Accounts'] = np.where(self.maindf['Roth_401k_Balance'] + self.maindf['Ind_Roth_401k_Balance'] + self.maindf['Roth_Ira_Balance'] > 0,
                                                      self.maindf['Roth_401k_Balance'] + self.maindf['Ind_Roth_401k_Balance'] + self.maindf['Roth_Ira_Balance'],
                                                      0)

        # 401K
        
        '''
        for now can't think of a more 'pythonic' way to do this next bit ... may need re-write ...
        ''' 
        self.starting_balance_401k = 50000
        self.pre_401k_balance = [self.initial_401k_balance for i in range(self.retirement_start)]
        self.pre_401k_capital_growth = [0. for i in range(self.retirement_start)]
        
        for i in range(1, self.retirement_start):
            self.pre_401k_capital_growth[i] = self.pre_portfolio_return[i] * self.pre_401k_balance[i - 1]
            self.pre_401k_balance[i] = (self.contrib_rate_employee_401k + self.contrib_rate_employer_401k) * self.pre_total_income[i] + self.pre_401k_capital_growth[i] + self.pre_401k_balance[i - 1]

        self.post_401k_balance = [self.pre_401k_balance[self.retirement_start - 1] for i in range(TOTALROWS - self.retirement_start)]
        self.post_401k_capital_growth = [0. for i in range(TOTALROWS - self.retirement_start)]
        self.post_total_tax_distrib = [0. for i in range(TOTALROWS - self.retirement_start)]
                
        for i in range(1, TOTALROWS - self.retirement_start): # **** NEED to add in 'total of taxable distribution'
            self.post_401k_capital_growth[i] = self.post_portfolio_return[i] * self.post_401k_balance[i - 1]

            if (self.contrib_rate_employee_401k + self.contrib_rate_employer_401k) * self.post_total_income[i] + self.post_401k_capital_growth[i] + self.post_401k_balance[i - 1] - self.post_total_tax_distrib[i - 1] > 0:
                self.post_401k_balance[i] = (self.contrib_rate_employee_401k + self.contrib_rate_employer_401k) * self.post_total_income[i] + self.post_401k_capital_growth[i] + self.post_401k_balance[i - 1] - self.post_total_tax_distrib[i - 1]
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
                                          + self.maindf['Nontaxable_Accounts']

                                                
        # RETIREMENT PERIOD INCOME

        self.maindf['Des_Ret_Inc_Pre_Tax'] = self.retirement_lifestyle * self.maindf['Adj_Gross_Income']

        if self.maindf['Person_Age'][self.retirement_start -1] < 66:
            self.tax_exempt_amount = self.retire_earn_under_fra
        else:
            self.tax_exempt_amount = self.retire_earn_at_fra
        self.maindf['Soc_Sec_Ret_Ear_Tax_Exempt'] = self.tax_exempt_amount  * (1+self.maindf['Proj_Inflation_Rate']).cumprod()

        '''
        use the 'flators'
        '''
        self.maindf['Nominal_Soc_Sec_Benefit'] = [self.ss_fra_retirement for i in range(TOTALROWS)]
        self.maindf['Soc_Sec_Benefit'] = self.maindf['Flator'] * self.maindf['Nominal_Soc_Sec_Benefit']

        self.maindf['Nominal_Ret_Working_Inc'] = np.where(self.maindf['Person_Age'] > 80, self.maindf['Retire_Work_Inc_Daily_Rate'] * 4 * self.paid_days, 0)
        self.maindf['Ret_Working_Inc'] = self.maindf['Deflator'] * self.maindf['Nominal_Ret_Working_Inc']
        
        self.maindf['Nominal_Pension_Payments'] = [0. for i in range(TOTALROWS)]
        self.maindf['Pension_Payments'] = self.maindf['Deflator'] * self.maindf['Nominal_Pension_Payments']

        self.maindf['Nominal_Annuity_Payments'] = [0. for i in range(TOTALROWS)]
        self.maindf['Annuity_Payments'] = self.maindf['Deflator'] * self.maindf['Nominal_Annuity_Payments']
        
        self.maindf['Nominal_Reverse_Mortgage'] = np.where(self.age > 0,
                                                   np.where(self.maindf['Total_Income'] == 0
                                                            , self.maindf['Home_Value'][self.retirement_start - 1] * (0.9/(self.retirement_years * 12.))
                                                            , 0)
                                                   , 0) 
        self.maindf['Reverse_Mortgage'] = self.maindf['Deflator'] * self.maindf['Nominal_Reverse_Mortgage']

        self.maindf['Certain_Ret_Inc'] = self.get_full_post_retirement_and_pre_deflated(self.maindf['Soc_Sec_Benefit']
                                                                                        + self.maindf['Ret_Working_Inc']
                                                                                        + self.maindf['Pension_Payments']
                                                                                        + self.maindf['Annuity_Payments']
                                                                                        + self.maindf['Reverse_Mortgage'])

        
        self.maindf['Ret_Certain_Inc_Gap'] = self.get_full_post_retirement_and_pre_deflated(self.maindf['Des_Ret_Inc_Pre_Tax']
                                                                                            - self.maindf['Certain_Ret_Inc'])

        self.maindf['Reqd_Min_Dist'] = np.where(self.maindf['Person_Age'] > 70.5, self.maindf['Taxable_Accounts'] /(self.ira_rmo_factor * 12.), 0)

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

        self.maindf['Taxable_Inc'] = self.maindf['Soc_Sec_Benefit'] + self.maindf['Ret_Working_Inc'] + self.maindf['Pension_Payments'] + self.maindf['Annuity_Payments'] + self.maindf['Tot_Taxable_Dist']

        self.maindf['Adj_Gross_Inc'] = self.maindf['Tot_Inc']

        self.maindf['Fed_Taxable_Inc'] = self.maindf['Taxable_Inc']

        self.maindf['Fed_Regular_Tax'] = [0. for i in range(TOTALROWS)] # *** NEED TO COMPLETE THIS from 'Projected Federal Tax Calc' tab

        self.maindf['State_Tax_After_Credits'] = self.maindf['Adj_Gross_Inc'] * self.state_effective_rate_to_agi

        self.maindf['After_Tax_Income'] = self.maindf['Adj_Gross_Inc'] - self.maindf['Fed_Regular_Tax'] - self.maindf['State_Tax_After_Credits']
        
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

        self.annual_taxable_income_post = [self.maindf['Taxable_Inc'][self.retirement_start + (i * 12)]
                                           + self.maindf['Taxable_Inc'][self.retirement_start + (i * 12) + 1]
                                           + self.maindf['Taxable_Inc'][self.retirement_start + (i * 12) + 2]
                                           + self.maindf['Taxable_Inc'][self.retirement_start + (i * 12) + 3]
                                           + self.maindf['Taxable_Inc'][self.retirement_start + (i * 12) + 4]
                                           + self.maindf['Taxable_Inc'][self.retirement_start + (i * 12) + 5]
                                           + self.maindf['Taxable_Inc'][self.retirement_start + (i * 12) + 6]
                                           + self.maindf['Taxable_Inc'][self.retirement_start + (i * 12) + 7]
                                           + self.maindf['Taxable_Inc'][self.retirement_start + (i * 12) + 8]
                                           + self.maindf['Taxable_Inc'][self.retirement_start + (i * 12) + 9]
                                           + self.maindf['Taxable_Inc'][self.retirement_start + (i * 12) + 10]
                                           + self.maindf['Taxable_Inc'][self.retirement_start + (i * 12) + 11] for i in range(self.retirement_years)]

        self.annual_taxable_income = self.set_full_series_with_indices(self.annual_taxable_income_pre,
                                                                       self.annual_taxable_income_post,
                                                                       self.years_pre,
                                                                       self.years_post)

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
                      tst_tx.state_tax_after_credits,
                      tst_tx.state_effective_rate_to_agi,
                      tst_tx.after_tax_income,
                      tst_tx.fica,
                      tst_tx.other_income,
                      tst_tx.ss_fra_retirement,
                      tst_tx.paid_days,
                      tst_tx.ira_rmo_factor,
                      tst_tx.initial_401k_balance,
                      tst_tx.inflation_level)
    
    tst_cls.create_maindf()
    pdb.set_trace()

        
