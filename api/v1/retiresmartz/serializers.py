import logging
from datetime import date

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.goals.serializers import PortfolioSerializer
from api.v1.serializers import ReadOnlyModelSerializer
from main import constants
from main.models import ExternalAsset
from main.risk_profiler import GoalSettingRiskProfile
from retiresmartz.models import RetirementAdvice, RetirementPlan, \
    RetirementPlanEinc

logger = logging.getLogger('api.v1.retiresmartz.serializers')


def get_default_tx_plan():
    return {
        'begin_date': now().today().date(),
        'amount': 0,
        'growth': settings.BETASMARTZ_CPI,
        'schedule': 'RRULE:FREQ=MONTHLY;BYMONTHDAY=1'
    }


def get_default_life_expectancy(client):
    return settings.MALE_LIFE_EXPECTANCY if client.gender == constants.GENDER_MALE else settings.FEMALE_LIFE_EXPECTANCY


def get_default_retirement_date(client):
    return date(client.date_of_birth.year + 67, client.date_of_birth.month, client.date_of_birth.day)


def who_validator(value):
    if value not in ['self', 'partner', 'joint']:
        raise ValidationError("'who' must be (self|partner|joint)")


def make_category_validator(category):
    def category_validator(value):
        if category(value) not in category:
            raise ValidationError("'cat' for %s must be one of %s" % (category, category.choices()))
    return category_validator


def make_json_list_validator(field, serializer):
    def list_item_validator(value):
        if not isinstance(value, list):
            raise ValidationError("%s must be a JSON list of objects" % field)
        for item in value:
            if not isinstance(item, dict) or not serializer(data=item).is_valid(raise_exception=True):
                raise ValidationError("Invalid %s object" % field)
    return list_item_validator


class PartnerDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    dob = serializers.DateField()
    ssn = serializers.CharField(),
    retirement_age = serializers.IntegerField(default=67)
    income = serializers.IntegerField()
    smoker = serializers.BooleanField(default=False)
    daily_exercise = serializers.IntegerField(default=0)
    weight = serializers.IntegerField(default=65)
    height = serializers.IntegerField(default=160)
    btc = serializers.IntegerField(required=False)
    atc = serializers.IntegerField(required=False)
    max_match = serializers.FloatField(required=False)
    calculated_life_expectancy = serializers.IntegerField(required=False)
    selected_life_expectancy = serializers.IntegerField(required=False)
    social_security_statement = serializers.FileField(required=False),
    social_security_statement_data = serializers.JSONField(required=False)


def partner_data_validator(value):
    if not isinstance(value, dict) or not PartnerDataSerializer(data=value).is_valid(raise_exception=True):
        raise ValidationError("Invalid partner_data object")


class ExpensesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    desc = serializers.CharField()
    cat = serializers.IntegerField(validators=[make_category_validator(RetirementPlan.ExpenseCategory)])
    who = serializers.CharField(validators=[who_validator])
    amt = serializers.IntegerField()


class SavingsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    desc = serializers.CharField()
    cat = serializers.IntegerField(validators=[make_category_validator(RetirementPlan.SavingCategory)])
    who = serializers.CharField(validators=[who_validator])
    amt = serializers.IntegerField()


class InitialDepositsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    asset = serializers.IntegerField(required=False)
    goal = serializers.IntegerField(required=False)
    amt = serializers.IntegerField()


class RetirementPlanSerializer(ReadOnlyModelSerializer):
    # We need to force JSON output for the JSON fields....
    expenses = serializers.JSONField()
    savings = serializers.JSONField()
    initial_deposits = serializers.JSONField()
    partner_data = serializers.JSONField()
    portfolio = PortfolioSerializer()
    on_track = serializers.BooleanField()
    statement_of_advice = serializers.PrimaryKeyRelatedField(read_only=True)
    statement_of_advice_url = serializers.SerializerMethodField(required=False)
    civil_status = serializers.SerializerMethodField(required=False)
    smoker = serializers.SerializerMethodField(required=False)
    daily_exercise = serializers.SerializerMethodField(required=False)
    weight = serializers.SerializerMethodField(required=False)
    height = serializers.SerializerMethodField(required=False)
    drinks = serializers.SerializerMethodField(required=False)

    balance = serializers.FloatField()
    home_value = serializers.SerializerMethodField(required=False)
    home_growth = serializers.SerializerMethodField(required=False)
    ss_fra_todays = serializers.SerializerMethodField(required=False)
    ss_fra_retirement = serializers.SerializerMethodField(required=False)
    state_tax_after_credits = serializers.SerializerMethodField(required=False)
    state_tax_effrate = serializers.SerializerMethodField(required=False)
    pension_name = serializers.SerializerMethodField(required=False)
    pension_amount = serializers.SerializerMethodField(required=False)
    pension_start_date = serializers.SerializerMethodField(required=False)
    employee_contributions_last_year = serializers.SerializerMethodField(required=False)
    employer_contributions_last_year = serializers.SerializerMethodField(required=False)
    total_contributions_last_year = serializers.SerializerMethodField(required=False)

    class Meta:
        model = RetirementPlan
        # Goal setting is an internal field that doesn't need to be shared externally.
        exclude = ('goal_setting',)

    def get_statement_of_advice_url(self, obj):
        if hasattr(obj, 'statement_of_advice'):
            return '/statements/retirement/{}.pdf'.format(obj.statement_of_advice.id)
        else:
            return None

    def get_civil_status(self, obj):
        return obj.client.civil_status

    def get_smoker(self, obj):
        return obj.client.smoker

    def get_daily_exercise(self, obj):
        return obj.client.daily_exercise

    def get_weight(self, obj):
        return obj.client.weight

    def get_height(self, obj):
        return obj.client.height

    def get_drinks(self, obj):
        return obj.client.drinks

    def get_home_value(self, obj):
        return obj.client.home_value

    def get_home_growth(self, obj):
        return obj.client.home_growth

    def get_ss_fra_todays(self, obj):
        return obj.client.ss_fra_todays

    def get_ss_fra_retirement(self, obj):
        return obj.client.ss_fra_retirement

    def get_state_tax_after_credits(self, obj):
        return obj.client.state_tax_after_credits

    def get_state_tax_effrate(self, obj):
        return obj.client.state_tax_effrate

    def get_pension_name(self, obj):
        return obj.client.pension_name

    def get_pension_amount(self, obj):
        return obj.client.pension_amount

    def get_pension_start_date(self, obj):
        return obj.client.pension_start_date

    def get_employee_contributions_last_year(self, obj):
        return obj.client.employee_contributions_last_year

    def get_employer_contributions_last_year(self, obj):
        return obj.client.employer_contributions_last_year

    def get_total_contributions_last_year(self, obj):
        return obj.client.total_contributions_last_year


class RetirementPlanWritableSerializer(serializers.ModelSerializer):
    expenses = serializers.JSONField(required=False,
                                     help_text=RetirementPlan._meta.get_field('expenses').help_text,
                                     validators=[make_json_list_validator('expenses', ExpensesSerializer)])
    savings = serializers.JSONField(required=False,
                                    help_text=RetirementPlan._meta.get_field('savings').help_text,
                                    validators=[make_json_list_validator('savings', SavingsSerializer)])
    initial_deposits = serializers.JSONField(required=False,
                                             help_text=RetirementPlan._meta.get_field('initial_deposits').help_text,
                                             validators=[make_json_list_validator('initial_deposits',
                                                                                  InitialDepositsSerializer)])
    selected_life_expectancy = serializers.IntegerField(required=False)
    retirement_age = serializers.IntegerField(required=False)
    desired_risk = serializers.FloatField(required=False)
    btc = serializers.FloatField(required=False)
    atc = serializers.FloatField(required=False)
    retirement_postal_code = serializers.CharField(max_length=10, required=False)
    partner_data = serializers.JSONField(required=False, validators=[partner_data_validator])
    civil_status = serializers.IntegerField(source='client.civil_status', required=False)
    smoker = serializers.BooleanField(source='client.smoker', required=False)
    daily_exercise = serializers.IntegerField(source='client.daily_exercise', required=False)
    weight = serializers.FloatField(source='client.weight', required=False)
    height = serializers.FloatField(source='client.height', required=False)
    drinks = serializers.IntegerField(source='client.drinks', required=False)

    balance = serializers.FloatField(required=False)
    home_value = serializers.FloatField(source='client.home_value', required=False)
    home_growth = serializers.FloatField(source='client.home_growth', required=False)
    ss_fra_todays = serializers.FloatField(source='client.ss_fra_todays', required=False)
    ss_fra_retirement = serializers.FloatField(source='client.ss_fra_retirement', required=False)
    state_tax_after_credits = serializers.FloatField(source='client.state_tax_after_credits', required=False)
    state_tax_effrate = serializers.FloatField(source='client.state_tax_effrate', required=False)
    pension_name = serializers.CharField(source='client.pension_name', required=False)
    pension_amount = serializers.FloatField(source='client.pension_amount', required=False)
    pension_start_date = serializers.DateField(source='client.pension_start_date', required=False)
    employee_contributions_last_year = serializers.FloatField(source='client.employee_contributions_last_year', required=False)
    employer_contributions_last_year = serializers.FloatField(source='client.employer_contributions_last_year', required=False)
    total_contributions_last_year = serializers.FloatField(source='client.total_contributions_last_year', required=False)

    class Meta:
        model = RetirementPlan
        fields = (
            'name',
            'description',
            'partner_plan',
            'lifestyle',
            'desired_income',
            'income',
            'volunteer_days',
            'paid_days',
            'same_home',
            'same_location',
            'retirement_postal_code',
            'reverse_mortgage',
            'retirement_home_style',
            'retirement_home_price',
            'beta_partner',
            'expenses',
            'savings',
            'initial_deposits',
            'income_growth',
            'expected_return_confidence',
            'retirement_age',
            'btc',
            'atc',
            'max_employer_match_percent',
            'desired_risk',
            'selected_life_expectancy',
            'partner_data',
            'agreed_on',
            'civil_status',  # this field on the client not the RetirementPlan
            'smoker',
            'daily_exercise',
            'weight',
            'height',
            'drinks',
            'balance',
            'home_value',
            'home_growth',
            'ss_fra_todays',
            'ss_fra_retirement',
            'state_tax_after_credits',
            'state_tax_effrate',
            'pension_name',
            'pension_amount',
            'pension_start_date',
            'employee_contributions_last_year',
            'employer_contributions_last_year',
            'total_contributions_last_year',

        )

    def __init__(self, *args, **kwargs):
        super(RetirementPlanWritableSerializer, self).__init__(*args, **kwargs)

        # request-based validation
        request = self.context.get('request')
        if request.method == 'PUT':
            for field in self.fields.values():
                field.required = False

    def validate(self, data):
        """
        Define custom validator so we can confirm if same_home is not true, same_location is specified.
        :param data:
        :return:
        """
        if (self.context.get('request').method == 'POST' and not data.get('same_home', None)
                and data.get('same_location', None) is None):
            raise ValidationError("same_location must be specified if same_home is not True.")

        return data

    @transaction.atomic
    def create(self, validated_data):
        client = validated_data['client']
        if not validated_data.get('retirement_postal_code', ''):
            if validated_data['same_home'] or validated_data['same_location']:
                postal_code = client.residential_address.post_code
                validated_data['retirement_postal_code'] = postal_code
            else:
                raise ValidationError('retirement_postal_code required if not same_home and not same_location')
        # Default the selected life expectancy to the calculated one if not specified.
        if not validated_data.get('selected_life_expectancy', None):
            validated_data['selected_life_expectancy'] = client.life_expectancy

        if not validated_data.get('retirement_age', None):
            validated_data['retirement_age'] = 67

        if not validated_data.get('btc', None):
            # defaults btc
            validated_data['btc'] = validated_data['income'] * min(validated_data.get('max_employer_match_percent', 0), 0.04)

        if not validated_data.get('atc', None):
            # default atc
            validated_data['atc'] = 0

        if validated_data['reverse_mortgage'] and validated_data.get('retirement_home_price', None) is None:
            home = client.external_assets.filter(type=ExternalAsset.Type.FAMILY_HOME.value).first()
            if home:
                validated_data['retirement_home_price'] = home.get_growth_valuation(timezone.now().date())

        # Use the recommended risk for the client if no desired risk specified.
        if not validated_data.get('desired_risk', None):
            bas_scores = client.get_risk_profile_bas_scores()
            validated_data['desired_risk'] = GoalSettingRiskProfile._recommend_risk(bas_scores)

        plan = RetirementPlan.objects.create(**validated_data)
        if plan.agreed_on: plan.generate_soa()

        return plan

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Override the default update because we have nested relations.
        :param instance:
        :param validated_data:
        :return: The updated RetirementPlan
        """

        if instance.agreed_on:
            raise ValidationError("Unable to make changes to a plan that has been agreed on")

        # Client civil_status check
        if 'client' in validated_data:
            if 'civil_status' in validated_data['client']:
                instance.client.civil_status = validated_data['client']['civil_status']
            if 'smoker' in validated_data['client']:
                instance.client.smoker = validated_data['client']['smoker']
            if 'drinks' in validated_data['client']:
                instance.client.drinks = validated_data['client']['drinks']
            if 'height' in validated_data['client']:
                instance.client.height = validated_data['client']['height']
            if 'weight' in validated_data['client']:
                instance.client.weight = validated_data['client']['weight']
            if 'daily_exercise' in validated_data['client']:
                instance.client.daily_exercise = validated_data['client']['daily_exercise']

            if 'home_value' in validated_data['client']:
                instance.client.home_value = validated_data['client']['home_value']
            if 'home_growth' in validated_data['client']:
                instance.client.home_growth = validated_data['client']['home_growth']
            if 'ss_fra_todays' in validated_data['client']:
                instance.client.ss_fra_todays = validated_data['client']['ss_fra_todays']
            if 'ss_fra_retirement' in validated_data['client']:
                instance.client.ss_fra_retirement = validated_data['client']['ss_fra_retirement']
            if 'state_tax_after_credits' in validated_data['client']:
                instance.client.state_tax_after_credits = validated_data['client']['state_tax_after_credits']
            if 'state_tax_effrate' in validated_data['client']:
                instance.client.state_tax_effrate = validated_data['client']['state_tax_effrate']
            if 'pension_name' in validated_data['client']:
                instance.client.pension_name = validated_data['client']['pension_name']
            if 'pension_amount' in validated_data['client']:
                instance.client.pension_amount = validated_data['client']['pension_amount']
            if 'pension_start_date' in validated_data['client']:
                instance.client.pension_start_date = validated_data['client']['pension_start_date']
            if 'employee_contributions_last_year' in validated_data['client']:
                instance.client.employee_contributions_last_year = validated_data['client']['employee_contributions_last_year']
            if 'employer_contributions_last_year' in validated_data['client']:
                instance.client.employer_contributions_last_year = validated_data['client']['employer_contributions_last_year']
            if 'total_contributions_last_year' in validated_data['client']:
                instance.client.total_contributions_last_year = validated_data['client']['total_contributions_last_year']
            instance.client.save()

        for attr, value in validated_data.items():
            if str(attr) != 'client':
                # civil_status update is on client
                setattr(instance, attr, value)

        reverse_plan = getattr(instance, 'partner_plan_reverse', None)
        if instance.partner_plan is not None and reverse_plan is not None and instance.partner_plan != reverse_plan:
            emsg = "Partner plan relationship must be symmetric. " \
                   "I.e. Your selected partner plan must have you as it's partner"
            raise ValidationError(emsg)

        instance.save()

        return instance


class RetirementPlanEincSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = RetirementPlanEinc


class RetirementPlanEincWritableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetirementPlanEinc
        fields = (
            'name',
            'plan',
            'begin_date',
            'amount',
            'growth',
            'schedule'
        )

    def __init__(self, *args, **kwargs):
        super(RetirementPlanEincWritableSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request.method == 'PUT':
            for field in self.fields.values():
                field.required = False


class RetirementAdviceReadSerializer(ReadOnlyModelSerializer):
    """
        Read-Only RetirementAdvice serializer, used for
        get request for retirement-plans advice-feed endpoint
    """

    class Meta:
        model = RetirementAdvice
        fields = (
            'id',
            'plan',
            'dt',
            'trigger',
            'text',
            'read',
            'actions',
        )


class RetirementAdviceWritableSerializer(serializers.ModelSerializer):
    """
        UPDATE PUT/POST RetirementAdvice serializer, used for
        put requests for retirement-plans advice-feed endpoint
    """
    class Meta:
        model = RetirementAdvice
        fields = (
            'read',
        )

    def __init__(self, *args, **kwargs):
        super(RetirementAdviceWritableSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request.method == 'PUT':
            for field in self.fields.values():
                field.required = False
