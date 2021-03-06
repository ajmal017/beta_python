from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth.hashers import make_password
from django.db.models.fields import TextField
from django.forms.widgets import Textarea
from django.shortcuts import HttpResponseRedirect, render_to_response
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from suit.admin import SortableModelAdmin, SortableTabularInline

from advisors import models as advisor_models
from genericadmin.admin import BaseGenericModelAdmin, GenericAdminModelAdmin
from main.models import AccountGroup, ActivityLog, ActivityLogEvent, Advisor, \
    AssetFeature, AssetFeePlan, AuthorisedRepresentative, Dividend, \
    EventMemo, Firm, FirmData, FiscalYear, Goal, GoalMetric, GoalMetricGroup, \
    GoalSetting, GoalType, Inflation, InvestmentType, MarketIndex, Performer, \
    Portfolio, PortfolioItem, PositionLot, PricingPlan, \
    ProxyAssetClass, ProxyTicker, Ticker, Transaction, User, View, \
    ManagerBenchmarks
from main.models import PortfolioProvider, DefaultPortfolioProvider, PortfolioSet, DefaultPortfolioSet


class AssetResource(resources.ModelResource):
    class Meta:
        model = ProxyAssetClass


class InflationResource(resources.ModelResource):
    class Meta:
        model = Inflation
        exclude = ('id', 'recorded')
        import_id_fields = ('year', 'month')


class TickerInline(BaseGenericModelAdmin, SortableTabularInline):
    model = ProxyTicker
    sortable = 'ordering'
    extra = 0
    generic_fk_fields = [{
        'ct_field': 'benchmark_content_type',
        'fk_field': 'benchmark_object_id',
    }]


class EventMemoInline(admin.StackedInline):
    model = EventMemo
    extra = 0


class PortfolioViewsInline(admin.StackedInline):
    model = View
    extra = 0


class AdvisorInline(admin.StackedInline):
    model = Advisor


class AuthorisedRepresentativeInline(admin.StackedInline):
    model = AuthorisedRepresentative


class FirmDataInline(admin.StackedInline):
    model = FirmData


class InvestmentTypeAdmin(admin.ModelAdmin):
    model = InvestmentType


class AssetClassAdmin(GenericAdminModelAdmin, SortableModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'display_name', 'display_order', 'investment_type')
    inlines = (TickerInline,)
    resource_class = AssetResource
    sortable = 'display_order'


class FirmFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'filter by firm'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'firm'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_id = [[None, "All"]]
        for firm in Firm.objects.all():
            list_id.append([firm.pk, firm.name])

        return list_id

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.

        if self.value() is None:
            return queryset.all()

        return queryset.filter(firm__pk=self.value())


def approve_application(modeladmin, request, queryset):
    for obj in queryset.all():
        obj.approve()


approve_application.short_description = "Approve application(s)"


class AdvisorAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_num', 'is_accepted', 'is_confirmed', 'firm',
                    'geolocation_lock')
    list_filter = ('is_accepted', FirmFilter)
    actions = (approve_application,)

    pass


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)

        def clean_password(me):
            password = me.cleaned_data['password']

            if me.instance:
                if me.instance.password != password:
                    password = make_password(password)
            else:
                password = make_password(password)

            print(password, "*******************")
            return password

        form.clean_password = clean_password

        return form

    pass


def rebalance(modeladmin, request, queryset):
    context = {'STATIC_URL': settings.STATIC_URL, 'MEDIA_URL': settings.MEDIA_URL, 'item_class': 'transaction'}

    if queryset.count() > 1:
        return render_to_response('admin/betasmartz/error_only_one_item.html', context)

    else:
        return HttpResponseRedirect('/betasmartz_admin/rebalance/{pk}?next=/admin/main/firm/'
                                    .format(pk=queryset.all()[0].pk))


def invite_authorised_representative(modeladmin, request, queryset):
    context = {'STATIC_URL': settings.STATIC_URL, 'MEDIA_URL': settings.MEDIA_URL, 'item_class': 'firm'}

    if queryset.count() > 1:
        return render_to_response('admin/betasmartz/error_only_one_item.html', context)

    else:
        return HttpResponseRedirect('/betasmartz_admin/firm/{pk}/invite_legal?next=/admin/main/firm/'
                                    .format(pk=queryset.all()[0].pk))


def invite_advisor(modeladmin, request, queryset):
    context = {'STATIC_URL': settings.STATIC_URL, 'MEDIA_URL': settings.MEDIA_URL, 'item_class': 'firm'}

    if queryset.count() > 1:
        return render_to_response('admin/betasmartz/error_only_one_item.html', context)

    else:
        return HttpResponseRedirect('/betasmartz_admin/firm/{pk}/invite_advisor?next=/admin/main/firm/'
                                    .format(pk=queryset.all()[0].pk))


def invite_supervisor(modeladmin, request, queryset):
    context = {'STATIC_URL': settings.STATIC_URL, 'MEDIA_URL': settings.MEDIA_URL, 'item_class': 'firm'}

    if queryset.count() > 1:
        return render_to_response('admin/betasmartz/error_only_one_item.html', context)

    else:
        return HttpResponseRedirect('/betasmartz_admin/firm/{pk}/invite_supervisor?next=/admin/main/firm/'
                                    .format(pk=queryset.all()[0].pk))


class PricingPlanAdmin(admin.ModelAdmin):
    list_display = 'firm', 'bps', 'fixed', 'system_bps', 'system_fixed'


class PricingPlanInline(admin.TabularInline):
    model = PricingPlan

    def has_delete_permission(self, request, obj=None):
        return False


class FirmAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (FirmDataInline, PricingPlanInline)
    actions = (invite_authorised_representative, invite_advisor, invite_supervisor)


class AuthorisedRepresentativeAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_num', 'is_accepted', 'is_confirmed', 'firm',
                    'geolocation_lock')
    list_filter = ('is_accepted', FirmFilter)
    actions = (approve_application,)


class GoalMetricInline(admin.StackedInline):
    model = GoalMetric


class GoalMetricGroupAdmin(admin.ModelAdmin):
    model = GoalMetricGroup
    inlines = (GoalMetricInline,)


class GoalSettingAdmin(admin.ModelAdmin):
    model = GoalSetting


class GoalTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'default_term', 'risk_sensitivity', 'order')
    list_editable = ('group', 'default_term', 'risk_sensitivity', 'order')

class DefaultDefaultPortfolioProviderAdmin(admin.ModelAdmin):
    list_display = ('default_provider', 'changed')

class DefaultPortfolioSetAdmin(admin.ModelAdmin):
    list_display = ('default_set', 'changed')

class PortfolioProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'TLH', 'portfolio_optimization')

class GoalAdmin(admin.ModelAdmin):
    list_display = ('account', 'name', 'type')
    actions = (rebalance,)


class PositionLotAdmin(admin.ModelAdmin):
    list_display = ('execution_distribution', 'quantity')


class PortfolioItemInline(admin.StackedInline):
    model = PortfolioItem


class PortfolioAdmin(admin.ModelAdmin):
    inlines = (PortfolioItemInline,)


class PortfolioSetAdmin(admin.ModelAdmin):
    filter_horizontal = ('asset_classes',)
    list_display = ('name', 'type')
    inlines = (PortfolioViewsInline,)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('reason', 'from_goal', 'to_goal', 'status', 'amount', 'created')
    list_filter = ('status',)


class PerformerAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'group', 'allocation')


def approve_changes(modeladmin, request, queryset):
    for obj in queryset.all():
        obj.approve()
    messages.info(request, "Changes have been approved and applied")


class AdvisorChangeDealerGroupAdmin(admin.ModelAdmin):
    list_display = ('advisor', 'new_email', 'old_firm', 'new_firm', 'approved', 'create_at', 'approved_at')
    list_filter = ('advisor', 'old_firm', 'new_firm', 'approved')
    actions = (approve_changes,)


class AdvisorBulkInvestorTransferAdmin(admin.ModelAdmin):
    filter_horizontal = ('investors',)
    list_display = ('from_advisor', 'to_advisor', 'approved', 'create_at', 'approved_at')
    list_filter = ('from_advisor', 'to_advisor', 'approved')
    actions = (approve_changes,)


class AdvisorSingleInvestorTransferAdmin(admin.ModelAdmin):
    list_display = ('from_advisor', 'to_advisor', 'firm', 'investor', 'approved', 'create_at', 'approved_at')
    list_filter = ('from_advisor', 'to_advisor', 'investor', 'approved')
    actions = (approve_changes,)


class ActivityLogEventAdminInline(admin.TabularInline):
    model = ActivityLogEvent


class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'format_str', 'format_args')
    list_editable = ('name', 'format_str', 'format_args')
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 100})},
    }
    inlines = (ActivityLogEventAdminInline,)


class FiscalYearAdmin(admin.ModelAdmin):
    model = FiscalYear


class ManagerBenchmarksAdmin(admin.TabularInline):
    model = ManagerBenchmarks


class TickerAdmin(admin.ModelAdmin):
    inlines = ManagerBenchmarksAdmin,
    list_display = (
        'symbol',
        'unit_price',
        'region_feature',
        'asset_class_feature',
        'investment_type_feature',
        'currency_feature',
    )
    search_fields = ['symbol']

    def region_feature(self, obj):
        return obj.get_region_feature_value()

    def asset_class_feature(self, obj):
        return obj.get_asset_class_feature_value()

    def investment_type_feature(self, obj):
        return obj.get_asset_type_feature_value()

    def currency_feature(self, obj):
        return obj.get_currency_feature_value()


class AssetFeePlanAdmin(admin.ModelAdmin):
    model = AssetFeePlan


class InflationAdmin(ImportExportModelAdmin):
    list_display = 'year', 'month', 'value'
    resource_class = InflationResource

class AssetFeaturesAdmin(admin.ModelAdmin):
    model = AssetFeature
    list_display = ('name', 'description', 'upper_limit')
    list_editable = ('upper_limit',)


admin.site.register(AccountGroup)
admin.site.register(Inflation, InflationAdmin)
admin.site.register(advisor_models.ChangeDealerGroup, AdvisorChangeDealerGroupAdmin)
admin.site.register(advisor_models.SingleInvestorTransfer, AdvisorSingleInvestorTransferAdmin)
admin.site.register(advisor_models.BulkInvestorTransfer, AdvisorBulkInvestorTransferAdmin)
admin.site.register(Performer, PerformerAdmin)
admin.site.register(PortfolioProvider, PortfolioProviderAdmin)
admin.site.register(DefaultPortfolioProvider, DefaultDefaultPortfolioProviderAdmin)
admin.site.register(DefaultPortfolioSet, DefaultPortfolioSetAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalType, GoalTypeAdmin)
admin.site.register(MarketIndex)
admin.site.register(GoalSetting, GoalSettingAdmin)
admin.site.register(GoalMetricGroup, GoalMetricGroupAdmin)
admin.site.register(Dividend)
admin.site.register(ProxyAssetClass, AssetClassAdmin)
admin.site.register(PricingPlan, PricingPlanAdmin)
admin.site.register(Firm, FirmAdmin)
admin.site.register(Advisor, AdvisorAdmin)
admin.site.register(AuthorisedRepresentative, AuthorisedRepresentativeAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(PortfolioSet, PortfolioSetAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(ActivityLog, ActivityLogAdmin)
admin.site.register(InvestmentType, InvestmentTypeAdmin)
admin.site.register(FiscalYear, FiscalYearAdmin)
admin.site.register(Ticker, TickerAdmin)
admin.site.register(PositionLot, PositionLotAdmin)
admin.site.register(AssetFeePlan, AssetFeePlanAdmin)
admin.site.register(AssetFeature, AssetFeaturesAdmin)


if settings.DEBUG:
    from main.models import (MarketOrderRequest, Execution, DailyPrice,
                             ExecutionDistribution)


    class DailyPriceAdmin(GenericAdminModelAdmin):
        model = DailyPrice
        list_display = (
        'date', 'price', 'instrument', 'instrument_content_type', 'instrument_object_id')
        # sortable = 'date'
        # extra = 0
        generic_fk_fields = [{
            'ct_field': 'instrument_content_type',
            'fk_field': 'instrument_object_id',
        }]
        list_editable = (
        'date', 'price', 'instrument_content_type', 'instrument_object_id')

    admin.site.register(DailyPrice, DailyPriceAdmin)
    admin.site.register(MarketOrderRequest)
    admin.site.register(Execution)
    admin.site.register(ExecutionDistribution)
