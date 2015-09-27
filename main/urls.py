from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import *
from django.views.decorators.csrf import csrf_exempt
from main import settings
from django.shortcuts import HttpResponseRedirect, HttpResponse


def ok_response_json(*args, **kwargs):

    return HttpResponse("[]", content_type='application/json')

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^session', csrf_exempt(Session.as_view()), name="session"),
    url(r'^betasmartz_admin/firm/(?P<pk>\d+)/invite_legal',
        InviteLegalView.as_view(), name='betasmartz_admin:invite_legal'),
    url(r'^betasmartz_admin/firm/(?P<pk>\d+)/invite_advisor',
        AdminInviteAdvisorView.as_view(), name='betasmartz_admin:invite_advisor'),
    url(r'^betasmartz_admin/firm/(?P<pk>\d+)/invite_supervisor',
        AdminInviteSupervisorView.as_view(), name='betasmartz_admin:invite_supervisor'),
    url(r'^betasmartz_admin/transaction/(?P<pk>\d+)/execute', AdminExecuteTransaction.as_view()),

    # firm views
    url(r'^(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/legal_signup$',
        AuthorisedRepresentativeSignUp.as_view(), name='firm:representative_signup'),

    url(r'^(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/advisor_signup',
        AdvisorSignUpView.as_view()),

    url(r'^login$', firm_login),
    url(r'^sign_out$', Logout.as_view()),
    url(r'^confirm_email/(?P<type>\d+)/(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
        EmailConfirmationView.as_view()),
    url(r'^confirmation/new$', NewConfirmation.as_view()),
    url(r'^$', lambda x: HttpResponseRedirect("/login")),
    url(r'^firm/login', lambda x: HttpResponseRedirect("/login")),
    url(r'^firm/sign_out', lambda x: HttpResponseRedirect("/sign_out")),

    url(r'^firm/advisor_invites', FirmAdvisorInvites.as_view()),
    url(r'^firm/supervisor_invites', FirmSupervisorInvites.as_view()),

    url(r'^firm/support$', FirmSupport.as_view()),
    url(r'^firm/support/forms$', FirmSupportForms.as_view()),
    url(r'^firm/summary',  FirmSummary.as_view()),
    url(r'^firm/change-details$',  FirmDataView.as_view()),


    # Advisor views

    url(r'^advisor/client_invites', AdvisorClientInvites.as_view(), name='advisor:client_invites'),
    url(r'^advisor/clients', AdvisorClients.as_view(), name='advisor:clients'),
    url(r'^advisor/agreements', AdvisorAgreements.as_view(), name='advisor:agreements'),
    url(r'^advisor/support$', AdvisorSupport.as_view(), name='advisor:support'),
    url(r'^advisor/support/getting-started$', AdvisorSupportGettingStarted.as_view()),

    url(r'^advisor/summary', AdvisorCompositeSummary.as_view(), name='advisor:summary'),
    url(r'^advisor/client/(?P<pk>\d+)$', AdvisorClientDetails.as_view(),),
    url(r'^composites/new$', AdvisorCompositeNew.as_view()),
    url(r'^composites/(?P<pk>\d+)/edit$', AdvisorCompositeEdit.as_view()),
    url(r'^composites/(?P<account_id>\d+)/account_groups/(?P<account_group_id>\d+)$',
        AdvisorRemoveAccountFromGroupView.as_view()),
    url(r'^composites/(?P<pk>\d+)$', AdvisorAccountGroupDetails.as_view()),
    url(r'^composites/(?P<pk>\d+)/clients$', AdvisorAccountGroupClients.as_view()),
    url(r'^composites/(?P<pk>\d+)/composite_secondary_advisors$', AdvisorAccountGroupSecondaryDetailView.as_view()),
    url(r'^composites/(?P<pk>\d+)/composite_secondary_advisors/new$', AdvisorAccountGroupSecondaryNewView.as_view()),
    url(r'^composites/(?P<pk>\d+)/composite_secondary_advisors/(?P<sa_pk>\d+)$',
        AdvisorAccountGroupSecondaryDeleteView.as_view()),
    url(r'^composites/client_account/(?P<pk>\d+)/change_fee$', AdvisorClientAccountChangeFee.as_view()),
    url(r'^betasmartz_admin/rebalance/(?P<pk>\d+)$', GoalRebalance.as_view()),


    url('^impersonate/(?P<pk>\d+)$', ImpersonateView.as_view()),

    # Client views
    url(r'^client/login', client_login, name='client:login'),
    url(r'^client/app', ClientApp.as_view(), name='client:app'),
    url(r'^(?P<slug>[\w-]+)/client/signup/(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$',
        ClientSignUp.as_view(), name='client:sign_up'),
    url(r'^client/api/account-groups/(?P<pk>\d+)/beneficiaries$', CancelableTransactionsView.as_view()),
    url(r'^client/api/appData', ClientAppData.as_view(), name='client:api:app_data'),
    url(r'^client/api/cancelable_transactions', CancelableTransactionsView.as_view()),
    url(r'^client/api/asset-classes', ClientAssetClasses.as_view(), name='client:api:asset_classes'),
    url(r'^client/api/user', ClientUserInfo.as_view(), name='client:api:user'),
    url(r'^client/api/visitor', ClientVisitor.as_view(), name='client:api:visitor'),
    url(r'^client/api/advisors/(?P<pk>\d+)', ClientAdvisor.as_view(), name='client:api:advisors'),
    url(r'^client/api/advisors$', ClientAdvisor.as_view(), name='client:api:advisors_2'),
    url(r'^client/api/contact-preference$', ContactPreference.as_view()),
    url(r'^client/api/accounts$', csrf_exempt(ClientAccounts.as_view()), name='client:api:accounts'),
    url(r'^client/api/firms', ClientFirm.as_view(), name='client:api:firms'),
    url(r'^client/api/accounts/(?P<pk>\d+)/positions', ClientAccountPositions.as_view(),
        name='client:api:accounts:positions'),
    url(r'^client/api/client/api/accounts/(?P<pk>\d+)/withdrawals$', csrf_exempt(Withdrawals.as_view())),

    url(r'^client/api/portfolio-sets/(?P<pk>\d+)/asset-classes', PortfolioAssetClasses.as_view(),
        name='client:api:portfolio_sets:asset_classes'),
    url(r'^client/api/portfolio-sets/(?P<pk>\d+)/portfolios', PortfolioPortfolios.as_view(),
        name='client:api:portfolio_sets:portfolios'),
    url(r'^client/api/portfolio-sets/(?P<pk>\d+)/risk-free-rates', PortfolioRiskFreeRates.as_view(),
        name='client:api:portfolio_sets:risk_free_rates'),
    url(r'^client/api/client/api/accounts/(?P<pk>\d+)/allocations$', csrf_exempt(ChangeAllocation.as_view())),


    url(r'^client/api/portfolio-sets/goal_(?P<goal_pk>\d+)_(?P<pk>\d+)/asset-classes', PortfolioAssetClasses.as_view(),
        name='client:api:portfolio_sets:asset_classes'),
    url(r'^client/api/portfolio-sets/goal_(?P<goal_pk>\d+)_(?P<pk>\d+)/portfolios', PortfolioPortfolios.as_view(),
        name='client:api:portfolio_sets:portfolios'),
    url(r'^client/api/portfolio-sets/goal_(?P<goal_pk>\d+)_(?P<pk>\d+)/risk-free-rates', PortfolioRiskFreeRates.as_view(),
        name='client:api:portfolio_sets:risk_free_rates'),

    url(r'^client/api/account-groups/(?P<pk>\d+)/pending-invites', ok_response_json),
    url(r'^transactions$', csrf_exempt(NewTransactionsView.as_view())),
    url(r'^transactions\.csv$', csrf_exempt(NewTransactionsView.as_view())),
    url(r'^client/api/transaction_memos$', csrf_exempt(NewTransactionMemoView.as_view())),
    url(r'^client/api/accounts/(?P<pk>\d+)$', csrf_exempt(ChangeGoalView.as_view())),
    url(r'^automaticDeposit$', csrf_exempt(SetAutoDepositView.as_view())),
    url(r'^automaticWithdrawal$', csrf_exempt(SetAutoWithdrawalView.as_view())),
    url(r'^analysisReturns$', AnalysisReturns.as_view()),
    url(r'^analysisBalances', AnalysisBalances.as_view()),
    url(r'^client/api/zip_codes/(?P<pk>\d+)$', ZipCodes.as_view()),
    url(r'^client/api/financial_profile$', csrf_exempt(FinancialProfileView.as_view())),
    url(r'^client/api/financial_plans$', csrf_exempt(FinancialPlansView.as_view())),
    url(r'^client/api/financial_plans/(?P<pk>\d+)$', csrf_exempt(FinancialPlansView.as_view())),
    url(r'^client/api/financial_plans/(?P<pk>\d+)/account_addition$', csrf_exempt(FinancialPlansAccountAdditionView.as_view())),
    url(r'^client/api/financial_plans/account_addition$', csrf_exempt(FinancialPlansAccountAdditionView.as_view())),
    url(r'^client/api/financial_plans/account_removal$', csrf_exempt(FinancialPlansAccountDeletionView.as_view())),
    url(r'^client/api/financial_plans/(?P<pk>\d+)/account_removal$', csrf_exempt(FinancialPlansAccountDeletionView.as_view())),

    url(r'^client/api/external_accounts$', csrf_exempt(FinancialPlansExternalAccountAdditionView.as_view())),
    url(r'^client/api/external_accounts/(?P<pk>\d+)$', csrf_exempt(FinancialPlansExternalAccountDeletionView.as_view())),




    url(r'^password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/password/reset/done/', 'template_name': 'registration/password_reset.html'},
        name="password_reset"),
    url(r'^password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/login'}, name='password_reset_confirm')
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT,
                              'show_indexes': True}), )
