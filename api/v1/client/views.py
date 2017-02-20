from django.contrib.auth import authenticate, login as auth_login
from rest_framework import viewsets, views, mixins
from rest_framework import exceptions, parsers, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from api.v1.client.serializers import EmailNotificationsSerializer, \
    PersonalInfoSerializer, RiskProfileResponsesSerializer
from api.v1.permissions import IsClient, IsAdvisorOrClient
from api.v1.views import ApiViewMixin, ReadOnlyApiViewMixin
from main.models import ExternalAsset, User, Goal
from user.models import SecurityAnswer
from client.models import Client, EmailInvite, ClientAccount
from support.models import SupportRequest
from api.v1.user.serializers import UserSerializer
from api.v1.retiresmartz.serializers import RetirementPlanEincSerializer, RetirementPlanEincWritableSerializer
from retiresmartz.models import RetirementPlan, RetirementPlanEinc, RetirementAdvice
from django.views.generic.detail import SingleObjectMixin
from . import serializers
from api.v1.goals.serializers import GoalSerializer
import logging
import json
from api.v1.utils import activity
from django.template.loader import render_to_string
from main import quovo, plaid
from client import healthdevice
from address.models import USState, USFips, USZipcode
from consumer_expenditure.models import AreaQuotient, PeerGroupData
from consumer_expenditure import utils as ce_utils
from functools import reduce
logger = logging.getLogger('api.v1.client.views')


class ExternalAssetViewSet(ApiViewMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    model = ExternalAsset
    # We define the queryset because our get_queryset calls super so the Nested queryset works.
    queryset = ExternalAsset.objects.all()
    serializer_class = serializers.ExternalAssetSerializer
    pagination_class = None

    # Set the response serializer because we want to use the 'get' serializer for responses from the 'create' methods.
    # See api/v1/views.py
    serializer_response_class = serializers.ExternalAssetSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'POST']:
            return serializers.ExternalAssetWritableSerializer
        else:
            # Default for get and other requests is the read only serializer
            return serializers.ExternalAssetSerializer

    def get_queryset(self):
        qs = super(ExternalAssetViewSet, self).get_queryset()

        # Only return assets which the user has access to.
        user = SupportRequest.target_user(self.request)
        return qs.filter_by_user(user)


class RetirementIncomeViewSet(ApiViewMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    model = RetirementPlanEinc
    # We define the queryset because our get_queryset calls super so the Nested queryset works.
    queryset = RetirementPlanEinc.objects.all()
    serializer_class = RetirementPlanEincSerializer
    pagination_class = None

    # Set the response serializer because we want to use the 'get' serializer for responses from the 'create' methods.
    # See api/v1/views.py
    serializer_response_class = RetirementPlanEincSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'POST']:
            return RetirementPlanEincWritableSerializer
        else:
            # Default for get and other requests is the read only serializer
            return RetirementPlanEincSerializer

    def get_queryset(self):
        qs = super(RetirementIncomeViewSet, self).get_queryset()

        # Only return assets which the user has access to.
        user = SupportRequest.target_user(self.request)
        allow_plans = RetirementPlan.objects.filter_by_user(user)
        return qs.filter(plan__in=allow_plans)


class ClientViewSet(ApiViewMixin,
                    NestedViewSetMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """
    Everything except delete
    """
    model = Client
    # We define the queryset because our get_queryset calls super so the Nested queryset works.
    queryset = Client.objects.all()
    serializer_class = serializers.ClientSerializer
    # Set the response serializer because we want to use the 'get' serializer for responses from the 'create' methods.
    # See api/v1/views.py
    serializer_response_class = serializers.ClientSerializer
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method in ['PUT']:
            return serializers.ClientUpdateSerializer
        elif self.request.method in ['POST']:
            return serializers.ClientCreateSerializer
        else:
            # Default for get and other requests is the read only serializer
            return serializers.ClientSerializer

    def get_queryset(self):
        qs = super(ClientViewSet, self).get_queryset()

        # Only return Clients the user has access to.
        user = SupportRequest.target_user(self.request)
        return qs.filter_by_user(user)

    def create(self, request, *args, **kwargs):
        if not hasattr(request.user, 'invitation') or EmailInvite.STATUS_ACCEPTED != getattr(request.user.invitation,
                                                                                             'status',
                                                                                             None):
            return Response({'error': 'requires account with accepted invitation'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # creat new client
        client = serializer.save(advisor=request.user.invitation.advisor, user=request.user)
        if isinstance(client.regional_data, dict):
            rd = client.regional_data
        else:
            rd = json.loads(client.regional_data)
        if not rd.get('tax_transcript_data'):
            # add tax_transcript and tax_transcript_data from
            # the invitation serializer to client.regional_data
            invitation_serializer = serializers.PrivateInvitationSerializer(request.user.invitation)
            if invitation_serializer.data.get('tax_transcript', None) is not None:
                rd['tax_transcript'] = invitation_serializer.data.get('tax_transcript')
                rd['tax_transcript_data'] = invitation_serializer.data.get('tax_transcript_data')
                client.regional_data = json.dumps(rd)
                client.save()

        if not rd.get('social_security_statement_data'):
            # add social_security_statement and social_security_statement_data from
            # the invitation serializer to client.regional_data
            invitation_serializer = serializers.PrivateInvitationSerializer(request.user.invitation)
            if invitation_serializer.data.get('social_security_statement', None) is not None:
                rd['social_security_statement'] = invitation_serializer.data.get('social_security_statement')
                rd['social_security_statement_data'] = invitation_serializer.data.get('social_security_statement_data')
                client.regional_data = json.dumps(rd)
                client.save()

        if not rd.get('partner_social_security_statement_data'):
            # add social_security_statement and social_security_statement_data from
            # the invitation serializer to client.regional_data
            invitation_serializer = serializers.PrivateInvitationSerializer(request.user.invitation)
            if invitation_serializer.data.get('partner_social_security_statement', None) is not None:
                rd['partner_social_security_statement'] = invitation_serializer.data.get('partner_social_security_statement')
                rd['partner_social_security_statement_data'] = invitation_serializer.data.get('partner_social_security_statement_data')
                client.regional_data = json.dumps(rd)
                client.save()

        # set client invitation status to complete
        client.user.invitation.status = EmailInvite.STATUS_COMPLETE
        client.user.invitation.save()

        # Email the user "Welcome Aboard"
        subject = 'Welcome to BetaSmartz!'
        context = {
            'advisor': client.advisor,
            'login_url': client.user.login_url,
            'category': 'Customer onboarding'
        }
        self.request.user.email_user(subject,
                                     html_message=render_to_string(
                                        'email/client/congrats_new_client_setup.html', context))

        headers = self.get_success_headers(serializer.data)
        serializer = self.serializer_response_class(client)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        orig = Client.objects.get(pk=instance.pk)
        updated = serializer.update(instance, serializer.validated_data)

        return Response(self.serializer_response_class(updated).data)

    @detail_route(methods=['get'])
    def goals(self, request, pk=None, **kwargs):
        """
        Return list of goals from all accounts of the given client
        """
        instance = self.get_object()
        accounts = ClientAccount.objects.filter(primary_owner=instance)
        goals = Goal.objects.filter(account__in=accounts)
        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def activity(self, request, pk=None, **kwargs):
        """
        Return list of activities from all accounts of the given client
        """
        client = self.get_object()
        return activity.get(request, client)

    @detail_route(methods=['put'], permission_classes=[IsAdvisorOrClient,], url_path='risk-profile-responses')
    def risk_profile_responses(self, request, pk=None, **kwargs):
        instance = Client.objects.get(pk=pk)
        user = SupportRequest.target_user(request)
        if (user.is_advisor and instance.advisor != user.advisor) or (user.is_client and instance != user.client):
            raise exceptions.PermissionDenied("You do not have permission to update risk profile responses")
        serializer = RiskProfileResponsesSerializer(instance, data={'risk_profile_responses':request.data})
        serializer.is_valid(raise_exception=True)
        client = serializer.save()
        return Response(serializer.data['risk_profile_responses'])

    @detail_route(methods=['get'], permission_classes=[IsAdvisorOrClient,], url_path='peer-group-expenses/')
    def peer_group_expenses(self, request, pk=None, **kwargs):
        client = Client.objects.get(pk=pk)
        user = SupportRequest.target_user(request)
        if (user.is_advisor and client.advisor != user.advisor) or (user.is_client and client != user.client):
            raise exceptions.PermissionDenied("You do not have permission to get peer group data")

        yearly_income = float(request.GET.get('income', client.income))
        age_group = ce_utils.get_age_group(client.age)
        state = USState.objects.get(code=client.residential_address.region.code)
        region_no = state.region
        region_col = ce_utils.get_region_column_name(region_no)
        # zipcodes = USZipcode.objects.filter(zip_code=client.residential_address.post_code)
        # rucc = zipcodes[0].fips.rucc
        # loc_col = ce_utils.get_location_column_name(rucc)
        pc_col = ce_utils.get_pc_column_name(yearly_income)
        tax_cat = expense_cat=RetirementPlan.ExpenseCategory.TAXES.value
        tax_item = PeerGroupData.objects.get(age_group=age_group, expense_cat=tax_cat)
        ep_pgd = getattr(tax_item, pc_col) # Expenditure from peer group data
        region_quot = getattr(tax_item, region_col) # Location quotient region
        tax_rate = region_quot * ep_pgd

        peer_group_data = PeerGroupData.objects.filter(
            age_group=age_group
        ).exclude(
            expense_cat=RetirementPlan.ExpenseCategory.TAXES.value
        )

        results = []
        for item in peer_group_data:
            ep_pgd = getattr(item, pc_col) # Expenditure from peer group data
            region_quot = getattr(item, region_col) # Location quotient region
            results += [{
                'cat': item.expense_cat.id,
                'adj_ep_based_100': region_quot * ep_pgd # Adjusted % Expenditure based to 100%
            }]

        ep_sum = reduce((lambda acc, item: acc + item['adj_ep_based_100']), results, 0.0)
        descriptions = ce_utils.get_category_descriptions()
        def build_response_item(item):
            return {
                'id': item['cat'],
                'cat': item['cat'],
                'who': 'self',
                'desc': descriptions[item['cat']],
                'rate': item['adj_ep_based_100'] / ep_sum,
            }

        results = list(map(build_response_item, results))
        results += [{
            'id': tax_cat,
            'cat': tax_cat,
            'who': 'self',
            'desc': descriptions[tax_cat],
            'rate': tax_rate,
        }]

        return Response(results)

    # @detail_route(methods=['post'], permission_classes=[IsAdvisorOrClient,], url_path='connect-health-device/')
    # def create_health_device(self, request, *args, **kwargs):
    #     user = SupportRequest.target_user(request)
    #     if not user.is_client:
    #         return Response('You do not have permission to access this page', status=status.HTTP_403_FORBIDDEN)
    #     data = healthdevices.create_access_token(request)
    #     return Response(data)

    @detail_route(methods=['get'], permission_classes=[IsAdvisorOrClient,], url_path='health-device-data/')
    def get_health_device(self, request, *args, **kwargs):
        user = SupportRequest.target_user(request)
        if not user.is_client:
            return Response('You do not have permission to access this page', status=status.HTTP_403_FORBIDDEN)
        data = healthdevice.get_data(user.client)
        return Response(data)


class InvitesView(ApiViewMixin, views.APIView):
    permission_classes = []
    serializer_class = serializers.PrivateInvitationSerializer
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,
    )

    def get(self, request, invite_key):
        find_invite = EmailInvite.objects.filter(invite_key=invite_key)
        if not find_invite.exists:
            return Response({'error': 'invitation not found'}, status=status.HTTP_404_NOT_FOUND)

        invite = find_invite.get()

        if request.user.is_authenticated():
            # include onboarding data
            data = self.serializer_class(instance=invite).data
        else:
            data = serializers.InvitationSerializer(instance=invite).data
        return Response(data)

    def put(self, request, invite_key):
        if not request.user.is_authenticated():
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        find_invite = EmailInvite.objects.filter(invite_key=invite_key)
        if not find_invite.exists:
            return Response({'error': 'invitation not found'}, status=status.HTTP_404_NOT_FOUND)

        invite = find_invite.get()

        if invite.status == EmailInvite.STATUS_EXPIRED:
            invite.advisor.user.email_user('A client tried to use an expired invitation'
                                           "Your potential client {} {} ({}) just tried to register using an invite "
                                           "you sent them, but it has expired!".format(invite.first_name,
                                                                                       invite.last_name,
                                                                                       invite.email))

        if invite.status != EmailInvite.STATUS_ACCEPTED:
            return Response(self.serializer_class(instance=invite).data,
                            status=status.HTTP_304_NOT_MODIFIED)

        serializer = self.serializer_class(invite, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data)


class ClientUserRegisterView(ApiViewMixin, views.APIView):
    """
    Register Client's User from an invite token
    """
    permission_classes = []
    serializer_class = serializers.ClientUserRegistrationSerializer

    def post(self, request):
        user = SupportRequest.target_user(request)
        if user.is_authenticated():
            raise exceptions.PermissionDenied("Another user is already logged in.")

        serializer = serializers.ClientUserRegistrationSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            logger.error('Error accepting invitation: %s' % serializer.errors['non_field_errors'][0])
            return Response({'error': 'invitation not found for this email'}, status=status.HTTP_404_NOT_FOUND)
        invite = serializer.invite

        user_params = {
            'email': invite.email,
            'username': invite.email,
            'first_name': invite.first_name,
            'last_name': invite.last_name,
            'password': serializer.validated_data['password'],
        }
        user = User.objects.create_user(**user_params)

        sa1 = SecurityAnswer(user=user, question=serializer.validated_data['question_one'])
        sa1.set_answer(serializer.validated_data['question_one_answer'])
        sa1.save()

        sa2 = SecurityAnswer(user=user, question=serializer.validated_data['question_two'])
        sa2.set_answer(serializer.validated_data['question_two_answer'])
        sa2.save()

        invite.status = EmailInvite.STATUS_ACCEPTED
        invite.user = user

        invite.save()

        login_params = {
            'username': user.email,
            'password': serializer.validated_data['password']
        }

        user = authenticate(**login_params)

        # check if user is authenticated
        if not user or not user.is_authenticated():
            raise exceptions.NotAuthenticated()

        # Log the user in with a session as well.
        auth_login(request, user)

        user_serializer = UserSerializer(instance=user)
        msg = "Your client %s %s (%s) has accepted your invitation to Betasmartz!" % (user.first_name,
                                                                                      user.last_name,
                                                                                      user.email)
        invite.advisor.user.email_user('Client has accepted your invitation', msg)
        return Response(user_serializer.data)


class EmailNotificationsView(ApiViewMixin, RetrieveUpdateAPIView):
    permission_classes = IsClient,
    serializer_class = EmailNotificationsSerializer

    def get_object(self):
        return Client.objects.get(user=self.request.user).notification_prefs


class ProfileView(ApiViewMixin, RetrieveUpdateAPIView):
    permission_classes = IsClient,
    serializer_class = PersonalInfoSerializer

    def get_object(self):
        return Client.objects.get(user=self.request.user)


class ClientResendInviteView(SingleObjectMixin, views.APIView):
    permission_classes = [IsAuthenticated, ]
    queryset = EmailInvite.objects.all()

    def post(self, request, invite_key):
        find_invite = EmailInvite.objects.filter(invite_key=invite_key)
        if not find_invite.exists:
            raise exceptions.NotFound("Invitation not found.")

        invite = find_invite.get()

        if invite.user != self.request.user:
            raise exceptions.PermissionDenied("You are not authorized to send invitation.")

        invite.send()
        return Response('ok', status=status.HTTP_200_OK)


class QuovoGetIframeTokenView(ReadOnlyApiViewMixin, views.APIView):
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        token = quovo.get_iframe_token(request, request.user)
        data = {"token": token}
        return Response({"data": data})


class QuovoGetAccountsView(ReadOnlyApiViewMixin, views.APIView):
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kwargs):
        data = quovo.get_accounts(request, request.user)
        return Response({"data": data})


class PlaidCreateAccessTokenView(ApiViewMixin, views.APIView):
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        public_token = request.data.get('public_token', None)
        if public_token is None:
            return Response('missing public_token', status=status.HTTP_400_BAD_REQUEST)
        success = plaid.create_access_token(request.user, public_token)
        data = {"success": success}
        return Response(data)


class PlaidGetAccountsView(ReadOnlyApiViewMixin, views.APIView):
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        data = plaid.get_accounts(request.user)
        return Response(data)
