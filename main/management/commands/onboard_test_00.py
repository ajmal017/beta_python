from django.core.management.base import NoArgsCommand
from main import constants
from main import abstract
import pandas as pd
import pdb
import os

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        '''
        runs test of IB onboarding, i.e. creates xml files, zips it, encrypts
        it and posts it to IB FTP site
        '''

        from onboarding.interactive_brokers import onboarding as onboard

        class TestOnboard(object):

            def __init__ (self,
                          user,
                          plan,
                          region,
                          address,
                          country_of_birth,
                          num_dependents,
                          residence_street_2,
                          phone_type,
                          phone_number,
                          identif_leg_residence_state,
                          identif_leg_citizenship,
                          identif_leg_residence_country,
                          identif_ssn,
                          gender,
                          employer,
                          occupation,
                          empl_business,
                          empl_add_state,
                          empl_add_street_2,
                          empl_add_postal_code,
                          empl_add_country,
                          empl_add_street_1,
                          empl_add_city,
                          empl_ownership,
                          empl_title,
                          fin_info_tot_assets,
                          fin_info_liq_net_worth,
                          fin_info_ann_net_inc,
                          fin_info_net_worth,
                          asset_exp_0_knowledge,
                          asset_exp_0_yrs,
                          asset_exp_0_trds_per_yr,
                          asset_exp_1_knowledge,
                          asset_exp_1_yrs,
                          asset_exp_1_trds_per_yr,
                          reg_status_broker_deal,
                          reg_status_exch_memb,
                          reg_status_disp,
                          reg_status_investig,
                          reg_status_stk_cont,
                          tax_resid_0_country,
                          tax_resid_0_tin_type,
                          tax_resid_0_tin,
                          doc_exec_ts,
                          doc_exec_login_ts,
                          doc_signed_by):
                
                self.user = user
                self.plan = plan
                self.address = address.address
                self.region = region
                self.country_of_birth = country_of_birth
                self.num_dependents = num_dependents
                self.residence_street_2 = residence_street_2
                self.phone_type = phone_type
                self.phone_number = phone_number
                self.identif_leg_residence_state = identif_leg_residence_state
                self.identif_leg_citizenship = identif_leg_citizenship
                self.identif_leg_residence_country = identif_leg_residence_country
                self.identif_ssn = identif_ssn
                self.gender = gender
                self.employer = employer
                self.occupation = occupation
                self.empl_business = empl_business
                self.empl_add_state = empl_add_state
                self.empl_add_street_2 = empl_add_street_2
                self.empl_add_postal_code = empl_add_postal_code
                self.empl_add_country = empl_add_country
                self.empl_add_street_1 = empl_add_street_1
                self.empl_add_city = empl_add_city
                self.empl_ownership = empl_ownership
                self.empl_title = empl_title
                self.fin_info_tot_assets = fin_info_tot_assets
                self.fin_info_liq_net_worth = fin_info_liq_net_worth
                self.fin_info_ann_net_inc = fin_info_ann_net_inc
                self.fin_info_net_worth = fin_info_net_worth
                self.asset_exp_0_knowledge = asset_exp_0_knowledge
                self.asset_exp_0_yrs = asset_exp_0_yrs
                self.asset_exp_0_trds_per_yr = asset_exp_0_trds_per_yr
                self.asset_exp_1_knowledge = asset_exp_1_knowledge
                self.asset_exp_1_yrs = asset_exp_1_yrs
                self.asset_exp_1_trds_per_yr = asset_exp_1_trds_per_yr
                self.reg_status_broker_deal = reg_status_broker_deal
                self.reg_status_exch_memb = reg_status_exch_memb
                self.reg_status_disp = reg_status_disp
                self.reg_status_investig = reg_status_investig
                self.reg_status_stk_cont = reg_status_stk_cont
                self.tax_resid_0_country = tax_resid_0_country
                self.tax_resid_0_tin_type = tax_resid_0_tin_type
                self.tax_resid_0_tin = tax_resid_0_tin
                self.doc_exec_ts = doc_exec_ts
                self.doc_exec_login_ts = doc_exec_login_ts
                self.doc_signed_by = doc_signed_by
                self.country = country

                self.email = user.email
                self.account_number = plan.client.account_number
                self.account_type = plan.client.account_type
                self.last_name = user.last_name
                self.first_name = user.first_name
                self.date_of_birth = plan.client.date_of_birth
                self.salutation = user.invitation.salutation
                self.suffix = user.invitation.suffix

                
        class TestUser(object):

            class TestInvitation(object):

                def __init__ (self,
                              salutation,
                              suffix):
                    
                    self.salutation = salutation
                    self.suffix = suffix
            
            def __init__(self, email,
                         first_name,
                         last_name,
                         salutation,
                         suffix):
                self.email = email
                self.first_name = first_name
                self.last_name = last_name

                self.invitation = self.TestInvitation(salutation,
                                                      suffix)

        class TestPlan(object):

            class TestChildClientAccount(object):
                
                def __init__ (self,
                              account_number,
                              account_type,
                              date_of_birth,
                              civil_status):
                    
                    self.account_number = account_number
                    self.account_type = account_type
                    self.date_of_birth = date_of_birth
                    self.civil_status = civil_status
                    
            def __init__(self,
                         account_number,
                         account_type,
                         date_of_birth,
                         civil_status,
                         income,
                         retirement_postal_code,
                         employment_status):
                
                self.account_number = account_number
                self.account_type = account_type
                self.income = income
                self.retirement_postal_code = retirement_postal_code
                self.employment_status = employment_status
                
                self.client = self.TestChildClientAccount(self.account_number,
                                                          self.account_type,
                                                          date_of_birth,
                                                          civil_status)

        class TestRegion(object):
            
            def __init__(self,
                         country):
                self.country = country

        class TestAddress(object):

            def __init__ (self,
                          address):
                self.address = address

        class TestIbAccount(object):

            def __init__(self,
                         ib_account):
                self.ib_account = ib_account

        num_dependents = 17
        email = 'corte_el_carnicero@captainhaddock.com'
        first_name = 'Juan'
        last_name = 'Lopez'
        salutation = 'Mr.'
        suffix = 'III'
        account_number = '656764798610877'
        account_type = constants.ACCOUNT_TYPES[0]
        income = 75432
        retirement_postal_code = 28660
        country = 'United States'
        address = '1, La Calle, Pueblo'
        street_2 = 'Anyborough'
        state = 'AL'
        phone_type = 'Home'
        phone_number = '1234567890'
        ib_account = 'UHYT769457001'
        ssn = '1112223333'
        gender = 'M'
        employer = 'ABC Corp'
        occupation = 'Human Resources'
        empl_business = 'Finance'
        postal_code = '12345'
        empl_add_street_1 = '1, the Road' 
        empl_add_city = 'Benavente'
        empl_ownership = '10%'   
        empl_title = 'Jefe' 
        fin_info_tot_assets = '5'
        fin_info_liq_net_worth = '6'
        fin_info_ann_net_inc = '7'
        fin_info_net_worth = '8'
        asset_exp_0_knowledge = 'Limited'
        asset_exp_0_yrs  = '1'
        asset_exp_0_trds_per_yr = '1'
        asset_exp_1_knowledge = 'Limited'
        asset_exp_1_yrs = '2'
        asset_exp_1_trds_per_yr = '2'
        reg_status_broker_deal = 'false'
        reg_status_exch_memb = 'false'
        reg_status_disp = 'false'
        reg_status_investig = 'false'
        reg_status_stk_cont = 'false'
        tax_resid_0_country = 'Spain'
        tax_resid_0_tin_type = 'NonUS_NationalIID'
        tax_resid_0_tin = '1112223456' 
        doc_exec_ts = '20170309140030'
        doc_exec_login_ts = '20170309140000'
        doc_signed_by = 'Juan Lopez'
        date_of_birth = pd.Timestamp('1990-04-05').date()
        civil_status = abstract.PersonalData.CivilStatus['SINGLE'].value
        employment_status = constants.EMPLOYMENT_STATUS_EMMPLOYED
        
        user = TestUser(email,
                        first_name,
                        last_name,
                        salutation,
                        suffix)
        
        plan = TestPlan(account_number,
                        account_type,
                        date_of_birth,
                        civil_status,
                        income,
                        retirement_postal_code,
                        employment_status)

        region = TestRegion(country)

        address = TestAddress(address)

        ib_account = TestIbAccount(ib_account)

        onboarding = TestOnboard(user,
                                plan,
                                region,
                                address,
                                country,
                                num_dependents,
                                street_2,
                                phone_type,
                                phone_number,
                                state,
                                country,
                                country,
                                ssn,
                                gender,
                                employer,
                                occupation,
                                empl_business,
                                state,
                                street_2,
                                postal_code,
                                country,
                                empl_add_street_1,
                                empl_add_city,
                                empl_ownership,
                                empl_title,
                                fin_info_tot_assets,
                                fin_info_liq_net_worth,
                                fin_info_ann_net_inc,
                                fin_info_net_worth,
                                asset_exp_0_knowledge,
                                asset_exp_0_yrs,
                                asset_exp_0_trds_per_yr,
                                asset_exp_1_knowledge,
                                asset_exp_1_yrs,
                                asset_exp_1_trds_per_yr,
                                reg_status_broker_deal,
                                reg_status_exch_memb,
                                reg_status_disp,
                                reg_status_investig,
                                reg_status_stk_cont,
                                country,
                                tax_resid_0_tin_type,
                                ssn,
                                doc_exec_ts,
                                doc_exec_login_ts,
                                doc_signed_by)

        success = onboard.onboard(onboarding)
