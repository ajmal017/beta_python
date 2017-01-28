import logging
import numpy as np
import pandas as pd
import scipy.stats as st
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from api.v1.goals.serializers import PortfolioSerializer
from api.v1.views import ApiViewMixin
from client.models import Client
from common.utils import d2ed
from main.event import Event
from main.models import Ticker
from portfolios.calculation import Unsatisfiable
from retiresmartz import advice_responses
from retiresmartz.calculator import Calculator, create_settings
from retiresmartz.calculator.assets import TaxDeferredAccount
from retiresmartz.calculator.cashflows import EmploymentIncome, \
    InflatedCashFlow, ReverseMortgage
from retiresmartz.calculator.desired_cashflows import RetiresmartzDesiredCashFlow
from retiresmartz.calculator.social_security import calculate_payments
from retiresmartz.models import RetirementAdvice, RetirementPlan
from support.models import SupportRequest
from . import serializers
from main import tax_sheet as tax
from main import zip2state
from main import abstract
from main import constants
from datetime import date, datetime
from pinax.eventlog.models import Log as EventLog
from main.inflation import inflation_level
from functools import reduce
logger = logging.getLogger('api.v1.retiresmartz.views')
import pdb

class RetiresmartzViewSet(ApiViewMixin, NestedViewSetMixin, ModelViewSet):
    model = RetirementPlan
    permission_classes = (IsAuthenticated,)

    # We don't want pagination for this viewset. Remove this line to enable.
    pagination_class = None

    # We define the queryset because our get_queryset calls super so the Nested queryset works.
    queryset = RetirementPlan.objects.all()

    # Set the response serializer because we want to use the 'get' serializer for responses from the 'create' methods.
    # See api/v1/views.py
    serializer_class = serializers.RetirementPlanSerializer
    serializer_response_class = serializers.RetirementPlanSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.RetirementPlanSerializer
        elif self.request.method == 'POST':
            return serializers.RetirementPlanWritableSerializer
        elif self.request.method == 'PUT':
            return serializers.RetirementPlanWritableSerializer

    def get_queryset(self):
        """
        The nested viewset takes care of only returning results for the client we are looking at.
        We need to add logic to only allow access to users that can view the plan.
        """
        qs = super(RetiresmartzViewSet, self).get_queryset()
        # Check user object permissions
        user = SupportRequest.target_user(self.request)
        return qs.filter_by_user(user)

    def perform_create(self, serializer):
        """
        We don't allow users to create retirement plans for others... So we set the client from the URL and validate
        the user has access to it.
        :param serializer:
        :return:
        """
        user = SupportRequest.target_user(self.request)
        client = Client.objects.filter_by_user(user).get(id=int(self.get_parents_query_dict()['client']))
        if 'client' in serializer.validated_data:
            if 'civil_status' in serializer.validated_data['client']:
                client.civil_status = serializer.validated_data['client']['civil_status']
            if 'smoker' in serializer.validated_data['client']:
                client.smoker = serializer.validated_data['client']['smoker']
            if 'drinks' in serializer.validated_data['client']:
                client.drinks = serializer.validated_data['client']['drinks']
            if 'height' in serializer.validated_data['client']:
                client.height = serializer.validated_data['client']['height']
            if 'weight' in serializer.validated_data['client']:
                client.weight = serializer.validated_data['client']['weight']
            if 'daily_exercise' in serializer.validated_data['client']:
                client.daily_exercise = serializer.validated_data['client']['daily_exercise']

            if 'home_value' in serializer.validated_data['client']:
                client.home_value = serializer.validated_data['client']['home_value']
            if 'home_growth' in serializer.validated_data['client']:
                client.home_growth = serializer.validated_data['client']['home_growth']
            if 'ss_fra_todays' in serializer.validated_data['client']:
                client.ss_fra_todays = serializer.validated_data['client']['ss_fra_todays']
            if 'ss_fra_retirement' in serializer.validated_data['client']:
                client.ss_fra_retirement = serializer.validated_data['client']['ss_fra_retirement']
            if 'state_tax_after_credits' in serializer.validated_data['client']:
                client.state_tax_after_credits = serializer.validated_data['client']['state_tax_after_credits']
            if 'state_tax_effrate' in serializer.validated_data['client']:
                client.state_tax_effrate = serializer.validated_data['client']['state_tax_effrate']
            if 'pension_name' in serializer.validated_data['client']:
                client.pension_name = serializer.validated_data['client']['pension_name']
            if 'pension_amount' in serializer.validated_data['client']:
                client.pension_amount = serializer.validated_data['client']['pension_amount']
            if 'pension_start_date' in serializer.validated_data['client']:
                client.pension_start_date = serializer.validated_data['client']['pension_start_date']
            if 'employee_contributions_last_year' in serializer.validated_data['client']:
                client.employee_contributions_last_year = serializer.validated_data['client']['employee_contributions_last_year']
            if 'employer_contributions_last_year' in serializer.validated_data['client']:
                client.employer_contributions_last_year = serializer.validated_data['client']['employer_contributions_last_year']
            if 'total_contributions_last_year' in serializer.validated_data['client']:
                client.total_contributions_last_year = serializer.validated_data['client']['total_contributions_last_year']
            client.save()
        return serializer.save(client=client)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.agreed_on:
            return Response({'error': 'Unable to update a RetirementPlan that has been agreed on'},
                            status=status.HTTP_400_BAD_REQUEST)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        orig = RetirementPlan.objects.get(pk=instance.pk)
        orig_client = orig.client
        updated = serializer.update(instance, serializer.validated_data)
        updated_client = updated.client

        if getattr(instance, '_prefetched_objects_cache', None) is not None:
            # If 'prefetch_related' has been applied to a queryset, we need to
            # refresh the instance from the database.
            instance = self.get_object()
            serializer = self.get_serializer(instance)

        # RetirementAdvice Triggers
        orig_daily_exercise = 0 if orig_client.daily_exercise is None else orig_client.daily_exercise
        orig_drinks = 0 if orig_client.drinks is None else orig_client.drinks
        orig_smoker = orig_client.smoker
        orig_height = orig_client.height
        orig_weight = orig_client.weight

        life_expectancy_field_updated = (updated_client.daily_exercise != orig_client.daily_exercise or
                                         updated_client.weight != orig_weight or
                                         updated_client.height != orig_height or
                                         updated_client.smoker != orig_smoker or
                                         updated_client.drinks != orig_drinks)

        # Advice feed for toggling smoker
        if updated_client.smoker != orig_smoker:
            if updated_client.smoker:
                e = Event.RETIRESMARTZ_IS_A_SMOKER.log(None,
                                                       user=updated_client.user,
                                                       obj=updated_client)
                advice = RetirementAdvice(plan=updated, trigger=e)
                advice.text = advice_responses.get_smoking_yes(advice)
                advice.save()
            elif updated_client.smoker is False:
                e = Event.RETIRESMARTZ_IS_NOT_A_SMOKER.log(None,
                                                           user=updated_client.user,
                                                           obj=updated_client)
                advice = RetirementAdvice(plan=updated, trigger=e)
                advice.text = advice_responses.get_smoking_no(advice)
                advice.save()

        # Advice feed for daily_exercise change
        if updated_client.daily_exercise != orig_daily_exercise:
            # exercise only
            e = Event.RETIRESMARTZ_EXERCISE_ONLY.log(None,
                                                     user=updated_client.user,
                                                     obj=updated_client)
            advice = RetirementAdvice(plan=updated, trigger=e)
            advice.text = advice_responses.get_exercise_only(advice)
            advice.save()

        # Advice feed for drinks change
        if updated_client.drinks != orig_drinks:
            if updated_client.drinks > 1:
                e = Event.RETIRESMARTZ_DRINKS_MORE_THAN_ONE.log(None,
                                                     user=updated_client.user,
                                                     obj=updated_client)
                advice = RetirementAdvice(plan=updated, trigger=e)
                advice.text = advice_responses.get_drinks_more_than_one(advice)
                advice.save()
            else:
                e = Event.RETIRESMARTZ_DRINKS_ONE_OR_LESS.log(None,
                                                     user=updated_client.user,
                                                     obj=updated_client)
                advice = RetirementAdvice(plan=updated, trigger=e)
                advice.text = advice_responses.get_drinks_one_or_less(advice)
                advice.save()

        # frontend posts one at a time, weight then height, not together in one post
        if (updated_client.weight != orig_weight or updated_client.height != orig_height):
            # weight and/or height updated
            e = Event.RETIRESMARTZ_WEIGHT_AND_HEIGHT_ONLY.log(None,
                                                              user=updated_client.user,
                                                              obj=updated_client)
            advice = RetirementAdvice(plan=updated, trigger=e)
            advice.text = advice_responses.get_weight_and_height_only(advice)
            advice.save()

        if life_expectancy_field_updated and (updated_client.daily_exercise and
           updated_client.weight and updated_client.height and updated_client.smoker is not None and
           updated_client.drinks is not None):
            # every wellbeing field
            e = Event.RETIRESMARTZ_ALL_WELLBEING_ENTRIES.log(None,
                                                             user=updated_client.user,
                                                             obj=updated_client)
            advice = RetirementAdvice(plan=updated, trigger=e)
            advice.text = advice_responses.get_all_wellbeing_entries(advice)
            advice.save()

        # Spending and Contributions
        # TODO: Replace income with function to calculate expected income
        # increase in these two calls to get_decrease_spending_increase_contribution
        # and get_increase_contribution_decrease_spending
        if orig.btc > updated.btc:
            # spending increased, contributions decreased\
            events = EventLog.objects.filter(
                Q(action='RETIRESMARTZ_SPENDING_UP_CONTRIB_DOWN') |
                Q(action='RETIRESMARTZ_SPENDING_DOWN_CONTRIB_UP')
            ).order_by('-timestamp')
            # TODO: calculate nth rate based on retirement age?
            nth_rate = reduce((lambda acc, rate: acc * (1 + rate)), inflation_level[:25], 1)

            if events.count() > 0 and events[0].action == 'RETIRESMARTZ_SPENDING_UP_CONTRIB_DOWN':
                e = Event.RETIRESMARTZ_SPENDING_UP_CONTRIB_DOWN_AGAIN.log(None,
                                                                            orig.btc,
                                                                            updated.btc,
                                                                            user=updated.client.user,
                                                                            obj=updated)
                advice = RetirementAdvice(plan=updated, trigger=e)
                advice.text = advice_responses.get_increase_spending_decrease_contribution_again(advice, orig.btc, orig.btc * nth_rate)
                advice.save()
            else:
                e = Event.RETIRESMARTZ_SPENDING_UP_CONTRIB_DOWN.log(None,
                                                                            orig.btc,
                                                                            updated.btc,
                                                                            user=updated.client.user,
                                                                            obj=updated)
                advice = RetirementAdvice(plan=updated, trigger=e)
                advice.text = advice_responses.get_increase_spending_decrease_contribution(advice, orig.btc, orig.btc * nth_rate)
                advice.save()

        if orig.btc < updated.btc:
            nth_rate = reduce((lambda acc, rate: acc * (1 + rate)), inflation_level[:25], 1)
            e = Event.RETIRESMARTZ_SPENDING_DOWN_CONTRIB_UP.log(None,
                                                                orig.btc,
                                                                updated.btc,
                                                                user=updated.client.user,
                                                                obj=updated)
            advice = RetirementAdvice(plan=updated, trigger=e)
            advice.text = advice_responses.get_increase_contribution_decrease_spending(advice, updated.btc, updated.btc * nth_rate)
            advice.save()

            # contributions increased, spending decreased
            # this one is suppose to trigger if there is a second
            # contribution increase - check if previous event is in current
            # retirementadvice feed
            # e = Event.RETIRESMARTZ_SPENDABLE_INCOME_DOWN_CONTRIB_UP.log(None,
            #                                                             orig.btc,
            #                                                             updated.btc,
            #                                                             user=updated.client.user,
            #                                                             obj=updated)
            # advice = RetirementAdvice(plan=updated, trigger=e)
            # advice.text = advice_responses.get_decrease_spending_increase_contribution(advice)
            # advice.save()

        # Risk Slider Changed
        if updated.desired_risk < orig.desired_risk:
            # protective move
            e = Event.RETIRESMARTZ_PROTECTIVE_MOVE.log(None,
                                                       orig.desired_risk,
                                                       updated.desired_risk,
                                                       user=updated.client.user,
                                                       obj=updated)
            advice = RetirementAdvice(plan=updated, trigger=e)
            advice.text = advice_responses.get_protective_move(advice)
            advice.save()
        elif updated.desired_risk > orig.desired_risk:
            # dynamic move
            e = Event.RETIRESMARTZ_DYNAMIC_MOVE.log(None,
                                                    orig.desired_risk,
                                                    updated.desired_risk,
                                                    user=updated.client.user,
                                                    obj=updated)
            advice = RetirementAdvice(plan=updated, trigger=e)
            advice.text = advice_responses.get_dynamic_move(advice)
            advice.save()

        # age manually adjusted selected_life_expectancy
        if updated.selected_life_expectancy != orig.selected_life_expectancy:
            e = Event.RETIRESMARTZ_RETIREMENT_AGE_ADJUSTED.log(None,
                                                               orig.retirement_age,
                                                               updated.retirement_age,
                                                               user=updated.client.user,
                                                               obj=updated)
            advice = RetirementAdvice(plan=updated, trigger=e)
            advice.text = advice_responses.get_manually_adjusted_age(advice)
            advice.save()

        # Retirement Age Adjusted
        if updated.retirement_age >= 62 and updated.retirement_age <= 70:
            if orig.retirement_age != updated.retirement_age:
                # retirement age changed
                if orig.retirement_age > 62 and updated.retirement_age == 62:
                    # decreased to age 62
                    e = Event.RETIRESMARTZ_RETIREMENT_AGE_ADJUSTED.log(None,
                                                                       orig.retirement_age,
                                                                       updated.retirement_age,
                                                                       user=updated.client.user,
                                                                       obj=updated)
                    advice = RetirementAdvice(plan=updated, trigger=e)
                    advice.text = advice_responses.get_decrease_retirement_age_to_62(advice)
                    advice.save()
                elif orig.retirement_age > 63 and updated.retirement_age == 63:
                    # decreased to age 63
                    e = Event.RETIRESMARTZ_RETIREMENT_AGE_ADJUSTED.log(None,
                                                                       orig.retirement_age,
                                                                       updated.retirement_age,
                                                                       user=updated.client.user,
                                                                       obj=updated)
                    advice = RetirementAdvice(plan=updated, trigger=e)
                    advice.text = advice_responses.get_decrease_retirement_age_to_63(advice)
                    advice.save()
                elif orig.retirement_age > 64 and updated.retirement_age == 64:
                    # decreased to age 64
                    e = Event.RETIRESMARTZ_RETIREMENT_AGE_ADJUSTED.log(None,
                                                                       orig.retirement_age,
                                                                       updated.retirement_age,
                                                                       user=updated.client.user,
                                                                       obj=updated)
                    advice = RetirementAdvice(plan=updated, trigger=e)
                    advice.text = advice_responses.get_decrease_retirement_age_to_64(advice)
                    advice.save()
                elif orig.retirement_age > 65 and updated.retirement_age == 65:
                    # decreased to age 65
                    e = Event.RETIRESMARTZ_RETIREMENT_AGE_ADJUSTED.log(None,
                                                                       orig.retirement_age,
                                                                       updated.retirement_age,
                                                                       user=updated.client.user,
                                                                       obj=updated)
                    advice = RetirementAdvice(plan=updated, trigger=e)
                    advice.text = advice_responses.get_decrease_retirement_age_to_65(advice)
                    advice.save()
                elif orig.retirement_age < 67 and updated.retirement_age == 67:
                    # increased to age 67
                    e = Event.RETIRESMARTZ_RETIREMENT_AGE_ADJUSTED.log(None,
                                                                       orig.retirement_age,
                                                                       updated.retirement_age,
                                                                       user=updated.client.user,
                                                                       obj=updated)
                    advice = RetirementAdvice(plan=updated, trigger=e)
                    advice.text = advice_responses.get_increase_retirement_age_to_67(advice)
                    advice.save()
                elif orig.retirement_age < 68 and updated.retirement_age == 68:
                    # increased to age 68
                    e = Event.RETIRESMARTZ_RETIREMENT_AGE_ADJUSTED.log(None,
                                                                       orig.retirement_age,
                                                                       updated.retirement_age,
                                                                       user=updated.client.user,
                                                                       obj=updated)
                    advice = RetirementAdvice(plan=updated, trigger=e)
                    advice.text = advice_responses.get_increase_retirement_age_to_68(advice)
                    advice.save()
                elif orig.retirement_age < 69 and updated.retirement_age == 69:
                    # increased to age 69
                    e = Event.RETIRESMARTZ_RETIREMENT_AGE_ADJUSTED.log(None,
                                                                       orig.retirement_age,
                                                                       updated.retirement_age,
                                                                       user=updated.client.user,
                                                                       obj=updated)
                    advice = RetirementAdvice(plan=updated, trigger=e)
                    advice.text = advice_responses.get_increase_retirement_age_to_69(advice)
                    advice.save()
                elif orig.retirement_age < 70 and updated.retirement_age == 70:
                    # increased to age 70
                    e = Event.RETIRESMARTZ_RETIREMENT_AGE_ADJUSTED.log(None,
                                                                       orig.retirement_age,
                                                                       updated.retirement_age,
                                                                       user=updated.client.user,
                                                                       obj=updated)
                    advice = RetirementAdvice(plan=updated, trigger=e)
                    advice.text = advice_responses.get_increase_retirement_age_to_70(advice)
                    advice.save()

        if orig.on_track != updated.on_track:
            # user update to goal caused on_track status changed
            if updated.on_track:
                # RetirementPlan now on track
                e = Event.RETIRESMARTZ_ON_TRACK_NOW.log(None,
                                                        user=updated.client.user,
                                                        obj=updated)
                advice = RetirementAdvice(plan=updated, trigger=e)
                advice.text = advice_responses.get_off_track_item_adjusted_to_on_track(advice)
                advice.save()
            else:
                # RetirementPlan now off track

                e = Event.RETIRESMARTZ_OFF_TRACK_NOW.log(None,
                                                         user=updated.client.user,
                                                         obj=updated)
                advice = RetirementAdvice(plan=updated, trigger=e)
                advice.text = advice_responses.get_on_track_item_adjusted_to_off_track(advice)
                advice.save()

        return Response(self.serializer_response_class(updated).data)

    @detail_route(methods=['get'], url_path='suggested-retirement-income')
    def suggested_retirement_income(self, request, parent_lookup_client, pk, format=None):
        """
        Calculates a suggested retirement income based on the client's
        retirement plan and personal profile.
        """
        # TODO: Make this work
        return Response(1234)

    @detail_route(methods=['get'], url_path='calculate-contributions')
    def calculate_contributions(self, request, parent_lookup_client, pk, format=None):
        """
        Calculates suggested contributions (value for the amount in the
        btc and atc) that will generate the desired retirement income.
        """
        # TODO: Make this work
        return Response({'btc_amount': 1111, 'atc_amount': 0})

    @detail_route(methods=['get'], url_path='calculate-income')
    def calculate_income(self, request, parent_lookup_client, pk, format=None):
        """
        Calculates retirement income possible given the current contributions
        and other details on the retirement plan.
        """
        # TODO: Make this work
        return Response(2345)

    @detail_route(methods=['get'], url_path='calculate-balance-income')
    def calculate_balance_income(self, request, parent_lookup_client, pk, format=None):
        """
        Calculates the retirement balance required to provide the
        desired_income as specified in the plan.
        """
        # TODO: Make this work
        return Response(5555555)

    @detail_route(methods=['get'], url_path='calculate-income-balance')
    def calculate_income_balance(self, request, parent_lookup_client, pk, format=None):
        """
        Calculates the retirement income possible with a suppli
ed
        retirement balance and other details on the retirement plan.
        """
        # TODO: Make this work
        return Response(1357)

    @detail_route(methods=['get'], url_path='calculate-balance-contributions')
    def calculate_balance_contributions(self, request, parent_lookup_client, pk, format=None):
        """
        Calculates the retirement balance generated from the contributions.
        """
        # TODO: Make this work
        return Response(6666666)

    @detail_route(methods=['get'], url_path='calculate-contributions-balance')
    def calculate_contributions_balance(self, request, parent_lookup_client, pk, format=None):
        """
        Calculates the contributions r
equired to generate the
        given retirement balance.
        """
        # TODO: Make this work
        return Response({'btc_amount': 2222, 'atc_amount': 88})

    @detail_route(methods=['get'], url_path='calculate-demo')
    def calculate_demo(self, request, parent_lookup_client, pk, format=None):
        """
        Calculate the single projection values for the
        current retirement plan settings.
        {
          "portfolio": [
            # list of [fund id, weight as percent]. There will be max 33 of these. Likely 5-10
            [1, 5],
            [53, 12],
            ...
          ],
          "projection": [
            # this is the asset and cash-flow projection. It is a list of [date, assets, income]. There will be at most 50 of these. (21 bytes each)
            [143356, 120000, 2000],
            [143456, 119000, 2004],
            ...
          ]
        }
        "portfolio": 10% each for the first 10 tickers in the systems
        that aren't Closed.
        "projection": 50 time points evenly spaced along the
        remaining time until expected end of life.  Each time
        point with assets starting at 100000,
        going up by 1000 every point, income starting
        at 200000, increasing by 50 every point.
        """

        retirement_plan = self.get_object()
        tickers = Ticker.objects.filter(~Q(state=Ticker.State.CLOSED.value))
        portfolio = []
        projection = []
        for idx, ticker in enumerate(tickers[:10]):
            percent = 0
            if idx <= 9:
                # 10% each for first 10 tickers
                percent = 10
            portfolio.append([ticker.id, percent])
        # grab 50 evenly spaced time points between dob and current time
        today = timezone.now().date()
        last_day = retirement_plan.client.date_of_birth + relativedelta(years=retirement_plan.selected_life_expectancy)
        day_interval = (last_day - today) / 49
        income_start = 20000
        assets_start = 100000
        for i in range(50):
            income = income_start + (i * 50)
            assets = assets_start + (i * 1000)
            dt = today + i * day_interval
            projection.append([d2ed(dt), assets, income])
        return Response({'portfolio': portfolio, 'projection': projection})

    @detail_route(methods=['get'], url_path='calculate')
    def calculate(self, request, parent_lookup_client, pk, format=None):
        """
        Calculate the single projection values for the current retirement plan.
        {
          "portfolio": [
            # list of [fund id, weight as percent]. There will be max 20 of these. Likely 5-10
            [1, 5],
            [53, 12],
            ...
          ],
          "projection": [
            # this is the asset and cash-flow projection. It is a list of [date, assets, income]. There will be at most 50 of these. (21 bytes each)
            [43356, 120000, 2000],
            [43456, 119000, 2004],
            ...
          ]
        }
        """
        plan = self.get_object()

        # We need a date of birth for the client
        if not plan.client.date_of_birth:
            raise ValidationError("Client must have a date of birth entered to calculate retirement plans.")

        # TODO: We can cache the portfolio on the plan and only update it every 24hrs, or if the risk changes.
        try:
            settings = create_settings(plan)
        except Unsatisfiable as e:
            rdata = {'reason': "No portfolio could be found: {}".format(e)}
            if e.req_funds is not None:
                rdata['req_funds'] = e.req_funds
            return Response({'error': rdata}, status=status.HTTP_400_BAD_REQUEST)

        plan.set_settings(settings)
        plan.save()

        # Get the z-multiplier for the given confidence
        z_mult = -st.norm.ppf(plan.expected_return_confidence)
        performance = (settings.portfolio.er + z_mult * settings.portfolio.stdev)/100
        
        # Get projection of future income and assets for US tax payer
        house_value = 0.
        adj_gross_income = 100000.
        taxable_income = 0.
        total_payments = 18219.
        after_tax_income = 110982.
        ss_fra_todays = 3311.
        ss_fra_retirement = 9773.
        paid_days = 1
        ira_rmd_factor = 26.5
        contrib_rate_employer_401k = 0.02
        contrib_rate_employee_401k = 0.0
        initial_401k_balance = 0.
        
        if plan.client.residential_address.post_code is None:
            raise Exception("plan.client.residential_address.post_code is None")

        state = zip2state.get_state(int(plan.client.residential_address.post_code))
        user = tax.TaxUser(plan.client,
                        plan.client.regional_data['ssn'],
                        pd.Timestamp(plan.client.date_of_birth),
                        plan.retirement_age,
                        plan.client.life_expectancy,
                        plan.lifestyle,
                        plan.reverse_mortgage,
                        house_value,
                        plan.desired_risk,
                        plan.client.civil_status,
                        plan.client.income,
                        adj_gross_income,
                        taxable_income,
                        total_payments,
                        after_tax_income,
                        plan.income_growth,
                        plan.client.employment_status,
                        ss_fra_todays,
                        ss_fra_retirement,
                        paid_days,
                        contrib_rate_employer_401k,
                        contrib_rate_employee_401k,
                        initial_401k_balance,
                        ira_rmd_factor,
                        state)

        user.create_maindf()
        
        print(" ************************************************************** ")
        print("plan.client.civil_status = " + str(plan.client.civil_status))
        print(" ************************************************************** ")
        if plan.client.civil_status == 1 or plan.client.civil_status == -1:
            print(" ************************************************************** ")
            print("partner: " + str(plan.client))
            print(" ************************************************************** ")
            partner = tax.TaxUser(plan.client,
                            plan.client.regional_data['ssn'],
                            pd.Timestamp(plan.partner_data.dob),
                            plan.partner_data.retirement_age,
                            plan.partner_data.life_expectancy,
                            plan.lifestyle,
                            plan.reverse_mortgage,
                            house_value,
                            plan.desired_risk,
                            plan.client.civil_status,
                            plan.partner_data.income,
                            adj_gross_income,
                            taxable_income,
                            total_payments,
                            after_tax_income,
                            plan.income_growth,
                            plan.client.employment_status,
                            ss_fra_todays,
                            ss_fra_retirement,
                            paid_days,
                            contrib_rate_employer_401k,
                            contrib_rate_employee_401k,
                            initial_401k_balance,
                            ira_rmd_factor,
                            state)

            partner.create_maindf()
       

        # Convert these returned values to a format for the API        
        if plan.client.civil_status == 1 or plan.client.civil_status == 2:
            print(" ************************************************************** ")
            print("if plan.client.civil_status == abstract.PersonalData.CivilStatus['MARRIED_FILING_SEPARATELY_LIVED_TOGETHER'] or plan.client.civil_status == abstract.PersonalData.CivilStatus['MARRIED_FILING_JOINTLY']:")
            print(" ************************************************************** ")
            user.maindf['Joint_Taxable_Accounts'] = user.maindf['Taxable_Accounts'] + partner.maindf['Taxable_Accounts']
            user.maindf['Joint_Actual_Inc'] = user.maindf['Actual_Inc'] + partner.maindf['Actual_Inc']
            user.maindf['Joint_Desired_Inc'] = user.maindf['Desired_Inc'] + partner.maindf['Desired_Inc']
            catd = pd.concat([user.maindf['Joint_Taxable_Accounts'], user.maindf['Joint_Actual_Inc'], user.maindf['Joint_Desired_Inc']], axis=1)

        else:
            print(" ************************************************************** ")
            print("else")
            print(" ************************************************************** ")
            catd = pd.concat([user.maindf['Taxable_Accounts'], user.maindf['Actual_Inc'], user.maindf['Desired_Inc']], axis=1)

        locs = np.linspace(0, len(catd)-1, num=50, dtype=int)
        proj_data = [(d2ed(d), a, i, desired) for d, a, i, desired in catd.iloc[locs, :].itertuples()]
        pser = PortfolioSerializer(instance=settings.portfolio)
        
        return Response({'portfolio': pser.data, 'projection': proj_data})


class RetiresmartzAdviceViewSet(ApiViewMixin, NestedViewSetMixin, ModelViewSet):
    model = RetirementPlan
    permission_classes = (IsAuthenticated,)
    queryset = RetirementAdvice.objects.filter(read=None).order_by('-dt')  # unread advice
    serializer_class = serializers.RetirementAdviceReadSerializer
    serializer_response_class = serializers.RetirementAdviceReadSerializer

    def get_queryset(self):
        """
        The nested viewset takes care of only returning results for the client we are looking at.
        We need to add logic to only allow access to users that can view the plan.
        """
        qs = super(RetiresmartzAdviceViewSet, self).get_queryset()
        # Check user object permissions
        user = SupportRequest.target_user(self.request)
        return qs.filter_by_user(user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.RetirementAdviceReadSerializer
        elif self.request.method == 'PUT':
            return serializers.RetirementAdviceWritableSerializer
