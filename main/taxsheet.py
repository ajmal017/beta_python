import pdb
import pandas as pd
import inflation

from dateutil.relativedelta import relativedelta



TOTALROWS = 12*50



class TaxUser(object):

    '''

    Contains a list of inputs and functions for Andrew's Excel tax sheet (Retirement Modelling v2 (1).xlsx).

    '''



    def __init__(self,name,ssn,dob,desired_retirement_age,life_exp,retirement_lifestyle,reverse_mort,house_value,filing_status,retire_earn_at_fra,retire_earn_under_fra,total_income,adj_gross,federal_taxable_income,

         federal_regular_tax,state_tax_after_credits,state_effective_rate_to_agi,

         after_tax_income,fica, other_income,projected_income_growth=0.01, risk_profile_over_cpi=0.01):

        '''

        Initialize inputs for user

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

        self.projected_income_growth = projected_income_growth

        self.other_income = other_income



        self.age = ((pd.Timestamp('today')-dob).days)/365.

        self.retirement_years = self.life_exp - self.desired_retirement_age

        self.inflation_level = inflation_level


        dateind = [pd.Timestamp('today').date() + relativedelta(months=+i) for i in range(TOTALROWS)] 

        self.maindf = pd.DataFrame(index=dateind)



    def create_maindf(self):

        self.maindf['Person_Age'] = [self.age + 0.08*i for i in range(TOTALROWS)]


        # MONTHLY GROWTH RATE ASSUMPTIONS

        self.port_return = self.risk_profile_over_cpi/12.

        self.maindf['Proj_Inc_Growth_Monthly'] = [self.projected_income_growth/12. for i in range(TOTALROWS)]

        self.maindf['Proj_Inflation_Rate'] = [self.inflation_level[i] for i in range(TOTALROWS)]

        self.maindf['Portfolio_Return'] = self.maindf['Proj_Inflation_Rate'] + self.risk_profile_over_cpi

        self.maindf['Retire_Work_Inc_Daily_Rate'] = [116*(1+self.projected_income_growth/12.)**i for i in range(TOTALROWS)]


        # INCOME RELATED - WORKING PERIOD
        
        self.maindf['Total_Income'] = self.total_income/12. * (1+self.maindf['Proj_Inc_Growth_Monthly'])

        self.maindf['Other_Income'] = self.other_income/12. * self.maindf['Proj_Inflation_Rate']

        self.maindf['Adj_Gross_Income'] = self.maindf['Total_Income'] + self.maindf['Other_Income']

        self.maindf['Fed_Regular_Tax'] = self.federal_regular_tax/12. * (1.+self.maindf['Proj_Inflation_Rate'])

        self.maindf['Fed_Taxable_Income'] = self.maindf['Adj_Gross_Income'] - self.maindf['Fed_Regular_Tax']

        self.maindf['State_Tax_After_Credits'] = self.state_tax_after_credits/12. * (1.+self.maindf['Proj_Inflation_Rate'])

        self.maindf['After_Tax_Income'] = self.maindf['Adj_Gross_Income'] - self.maindf['Fed_Regular_Tax'] - self.maindf['State_Tax_After_Credits']

        self.maindf['FICA'] = self.fica/12. * (1.+self.maindf['Proj_Inflation_Rate'])

        self.maindf['Home_Value'] = self.house_value * (1.+self.maindf['Proj_Inflation_Rate'])


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


        self.starting_balance_401k = 50000
        
        self.maindf['401k_Capital_Growth'] = self.maindf['Portfolio_Return'] * self.starting_balance_401k


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

        self.maindf['Pension_Balance'] = self.maindf['Pension_Employee'] + self.maindf['Pension_Employer'] + self.maindf['Pension_Capital_Growth'] + self.starting_balance_pension
  
        self.maindf['401k_Balance'] = self.maindf['401k_Employee'] + self.maindf['401k_Employer'] + self.maindf['401k_Capital_Growth'] + self.starting_balance_401k

        self.maindf['Profit_Sharing_Balance'] = self.maindf['Profit_Sharing_Employee'] + self.maindf['Profit_Sharing_Employer'] + self.maindf['Profit_Sharing_Capital_Growth'] + self.starting_balance_profit_sharing

        self.maindf['Money_Purchase_Balance'] = self.maindf['Money_Purchase_Employee'] + self.maindf['Money_Purchase_Employer'] + self.maindf['Money_Purchase_Capital_Growth'] + self.starting_balance_money_purchase

        self.maindf['Esop_Balance'] = self.maindf['Esop_Employee'] + self.maindf['Esop_Employer'] + self.maindf['Esop_Capital_Growth'] + self.starting_balance_esop

        self.maindf['Roth_401k_Balance'] = self.maindf['Roth_401k_Employee'] + self.maindf['Roth_401k_Employer'] + self.maindf['Roth_401k_Capital_Growth'] + self.starting_balance_roth_401k

        self.maindf['Individual_401k_Balance'] = self.maindf['Individual_401k_Employee'] + self.maindf['Individual_401k_Employer'] + self.maindf['Individual_401k_Capital_Growth'] + self.starting_balance_individual_401k

        self.maindf['Ind_Roth_401k_Balance'] = self.maindf['Ind_Roth_401k_Employee'] + self.maindf['Ind_Roth_401k_Employer'] + self.maindf['Ind_Roth_401k_Capital_Growth'] + self.starting_balance_ind_roth_401k

        self.maindf['401a_Keogh_Balance'] = self.maindf['401a_Keogh_Employee'] + self.maindf['401a_Keogh_Employer'] + self.maindf['401a_Keogh_Capital_Growth'] + self.starting_balance_401a_Keogh

        self.maindf['Qual_Np_Balance'] = self.maindf['Qual_Np_Employee'] + self.maindf['Qual_Np_Employer'] + self.maindf['Qual_Np_Capital_Growth'] + self.starting_balance_qual_np

        self.maindf['Qual_Priv_457_Balance'] = self.maindf['Qual_Priv_457_Employee'] + self.maindf['Qual_Priv_457_Employer'] + self.maindf['Qual_Priv_457_Capital_Growth'] + self.starting_balance_qual_priv_457

        self.maindf['457_Balance'] = self.maindf['457_Employee'] + self.maindf['457_Employer'] + self.maindf['457_Capital_Growth'] + self.starting_balance_457

        self.maindf['Qual_Np_Roth_Balance'] = self.maindf['Qual_Np_Roth_Employee'] + self.maindf['Qual_Np_Roth_Employer'] + self.maindf['Qual_Np_Roth_Capital_Growth'] + self.starting_balance_qual_np_roth

        self.maindf['Ira_Balance'] = self.maindf['Ira_Employee'] + self.maindf['Ira_Employer'] + self.maindf['Ira_Capital_Growth'] + self.starting_balance_ira

        self.maindf['Roth_Ira_Balance'] = self.maindf['Roth_Ira_Employee'] + self.maindf['Roth_Ira_Employer'] + self.maindf['Roth_Ira_Capital_Growth'] + self.starting_balance_roth_ira

        self.maindf['Simple_Ira_Balance'] = self.maindf['Simple_Ira_Employee'] + self.maindf['Simple_Ira_Employer'] + self.maindf['Simple_Ira_Capital_Growth'] + self.starting_balance_simple_ira

        self.maindf['Sar_Sep_Ira_Balance'] = self.maindf['Sar_Sep_Ira_Employee'] + self.maindf['Sar_Sep_Ira_Employer'] + self.maindf['Sar_Sep_Ira_Capital_Growth'] + self.starting_balance_sar_sep_ira

        self.maindf['Sep_Ira_Balance'] = self.maindf['Sep_Ira_Employee'] + self.maindf['Sep_Ira_Employer'] + self.maindf['Sep_Ira_Capital_Growth'] + self.starting_balance_sep_ira

        self.maindf['Qual_Annuity_Balance'] = self.maindf['Qual_Annuity_Employee'] + self.maindf['Qual_Annuity_Employer'] + self.maindf['Qual_Annuity_Capital_Growth'] + self.starting_balance_qual_annuity

        self.maindf['Tax_Def_Annuity_Balance'] = self.maindf['Tax_Def_Annuity_Employee'] + self.maindf['Tax_Def_Annuity_Employer'] + self.maindf['Tax_Def_Annuity_Capital_Growth'] + self.starting_balance_tax_def_annuity


        



if __name__ == "__main__":

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

    inflation_level = inflation.inflation_level


    tst_cls = TaxUser(name,ssn,dob,desired_retirement_age,life_exp,retirement_lifestyle,reverse_mort,house_value,filing_status,retire_earn_at_fra,retire_earn_under_fra,total_income,adj_gross,federal_taxable_income,

         federal_regular_tax,state_tax_after_credits,state_effective_rate_to_agi,

         after_tax_income,fica,other_income)

    tst_cls.create_maindf()
    pdb.set_trace()

        
