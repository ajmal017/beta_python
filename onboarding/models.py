from django.db import models
from onboarding.serializer import  Serialize
from onboarding.serializable_model import SerializableModelCustom, SerializableModelNodes, SerializableModelInline


class ACHDetailsType(models.Model):
    cust_init_ACH = models.NullBooleanField(blank=True, null=True)
    bank_name = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class ACHInstructionType(models.Model):
    cust_init_ACH = models.NullBooleanField(blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    ib_acct = models.CharField(max_length=250, blank=True, null=True)
    bank_country = models.CharField(max_length=250, blank=True, null=True)
    currency = models.CharField(max_length=250, blank=True, null=True)
    routing_number = models.CharField(max_length=250, blank=True, null=True)
    acct_number = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class Account(models.Model):
    idx = models.CharField(max_length=250, blank=True, null=True)
    external_id = models.CharField(max_length=250, blank=True, null=True)
    base_currency = models.CharField(max_length=250, blank=True, null=True)
    multicurrency = models.NullBooleanField(blank=True, null=True)
    margin = models.CharField(max_length=250, blank=True, null=True)
    IRA = models.NullBooleanField(blank=True, null=True)
    IRA_type = models.CharField(max_length=250, blank=True, null=True)
    IRA_official_title = models.CharField(max_length=250, blank=True, null=True)
    client_active_trading = models.NullBooleanField(blank=True, null=True)
    duplicate = models.NullBooleanField(blank=True, null=True)
    no_of_duplicates = models.IntegerField(blank=True, null=True)
    stock_yield_program = models.NullBooleanField(blank=True, null=True)
    alias = models.CharField(max_length=250, blank=True, null=True)
    InvestmentObjectives = models.ForeignKey("InvestmentObjectivesType", null=True, blank=True)
    BrokerageServices = models.ForeignKey("BrokerageServices", null=True, blank=True)
    Capabilities = models.ForeignKey("Capabilities", null=True, blank=True)
    TradingPermissions = models.ForeignKey("TradingPermissions", null=True, blank=True)
    CommissionConfigs = models.ForeignKey("CommissionConfigs", null=True, blank=True)
    AllExchangeAccess = models.ForeignKey("AllExchangeAccess", null=True, blank=True)
    DVPInstructions = models.ForeignKey("DVPInstructions", null=True, blank=True)
    TradingLimits = models.ForeignKey("TradingLimits", null=True, blank=True)
    AdvisorWrapFees = models.ForeignKey("AdvisorWrapFeesType", null=True, blank=True)
    Fees = models.ForeignKey("FeesTemplateBasedType", null=True, blank=True)
    ClientCommissionSchedule = models.ForeignKey("CommissionScheduleType", null=True, blank=True)
    ClientInterestMarkupSchedule = models.ForeignKey("InterestMarkupScheduleType", null=True, blank=True)
    Decendent = models.ForeignKey("IRADecedent", null=True, blank=True)
    IRABeneficiaries = models.ForeignKey("IRABeneficiariesType", null=True, blank=True)
    ExtPositionsTransfer = models.ForeignKey("ExtPositionsTransferType", null=True, blank=True)
    DepositNotification = models.ForeignKey("DepositNotificationType", null=True, blank=True)
    ACHInstruction = models.ForeignKey("ACHInstructionType", null=True, blank=True)
    RecurringTransaction = models.ForeignKey("RecurringTransactionType", null=True, blank=True)
    Custodian = models.ForeignKey("CustodianType", related_name="Custodian", null=True, blank=True)
    SuccessorCustodian = models.ForeignKey("CustodianType", related_name="SuccessorCustodian", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AccountSupportType(models.Model):
    type = models.CharField(max_length=250, blank=True, null=True)
    BusinessDescription = models.CharField(max_length=250, blank=True, null=True)
    PrimaryContributor = models.ForeignKey("PrimaryContributorType", null=True, blank=True)
    Administrator = models.ForeignKey("AdministratorType", null=True, blank=True)
    AdministratorContactPerson = models.ForeignKey("AdministratorContactPersonType", null=True, blank=True)
    OwnersResideUS = models.NullBooleanField(blank=True, null=True)
    SolicitOwnersResideUS = models.NullBooleanField(blank=True, null=True)
    AcceptOwnersResideUS = models.NullBooleanField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AccreditedInvestorInformation(models.Model):
    q1 = models.NullBooleanField(blank=True, null=True)
    q2 = models.NullBooleanField(blank=True, null=True)
    q3 = models.NullBooleanField(blank=True, null=True)
    q4 = models.NullBooleanField(blank=True, null=True)
    q5 = models.NullBooleanField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AdditionalSourceOfIncomeType(models.Model):
    SourceOfIncome = models.ForeignKey("SourceOfIncomeType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class Address(SerializableModelInline,models.Model):
    street_1 = models.CharField(max_length=250, blank=True, null=True)
    street_2 = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    postal_code = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AdministratorContactPersonType(models.Model):
    FirstName = models.CharField(max_length=250, blank=True, null=True)
    MiddleInitial = models.CharField(max_length=250, blank=True, null=True)
    LastName = models.CharField(max_length=250, blank=True, null=True)
    Suffix = models.CharField(max_length=250, blank=True, null=True)
    PhoneNumber = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AdministratorType(models.Model):
    FirstName = models.CharField(max_length=250, blank=True, null=True)
    MiddleInitial = models.CharField(max_length=250, blank=True, null=True)
    LastName = models.CharField(max_length=250, blank=True, null=True)
    Suffix = models.CharField(max_length=250, blank=True, null=True)
    Address = models.ForeignKey("Address", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AdvisorWrapFeesType(models.Model):
    strategy = models.CharField(max_length=250, blank=True, null=True)
    ChargeAdvisor = models.NullBooleanField(blank=True, null=True)
    automated_fees_details = models.ForeignKey("AutomatedWrapFeeDetailsType", null=True, blank=True)
    highWaterMarkConfigHwma = models.ForeignKey("HighWaterMarkType", related_name="highWaterMarkConfigHwma_1", null=True, blank=True)
    highWaterMarkConfigHwmq = models.ForeignKey("HighWaterMarkType", related_name="highWaterMarkConfigHwma_2", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AffiliationDetailsType(models.Model):
    affiliation_relationship = models.CharField(max_length=250, blank=True, null=True)
    person_name = models.CharField(max_length=250, blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    company = models.CharField(max_length=250, blank=True, null=True)
    company_mailing_address = models.ForeignKey("Address")
    company_phone = models.CharField(max_length=250, blank=True, null=True)
    company_email_address = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AllExchangeAccess(models.Model):
    ExchangeAccess = models.ForeignKey("ExchangeAccess", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AssetClass(models.Model):
    code = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AssetExperience(models.Model):
    asset_class = models.CharField(max_length=250, blank=True, null=True)
    years_trading = models.IntegerField(blank=True, null=True)
    trades_per_year = models.IntegerField(blank=True, null=True)
    knowledge_level = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AssociatedEntities(models.Model):
    AssociatedIndividual = models.ForeignKey("AssociatedIndividual", null=True, blank=True)
    AssociatedEntity = models.ForeignKey("AssociatedEntity", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AssociatedEntity(models.Model):
    LegalEntity = models.ForeignKey("LegalEntity", null=True, blank=True)
    Ownership = models.ForeignKey("Ownership", null=True, blank=True)
    Title = models.ForeignKey("Title", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AssociatedIndividual(models.Model):
    Individual = models.ForeignKey("Individual", null=True, blank=True)
    Ownership = models.ForeignKey("Ownership", null=True, blank=True)
    Title = models.ForeignKey("Title")
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AssociationTypeEntities(models.Model):
    Individual = models.ForeignKey("Individual", null=True, blank=True)
    LegalEntity = models.ForeignKey("LegalEntity", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class AutomatedWrapFeeDetailsType(models.Model):
    type = models.CharField(max_length=250, blank=True, null=True)
    max_fee = models.FloatField(blank=True, null=True)
    num_contracts = models.IntegerField(blank=True, null=True)
    PostFrequency = models.CharField(max_length=250, blank=True, null=True)
    PercentOfNLVCap = models.CharField(max_length=250, blank=True, null=True)
    PercentOfNLVCap_Q = models.CharField(max_length=250, blank=True, null=True)
    per_trade_markups = models.ForeignKey("CommissionScheduleType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class BrokerageService(models.Model):
    code = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class BrokerageServices(models.Model):
    BrokerageService = models.ForeignKey("BrokerageService", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class Capabilities(models.Model):
    Capability = models.ForeignKey("Capability", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class Capability(models.Model):
    code = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class CheckDetailsType(models.Model):
    check_number = models.CharField(max_length=250, blank=True, null=True)
    routing_number = models.CharField(max_length=250, blank=True, null=True)
    acct_number = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class CommissionConfig(models.Model):
    style = models.CharField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class CommissionConfigs(models.Model):
    CommissionConfig = models.ForeignKey("CommissionConfig", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class CommissionMarkupType(models.Model):
    code = models.CharField(max_length=250, blank=True, null=True)
    minimum = models.FloatField(blank=True, null=True)
    maximum = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    plus_cost = models.NullBooleanField(blank=True, null=True)
    stair = models.ForeignKey("MarkupStaircaseType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class CommissionScheduleType(models.Model):
    markup = models.ForeignKey("CommissionMarkupType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class ControllingOfficer(models.Model):
    Individual = models.ForeignKey("Individual", null=True, blank=True)
    Ownership = models.ForeignKey("Ownership", null=True, blank=True)
    Title = models.ForeignKey("Title", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class CustodianType(models.Model):
    Individual = models.ForeignKey("Individual", related_name="Individual", null=True, blank=True)
    LegalEntity = models.ForeignKey("LegalEntity", null=True, blank=True)
    Employee = models.ForeignKey("Individual", related_name="Employee", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class Customer(models.Model):
    idx = models.CharField(max_length=250, blank=True, null=True)
    external_id = models.CharField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    prefix = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    md_status_nonpro = models.NullBooleanField(blank=True, null=True)
    legal_residence_country = models.CharField(max_length=250, blank=True, null=True)
    tax_treaty_country = models.CharField(max_length=250, blank=True, null=True)
    meet_aml_standard = models.NullBooleanField(blank=True, null=True)
    has_direct_trading_access = models.NullBooleanField(blank=True, null=True)
    origin_country = models.CharField(max_length=250, blank=True, null=True)
    termination_age = models.IntegerField(blank=True, null=True)
    governing_state = models.CharField(max_length=250, blank=True, null=True)
    Organization = models.ForeignKey("OrganizationApplicant", null=True, blank=True)
    AccountHolder = models.ForeignKey("IndividualApplicant", null=True, blank=True)
    JointHolders = models.ForeignKey("JointApplicant", null=True, blank=True)
    Trust = models.ForeignKey("TrustApplicant", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class DVPInstruction(models.Model):
    idx = models.CharField(max_length=250, blank=True, null=True)
    external_id = models.CharField(max_length=250, blank=True, null=True)
    ExternalAcctID = models.CharField(max_length=250, blank=True, null=True)
    AcctID = models.CharField(max_length=250, blank=True, null=True)
    Name = models.CharField(max_length=250, blank=True, null=True)
    Type = models.CharField(max_length=250, blank=True, null=True)
    Role = models.CharField(max_length=250, blank=True, null=True)
    AgentID = models.CharField(max_length=250, blank=True, null=True)
    FirmID = models.CharField(max_length=250, blank=True, null=True)
    AccountID = models.CharField(max_length=250, blank=True, null=True)
    AgentName = models.CharField(max_length=250, blank=True, null=True)
    AccountName = models.CharField(max_length=250, blank=True, null=True)
    DayDoID = models.CharField(max_length=250, blank=True, null=True)
    TXGroupCode = models.CharField(max_length=250, blank=True, null=True)
    BrokerCode = models.CharField(max_length=250, blank=True, null=True)
    AssetClass = models.CharField(max_length=250, blank=True, null=True)
    Exchange = models.CharField(max_length=250, blank=True, null=True)
    PrepayTax = models.NullBooleanField(blank=True, null=True)
    PrepayCommission = models.NullBooleanField(blank=True, null=True)
    Default = models.NullBooleanField(blank=True, null=True)
    Expiry = models.DateField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class DVPInstructions(models.Model):
    DVPInstruction = models.ForeignKey("DVPInstruction", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class DayQuantityLimit(models.Model):
    asset = models.CharField(max_length=250, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class DepositNotificationType(models.Model):
    type = models.CharField(max_length=250, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=250, blank=True, null=True)
    ib_acct = models.CharField(max_length=250, blank=True, null=True)
    CheckDetails = models.ForeignKey("CheckDetailsType", null=True, blank=True)
    WireDetails = models.ForeignKey("WireDetailsType", null=True, blank=True)
    ACHDetails = models.ForeignKey("ACHDetailsType", null=True, blank=True)
    IRADepositDetails = models.ForeignKey("IRADepositDetailsType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class EFPQuantityLimits(models.Model):
    max_nominal_efp_per_order = models.IntegerField(blank=True, null=True)
    max_net_efp_trades = models.IntegerField(blank=True, null=True)
    max_gross_efp_trades = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class Email(models.Model):
    email = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class EmploymentDetailsType(models.Model):
    employer = models.CharField(max_length=250, blank=True, null=True)
    occupation = models.CharField(max_length=250, blank=True, null=True)
    employer_business = models.CharField(max_length=250, blank=True, null=True)
    employer_address = models.ForeignKey("Address", null=True, blank=True)
    employer_phone = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class EntityName(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class ExchangeAccess(models.Model):
    asset_class = models.CharField(max_length=250, blank=True, null=True)
    exchange = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class ExtPositionsTransferType(models.Model):
    type = models.CharField(max_length=250, blank=True, null=True)
    sub_type = models.CharField(max_length=250, blank=True, null=True)
    broker_id = models.CharField(max_length=250, blank=True, null=True)
    broker_name = models.CharField(max_length=250, blank=True, null=True)
    acct_at_broker = models.CharField(max_length=250, blank=True, null=True)
    src_IRA_type = models.CharField(max_length=250, blank=True, null=True)
    margin_loan = models.NullBooleanField(blank=True, null=True)
    short_pos = models.NullBooleanField(blank=True, null=True)
    option_pos = models.NullBooleanField(blank=True, null=True)
    ib_acct = models.CharField(max_length=250, blank=True, null=True)
    third_party_type = models.CharField(max_length=250, blank=True, null=True)
    approximate_acct_value = models.IntegerField(blank=True, null=True)
    ssn = models.CharField(max_length=250, blank=True, null=True)
    ein = models.CharField(max_length=250, blank=True, null=True)
    signature = models.CharField(max_length=250, blank=True, null=True)
    authorize_to_remove_fund = models.NullBooleanField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class ExtPositionsTransfers(models.Model):
    ExtPositionsTransfer = models.ForeignKey("ExtPositionsTransferType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class FeesTemplateBasedType(models.Model):
    template_name = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class FinancialInformation(models.Model):
    net_worth = models.FloatField(blank=True, null=True)
    liquid_net_worth = models.FloatField(blank=True, null=True)
    annual_net_income = models.FloatField(blank=True, null=True)
    total_assets = models.FloatField(blank=True, null=True)
    source_of_funds = models.CharField(max_length=250, blank=True, null=True)
    is_translated = models.NullBooleanField(blank=True, null=True)
    InvestmentExperience = models.ForeignKey("InvestmentExperience", null=True, blank=True)
    InvestmentObjectives = models.ForeignKey("InvestmentObjectivesType", null=True, blank=True)
    AdditionalSourceOfIncome = models.ForeignKey("AdditionalSourceOfIncomeType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class FinancialOrgType(models.Model):
    code = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class FormW8BEN(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    country_of_citizenship = models.CharField(max_length=250, blank=True, null=True)
    residence_address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    mailing_address = models.CharField(max_length=250, blank=True, null=True)
    mailing_city = models.CharField(max_length=250, blank=True, null=True)
    mailing_country = models.CharField(max_length=250, blank=True, null=True)
    tin = models.CharField(max_length=250, blank=True, null=True)
    foreign_tax_id = models.CharField(max_length=250, blank=True, null=True)
    reference_number = models.IntegerField(blank=True, null=True)
    part_2_9a_country = models.CharField(max_length=250, blank=True, null=True)
    part_2_10_article = models.CharField(max_length=250, blank=True, null=True)
    part_2_10_percent = models.CharField(max_length=250, blank=True, null=True)
    part_2_10_income_type = models.CharField(max_length=250, blank=True, null=True)
    part_2_10_reasons = models.CharField(max_length=250, blank=True, null=True)
    cert = models.NullBooleanField(blank=True, null=True)
    signature_type = models.CharField(max_length=250, blank=True, null=True)
    blank_form = models.NullBooleanField(blank=True, null=True)
    tax_form_file = models.CharField(max_length=250, blank=True, null=True)
    proprietary_form_number = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class FormW8BENE(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    disregarded_entity_name = models.CharField(max_length=250, blank=True, null=True)
    entity_type = models.CharField(max_length=250, blank=True, null=True)
    fatca_status = models.CharField(max_length=250, blank=True, null=True)
    residence_address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    mailing_address = models.CharField(max_length=250, blank=True, null=True)
    mailing_city = models.CharField(max_length=250, blank=True, null=True)
    mailing_country = models.CharField(max_length=250, blank=True, null=True)
    us_tin = models.CharField(max_length=250, blank=True, null=True)
    giin = models.CharField(max_length=250, blank=True, null=True)
    foreign_tin = models.CharField(max_length=250, blank=True, null=True)
    reference_number = models.IntegerField(blank=True, null=True)
    box_11_status = models.CharField(max_length=250, blank=True, null=True)
    part_3_14a = models.NullBooleanField(blank=True, null=True)
    part_3_14a_country = models.CharField(max_length=250, blank=True, null=True)
    part_3_14b = models.NullBooleanField(blank=True, null=True)
    part_3_14c = models.NullBooleanField(blank=True, null=True)
    part_3_15_article = models.CharField(max_length=250, blank=True, null=True)
    part_3_15_wh_rate = models.CharField(max_length=250, blank=True, null=True)
    part_3_15_income_type = models.CharField(max_length=250, blank=True, null=True)
    part_3_15_reasons = models.CharField(max_length=250, blank=True, null=True)
    part_4_16 = models.CharField(max_length=250, blank=True, null=True)
    part_4_17_i = models.NullBooleanField(blank=True, null=True)
    part_4_17_ii = models.NullBooleanField(blank=True, null=True)
    part_5_18 = models.NullBooleanField(blank=True, null=True)
    part_6_19 = models.NullBooleanField(blank=True, null=True)
    part_7_20 = models.CharField(max_length=250, blank=True, null=True)
    part_7_21 = models.NullBooleanField(blank=True, null=True)
    part_8_22 = models.NullBooleanField(blank=True, null=True)
    part_9_23 = models.NullBooleanField(blank=True, null=True)
    part_10_24a = models.NullBooleanField(blank=True, null=True)
    part_10_24b = models.NullBooleanField(blank=True, null=True)
    part_10_24c = models.NullBooleanField(blank=True, null=True)
    part_10_24d = models.NullBooleanField(blank=True, null=True)
    part_11_25a = models.NullBooleanField(blank=True, null=True)
    part_11_25b = models.NullBooleanField(blank=True, null=True)
    part_11_25c = models.NullBooleanField(blank=True, null=True)
    part_12_26 = models.NullBooleanField(blank=True, null=True)
    part_12_26_desc1 = models.CharField(max_length=250, blank=True, null=True)
    part_12_26_desc2 = models.CharField(max_length=250, blank=True, null=True)
    part_12_26_desc3 = models.CharField(max_length=250, blank=True, null=True)
    part_13_27 = models.NullBooleanField(blank=True, null=True)
    part_14_28a = models.NullBooleanField(blank=True, null=True)
    part_14_28b = models.NullBooleanField(blank=True, null=True)
    part_15_29a = models.NullBooleanField(blank=True, null=True)
    part_15_29b = models.NullBooleanField(blank=True, null=True)
    part_15_29c = models.NullBooleanField(blank=True, null=True)
    part_15_29d = models.NullBooleanField(blank=True, null=True)
    part_15_29e = models.NullBooleanField(blank=True, null=True)
    part_15_29f = models.NullBooleanField(blank=True, null=True)
    part_16_30 = models.NullBooleanField(blank=True, null=True)
    part_17_31 = models.NullBooleanField(blank=True, null=True)
    part_18_32 = models.NullBooleanField(blank=True, null=True)
    part_19_33 = models.NullBooleanField(blank=True, null=True)
    part_20_34 = models.NullBooleanField(blank=True, null=True)
    part_21_35 = models.NullBooleanField(blank=True, null=True)
    part_21_35_date = models.CharField(max_length=250, blank=True, null=True)
    part_22_36 = models.NullBooleanField(blank=True, null=True)
    part_23_37a = models.NullBooleanField(blank=True, null=True)
    part_23_37a_desc = models.CharField(max_length=250, blank=True, null=True)
    part_23_37b = models.NullBooleanField(blank=True, null=True)
    part_23_37b_desc1 = models.CharField(max_length=250, blank=True, null=True)
    part_23_37b_desc2 = models.CharField(max_length=250, blank=True, null=True)
    part_24_38 = models.NullBooleanField(blank=True, null=True)
    part_25_39 = models.NullBooleanField(blank=True, null=True)
    part_26_40a = models.NullBooleanField(blank=True, null=True)
    part_26_40b = models.NullBooleanField(blank=True, null=True)
    part_26_40c = models.NullBooleanField(blank=True, null=True)
    part_27_41 = models.NullBooleanField(blank=True, null=True)
    part_28_42 = models.CharField(max_length=250, blank=True, null=True)
    part_28_43 = models.NullBooleanField(blank=True, null=True)
    cert = models.NullBooleanField(blank=True, null=True)
    SubstantialUsOwners = models.ForeignKey("SubstantialUsOwners", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class FormW8IMY(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    country_of_incorporation = models.CharField(max_length=250, blank=True, null=True)
    disregarded_entity_name = models.CharField(max_length=250, blank=True, null=True)
    entity_type = models.CharField(max_length=250, blank=True, null=True)
    fatca_status = models.CharField(max_length=250, blank=True, null=True)
    residence_address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    mailing_address = models.CharField(max_length=250, blank=True, null=True)
    mailing_city = models.CharField(max_length=250, blank=True, null=True)
    mailing_country = models.CharField(max_length=250, blank=True, null=True)
    us_tin = models.CharField(max_length=250, blank=True, null=True)
    us_tin_type = models.CharField(max_length=250, blank=True, null=True)
    giin = models.CharField(max_length=250, blank=True, null=True)
    reference_number = models.IntegerField(blank=True, null=True)
    box_11_status = models.CharField(max_length=250, blank=True, null=True)
    part_3_14a = models.NullBooleanField(blank=True, null=True)
    part_3_14b = models.NullBooleanField(blank=True, null=True)
    part_3_14c = models.NullBooleanField(blank=True, null=True)
    part_3_14c_desc = models.CharField(max_length=250, blank=True, null=True)
    part_3_14d = models.NullBooleanField(blank=True, null=True)
    part_3_14d_desc = models.CharField(max_length=250, blank=True, null=True)
    part_3_14e = models.NullBooleanField(blank=True, null=True)
    part_3_14e_desc = models.CharField(max_length=250, blank=True, null=True)
    part_3_14e_i = models.NullBooleanField(blank=True, null=True)
    part_3_14e_ii = models.NullBooleanField(blank=True, null=True)
    part_4_15a = models.NullBooleanField(blank=True, null=True)
    part_4_15b = models.NullBooleanField(blank=True, null=True)
    part_4_15c = models.NullBooleanField(blank=True, null=True)
    part_4_15d = models.NullBooleanField(blank=True, null=True)
    part_5_16a = models.NullBooleanField(blank=True, null=True)
    part_5_16b = models.NullBooleanField(blank=True, null=True)
    part_5_16c = models.NullBooleanField(blank=True, null=True)
    part_6_17a = models.NullBooleanField(blank=True, null=True)
    part_6_17b = models.NullBooleanField(blank=True, null=True)
    part_6_17c = models.NullBooleanField(blank=True, null=True)
    part_7_18 = models.NullBooleanField(blank=True, null=True)
    part_8_19 = models.NullBooleanField(blank=True, null=True)
    part_9_20 = models.NullBooleanField(blank=True, null=True)
    part_10_21 = models.CharField(max_length=250, blank=True, null=True)
    part_10_21a = models.CharField(max_length=250, blank=True, null=True)
    part_10_21b = models.NullBooleanField(blank=True, null=True)
    part_10_21c = models.NullBooleanField(blank=True, null=True)
    part_11_22a = models.NullBooleanField(blank=True, null=True)
    part_11_22b = models.NullBooleanField(blank=True, null=True)
    part_11_22c = models.NullBooleanField(blank=True, null=True)
    part_12_23 = models.NullBooleanField(blank=True, null=True)
    part_13_24 = models.NullBooleanField(blank=True, null=True)
    part_14_25a = models.CharField(max_length=250, blank=True, null=True)
    part_14_25b = models.NullBooleanField(blank=True, null=True)
    part_15_26 = models.NullBooleanField(blank=True, null=True)
    part_16_27a = models.NullBooleanField(blank=True, null=True)
    part_16_27b = models.NullBooleanField(blank=True, null=True)
    part_16_27c = models.NullBooleanField(blank=True, null=True)
    part_17_28 = models.NullBooleanField(blank=True, null=True)
    part_18_29 = models.NullBooleanField(blank=True, null=True)
    part_18_29_desc1 = models.CharField(max_length=250, blank=True, null=True)
    part_18_29_desc2 = models.CharField(max_length=250, blank=True, null=True)
    part_18_29_desc3 = models.CharField(max_length=250, blank=True, null=True)
    part_19_30a = models.NullBooleanField(blank=True, null=True)
    part_19_30b = models.NullBooleanField(blank=True, null=True)
    part_19_30c = models.NullBooleanField(blank=True, null=True)
    part_19_30d = models.NullBooleanField(blank=True, null=True)
    part_19_30e = models.NullBooleanField(blank=True, null=True)
    part_19_30f = models.NullBooleanField(blank=True, null=True)
    part_20_31 = models.NullBooleanField(blank=True, null=True)
    part_21_32 = models.NullBooleanField(blank=True, null=True)
    part_21_32_desc = models.CharField(max_length=250, blank=True, null=True)
    part_22_33 = models.NullBooleanField(blank=True, null=True)
    part_22_33_desc = models.CharField(max_length=250, blank=True, null=True)
    part_23_34a = models.NullBooleanField(blank=True, null=True)
    part_23_34a_desc = models.CharField(max_length=250, blank=True, null=True)
    part_23_34b = models.NullBooleanField(blank=True, null=True)
    part_23_34b_desc = models.CharField(max_length=250, blank=True, null=True)
    part_24_35 = models.NullBooleanField(blank=True, null=True)
    part_25_36 = models.NullBooleanField(blank=True, null=True)
    part_26_37 = models.NullBooleanField(blank=True, null=True)
    part_27_38 = models.CharField(max_length=250, blank=True, null=True)
    part_27_39 = models.NullBooleanField(blank=True, null=True)
    cert = models.NullBooleanField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class FormW9(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    business_name = models.CharField(max_length=250, blank=True, null=True)
    customer_type = models.CharField(max_length=250, blank=True, null=True)
    tax_classification = models.CharField(max_length=250, blank=True, null=True)
    other_customer_type = models.CharField(max_length=250, blank=True, null=True)
    tin = models.CharField(max_length=250, blank=True, null=True)
    tin_type = models.CharField(max_length=250, blank=True, null=True)
    cert1 = models.NullBooleanField(blank=True, null=True)
    cert2 = models.NullBooleanField(blank=True, null=True)
    cert3 = models.NullBooleanField(blank=True, null=True)
    cert4 = models.NullBooleanField(blank=True, null=True)
    fatca_exempt_payee_code = models.CharField(max_length=250, blank=True, null=True)
    fatca_exempt_report_code = models.CharField(max_length=250, blank=True, null=True)
    signature_type = models.CharField(max_length=250, blank=True, null=True)
    blank_form = models.NullBooleanField(blank=True, null=True)
    tax_form_file = models.CharField(max_length=250, blank=True, null=True)
    proprietary_form_number = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class FullyPaidSLBRequestType(models.Model):
    ib_acct = models.CharField(max_length=250, blank=True, null=True)
    user_name = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class HighWaterMarkConfigurationType(models.Model):
    NumberOfPeriods = models.IntegerField(blank=True, null=True)
    ProrateForWithdrawals = models.NullBooleanField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class HighWaterMarkType(models.Model):
    hwm = models.ForeignKey("HighWaterMarkConfigurationType", null=True, blank=True)
    previousLosses = models.ForeignKey("PreviousLossesType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class IRABeneficiariesType(models.Model):
    spouse_primary_beneficary = models.NullBooleanField(blank=True, null=True)
    PrimaryBeneficiary = models.ForeignKey("IRAPrimaryBeneficiary", null=True, blank=True)
    PrimaryBeneficiaryEntity = models.ForeignKey("IRAPrimaryBeneficiaryEntity", null=True, blank=True)
    ContingentBeneficiary = models.ForeignKey("IRAContingentBeneficiary", null=True, blank=True)
    ContingentBeneficiaryEntity = models.ForeignKey("IRAContingentBeneficiaryEntity", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class IRAContingentBeneficiary(models.Model):
    Individual = models.ForeignKey("Individual", null=True, blank=True)
    Ownership = models.ForeignKey("Ownership", null=True, blank=True)
    Title = models.ForeignKey("Title", null=True, blank=True)
    Relationship = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class IRAContingentBeneficiaryEntity(models.Model):
    SimpleLegalEntityType = models.ForeignKey("SimpleLegalEntityType", null=True, blank=True)
    Ownership = models.ForeignKey("Ownership", null=True, blank=True)
    Title = models.ForeignKey("Title", null=True, blank=True)
    Relationship = models.CharField(max_length=250, blank=True, null=True)
    Executor = models.ForeignKey("Individual", null=True, blank=True)
    ExecutionDate = models.DateField(blank=True, null=True)
    ArticleOfWill = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class IRADecedent(models.Model):
    Individual = models.ForeignKey("Individual", null=True, blank=True)
    DateOfDeath = models.DateField(blank=True, null=True)
    Title = models.ForeignKey("Title", null=True, blank=True)
    InheritorType = models.CharField(max_length=250, blank=True, null=True)
    Relationship = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class IRADepositDetailsType(models.Model):
    deposit_type = models.CharField(max_length=250, blank=True, null=True)
    tax_year = models.CharField(max_length=250, blank=True, null=True)
    from_ira_type = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class IRAPrimaryBeneficiary(models.Model):
    Individual = models.ForeignKey("Individual", null=True, blank=True)
    Ownership = models.ForeignKey("Ownership", null=True, blank=True)
    Title = models.ForeignKey("Title", null=True, blank=True)
    Relationship = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class IRAPrimaryBeneficiaryEntity(models.Model):
    SimpleLegalEntityType = models.ForeignKey("SimpleLegalEntityType", null=True, blank=True)
    Ownership = models.ForeignKey("Ownership", null=True, blank=True)
    Title = models.ForeignKey("Title", null=True, blank=True)
    Relationship = models.CharField(max_length=250, blank=True, null=True)
    Executor = models.ForeignKey("Individual", null=True, blank=True)
    ExecutionDate = models.DateField(blank=True, null=True)
    ArticleOfWill = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class IRAWithdrawalDetailsType(models.Model):
    distribution_type = models.CharField(max_length=250, blank=True, null=True)
    excess_contrib_yr = models.IntegerField(blank=True, null=True)
    fed_tax_rate = models.FloatField(blank=True, null=True)
    legal_residence_state = models.CharField(max_length=250, blank=True, null=True)
    state_tax_rate = models.FloatField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class Individual(SerializableModelCustom ,models.Model):
    idx = models.CharField(max_length=250, blank=True, null=True)
    external_id = models.CharField(max_length=250, blank=True, null=True)
    same_mail_address = models.NullBooleanField(blank=True, null=True)
    is_authorized_to_sign_on_behalf_of_owner = models.NullBooleanField(blank=True, null=True)
    is_us_tax_resident = models.NullBooleanField(blank=True, null=True)
    is_translated = models.NullBooleanField(blank=True, null=True)
    Name = models.ForeignKey("IndividualName", null=True, blank=True)
    DOB = models.DateField(blank=True, null=True)
    CountryOfBirth = models.CharField(max_length=250, blank=True, null=True)
    Gender = models.CharField(max_length=250, blank=True, null=True)
    MaritalStatus = models.CharField(max_length=250, blank=True, null=True)
    NumDependents = models.IntegerField(blank=True, null=True)
    Residence = models.ForeignKey("Address", related_name="Individual_Residence", null=True, blank=True)
    MailingAddress = models.ForeignKey("Address", related_name="Individual_MailingAddress", null=True, blank=True)
    Phones = models.ForeignKey("PhonesList", null=True, blank=True)
    Email = models.ForeignKey("Email", null=True, blank=True)
    Identification = models.ForeignKey("IndividualIdentification", null=True, blank=True)
    EmploymentType = models.CharField(max_length=250, blank=True, null=True)
    EmploymentDetails = models.ForeignKey("EmploymentDetailsType", null=True, blank=True)
    EmployeeTitle = models.CharField(max_length=250, blank=True, null=True)
    TaxResidencies = models.ForeignKey("TaxResidencies", blank=True, null=True)
    W9 = models.ForeignKey("FormW9", blank=True, null=True)
    W8Ben = models.ForeignKey("FormW8BEN", blank=True, null=True)
    def __str__(self):
        xmldoc = "<AccountHolder>"
        xmldoc += "\n\r<AccountHolderDetails " + Serialize(self, True, ['external_id', 'same_mail_address']) +">"
        xmldoc += "\n\r"+Serialize(self, False, ['Name_id','Gender', 'DOB', 'MaritalStatus', 'Residence_id'])
        xmldoc += "\n\r<Title>Account Holder</Title>"
        xmldoc += "\n\r"+Serialize(self, False, ['Phones_id'])
        return xmldoc
    def __unicode__(self):
        return "id: %s" % (self.id, )

class IndividualApplicant(models.Model):
    AccountHolderDetails = models.ForeignKey("AssociatedIndividual", null=True, blank=True)
    FinancialInformation = models.ForeignKey("FinancialInformation", null=True, blank=True)
    RegulatoryInformation = models.ForeignKey("RegulatoryInformation", null=True, blank=True)
    RegulatedMemberships = models.ForeignKey("RegulatedMemberships", null=True, blank=True)
    AccreditedInvestorInformation = models.ForeignKey("AccreditedInvestorInformation", null=True, blank=True)
    TaxInformation = models.ForeignKey("IndividualTaxInformation", null=True, blank=True)
    WithholdingStatement = models.ForeignKey("WithholdingStatementType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class IndividualIdentification(models.Model):
    citizenship = models.CharField(max_length=250, blank=True, null=True)
    SSN = models.CharField(max_length=250, blank=True, null=True)
    DriversLicense = models.CharField(max_length=250, blank=True, null=True)
    Passport = models.CharField(max_length=250, blank=True, null=True)
    AlienCard = models.CharField(max_length=250, blank=True, null=True)
    NationalCard = models.CharField(max_length=250, blank=True, null=True)
    IssuingCountry = models.CharField(max_length=250, blank=True, null=True)
    LegalResidenceCountry = models.CharField(max_length=250, blank=True, null=True)
    LegalResidenceState = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class IndividualName(SerializableModelInline, models.Model):
    salutation = models.CharField(max_length=250, blank=True, null=True)
    first = models.CharField(max_length=250, blank=True, null=True)
    last = models.CharField(max_length=250, blank=True, null=True)
    middle = models.CharField(max_length=250, blank=True, null=True)
    suffix = models.CharField(max_length=250, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class IndividualTaxInformation(models.Model):
    W9 = models.ForeignKey("FormW9", null=True, blank=True)
    W8Ben = models.ForeignKey("FormW8BEN", null=True, blank=True)
    W8BenE = models.ForeignKey("FormW8BENE", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class InterestMarkupScheduleType(models.Model):
    markup = models.ForeignKey("InterestMarkupType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class InterestMarkupType(models.Model):
    currency = models.CharField(max_length=250, blank=True, null=True)
    debit_markup = models.FloatField(blank=True, null=True)
    credit_markdown = models.FloatField(blank=True, null=True)
    short_credit_markdown = models.FloatField(blank=True, null=True)
    short_cfd_credit_markdown = models.FloatField(blank=True, null=True)
    long_cfd_debit_markdown = models.FloatField(blank=True, null=True)
    short_index_cfd_credit_markdown = models.FloatField(blank=True, null=True)
    long_index_cfd_debit_markdown = models.FloatField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class InvestmentExperience(models.Model):
    AssetExperience = models.ForeignKey("AssetExperience", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class InvestmentObjectivesType(models.Model):
    objective = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class JointApplicant(models.Model):
    type = models.CharField(max_length=250, blank=True, null=True)
    FirstHolderDetails = models.ForeignKey("AssociatedIndividual", related_name="FirstHolderDetails", null=True, blank=True)
    SecondHolderDetails = models.ForeignKey("AssociatedIndividual", related_name="SecondHolderDetails", null=True, blank=True)
    FinancialInformation = models.ForeignKey("FinancialInformation", null=True, blank=True)
    RegulatoryInformation = models.ForeignKey("RegulatoryInformation", null=True, blank=True)
    RegulatedMemberships = models.ForeignKey("RegulatedMemberships", null=True, blank=True)
    AccreditedInvestorInformation = models.ForeignKey("AccreditedInvestorInformation", null=True, blank=True)
    TaxInformation = models.ForeignKey("IndividualTaxInformation", null=True, blank=True)
    WithholdingStatement = models.ForeignKey("WithholdingStatementType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class LegalEntity(models.Model):
    idx = models.CharField(max_length=250, blank=True, null=True)
    external_id = models.CharField(max_length=250, blank=True, null=True)
    is_us_tax_resident = models.NullBooleanField(blank=True, null=True)
    is_translated = models.NullBooleanField(blank=True, null=True)
    Name = models.ForeignKey("EntityName", null=True, blank=True)
    Location = models.ForeignKey("Address", null=True, blank=True)
    Phones = models.ForeignKey("PhonesList", null=True, blank=True)
    Email = models.ForeignKey("Email", null=True, blank=True)
    LegalEntityIdentification = models.ForeignKey("LegalEntityIdentification")
    TaxResidencies = models.ForeignKey("TaxResidencies")
    def __unicode__(self):
        return "id: %s" % (self.id, )

class LegalEntityIdentification(models.Model):
    identification = models.CharField(max_length=250, blank=True, null=True)
    identification_country = models.CharField(max_length=250, blank=True, null=True)
    formation_country = models.CharField(max_length=250, blank=True, null=True)
    formation_type = models.CharField(max_length=250, blank=True, null=True)
    exchange_code = models.CharField(max_length=250, blank=True, null=True)
    exchange_symbol = models.CharField(max_length=250, blank=True, null=True)
    same_mail_address = models.NullBooleanField(blank=True, null=True)
    PlaceOfBusiness = models.ForeignKey("Address", related_name="LegalEntityIdentification_PlaceOfBusiness", null=True, blank=True)
    MailingAddress = models.ForeignKey("Address", related_name="LegalEntityIdentification_MailingAddress", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class MarkupStaircaseType(models.Model):
    Break = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class ORGRegulatorType(models.Model):
    RegulatorName = models.CharField(max_length=250, blank=True, null=True)
    RegulatorCountry = models.CharField(max_length=250, blank=True, null=True)
    RegulatedInCapacity = models.CharField(max_length=250, blank=True, null=True)
    RegulatorId = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class ORGRegulatoryInfoType(models.Model):
    is_public = models.NullBooleanField(blank=True, null=True)
    is_regulated = models.NullBooleanField(blank=True, null=True)
    PublicCompanyInfo = models.ForeignKey("PublicCompanyInfoType", null=True, blank=True)
    ORGRegulator = models.ForeignKey("ORGRegulatorType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class OrderQuantityLimit(models.Model):
    asset = models.CharField(max_length=250, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class OrderValueLimits(models.Model):
    max_order_value = models.FloatField(blank=True, null=True)
    max_gross_value = models.FloatField(blank=True, null=True)
    max_net_value = models.FloatField(blank=True, null=True)
    net_contract_limit = models.FloatField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class OrganizationApplicant(models.Model):
    type_of_trading = models.CharField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    is_org_us_subsidiary = models.NullBooleanField(blank=True, null=True)
    is_qualified_intermediary = models.NullBooleanField(blank=True, null=True)
    has_assumed_primary_reporting = models.NullBooleanField(blank=True, null=True)
    has_accepted_primary_withholding = models.NullBooleanField(blank=True, null=True)
    Identification = models.ForeignKey("OrganizationIdentification", null=True, blank=True)
    AccountSupport = models.ForeignKey("AccountSupportType", null=True, blank=True)
    FinancialInformation = models.ForeignKey("FinancialInformation", null=True, blank=True)
    AccreditedInvestorInformation = models.ForeignKey("AccreditedInvestorInformation", null=True, blank=True)
    RegulatoryInformation = models.ForeignKey("RegulatoryInformation", null=True, blank=True)
    PrimaryTrader = models.ForeignKey("PrimaryTrader", null=True, blank=True)
    ControllingOfficer = models.ForeignKey("ControllingOfficer", null=True, blank=True)
    AssociatedEntities = models.ForeignKey("AssociatedEntities", null=True, blank=True)
    RegulatedMemberships = models.ForeignKey("RegulatedMemberships", null=True, blank=True)
    TaxResidencies = models.ForeignKey("TaxResidencies", null=True, blank=True)
    W8BenE = models.ForeignKey("FormW8BENE", null=True, blank=True)
    W8IMY = models.ForeignKey("FormW8IMY", null=True, blank=True)
    WithholdingStatement = models.ForeignKey("WithholdingStatementType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class OrganizationIdentification(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    business_description = models.CharField(max_length=250, blank=True, null=True)
    identification = models.CharField(max_length=250, blank=True, null=True)
    identification_country = models.CharField(max_length=250, blank=True, null=True)
    formation_country = models.CharField(max_length=250, blank=True, null=True)
    formation_state = models.CharField(max_length=250, blank=True, null=True)
    same_mail_address = models.NullBooleanField(blank=True, null=True)
    is_translated = models.NullBooleanField(blank=True, null=True)
    PlaceOfBusiness = models.ForeignKey("Address", related_name="OrganizationIdentification_PlaceOfBusiness", null=True, blank=True)
    MailingAddress = models.ForeignKey("Address", related_name="OrganizationIdentification_MailingAddress", null=True, blank=True)
    Phones = models.ForeignKey("PhonesList", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class Ownership(models.Model):
    percentage = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class PhoneInfo(models.Model):
    type = models.CharField(max_length=250, blank=True, null=True)
    number = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class PhonesList(models.Model):
    Phone = models.ForeignKey("PhoneInfo", blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class PreviousLossesType(models.Model):
    loss = models.IntegerField(blank=True, null=True)
    quarter = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    currency = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class PrimaryContributorType(models.Model):
    FirstName = models.CharField(max_length=250, blank=True, null=True)
    MiddleInitial = models.CharField(max_length=250, blank=True, null=True)
    LastName = models.CharField(max_length=250, blank=True, null=True)
    Suffix = models.CharField(max_length=250, blank=True, null=True)
    Employer = models.CharField(max_length=250, blank=True, null=True)
    Occupation = models.CharField(max_length=250, blank=True, null=True)
    Address = models.ForeignKey("Address", null=True, blank=True)
    SourceOfFunds = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class PrimaryTrader(models.Model):
    Individual = models.ForeignKey("Individual", null=True, blank=True)
    Ownership = models.ForeignKey("Ownership", null=True, blank=True)
    Title = models.ForeignKey("Title", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class PublicCompanyInfoType(models.Model):
    ExchangeTradedOn = models.CharField(max_length=250, blank=True, null=True)
    QuotedSymbol = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class RecurringTransactionType(models.Model):
    type = models.CharField(max_length=250, blank=True, null=True)
    method = models.CharField(max_length=250, blank=True, null=True)
    instruction = models.CharField(max_length=250, blank=True, null=True)
    frequency = models.CharField(max_length=250, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=250, blank=True, null=True)
    ib_acct = models.CharField(max_length=250, blank=True, null=True)
    ACHInstruction = models.ForeignKey("ACHInstructionType", null=True, blank=True)
    IRAWithdrawalDetails = models.ForeignKey("IRAWithdrawalDetailsType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class RegulatedMembership(models.Model):
    organization_code = models.CharField(max_length=250, blank=True, null=True)
    membership_id = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class RegulatedMemberships(models.Model):
    RegulatedMembership = models.ForeignKey("RegulatedMembership", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class RegulatoryDetail(models.Model):
    code = models.CharField(max_length=250, blank=True, null=True)
    status = models.NullBooleanField(blank=True, null=True)
    detail = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class RegulatoryInformation(models.Model):
    is_translated = models.NullBooleanField(blank=True, null=True)

    RegulatoryDetails = models.ForeignKey("RegulatoryDetail", related_name="RegulatoryDetails", null=True, blank=True)
    SelfRegulatedMembership = models.ForeignKey("SelfRegulatedMembershipType", null=True, blank=True)
    AffiliationDetails = models.ForeignKey("AffiliationDetailsType", null=True, blank=True)
    FinancialOrgType = models.ForeignKey("FinancialOrgType", null=True, blank=True)
    ORGRegulatoryInfo = models.ForeignKey("ORGRegulatoryInfoType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class Security(models.Model):
    Challenge = models.CharField(max_length=250, blank=True, null=True)
    Response = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class SelfRegulatedMembershipType(models.Model):
    exchanges = models.CharField(max_length=250, blank=True, null=True)
    organizations = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class SimpleLegalEntityType(models.Model):
    idx = models.CharField(max_length=250, blank=True, null=True)
    external_id = models.CharField(max_length=250, blank=True, null=True)
    Name = models.ForeignKey("EntityName", null=True, blank=True)
    Location = models.ForeignKey("Address", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class SourceOfIncomeType(models.Model):
    source_type = models.CharField(max_length=250, blank=True, null=True)
    percentage = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class SubstantialUsOwner(models.Model):
    external_id = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class SubstantialUsOwners(models.Model):
    SubstantialUsOwner = models.ForeignKey("SubstantialUsOwner", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class TaxResidencies(models.Model):
    TaxResidency = models.ForeignKey("TaxResidency", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class TaxResidency(models.Model):
    country = models.CharField(max_length=250, blank=True, null=True)
    TIN = models.CharField(max_length=250, blank=True, null=True)
    TINType = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class Title(models.Model):
    code = models.CharField(max_length=250, blank=True, null=True)
    valueOf_x = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class TradingLimits(models.Model):
    OrderValueLimits = models.ForeignKey("OrderValueLimits", null=True, blank=True)
    EFPQuantityLimits = models.ForeignKey("EFPQuantityLimits", null=True, blank=True)
    OrderQuantityLimit = models.ForeignKey("OrderQuantityLimit", null=True, blank=True)
    DayQuantityLimit = models.ForeignKey("DayQuantityLimit", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class TradingPermission(models.Model):
    asset_class = models.CharField(max_length=250, blank=True, null=True)
    exchange_group = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class TradingPermissions(models.Model):
    TradingPermission = models.ForeignKey("TradingPermission", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class TrustApplicant(models.Model):
    third_party_mgmt = models.NullBooleanField(blank=True, null=True)
    trust_type = models.CharField(max_length=250, blank=True, null=True)
    Identification = models.ForeignKey("TrustIdentification", null=True, blank=True)
    FinancialInformation = models.ForeignKey("FinancialInformation", null=True, blank=True)
    RegulatoryInformation = models.ForeignKey("RegulatoryInformation", null=True, blank=True)
    RegulatedMemberships = models.ForeignKey("RegulatedMemberships", null=True, blank=True)
    AccreditedInvestorInformation = models.ForeignKey("AccreditedInvestorInformation", null=True, blank=True)
    Trustees = models.ForeignKey("TrusteesType")
    Beneficiaries = models.ForeignKey("AssociationTypeEntities", related_name="Beneficiaries", null=True, blank=True)
    Grantors = models.ForeignKey("AssociationTypeEntities", related_name="Grantors", null=True, blank=True)
    TaxResidencies = models.ForeignKey("TaxResidencies", null=True, blank=True)
    W8BenE = models.ForeignKey("FormW8BENE", null=True, blank=True)
    W8IMY = models.ForeignKey("FormW8IMY", null=True, blank=True)
    WithholdingStatement = models.ForeignKey("WithholdingStatementType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class TrustIdentification(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    type_of_trust = models.CharField(max_length=250, blank=True, null=True)
    purpose_of_trust = models.CharField(max_length=250, blank=True, null=True)
    date_formed = models.DateField(blank=True, null=True)
    formation_country = models.CharField(max_length=250, blank=True, null=True)
    formation_state = models.CharField(max_length=250, blank=True, null=True)
    registration_number = models.CharField(max_length=250, blank=True, null=True)
    registration_type = models.CharField(max_length=250, blank=True, null=True)
    registration_country = models.CharField(max_length=250, blank=True, null=True)
    same_mail_address = models.NullBooleanField(blank=True, null=True)
    is_translated = models.NullBooleanField(blank=True, null=True)
    Address = models.ForeignKey("Address", related_name="TrustIdentification_Address", null=True, blank=True)
    MailingAddress = models.ForeignKey("Address", related_name="TrustIdentification_MailingAddress", null=True, blank=True)
    Phones = models.ForeignKey("PhonesList", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class TrusteeEntityType(models.Model):
    LegalEntity = models.ForeignKey("LegalEntity", null=True, blank=True)
    Employee = models.ForeignKey("Individual", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class TrusteeIndividual(models.Model):
    Individual = models.ForeignKey("Individual", null=True, blank=True)
    Occupation = models.CharField(max_length=250, blank=True, null=True)
    IsNFA_Registered = models.NullBooleanField(blank=True, null=True)
    NFA_RegistrationNumber = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class TrusteesType(models.Model):
    Individual = models.ForeignKey("Individual", null=True, blank=True)
    Entity = models.ForeignKey("TrusteeEntityType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class WireDetailsType(models.Model):
    bank_name = models.CharField(max_length=250, blank=True, null=True)
    reference_number = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class WithholdingStatementType(models.Model):
    acct_id = models.CharField(max_length=250, blank=True, null=True)
    fatca_compliant_type = models.CharField(max_length=250, blank=True, null=True)
    us_backup_withholding = models.NullBooleanField(blank=True, null=True)
    treaty_country = models.CharField(max_length=250, blank=True, null=True)
    is_corporation = models.NullBooleanField(blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    is_flow_through = models.NullBooleanField(blank=True, null=True)
    dividend_rate = models.FloatField(blank=True, null=True)
    interest_rate = models.FloatField(blank=True, null=True)
    us_other_rate = models.FloatField(blank=True, null=True)
    eci_rate = models.FloatField(blank=True, null=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )

class WithholdingStatementsType(models.Model):
    qi_class = models.CharField(max_length=250, blank=True, null=True)
    signature = models.CharField(max_length=250, blank=True, null=True)
    signature_timestamp = models.IntegerField(blank=True, null=True)
    WithholdingStatement = models.ForeignKey("WithholdingStatementType", null=True, blank=True)
    def __unicode__(self):
        return "id: %s" % (self.id, )
