import csv
import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db.models import F, Q, Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from functools import reduce
from operator import itemgetter

from client.models import Client, IBOnboard
from main.constants import (INVITATION_ADVISOR, INVITATION_SUPERVISOR, INVITATION_TYPE_DICT,
                            EMPLOYMENT_STATUS_EMMPLOYED, EMPLOYMENT_STATUS_SELF_EMPLOYED)
from main.forms import BetaSmartzGenericUserSignupForm, EmailInvitationForm
from main.models import Advisor, EmailInvitation, Goal, GoalMetric, GoalType, \
    PositionLot, Supervisor, Ticker, Transaction, User
from main.views.base import LegalView
from django.core.urlresolvers import reverse
from main.views.firm.forms import PricingPlanAdvisorFormset, \
    PricingPlanClientFormset, PricingPlanForm, FirmApplicationClientForm, FirmApplicationIBOnboardFormSet
from notifications.models import Notification, Notify
from support.models import SupportRequest
from .filters import FirmActivityFilterSet, FirmAnalyticsAdvisorsFilterSet, \
    FirmAnalyticsClientsFilterSet, FirmAnalyticsGoalsAdvisorsFilterSet, \
    FirmAnalyticsGoalsClientsFilterSet, FirmAnalyticsGoalsUsersFilterSet, \
    FirmAnalyticsOverviewFilterSet, FirmApplicationsClientsFilterSet
from retiresmartz.models import RetirementPlan
logger = logging.getLogger('main.views.firm.dashboard')


class FirmSupervisorDelete(DeleteView, LegalView):
    template_name = "firm/supervisors-delete.html"
    success_url = '/firm/supervisors' # reverse_lazy('firm:supervisors-delete')
    model = User

    def get_success_url(self):
        messages.success(self.request, "supervisor delete successfully")
        return super(FirmSupervisorDelete, self).get_success_url()


class SupervisorProfile(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ('can_write',)


class SupervisorUserForm(BetaSmartzGenericUserSignupForm):
    user_profile_type = "supervisor"
    firm = None
    betasmartz_agreement = forms.BooleanField(initial=True, widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'middle_name', 'last_name', 'password', 'confirm_password')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(SupervisorUserForm, self).__init__(*args, **kwargs)
        profile_kwargs = kwargs.copy()
        if 'instance' in kwargs:
            self.profile = getattr(kwargs['instance'], self.user_profile_type, None)
            profile_kwargs['instance'] = self.profile
        self.profile_form = SupervisorProfile(*args, **profile_kwargs)
        self.fields.update(self.profile_form.fields)
        self.initial.update(self.profile_form.initial)

    def save(self, *args, **kw):
        user = super(SupervisorUserForm, self).save(*args, **kw)
        self.profile = self.profile_form.save(commit=False)
        self.profile.user = user
        self.profile.firm = self.firm
        self.profile.save()
        return user


class SupervisorUserFormEdit(forms.ModelForm):
    user_profile_type = "supervisor"
    firm = None
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput(), required=False)
    new_password = None

    class Meta:
        model = User
        fields = ('email', 'first_name', 'middle_name', 'last_name')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(SupervisorUserFormEdit, self).__init__(*args, **kwargs)
        profile_kwargs = kwargs.copy()
        if 'instance' in kwargs:
            self.profile = getattr(kwargs['instance'], self.user_profile_type, None)
            profile_kwargs['instance'] = self.profile
        self.profile_form = SupervisorProfile(*args, **profile_kwargs)
        self.fields.update(self.profile_form.fields)
        self.initial.update(self.profile_form.initial)

    def clean(self):
        cleaned_data = super(SupervisorUserFormEdit, self).clean()

        password1 = cleaned_data.pop('password')
        password2 = cleaned_data.pop('confirm_password')

        if password1:
            if password1 != password2:
                self._errors['confirm_password'] = mark_safe(
                    '<ul class="errorlist"><li>Passwords don\'t match.</li></ul>')
            else:
                self.new_password = make_password(password1)

        return cleaned_data

    def save(self, *args, **kw):
        user = super(SupervisorUserFormEdit, self).save(*args, **kw)
        if self.new_password is not None:
            user.password = self.new_password
            user.save()
        self.profile = self.profile_form.save()
        return user


class FirmSupervisorsCreate(CreateView, LegalView):
    template_name = "firm/supervisors-edit.html"
    form_class = SupervisorUserForm
    success_url = "/firm/supervisors"

    def get_success_url(self):
        user = self.object
        logger.error(user)
        Notify.CREATE_SUPERVISOR.send(
            actor=self.firm,
            target=user,
            recipient=self.request.user,
            description='Can write' if user.supervisor.can_write else 'Read only'
        )
        messages.success(self.request, "New supervisor created successfully")
        return super(FirmSupervisorsCreate, self).get_success_url()

    def get_form(self, form_class=None):
        form = super(FirmSupervisorsCreate, self).get_form(form_class)
        form.firm = self.firm
        return form


class FirmSupervisorsEdit(UpdateView, LegalView):
    template_name = "firm/supervisors-edit.html"
    form_class = SupervisorUserFormEdit
    success_url = "/firm/supervisors"
    model = User

    def get_success_url(self):
        messages.success(self.request, "Supervisor edited successfully")
        return super(FirmSupervisorsEdit, self).get_success_url()

    def get_form(self, form_class=None):
        form = super(FirmSupervisorsEdit, self).get_form(form_class)
        form.firm = self.firm
        return form


class FirmSupervisors(TemplateView, LegalView):
    template_name = "firm/supervisors.html"

    def get_context_data(self, **kwargs):
        ctx = super(FirmSupervisors, self).get_context_data(**kwargs)
        ctx.update({
            "supervisors": self.firm.supervisors.all(),
            "firm": self.firm,
        })
        return ctx


# OBSOLETED
#class FirmAgreements(TemplateView, LegalView):
#    template_name = "commons/agreements.html"
#
#    def __init__(self, *args, **kwargs):
#        super(FirmAgreements, self).__init__(*args, **kwargs)
#        self.search = ""
#
#    def get(self, request, *args, **kwargs):
#        self.search = request.GET.get("search", self.search)
#        return super(FirmAgreements, self).get(request, *args, **kwargs)
#
#    @property
#    def clients(self):
#        clients = Client.objects.filter(advisor__firm=self.firm, is_confirmed=True, user__prepopulated=False)
#
#        if self.search:
#            sq = Q(user__first_name__icontains=self.search)
#            clients = clients.filter(sq)
#        return clients.all()
#
#    def get_context_data(self, **kwargs):
#        ctx = super(FirmAgreements, self).get_context_data(**kwargs)
#        ctx.update({
#            "clients": self.clients,
#            "search": self.search,
#            "firm": self.firm,
#        })
#        return ctx


class FirmAnalyticsMixin(object):
    """
    @self.firm: current firm to filter by (maybe good to rename it)
    @self.advisor: current advisor to filter by (maybe good to rename it)
    @self.filter: django_filter object (with filter params)
    """
    AGE_STEP = 5
    AGE_RANGE = range(20, 70, AGE_STEP)
    SECONDS_PER_YEAR = 365.25 * 24 * 3600

    def get_queryset_clients(self):
        if not hasattr(self, '_queryset_clients'):
            qs = Client.objects.all()

            if hasattr(self, 'firm'):
                qs = qs.filter_by_firm(self.firm)

            if hasattr(self, 'advisor_filter'):
                advisors = self.advisor_filter.qs
                if self.advisor_filter.data.get('advisor'):
                    if advisors.count() > 0:
                        qs = qs.filter_by_advisors(advisors)
                    else:
                        qs = Client.objects.none()

            if hasattr(self, 'client_filter'):
                clients = self.client_filter.qs
                if self.client_filter.data.get('client'):
                    clients_pk = [c.pk for c in clients]
                    qs = qs.filter(pk__in=clients_pk)

            if hasattr(self, 'filter'):
                data = self.filter.data
                risk = None
                if 'risk' in data.keys():
                    risk = data.getlist('risk')
                if risk:
                    qs = qs.filter_by_risk_level(risk)

                worth = data.get('worth')
                if worth:
                    qs = qs.filter_by_worth(worth)

            self._queryset_clients = qs

        return self._queryset_clients

    def get_queryset_goals(self):
        if not hasattr(self, '_queryset_goals'):
            qs = Goal.objects.all()
            # .filter(selected_settings__target__gt=0) # ignore "unset" goals

            if hasattr(self, 'firm'):
                qs = qs.filter_by_firm(self.firm)

            if hasattr(self, 'advisor_filter'):
                # check for advisor/s since some advisors might share names etc.
                advisors = self.advisor_filter.qs
                if self.advisor_filter.data.get('advisor'):
                    qs = qs.filter_by_advisors(advisors)

            if hasattr(self, 'client_filter'):
                clients = self.client_filter.qs
                if self.client_filter.data.get('client'):
                    qs = qs.filter_by_clients(clients)

            if hasattr(self, 'users_filter'):
                users = self.users_filter.qs
                user_ids = self.users_filter.data.get('users')
                if user_ids:
                    ids_list = list(map(int, user_ids.split(',')))
                    advisors = Advisor.objects.filter(Q(user_id__in=ids_list))
                    if advisors:
                        qs = qs.filter_by_advisors(advisors)
                    clients = Client.objects.filter(Q(user_id__in=ids_list))
                    if clients:
                        qs = qs.filter_by_clients(clients)

            if hasattr(self, 'filter'):
                data = self.filter.data
                risk = None
                if 'risk' in data.keys():
                    risk = data.getlist('risk')

                if risk:
                    qs = qs.filter_by_risk_level(risk)

                worth = data.get('worth')
                if worth:
                    qs = qs.filter_by_worth(worth)

            self._queryset_goals = qs

        return self._queryset_goals

    def get_queryset_goals_filterless(self):
        if not hasattr(self, '_queryset_goals_filterless'):
            qs = Goal.objects.all()
            # .filter(selected_settings__target__gt=0) # ignore "unset" goals

            if hasattr(self, 'firm'):
                qs = qs.filter_by_firm(self.firm)

            if hasattr(self, 'filter'):
                # data = self.filter.data
                pass

            self._queryset_goals_filterless = qs

        return self._queryset_goals_filterless

    def get_queryset_positions(self):
        if not hasattr(self, '_queryset_positions'):
            qs = PositionLot.objects.filter(execution_distribution__execution__asset__state=Ticker.State.ACTIVE.value)

            if hasattr(self, 'firm'):
                qs = qs.filter_by_firm(self.firm)

            if hasattr(self, 'advisor_filter'):
                advisors = self.advisor_filter.qs
                if self.advisor_filter.data.get('advisor'):
                    if advisors.count() > 0:
                        qs = qs.filter_by_advisors(advisors)
                    else:
                        qs = PositionLot.objects.none()

            if hasattr(self, 'client_filter'):
                clients = self.client_filter.qs
                if self.client_filter.data.get('client'):
                    qs = qs.filter_by_clients(clients)

            if hasattr(self, 'filter'):
                data = self.filter.data
                risk = None
                if 'risk' in data.keys():
                    risk = data.getlist('risk')
                if risk:
                    qs = qs.filter_by_risk_level(risk)

                worth = data.get('worth')
                if worth:
                    qs = qs.filter_by_worth(worth)

            self._queryset_positions = qs

        return self._queryset_positions

    def get_context_worth(self):
        """
        Les:
        Net worth is sum of Goal.total_balance per client
        where they are the primary account holder, age is age of primary account holder.
        Net worth also sums the value of the client's external assets.  Value for assets
        is determine by the external assets' growth from valuation date.

        Cash flow is a monthly net Transactions in and out of the goals
        for each primary account holder. Ignore incoming dividend type transactions,
        and outgoing fee type transactions. monthly net transactions:
        monthly average for the last year if available, otherwise, whatever's available.
        age: should be “round” to 1 year

        Savva:
        transactions: monthly net transactions for the last month
        """
        qs_goals = self.get_queryset_goals()
        clients = self.get_queryset_clients()
        data = []
        current_date = datetime.now().today()
        if qs_goals and clients:
            for age in self.AGE_RANGE:
                # client.net_worth will return a clients estimated net_worth here
                # client.net_worth takes into account external assets
                # we are graphing average clients' net_worth by age
                value_worth = 0.0
                range_dates = map(lambda x: current_date - relativedelta(years=x),
                                  [age + self.AGE_STEP, age])  # yes, max goes first

                clients_by_age = clients.filter(date_of_birth__range=range_dates)
                for client in clients_by_age:
                    value_worth += client.net_worth
                if clients_by_age.count() > 0:
                    value_worth = value_worth / clients_by_age.count()

                # for every goal for clients in this age range,
                # we're going to add the transaction
                # amount to the total_cashflow, then divide
                # the total by the number of unique clients
                # to get the average cashflow for clients of this age
                total_cashflow = 0.0
                average_client_cashflow = 0.0
                cashflow_goals = qs_goals.filter_by_client_age(age, age + self.AGE_STEP)
                number_of_clients = len(set([goal.account.primary_owner for goal in cashflow_goals]))
                for goal in cashflow_goals:
                    txs = Transaction.objects.filter(Q(to_goal=goal) | Q(from_goal=goal),
                                                 status=Transaction.STATUS_EXECUTED,
                                                 reason__in=Transaction.CASH_FLOW_REASONS) \
                                                .filter(executed__gt=timezone.now()- relativedelta(years=1))
                    # subtract from_goal amounts and add to_goal amounts
                    for tx in txs:
                        if tx.from_goal:
                            total_cashflow -= tx.amount
                        elif tx.to_goal:
                            total_cashflow += tx.amount

                if number_of_clients > 0:
                    average_client_cashflow = total_cashflow / number_of_clients

                data.append({
                    'value_worth': value_worth,
                    'value_cashflow': average_client_cashflow,
                    'age': age + self.AGE_STEP / 2,
                })

        return data

    def get_context_events(self):
        """
        x axis - max(age at Goal.selected_settings.completion, current age)
        y axis - max(Goal.total_balance, Goal.selected_settings.target)
        """
        qs_goals = self.get_queryset_goals()

        data = []
        goal_types = GoalType.objects.all()
        today = datetime.today()
        for goal_type in goal_types:
            total_max_age = 0
            total_max_value = 0
            for goal in qs_goals.filter(type=goal_type):
                # client age at goal creation
                client = goal.account.primary_owner
                client_age = relativedelta(today, client.date_of_birth).years
                # expected age of completion based on completion date field
                if goal.selected_settings:
                    completion_age = relativedelta(goal.selected_settings.completion, client.date_of_birth).years
                else:
                    completion_age = 0
                max_age = max(completion_age, client_age)

                if goal.selected_settings:
                    target_balance = goal.selected_settings.target
                else:
                    target_balance = 0
                max_value = max(goal.total_balance, target_balance)
                total_max_age = max(total_max_age, max_age)
                total_max_value = max(total_max_value, max_value)

            if total_max_value > 0 and total_max_age > 0:
                data.append({
                    'category': goal_type.name,  # maybe we should pass id also
                    'value': total_max_value,
                    'age': total_max_age,
                })
        return data

    def get_context_positions(self):
        qs_positions = self.get_queryset_positions()

        positions_by_asset_class = qs_positions \
            .annotate(
                asset_class=F('execution_distribution__execution__asset__asset_class'),
                name=F('execution_distribution__execution__asset__asset_class__display_name'),
                color=F('execution_distribution__execution__asset__asset_class__primary_color'),
            ) \
            .values('asset_class', 'name', 'color') \
            .annotate(value=Coalesce(Sum(F('quantity') * F('execution_distribution__execution__asset__unit_price')), 0))

        positions_by_region = qs_positions \
            .annotate(
                region=F('execution_distribution__execution__asset__region'),
                name=F('execution_distribution__execution__asset__region__name')
            ) \
            .values('region', 'name') \
            .annotate(value=Coalesce(Sum(F('quantity') * F('execution_distribution__execution__asset__unit_price')), 0))

        positions_by_investment_type = qs_positions \
            .annotate(
                name=F('execution_distribution__execution__asset__asset_class__investment_type__name'),
            ) \
            .values('name') \
            .annotate(value=Coalesce(Sum(F('quantity') * F('execution_distribution__execution__asset__unit_price')), 0))

        positions_by_allocation = qs_positions \
            .annotate(
                name=F('execution_distribution__execution__asset__asset_class__portfolio_sets__name'),
            ).values('name') \
            .annotate(value=Coalesce(Sum(F('quantity') * F('execution_distribution__execution__asset__unit_price')), 0))

        data = {
            'asset_class': positions_by_asset_class,
            'region': positions_by_region,
            'investment_type': positions_by_investment_type,
            'allocation': positions_by_allocation,
        }
        return data


class FirmAnalyticsOverviewView(FirmAnalyticsMixin, TemplateView, LegalView):
    template_name = "firm/analytics.html"

    def get_context_data(self, **kwargs):
        user = SupportRequest.target_user(self.request)
        self.firm  = user.authorised_representative.firm
        self.filter = FirmAnalyticsOverviewFilterSet(self.request.GET)
        self.advisor_filter = FirmAnalyticsGoalsAdvisorsFilterSet(self.request.GET)
        self.client_filter = FirmAnalyticsGoalsClientsFilterSet(self.request.GET)
        self.users_filter = FirmAnalyticsGoalsUsersFilterSet(self.request.GET)
        positions = self.get_context_positions()
        risks = self.get_context_risks()
        worth = self.get_context_worth()
        events = self.get_context_events()
        empty_worth = len(worth) == 0
        empty_segments = len(positions) == 0 or empty_worth
        empty_events = len(events) == 0 or empty_worth
        return {
            'empty_worth': empty_worth,
            'empty_segments': empty_segments,
            'empty_events': empty_events,
            'filter': self.filter,
            'advisor_filter': self.advisor_filter,
            'client_filter': self.client_filter,
            'users_filter': self.users_filter,
            'filtered_users_json': self.get_context_users,
            'risks': risks,
            'worth': worth,
            'events': events,
            'positions': positions,
        }

    def get_context_risks(self):
        """
        Les:
        Risk stat cards get their values from the GoalMetric model.
        The risk score is the GoalMetric.configured_val when
        GoalMetric.metric_type == GoalMetric.METRIC_TYPE_RISK_SCORE.

        Get the metrics for a goal from
        Goal.selected_settings__metric_group__metrics

        There will only be one metric of type METRIC_TYPE_RISK_SCORE in each group.
        """
        qs_goals = self.get_queryset_goals_filterless()

        data = []
        for risk_level_tuple in GoalMetric.RISK_LEVELS:

            value = qs_goals \
                .filter_by_risk_level(risk_level_tuple[0]) \
                .values('account__primary_owner__id') \
                .annotate(positions_sum=Coalesce(Sum(
                    F('transactions_to__execution_distribution__position_lot__quantity') * F('transactions_to__execution_distribution__execution__asset__unit_price')
                ), 0)) \
                .aggregate(
                    positions=Coalesce(Sum('positions_sum'), 0),
                    cash=Coalesce(Sum('cash_balance'), 0),
                )

            data.append({
                'level': risk_level_tuple[0],
                'name': risk_level_tuple[1],
                'value': value['positions'] + value['cash'],
            })

        # calculate percentages manually, brrr
        data_value_sum = reduce(lambda sum, item: sum + item['value'], data, 0)
        for item in data:
            item['value_percent'] = (item['value'] / data_value_sum
                if data_value_sum else 0)

        return data

    def get_context_users(self):
        users = self.users_filter.qs
        data = []
        if self.users_filter.data.get('users'):
            for user in users:
                data.append({
                    'id': user.pk,
                    'name': user.full_name,
                    'role': user.role
                })
        return data

class FirmAnalyticsOverviewMetricView(FirmAnalyticsMixin, TemplateView, LegalView):
    template_name = "firm/partials/modal-analytics-metric-content.html"

    def get_context_data(self, **kwargs):
        user = SupportRequest.target_user(self.request)
        self.firm  = user.authorised_representative.firm
        self.filter = FirmAnalyticsOverviewFilterSet(self.request.GET)

        return {
            'risk': self.get_context_risk(),
            'clients': self.get_context_clients(),
            #'positions': self.get_context_positions(),
        }

    def get_context_risk(self):
        param = int(self.filter.data.get('risk', 0))
        risk = dict(GoalMetric.RISK_LEVELS)[param]
        return risk

    def get_context_clients(self):
        qs = self.get_queryset_clients()

        data = qs \
            .order_by('user__last_name') \

        # TODO: add custom annotaion to fetch Goal type names (!!!)
        # the current solution is very temporal and really slow

        return data


class FirmAnalyticsAdvisorsView(ListView, LegalView):
    template_name = "firm/analytics-advisors.html"
    model = Advisor

    # TODO: do we weed that filter at all?
    def get_context_data(self, **kwargs):
        qs = self.get_queryset()
        f = FirmAnalyticsAdvisorsFilterSet(self.request.GET, queryset=qs)

        return {
            'filter': f,
        }


class FirmAnalyticsAdvisorsDetailView(FirmAnalyticsMixin, DetailView, LegalView):
    template_name = "firm/partials/modal-analytics-advisor-content.html"
    model = Advisor

    def get_context_data(self, **kwargs):
        context = super(FirmAnalyticsAdvisorsDetailView, self).get_context_data(**kwargs)

        self.advisor = self.object

        context.update(
            worth=self.get_context_worth(),
            events=self.get_context_events(),
            positions=self.get_context_positions(),
        )

        return context


class FirmAnalyticsClientsView(ListView, LegalView):
    template_name = "firm/analytics-clients.html"
    model = Client

    # TODO: do we weed that filter at all?
    def get_context_data(self, **kwargs):
        qs = self.get_queryset()
        f = FirmAnalyticsClientsFilterSet(self.request.GET, queryset=qs)

        return {
            'filter': f,
        }


class FirmAnalyticsClientsDetailView(FirmAnalyticsMixin, DetailView, LegalView):
    template_name = "firm/partials/modal-analytics-client-content.html"
    model = Client

    def get_context_data(self, **kwargs):
        context = super(FirmAnalyticsClientsDetailView, self).get_context_data(**kwargs)

        self.client = self.object

        context.update(
            worth=self.get_context_worth(),
            events=self.get_context_events(),
            positions=self.get_context_positions(),
        )

        return context


class FirmActivityView(ListView, LegalView):
    template_name = "firm/activity.html"
    model = Notification

    def get_context_data(self, **kwargs):
        qs = self.get_queryset().order_by('-timestamp')
        f = FirmActivityFilterSet(self.request.GET, queryset=qs)
        return {
            'filter': f,
            'retirement_plan_class_name': RetirementPlan.__name__
        }

    def post(self, request):
        self.request = request
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="firm-activity-%s.csv"' % now().strftime('%Y%m%d-%H%M%S')

        writer = csv.writer(response)
        writer.writerow(['Who', 'Did', 'What', 'When', 'Comment'])

        data = self.get_context_data()
        for item in iter(data['filter']):  # type: Notification
            writer.writerow([
                item.actor,
                item.verb,
                '%s / %s' % (item.target or '-', item.action_object or '-'),
                item.timestamp.strftime('%d-%b-%Y %H:%M'),
                item.description,
            ])
        return response


class FirmApplicationView(ListView, LegalView):
    template_name = "firm/application.html"
    model = Client

    def get_context_data(self, **kwargs):
        qs = self.get_queryset().order_by('user__first_name').order_by('user__last_name')
        f = FirmApplicationsClientsFilterSet(self.request.GET, queryset=qs)
        return {
            'filter': f
        }


class FirmApplicationDetailView(UpdateView, LegalView):
    template_name = "firm/application-details.html"
    form_class = FirmApplicationClientForm
    model = Client

    def get_success_url(self):
        messages.success(self.request, "Client Information Updated successfully")
        return reverse('firm:application')

    def get_context_data(self, **kwargs):
        context = super(FirmApplicationDetailView, self).get_context_data(**kwargs)
        context['employed_statuses'] = [
            EMPLOYMENT_STATUS_EMMPLOYED,
            EMPLOYMENT_STATUS_SELF_EMPLOYED
        ]
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        ib_formset = FirmApplicationIBOnboardFormSet(instance=self.object)
        return self.render_to_response(self.get_context_data(form=self.get_form(), ib_formset=ib_formset))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        ib_formset = FirmApplicationIBOnboardFormSet(self.request.POST, instance=self.object)
        if form.is_valid() and ib_formset.is_valid():
            return self.form_valid(form, ib_formset)
        else:
            return self.form_invalid(form, ib_formset)

    def form_valid(self, form, ib_formset):
        self.object = form.save()
        ib_formset.instance = self.object
        ib_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ib_formset):
        return self.render_to_response(self.get_context_data(form=form, ib_formset=ib_formset))


class FirmApplicationSendEmailView(TemplateView, LegalView):
    def redirect_url(self):
        return reverse('firm:application-detail', kwargs={'pk': self.kwargs['pk']})

    def redirect_success(self):
        messages.success(self.request, "Email sent successfully")
        return HttpResponseRedirect(self.redirect_url())

    def redirect_fail(self, message):
        messages.error(self.request, message)
        return HttpResponseRedirect(self.redirect_url())

    def get_csv_content(self, client):
        try:
            ib_onboard = client.ib_onboard
        except:
            ib_onboard = None

        context = {
            'client': client,
            'ib_onboard': ib_onboard,
            'user': client.user
        }
        return render_to_string('email/firm_client_application/csv.txt', context)

    def get(self, request, *args, **kwargs):
        redirect_url = reverse('firm:application-detail', kwargs={'pk': self.kwargs['pk']})
        return HttpResponseRedirect(redirect_url)

    def post(self, request, *args, **kwargs):
        email_to = request.POST.get('email_to', '')
        if email_to in ['advisor', 'client']:
            client = Client.objects.get(pk=kwargs['pk'])
            advisor = client.advisor
            context = {
                'advisor': advisor,
                'client': client,
                'firm': client.firm
            }

            if email_to == 'advisor':
                subject = 'Your Client\'s BetaSmartz Account Information'
                html_content = render_to_string('email/firm_client_application/to_advisor.html', context)
                recipient = advisor.user.email
            else:
                subject = 'Your BetaSmartz Account Information'
                html_content = render_to_string('email/firm_client_application/to_client.html', context)
                recipient = client.user.email
            csv_content = self.get_csv_content(client)
            email = EmailMessage(subject, html_content, None, [recipient])
            email.content_subtype = "html"
            email.attach('Client Data - {}.csv'.format(client.name), csv_content, 'text/csv')
            email.send()
            return self.redirect_success()
        else:
            return self.redirect_fail('Please choose advisor/client')


class FirmSupportPricingView(TemplateView, LegalView):
    template_name = "firm/support-pricing.html"

    def _get_person_formset(self, formset_class, prefix, can_add, data=None):
        formset = formset_class(
            data=data,
            prefix=prefix,
            queryset=formset_class.model.objects.filter(parent__firm=self.firm,
                                                        person__isnull=False)
        )
        formset.extra = can_add and 1 or 0
        formset.firm = self.firm

        return formset

    def get_advisor_formset(self, data=None):
        return self._get_person_formset(
            data=data,
            formset_class=PricingPlanAdvisorFormset,
            prefix='advisor',
            can_add=Advisor.objects.filter(firm=self.firm,
                                           pricing_plan__isnull=True)
        )

    def get_client_formset(self, data=None):
        return self._get_person_formset(
            data=data,
            formset_class=PricingPlanClientFormset,
            prefix='client',
            can_add=Client.objects.filter(advisor__firm=self.firm,
                                          pricing_plan__isnull=True)
        )

    def _get_firm_form(self, data=None, instance=None):
        return PricingPlanForm(prefix='firm', data=data, instance=instance)

    def get_context_data(self, **kwargs):
        ctx = super(FirmSupportPricingView, self).get_context_data(**kwargs)

        if 'firm_form' not in ctx:
            ctx['firm_form'] = self._get_firm_form()

        if 'advisor_formset' not in ctx:
            ctx['advisor_formset'] = self.get_advisor_formset()

        if 'client_formset' not in ctx:
            ctx['client_formset'] = self.get_client_formset()

        return ctx

    def post(self, request):
        save_form = request.POST.get('submit', None)
        if save_form not in ['firm', 'advisor', 'client']:
            return HttpResponseRedirect(self.request.get_full_path())

        return getattr(self, 'save_%s' % save_form)(request)

    def save_firm(self, request):
        form = self._get_firm_form(request.POST, self.firm.pricing_plan)
        return self._save(request, form, 'firm_form')

    def save_advisor(self, request):
        formset = self.get_advisor_formset(request.POST)
        return self._save(request, formset, 'advisor_formset')

    def save_client(self, request):
        formset = self.get_client_formset(request.POST)
        return self._save(request, formset, 'client_formset')

    def _save(self, request, form_or_formset, context_name):
        if form_or_formset.is_valid():
            form_or_formset.save()
            return HttpResponseRedirect(request.get_full_path())
        print(form_or_formset.errors)
        ctx = {
            context_name: form_or_formset,
        }
        context = self.get_context_data(**ctx)
        return self.render_to_response(context)


class FirmAdvisorClientDetails(DetailView, LegalView):
    template_name = "firm/client-details.html"
    model = Advisor

    def get_queryset(self):
        return super(FirmAdvisorClientDetails, self).get_queryset().filter(firm=self.firm)

    def get_context_data(self, **kwargs):
        ctx = super(FirmAdvisorClientDetails, self).get_context_data(**kwargs)
        client_id = self.kwargs.get("client_id", None)
        client = Client.objects.get(pk=client_id, advisor__firm=self.firm)
        ctx.update({"client": client})
        return ctx


class FirmAdvisorClients(DetailView, LegalView):
    template_name = "firm/advisor-clients.html"
    model = Advisor

    def get_queryset(self):
        return super(FirmAdvisorClients, self).get_queryset().filter(firm=self.firm)

    def get_context_data(self, **kwargs):
        ctx = super(FirmAdvisorClients, self).get_context_data(**kwargs)
        ctx["clients"] = set(map(lambda x: x.primary_owner, self.object.client_accounts))

        return ctx


class FirmAdvisorAccountOverview(DetailView, LegalView):
    template_name = "firm/overview-advisor.html"
    model = Advisor

    def get_queryset(self):
        return super(FirmAdvisorAccountOverview, self).get_queryset().filter(firm=self.firm)


class FirmOverview(TemplateView, LegalView):
    template_name = 'firm/overview.html'
    col_dict = {
        "name": 2,
        "cs_number": 0,
        'total_balance': 3,
        'total_return': 4,
        'total_fees': 5,
    }

    def __init__(self, *args, **kwargs):
        super(FirmOverview, self).__init__(*args, **kwargs)
        self.filter = "0"
        self.search = ""
        self.sort_col = "name"
        self.sort_dir = "desc"

    def get(self, request, *args, **kwargs):
        self.filter = request.GET.get("filter", self.filter)
        self.search = request.GET.get("search", self.search)
        self.sort_col = request.GET.get("sort_col", self.sort_col)
        self.sort_dir = request.GET.get("sort_dir", self.sort_dir)
        response = super(FirmOverview, self).get(request, *args, **kwargs)
        return response

    @property
    def advisors(self):
        pre_advisors = self.firm.advisors

        if self.search:
            sq = Q(user__first_name__icontains=self.search)
            pre_advisors = pre_advisors.filter(sq)

        advisors = []
        for advisor in set(pre_advisors.distinct().all()):
            advisors.append(
                [advisor.pk, advisor, advisor.user.full_name, advisor.total_balance,
                 advisor.average_return, advisor.total_fees, advisor.user.date_joined])

        reverse = self.sort_dir != "asc"

        advisors = sorted(advisors,
                          key=itemgetter(self.col_dict[self.sort_col]),
                          reverse=reverse)
        return advisors

    def get_context_data(self, **kwargs):
        ctx = super(FirmOverview, self).get_context_data(**kwargs)
        if self.firm.fiscal_years.count() > 0:
            fiscal_years_added = True
        else:
            fiscal_years_added = False
        ctx.update({
            "filter": self.filter,
            "search": self.search,
            "sort_col": self.sort_col,
            "sort_dir": self.sort_dir,
            "sort_inverse": 'asc' if self.sort_dir == 'desc' else 'desc',
            "advisors": self.advisors,
            "fiscal_years_added": fiscal_years_added,
        })
        return ctx


class FirmSupport(TemplateView, LegalView):
    template_name = "firm/support.html"


class FirmSupportForms(TemplateView, LegalView):
    template_name = "firm/support-forms.html"


class FirmSupervisorInvites(CreateView, LegalView):
    form_class = EmailInvitationForm
    template_name = 'firm/supervisor_invite.html'

    def get_success_url(self):
        messages.info(self.request, "Invite sent successfully!")
        return self.request.get_full_path()

    def dispatch(self, request, *args, **kwargs):
        response = super(FirmSupervisorInvites, self).dispatch(request, *args, **kwargs)
        if hasattr(response, 'context_data'):
            firm = request.user.authorised_representative.firm
            invitation_type = INVITATION_SUPERVISOR
            response.context_data["inviter"] = firm
            response.context_data["invite_url"] = firm.supervisor_invite_url
            response.context_data["invite_type"] = INVITATION_TYPE_DICT[str(invitation_type)].title()
            response.context_data["invitation_type"] = invitation_type
            response.context_data["next"] = request.GET.get("next", None)
            response.context_data["invites"] = EmailInvitation.objects.filter(invitation_type=invitation_type,
                                                                              inviter_id=firm.pk,
                                                                              inviter_type=firm.content_type,
                                                                              )
        return response


class FirmAdvisorInvites(CreateView, LegalView):
    form_class = EmailInvitationForm
    template_name = 'firm/advisor_invite.html'

    def get_success_url(self):
        messages.info(self.request, "Invite sent successfully!")
        return self.request.get_full_path()

    def dispatch(self, request, *args, **kwargs):
        response = super(FirmAdvisorInvites, self).dispatch(request, *args, **kwargs)
        if hasattr(response, 'context_data'):
            firm = request.user.authorised_representative.firm
            invitation_type = INVITATION_ADVISOR
            response.context_data["inviter"] = firm
            response.context_data["invite_url"] = firm.supervisor_invite_url
            response.context_data["invite_type"] = INVITATION_TYPE_DICT[str(invitation_type)].title()
            response.context_data["invitation_type"] = invitation_type
            response.context_data["next"] = request.GET.get("next", None)
            response.context_data["invites"] = EmailInvitation.objects.filter(invitation_type=invitation_type,
                                                                              inviter_id=firm.pk,
                                                                              inviter_type=firm.content_type,
                                                                              )
        return response



class FirmAcquireSmartzLeads(TemplateView, LegalView):
    template_name = 'firm/acquiresmartz-leads.html'


class FirmAcquireSmartzTargets(TemplateView, LegalView):
    template_name = 'firm/acquiresmartz-targets.html'


class FirmAcquireSmartzCognitics(TemplateView, LegalView):
    template_name = 'firm/acquiresmartz-cognitics.html'
