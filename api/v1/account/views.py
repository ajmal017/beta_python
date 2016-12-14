import logging

from django.db import transaction
from django.db.models.query_utils import Q
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from api.v1.permissions import IsAdvisorOrClient
from api.v1.utils import activity
from api.v1.views import ApiViewMixin
from client.models import AccountBeneficiary, ClientAccount, \
    CloseAccountRequest
from support.models import SupportRequest
from . import serializers

logger = logging.getLogger('api.v1.account.views')


class AccountViewSet(ApiViewMixin, NestedViewSetMixin,
                     viewsets.ReadOnlyModelViewSet):
    model = ClientAccount
    # We define the queryset because our get_queryset calls super so the Nested queryset works.
    queryset = ClientAccount.objects.all()
    pagination_class = None

    permission_classes = (IsAdvisorOrClient,)

    serializer_class = serializers.ClientAccountSerializer

    # Override this method so we can also look for accounts from signatories
    def filter_queryset_by_parents_lookups(self, queryset):
        parents_query_dict = self.get_parents_query_dict()
        if parents_query_dict:
            q = None
            try:
                for key, value in parents_query_dict.items():
                    if key == 'primary_owner':
                        tq = (Q(primary_owner=value) | Q(signatories__id=value))
                    else:
                        tq = Q({key: value})
                    if q:
                        q &= tq
                    else:
                        q = tq

                return queryset.filter(q)
            except ValueError:
                raise NotFound()
        else:
            return queryset

    def get_queryset(self):
        """
        Because this viewset can have a primary owner and signatories,
        we don't use the queryset parsing features from NestedViewSetMixin as
        it only allows looking at one field for the parent.
        :return:
        """
        qs = super(AccountViewSet, self).get_queryset()

        # show "permissioned" records only
        user = SupportRequest.target_user(self.request)
        if user.is_advisor:
            qs = qs.filter_by_advisor(user.advisor)
        elif user.is_client:
            qs = qs.filter_by_client(user.client)
        else:
            raise PermissionDenied('Only Advisors or Clients '
                                   'are allowed to access goals.')

        return qs

    @detail_route(methods=['get'])
    def activity(self, request, pk=None, **kwargs):
        account = self.get_object()
        return activity.get(request, account)

    @transaction.atomic
    def create_new_account(self, request):
        client = SupportRequest.target_user(self.request).client
        serializer = serializers.new_account_fabric(request.data)
        if serializer.is_valid():
            account = serializer.save(request, client)
            return account
            # return Response(ClientAccountSerializer(instance=account).data)
        return Response({'error': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def rollover(self, request):
        return self.create_new_account(request)

    @detail_route(methods=['get', 'post'], url_path='beneficiaries')
    def beneficiaries(self, request, pk=None, **kwargs):
        instance = self.get_object()
        if instance.status != 0:  # if account is not open, block update from client
            return Response('Account is not open, cannot update', status=status.HTTP_403_FORBIDDEN)
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        if request.user != instance.primary_owner.user and request.user != instance.primary_owner.advisor.user:
            raise PermissionDenied()
        if request.method == 'POST':
            # create new beneficiary and add to account
            request.data['account'] = instance.id
            serializer = serializers.AccountBeneficiaryCreateSerializer(data=request.data, partial=partial, context={'request': request})
            serializer.is_valid(raise_exception=True)
            beneficiary = serializer.save()
            beneficiaries = AccountBeneficiary.objects.filter(account=instance)
            serializer = serializers.AccountBeneficiarySerializer(beneficiaries, many=True)
            return Response(serializer.data)
        beneficiaries = AccountBeneficiary.objects.filter(account=instance)
        serializer = serializers.AccountBeneficiarySerializer(beneficiaries, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'], url_path='close')
    def close(self, request, pk=None, **kwargs):
        instance = self.get_object()
        serializer = serializers.CloseAccountRequestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        close_account = serializer.save()
        close_account.account.status = 1
        close_account.account.save()
        close_account.send_admin_email()
        # close choice check
        if close_account.close_choice == CloseAccountRequest.CloseChoice.liquidate.value:
            # email Advisor
            close_account.send_advisor_email()
        elif close_account.close_choice == CloseAccountRequest.CloseChoice.transfer_to_account.value:
            pass
        elif close_account.close_choice == CloseAccountRequest.CloseChoice.transfer_to_custodian.value:
            close_account.send_advisor_email()
        else:  # take direct custody
            close_account.send_advisor_email()
        return Response(serializer.data)


class AccountBeneficiaryViewSet(ApiViewMixin,
                                NestedViewSetMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.ReadOnlyModelViewSet):
    model = AccountBeneficiary
    queryset = AccountBeneficiary.objects.all()
    permission_classes = (IsAdvisorOrClient,)
    serializer_response_class = serializers.AccountBeneficiarySerializer

    def get_queryset(self):
        """
        Because this viewset can have a primary owner and signatories,
        we don't use the queryset parsing features from NestedViewSetMixin as
        it only allows looking at one field for the parent.
        :return:
        """
        qs = super(AccountBeneficiaryViewSet, self).get_queryset()

        # show "permissioned" records only
        user = SupportRequest.target_user(self.request)
        qs.filter(Q(account__primary_owner__user=user) | Q(account__primary_owner__advisor__user=user) )
        return qs

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return serializers.AccountBeneficiaryUpdateSerializer
        elif self.request.method == 'POST':
            return serializers.AccountBeneficiaryCreateSerializer
        else:
            # Default for get and other requests is the read only serializer
            return serializers.AccountBeneficiarySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.account.primary_owner.user and request.user != instance.account.primary_owner.advisor.user:
            raise PermissionDenied()
        super(AccountBeneficiaryViewSet, self).destroy(request, *args, **kwargs)
        return Response('null', status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.account.primary_owner.user and request.user != instance.account.primary_owner.advisor.user:
            raise PermissionDenied()
        return super(AccountBeneficiaryViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        if request.user != instance.account.primary_owner.user and request.user != instance.account.primary_owner.advisor.user:
            raise PermissionDenied()
        serializer = self.get_serializer_class()(data=request.data, partial=partial, context={'account': instance.account, 'beneficiary': instance})
        serializer.is_valid(raise_exception=True)
        updated = serializer.update(instance, serializer.validated_data)
        return Response(self.serializer_response_class(updated).data)
