from __future__ import unicode_literals

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.AdvisorForms.as_view(), name='list'),
    url(r'^change/firm$', views.AdvisorChangeDealerGroupView.as_view(),
        name='change-firm'),
    url(r'^change/firm/update/(?P<pk>\d+)$',
        views.AdvisorChangeDealerGroupUpdateView.as_view()),
    url(r'^transfer/single$',
        views.AdvisorSingleInvestorTransferView.as_view(),
        name='transfer-single'),
    url(r'^transfer/single/update/(?P<pk>\d+)$',
        views.AdvisorSingleInvestorTransferUpdateView.as_view()),
    url(r'^transfer/bulk$',
        views.AdvisorBulkInvestorTransferView.as_view(),
        name='transfer-bulk'),
    url(r'^transfer/bulk/update/(?P<pk>\d+)$',
        views.AdvisorBulkInvestorTransferUpdateView.as_view()),
)
