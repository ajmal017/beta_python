from onboarding.interactive_brokers import onboarding_helpers as onb_help
from onboarding.interactive_brokers import onboarding as onb
from main import constants
from main import abstract
from main import zip2state
import xml.etree.ElementTree as ET
import pdb
import os


def get_tree(onboard,
             docs,
             tax_forms):
    '''
    returns a new xml tree conforming to IB spec for individual applications 
    '''
    
    uri = onb.URI
    ET.register_namespace('', uri)
    applications = ET.Element('Applications')
    tree = ET.ElementTree(applications)
    
    application = ET.SubElement(applications,'Application')

    # Customer
    attrib_customer = {'email': str(onboard.email),
                       'external_id' :str(onboard.account_number),
                       'type' : str(get_account_type(onboard.account_type))}
    customer = ET.SubElement(application,'Customer', attrib_customer)

    account_holder = ET.SubElement(customer,'AccountHolder')

    attrib_account_holder_details = {'external_id' : str(onboard.account_number)}
    account_holder_details = ET.SubElement(account_holder,'AccountHolderDetails', attrib_account_holder_details)

    attrib_name = {'last': str(onboard.last_name),
                   'first': str(onboard.first_name),
                   'salutation': str(onboard.salutation),
                   'suffix': str(onboard.suffix)}
    name = ET.SubElement(account_holder_details,'Name', attrib_name)

    dob = ET.SubElement(account_holder_details,'DOB')
    dob.text = str(onboard.date_of_birth)

    country_of_birth = ET.SubElement(account_holder_details,'CountryOfBirth')
    country_of_birth.text = str(onboard.country_of_birth) 

    marital_status = ET.SubElement(account_holder_details,'MaritalStatus')
    marital_status.text = str(get_marital_status(onboard.plan))

    num_dependents = ET.SubElement(account_holder_details,'NumDependents')
    num_dependents.text = str(onboard.num_dependents)

    attrib_residence =  {'state': str(zip2state.get_state(get_zip_code(onboard.plan))),
                         'street_2': str(onboard.residence_street_2),
                         'postal_code': str(get_zip_code(onboard.plan)),
                         'country': str(onboard.country),
                         'street_1': str(get_address(onboard.address)),
                         'city': str(get_city(onboard.address))}
    residence = ET.SubElement(account_holder_details,'Residence', attrib_residence)

    phones = ET.SubElement(account_holder_details,'Phones')

    attrib_phone = {'number': str(onboard.phone_number) ,
                    'type' : str(onboard.phone_type)}
    phone = ET.SubElement(phones,'Phone', attrib_phone)

    attrib_email = {'email': str(onboard.email)}
    email = ET.SubElement(account_holder_details,'Email', attrib_email)

    attrib_identification = {'citizenship': str(onboard.identif_leg_citizenship),
                             'LegalResidenceState': str(onboard.identif_leg_residence_state),
                             'LegalResidenceCountry': str(onboard.identif_leg_residence_country),
                             'SSN': str(onboard.identif_ssn)}
    identification = ET.SubElement(account_holder_details,'Identification', attrib_identification)

    gender = ET.SubElement(account_holder_details,'Gender')
    gender.text = str(onboard.gender)

    employment_type = ET.SubElement(account_holder_details,'EmploymentType')
    employment_type.text = str(get_employment_type(onboard.plan))

    employment_details = ET.SubElement(account_holder_details,'EmploymentDetails')

    employer = ET.SubElement(employment_details,'employer')
    employer.text = str(onboard.employer)
    
    occupation = ET.SubElement(employment_details,'occupation')
    occupation.text = str(onboard.occupation)
    
    employer_business = ET.SubElement(employment_details,'employer_business')
    employer_business.text = str(onboard.empl_business)

    attrib_employer_address =  {'state': str(onboard.empl_add_state),
                                'street_2': str(onboard.empl_add_street_2),
                                'postal_code': str(onboard.empl_add_postal_code),
                                'country': str(onboard.empl_add_country),
                                'street_1': str(onboard.empl_add_street_1),
                                'city': str(onboard.empl_add_city)}
    employer_address = ET.SubElement(employment_details,'employer_address', attrib_employer_address)

    attrib_fin_info = {'net_worth': str(onboard.fin_info_net_worth),
                                    'liquid_net_worth': str(onboard.fin_info_liq_net_worth),
                                    'annual_net_income': str(onboard.fin_info_ann_net_inc),
                                    'total_assets': str(onboard.fin_info_tot_assets)}
    financial_information = ET.SubElement(account_holder,'FinancialInformation', attrib_fin_info)

    investment_experience = ET.SubElement(financial_information,'InvestmentExperience')

    attrib_asset_experience_0 = {'trades_per_year': str(onboard.asset_exp_0_trds_per_yr),
                                 'years_trading': str(onboard.asset_exp_0_yrs ),
                                 'knowledge_level': str(onboard.asset_exp_0_knowledge),
                                 'asset_class': 'FUND'}
    asset_experience_0 = ET.SubElement(investment_experience,'AssetExperience', attrib_asset_experience_0)

    attrib_asset_experience_1 = {'trades_per_year': str(onboard.asset_exp_1_trds_per_yr),
                                 'years_trading': str(onboard.asset_exp_1_yrs ),
                                 'knowledge_level': str(onboard.asset_exp_1_knowledge),
                                 'asset_class': 'STK'}
    asset_experience_1 = ET.SubElement(investment_experience,'AssetExperience', attrib_asset_experience_1)

    investment_objectives = ET.SubElement(financial_information,'InvestmentObjectives')
    income = ET.SubElement(investment_objectives,'Income')
    growth = ET.SubElement(investment_objectives,'Growth')
    preservation = ET.SubElement(investment_objectives,'Preservation')

    regulatory_details = ET.SubElement(financial_information, 'RegulatoryInformation')
    
    attrib_reg_broker_deal = {'status' : str(onboard.reg_status_broker_deal),
                              'code' : 'BROKERDEALER'}
    
    attrib_reg_exch_memb = {'status' : str(onboard.reg_status_exch_memb),
                              'code' : 'EXCHANGEMEMBERSHIP'}

    attrib_reg_disp = {'status' : str(onboard.reg_status_disp),
                              'code' : 'DISPUTE'}

    attrib_reg_investig = {'status' : str(onboard.reg_status_investig),
                              'code' : 'INVESTIGATION'}

    attrib_reg_stk_cont = {'status' : str(onboard.reg_status_stk_cont),
                              'code' : 'STOCKCONTROL'}

    reg_broker_deal = ET.SubElement(regulatory_details, 'RegulatoryDetail', attrib_reg_broker_deal)

    reg_exch_memb = ET.SubElement(regulatory_details, 'RegulatoryDetail', attrib_reg_exch_memb)

    reg_disp = ET.SubElement(regulatory_details, 'RegulatoryDetail', attrib_reg_disp)

    reg_investig = ET.SubElement(regulatory_details, 'RegulatoryDetail', attrib_reg_investig)

    reg_stk_cont = ET.SubElement(regulatory_details, 'RegulatoryDetail', attrib_reg_stk_cont)

    tax_residencies = ET.SubElement(account_holder,'TaxResidencies')

    attrib_tax_resid_0 = {'country': str(onboard.tax_resid_0_country),
                              'TIN_Type': str(onboard.tax_resid_0_tin_type),
                              'TIN': str(onboard.tax_resid_0_tin)}
    tax_resid_0 = ET.SubElement(tax_residencies,'TaxResidency', attrib_tax_resid_0)

    # Accounts                     
    accounts = ET.SubElement(application,'Accounts')

    attrib_account = {'external_id': str(onboard.account_number),
                      'margin': 'Cash',
                      'base_currency': 'USD',
                      'multicurrency': 'False',
                      'prefix': str(onb_help.get_prefix(onboard.last_name, onboard.first_name))}
    account = ET.SubElement(accounts,'Account', attrib_account)
    
    trading_permissions = ET.SubElement(account,'TradingPermissions')

    attrib_trad_perm_0 = {'exchange_group': 'US-Sec'}
    trad_perm_0 = ET.SubElement(trading_permissions,'TradingPermission', attrib_trad_perm_0)

    attrib_trad_perm_1 = {'exchange_group': 'US-Funds'}
    trad_perm_1 = ET.SubElement(trading_permissions,'TradingPermission', attrib_trad_perm_1)
    
    # Users
    users = ET.SubElement(application,'Users')

    attrib_user = {'external_individual_id': str(onboard.account_number)}
    user_onboard = ET.SubElement(users,'User', attrib_user)

    # Documents
    documents = ET.SubElement(application, 'Documents')

    for dc in docs + tax_forms:
        attrib_doc = {'exec_ts' : onboard.doc_exec_ts,
                        'exec_login_ts' : onboard.doc_exec_login_ts,
                        'form_no' : dc}
        doc = ET.SubElement(documents,'Document', attrib_doc)

        doc_signed_by = ET.SubElement(doc, 'SignedBy')
        doc_signed_by.text = onboard.doc_signed_by

        file = onb.PATH_TO_FILES + onb.DOCUMENTS + dc
        attrib_doc_attached_file = {'file_name' : dc,
                                      'sha1_checksum' : str(onb_help.get_sha1_checksum(file).hexdigest()),
                                      'file_length' :  str(os.path.getsize(file))}
        doc_attached_file = ET.SubElement(doc,'AttachedFile', attrib_doc_attached_file)

    # W8
    for tx_frm in tax_forms:
        attrib_w8_ben = {'part_2_9a_country' : str(onboard.identif_leg_residence_country),
                        'name' : str(onboard.first_name) + ' ' + str(onboard.last_name),
                        'signature_type' : 'Electronic',
                        'blank_form' : 'true',
                        'tax_form_file' : tx_frm}
        tax_form = ET.SubElement(application,'W8Ben', attrib_w8_ben)
    
    return tree

        
def get_account_type(account_type):
    '''
    returns one of 'INDIVIDUAL' of 'JOINT' depending on filing_status
    '''
    if account_type == constants.ACCOUNT_TYPES[0]:
        return 'INDIVIDUAL'

    elif account_type == constants.ACOUNT_TYPES[1]:
        return 'JOINT'

    else:
        raise Exception('account_type not handled')


def get_address(full_address):
    '''
    returns address from full_address
    '''
    ads = [x for x in full_address.split(',') if x != '']
    if len(ads) >= 2:
        return ads[0]
    else:
        return full_address


def get_city(full_address):
    '''
    returns city from full_address
    '''
    ads = [x for x in full_address.split(',') if x != '']
    if len(ads) >= 2:
        return ads[1]
    else:
        return ''


def get_employment_type(plan):
    '''
    returns 'EMPLOYED', 'UNEMPLOYED', 'SELF EMPLOYED', 'RETIRED', or 'NOT LABORFORCE'
    depening on value of plan.employment_status
    '''
    employment_status = plan.employment_status
    
    if employment_status == constants.EMPLOYMENT_STATUS_EMMPLOYED:
        return 'EMPLOYED'

    elif employment_status == constants.EMPLOYMENT_STATUS_UNEMPLOYED:
        return 'UNEMPLOYED'

    elif employment_status == constants.EMPLOYMENT_STATUS_SELF_EMPLOYED:
        return 'SELFEMPLOYED'

    elif employment_status == constants.EMPLOYMENT_STATUS_RETIRED:
        return 'RETIRED'

    elif employment_status == constants.EMPLOYMENT_STATUS_NOT_LABORFORCE:
        return 'ATHOMETRADER'

    else:
        raise Exception('employment_status not handled')
        
        
def get_marital_status(plan):
    '''
    returns 'S', 'M' or 'U', depening on value of plan.client.civil_status
    '''
    filing_status = abstract.PersonalData.CivilStatus(plan.client.civil_status)
    
    if filing_status == abstract.PersonalData.CivilStatus['SINGLE']:
        return 'S'

    elif filing_status == abstract.PersonalData.CivilStatus['MARRIED_FILING_SEPARATELY_LIVED_TOGETHER']:
        return 'M'

    elif filing_status == abstract.PersonalData.CivilStatus['MARRIED_FILING_SEPARATELY_NOT_LIVED_TOGETHER']:
        return 'M'

    elif filing_status == abstract.PersonalData.CivilStatus['HEAD_OF_HOUSEHOLD']:
        return  'M'
          
    elif filing_status == abstract.PersonalData.CivilStatus['QUALIFYING_WIDOWER']:
        return 'W'

    elif filing_status == abstract.PersonalData.CivilStatus['MARRIED_FILING_JOINTLY']:
        return 'M'

    else:
        raise Exception('filing_status not handled')        

        
def get_zip_code(plan):
    '''
    returns zip code from plan
    '''
    try:
        if not plan.retirement_postal_code:
            return int(plan.client.residential_address.post_code)
        else:
            return int(plan.retirement_postal_code)
    except:
        raise Exception("no valid zip code provided")

