from __future__ import unicode_literals

from django.conf.urls import include, patterns, url

from main import views

urlpatterns = patterns(
    '',

    url(r'^clients/', include('advisors.clients.urls', namespace='clients', app_name='clients')),


    url(r'^composites/create$', views.AdvisorCompositeNew.as_view(),
        name='composites-create'),
    url(r'^composites/(?P<pk>\d+)$', views.AdvisorAccountGroupDetails.as_view(),
        name='composites-detail'),
    url(r'^composites/(?P<pk>\d+)/edit$', views.AdvisorCompositeEdit.as_view(),
        name='composites-edit'),
    url(
        r'^composites/(?P<account_id>\d+)/account-groups/(?P<account_group_id>\d+)$',
        views.AdvisorRemoveAccountFromGroupView.as_view(),
        name='composites-detail-account-groups-delete'),
    url(r'^composites/(?P<pk>\d+)/clients$',
        views.AdvisorAccountGroupClients.as_view(),
        name='composites-detail-clients'),
    url(r'^composites/(?P<pk>\d+)/secondary-advisors$',
        views.AdvisorAccountGroupSecondaryDetailView.as_view(),
        name='composites-detail-secondary-advisors'),
    url(r'^composites/(?P<pk>\d+)/secondary-advisors/create$',
        views.AdvisorAccountGroupSecondaryCreateView.as_view(),
        name='composites-detail-secondary-advisors-create'),
    url(r'^composites/(?P<pk>\d+)/secondary-advisors/(?P<sa_pk>\d+)$',
        views.AdvisorAccountGroupSecondaryDeleteView.as_view(),
        name='composites-detail-secondary-advisors-delete'),
    url(r'^composites/client-accounts/(?P<pk>\d+)/fee$',
        views.AdvisorClientAccountChangeFee.as_view(),
        name='composites-client-accounts-fee'),

    url(r'^agreements$', views.AdvisorAgreements.as_view(), name='agreements'),
    url(r'^agreements/(?P<client_id>\d+)/download$', views.AdvisorDownloadAgreement.as_view(), name='download-agreement'),

    url(r'^support$', views.AdvisorSupport.as_view(), name='support'),
    url(r'^support/getting-started$', views.AdvisorSupportGettingStarted.as_view(),
        name='support-getting-started'),
    url(r'^support/forms/?', include('advisors.forms.urls', namespace='support-forms', app_name='support-forms')),

    url(r'^overview', views.AdvisorCompositeOverview.as_view(), name='overview'),
)
