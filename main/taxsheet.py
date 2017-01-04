import pdb
import pandas as pd

from dateutil.relativedelta import relativedelta



TOTALROWS = 12*50



class TaxUser(object):

    '''

    Contains a list of inputs and functions for Andrew's Excel tax sheet.

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

        self.after_tax_income = self.adj_gross - self.federal_regular_tax - self.state_tax_after_credits



        dateind = [pd.Timestamp('today').date() + relativedelta(months=+i) for i in range(TOTALROWS)] 

        self.maindf = pd.DataFrame(index=dateind)



    def create_maindf(self):

        self.maindf['Person_Age'] = [self.age + 0.08*i for i in range(TOTALROWS)]

        self.projected_inflation_rate = 0.019



        self.port_return = self.risk_profile_over_cpi/12.

        self.maindf['Retire_Working_Income'] = [116*(1+self.projected_income_growth/12.)**i for i in range(TOTALROWS)]

        self.maindf['Total_Income'] = [self.total_income/12.*(1+self.projected_income_growth/12.)**i for i in range(TOTALROWS)]

        self.maindf['Other_Income'] = [self.other_income/12.*(1+self.projected_inflation_rate/12.)**i for i in range(TOTALROWS)]

        self.maindf['Adj_Gross_Income'] = self.maindf['Retire_Working_Income'] + self.maindf['Total_Income'] + self.maindf['Other_Income']

        self.maindf['Fed_Tax'] = [self.federal_regular_tax/12.*(1.+self.projected_inflation_rate/12)**i for i in range(TOTALROWS)]

        self.maindf['State_Tax_Income'] = [self.state_tax_after_credits/12.*(1.+self.projected_inflation_rate/12)**i for i in range(TOTALROWS)]

        self.maindf['FICA'] = [self.fica/12.*(1.+self.projected_inflation_rate/12)**i for i in range(TOTALROWS)]

        self.maindf['Home_Value'] = [self.house_value*(1.+self.projected_inflation_rate/12)**i for i in range(TOTALROWS)]

        self.maindf['Fed_Tax_Income'] = self.maindf['Adj_Gross_Income'] - self.maindf['Fed_Tax']

        self.maindf['After_Tax_Income'] = self.maindf['Adj_Gross_Income'] - self.maindf['Fed_Tax_Income'] - self.maindf['State_Tax_Income']

        self.maindf['401k'] = 0.055*self.maindf['Total_Income']

        self.maindf['IRA'] = 0.015*self.maindf['Total_Income']

        self.maindf['Roth'] = 0.02*self.maindf['Total_Income']

        self.maindf['401k_employer'] = 0.02*self.maindf['Total_Income']



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



    tst_cls = TaxUser(name,ssn,dob,desired_retirement_age,life_exp,retirement_lifestyle,reverse_mort,house_value,filing_status,retire_earn_at_fra,retire_earn_under_fra,total_income,adj_gross,federal_taxable_income,

         federal_regular_tax,state_tax_after_credits,state_effective_rate_to_agi,

         after_tax_income,fica,other_income)

    tst_cls.create_maindf()
    pdb.set_trace()

        
