import pdb
import hashlib
import time
from . import onboarding as onboard
from main import constants

def get_sha1_checksum(file):
    '''
    returns sha1 checksum
    '''
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1


def set_modified_element(rt, params):
    '''
    sets to 'val' the attribute of element in root 'rt' with position 'pos'
    '''
    val, pos = params
    if len(pos) == 1:
        rt[pos[0]].text = str(val)
    elif len(pos) == 2:
        rt[pos[0]][pos[1]].text = str(val)
    elif len(pos) == 3:
        rt[pos[0]][pos[1]][pos[2]].text = str(val)
    elif len(pos) == 4:
        rt[pos[0]][pos[1]][pos[2]][pos[3]].text = str(val)
    elif len(pos) == 5:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]].text = str(val)
    elif len(pos) == 6:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]][pos[5]].text = str(val)
    elif len(pos) == 7:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]][pos[5]][pos[6]].text = str(val)
    elif len(pos) == 8:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]][pos[5]][pos[6]][pos[7]].text = str(val)


def set_modified_val(rt, params):
    '''
    sets to 'val' the value of item with key 'ky' for the element in root 'rt' with position 'pos'
    '''
    val, ky, pos = params
    if len(pos) == 1:
        rt[pos[0]].attrib[ky] = val
    elif len(pos) == 2:
        rt[pos[0]][pos[1]].attrib[ky] = val
    elif len(pos) == 3:
        rt[pos[0]][pos[1]][pos[2]].attrib[ky] = val
    elif len(pos) == 4:
        rt[pos[0]][pos[1]][pos[2]][pos[3]].attrib[ky] = val
    elif len(pos) == 5:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]].attrib[ky] = val
    elif len(pos) == 6:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]][pos[5]].attrib[ky] = val
    elif len(pos) == 7:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]][pos[5]][pos[6]].attrib[ky] = val
    elif len(pos) == 8:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]][pos[5]][pos[6]][pos[7]].attrib[ky] = val


def get_prefix(last_name, first_name):
    '''
    5 or more lowercase letters which will be used to create the client's username.
    IB will add 3 or 4 numbers to the prefix to create the username.

    Below function attempts to construct 5 letter lower case prefix from last_name and
    first_name. If not enough letters are available, dummy_prefix is used. If the resulting
    prefix contains any non alphabetic these are replaced by 'b'.
    '''
    dummy_prefix = 'abcde'
    prefix = ''
    if len(last_name) >= 5:
        prefix = last_name[:5]
    elif len(last_name) == 4 and len(first_name) >= 1:
        prefix = last_name + first_name[:1]
    elif len(last_name) == 3 and len(first_name) >= 2:
        prefix = last_name + first_name[:2]
    elif len(last_name) == 2 and len(first_name) >= 3:
        prefix = last_name + first_name[:3]
    elif len(last_name) == 1 and len(first_name) >= 4:
        prefix = last_name + first_name[:4]
    elif len(last_name) == 0 and len(first_name) >= 5:
        prefix = last_name + first_name[:5]
    else:
        prefix = dummy_prefix

    prefix = ''.join([c if c.isalpha() else 'x' for c in prefix])

    return prefix.lower()


def show_tree(root):
    '''
    shows up to the top 8 elements in root
    '''
    for i in range(len(root)):
        print(i, root[i].tag, root[i].text, root[i].attrib)
        for j in range(len(root[i])):
            print(i, j, root[i][j].tag, root[i][j].text, root[i][j].attrib)
            for k in range(len(root[i][j])):
                print(i, j, k, root[i][j][k].tag, root[i][j][k].text, root[i][j][k].attrib)
                for m in range(len(root[i][j][k])):
                    print(i, j, k, m, root[i][j][k][m].tag, root[i][j][k][m].text, root[i][j][k][m].attrib)
                    for n in range(len(root[i][j][k][m])):
                        print(i, j, k, m, n, root[i][j][k][m][n].tag, root[i][j][k][m][n].text, root[i][j][k][m][n].attrib)
                        for p in range(len(root[i][j][k][m][n])):
                            print(i, j, k, m, n, p, root[i][j][k][m][n][p].tag, root[i][j][k][m][n][p].text, root[i][j][k][m][n][p].attrib)
                            for q in range(len(root[i][j][k][m][n][p])):
                                print(i, j, k, m, n, p, q, root[i][j][k][m][n][p][q].tag, root[i][j][k][m][n][p][q].text, root[i][j][k][m][n][p][q].attrib)
                                for r in range(len(root[i][j][k][m][n][p][q])):
                                    print(i, j, k, m, n, p, q, r, root[i][j][k][m][n][p][q][r].tag, root[i][j][k][m][n][p][q][r].text, root[i][j][k][m][n][p][q][r].attrib)
                                    print('--- NB there may be more levels with child elements, but these will not be shown ---')


def onboarding_from_invitation(ib_onboard):
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
            self.country = country_of_birth # FIX IT BEN

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

    debug = True
    if debug:
        print('-----------------------')
        print('starting onboarding _from_invitation')
        print('-----------------------')


    user = TestUser(email=ib_onboard.email,
                    first_name=ib_onboard.first_name,
                    last_name=ib_onboard.last_name,
                    salutation=ib_onboard.salutation,
                    suffix=ib_onboard.suffix)

    plan = TestPlan(account_number=ib_onboard.account_number,
                    account_type=constants.ACCOUNT_TYPES[0],
                    date_of_birth=ib_onboard.date_of_birth,
                    civil_status=ib_onboard.civil_status,
                    income=ib_onboard.income,
                    retirement_postal_code=ib_onboard.residential_address.post_code,
                    employment_status=ib_onboard.employment_status)

    region = TestRegion(country=ib_onboard.residential_address.country)

    address = TestAddress(ib_onboard.residential_address.address1)

    ib_account = TestIbAccount(ib_account=ib_onboard.account_number)

    onboarding = TestOnboard(
        user,
        plan,
        region,
        address,
        country_of_birth = ib_onboard.country_of_birth,
        num_dependents = ib_onboard.num_dependents,
        residence_street_2 = ib_onboard.residential_address.address2,
        phone_type=ib_onboard.phone_type,
        phone_number = ib_onboard.phone_number,
        identif_leg_residence_state = ib_onboard.residential_address.state_code,
        identif_leg_citizenship = ib_onboard.identif_leg_citizenship,
        identif_leg_residence_country = ib_onboard.residential_address.country,
        identif_ssn = ib_onboard.identif_ssn,
        gender = ib_onboard.gender,
        employer = ib_onboard.employer,
        occupation = ib_onboard.occupation,
        empl_business = ib_onboard.empl_business,
        empl_add_state = ib_onboard.employer_address.state_code,
        empl_add_street_2 = ib_onboard.employer_address.address2,
        empl_add_postal_code = ib_onboard.employer_address.post_code,
        empl_add_country = ib_onboard.employer_address.country,
        empl_add_street_1 = ib_onboard.employer_address.address1,
        empl_add_city = ib_onboard.employer_address.city,
        empl_ownership = '100%', # HARD_CODED
        empl_title = ib_onboard.employer,
        fin_info_tot_assets = ib_onboard.fin_info_tot_assets,
        fin_info_liq_net_worth = ib_onboard.fin_info_liq_net_worth,
        fin_info_ann_net_inc = ib_onboard.fin_info_ann_net_inc,
        fin_info_net_worth = ib_onboard.fin_info_net_worth, # HARD_CODED
        asset_exp_0_knowledge = ib_onboard.asset_exp_0_knowledge,
        asset_exp_0_yrs = ib_onboard.asset_exp_0_yrs,
        asset_exp_0_trds_per_yr = ib_onboard.asset_exp_0_trds_per_yr,
        asset_exp_1_knowledge = ib_onboard.asset_exp_1_knowledge,
        asset_exp_1_yrs = ib_onboard.asset_exp_1_yrs,
        asset_exp_1_trds_per_yr = ib_onboard.asset_exp_1_trds_per_yr,
        reg_status_broker_deal = ib_onboard.reg_status_broker_deal,
        reg_status_exch_memb = ib_onboard.reg_status_exch_memb,
        reg_status_disp = ib_onboard.reg_status_disp,
        reg_status_investig = ib_onboard.reg_status_investig,
        reg_status_stk_cont = ib_onboard.reg_status_stk_cont,
        tax_resid_0_country = ib_onboard.tax_address.country,
        tax_resid_0_tin_type = ib_onboard.tax_resid_0_tin_type,
        tax_resid_0_tin = ib_onboard.tax_resid_0_tin,
        doc_exec_ts = ib_onboard.doc_exec_ts,
        doc_exec_login_ts = ib_onboard.doc_exec_login_ts,
        doc_signed_by = ib_onboard.doc_signed_by
    )

    success = onboard.onboard(onboarding)
    return success
