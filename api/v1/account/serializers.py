from rest_framework import serializers

from api.v1.serializers import (NoCreateModelSerializer,
                                NoUpdateModelSerializer,
                                ReadOnlyModelSerializer)
from client.models import ClientAccount, AccountBeneficiary, CloseAccountRequest
import logging
from user.models import SecurityAnswer

logger = logging.getLogger('api.v1.account.serializers')


class AccountBeneficiarySerializer(ReadOnlyModelSerializer):
    class Meta:
        model = AccountBeneficiary


class AccountBeneficiaryUpdateSerializer(serializers.ModelSerializer):
    """
    For PUT update requests
    """
    class Meta:
        model = AccountBeneficiary
        fields = (
            'type',
            'name',
            'relationship',
            'birthdate',
            'share',
        )

    def validate(self, data):
        account = self.context.get('account')
        beneficiary = self.context.get('beneficiary')
        if 'type' in data:
            beneficiaries = AccountBeneficiary.objects.filter(account=account, type=data['type'])
        else:
            beneficiaries = AccountBeneficiary.objects.filter(account=account, type=beneficiary.type)
        shares = [b.share for b in beneficiaries if b.id != beneficiary.id]
        shares.append(data['share'])
        if sum(shares) > 1.0:
            raise serializers.ValidationError({'share': 'Beneficiaries for account would be over 100%'})
        return data


class AccountBeneficiaryCreateSerializer(serializers.ModelSerializer):
    """
    For POST create requests
    """
    class Meta:
        model = AccountBeneficiary
        fields = (
            'type',
            'name',
            'relationship',
            'birthdate',
            'share',
            'account',
        )

    def validate(self, data):
        beneficiaries = AccountBeneficiary.objects.filter(account=data['account'], type=data['type'])
        shares = [b.share for b in beneficiaries]
        shares.append(data['share'])
        if sum(shares) > 1.0:
            raise serializers.ValidationError({'share': 'Beneficiaries for account would be over 100%'})
        return data


class ClientAccountSerializer(ReadOnlyModelSerializer):
    """
    Read-only ClientAccount Serializer
    """

    class Meta:
        model = ClientAccount


class ClientAccountCreateSerializer(NoUpdateModelSerializer):
    """
    When creating an account via the API, we want the name to be required,
    so enforce it.
    """
    account_name = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = ClientAccount
        fields = (
            'account_type',
            'account_name',
            'account_number',
            'primary_owner',
        )

    def create(self, validated_data):
        ps = validated_data['primary_owner'].advisor.default_portfolio_set
        validated_data.update({
            'default_portfolio_set': ps,
        })
        return (super(ClientAccountCreateSerializer, self)
                .create(validated_data))


class ClientAccountUpdateSerializer(NoCreateModelSerializer):
    """
    Updatable ClientAccount Serializer
    """
    question_one = serializers.IntegerField(required=True)
    answer_one = serializers.CharField(required=True)
    question_two = serializers.IntegerField(required=True)
    answer_two = serializers.CharField(required=True)

    class Meta:
        model = ClientAccount
        fields = (
            'account_name',
            'tax_loss_harvesting_status',

            'question_one',
            'answer_one',
            'question_two',
            'answer_two',
        )

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        # no user is create request for initial registration

        # SecurityAnswer checks
        if data.get('question_one') == data.get('question_two'):
            logger.error('ClientAccountUpdateSerializer given matching questions %s' % data.get('question_one'))
            raise serializers.ValidationError({'question_two': 'Questions must be unique'})

        try:
            sa1 = SecurityAnswer.objects.get(pk=data.get('question_one'))
            if sa1.user != user:
                logger.error('SecurityAnswer not found for user %s and question %s with ClientAccountUpdateSerializer' % (user.email, data.get('question_one')))
                raise serializers.ValidationError({'question_one': 'User does not own given question'})
        except:
            logger.error('ClientAccountUpdateSerializer question %s not found' % data.get('question_one'))
            raise serializers.ValidationError({'question_one': 'Question not found'})

        if not sa1.check_answer(data.get('answer_one')):
            logger.error('ClientAccountUpdateSerializer answer two was wrong')
            raise serializers.ValidationError({'answer_one': 'Wrong answer'})

        try:
            sa2 = SecurityAnswer.objects.get(pk=data.get('question_two'))
            if sa2.user != user:
                logger.error('SecurityAnswer not found for user %s and question %s with ClientAccountUpdateSerializer' % (user.email, data.get('question_two')))
                raise serializers.ValidationError({'question_two': 'User does not own given question'})
        except:
            logger.error('ClientAccountUpdateSerializer question %s not found' % data.get('question_two'))
            raise serializers.ValidationError({'question_two': 'Question not found'})

        if not sa2.check_answer(data.get('answer_two')):
            logger.error('ClientAccountUpdateSerializer answer two was wrong')
            raise serializers.ValidationError({'answer_two': 'Wrong answer'})

        return data


class CloseAccountRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = CloseAccountRequest
        fields = ('account', 'close_choice', 'account_transfer_form')

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        account_ids = [a.id for a in ClientAccount.objects.filter(primary_owner__user=user)]
        if data['account'].id not in account_ids:
            raise serializers.ValidationError({'account': 'User does not own account'})
        if data['close_choice'] == 1:
            # internal transfer needs pdf
            if 'account_transfer_form' not in data:
                raise serializers.ValidationError({'account_transfer_form': 'Account transfer form pdf file required for account transfer'})
        return data
