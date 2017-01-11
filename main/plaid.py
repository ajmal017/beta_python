from django.conf import settings
from main.models import PlaidUser
import os
import requests
import logging
logger = logging.getLogger('main.plaid')

from plaid import Client as PlaidClient
PlaidClient.config({
    'url': settings.PLAID_DEVELOPMENT_URL
})


client_id = settings.PLAID_CLIENT_ID
public_key = settings.PLAID_PUBLIC_KEY
secret = settings.PLAID_SECRET

def create_access_token(django_user, public_token):
    client = PlaidClient(client_id=client_id, secret=secret)
    resp = client.exchange_token(public_token)
    if resp.status_code != 200:
        logger.error("Unable to exchange public token for access token for user {0}".format(
            django_user
        ))
        return None

    # else "client.access_token" should now be populated with
    # a valid access_token for making authenticated requests

    # Get the plaid user for this django user; make one if nec.
    if not getattr(django_user, 'plaid_user', False):
        plaid_user = PlaidUser(user=django_user)
        plaid_user.save()

    plaid_user = django_user.plaid_user
    plaid_user.access_token = client.access_token
    plaid_user.save()
    return True


def get_accounts(django_user):
    
    plaid_user = getattr(django_user, 'plaid_user', False)
    if not plaid_user:
        logger.error("There is no Plaid user corresponding to user {0}".format(
            django_user
        ))
        return None

    # else
    access_token = getattr(plaid_user, 'access_token', False)
    if not access_token:
        logger.error("User {0} has a Plaid User but no access token".format(
            django_user
        ))
        return None

    # else
    client = PlaidClient(client_id=client_id, secret=secret, access_token=access_token)
    resp = client.auth_get()
    if resp.status_code != 200:
        logger.error("Unable to retrieve client accounts for user {0}".format(
            django_user
        ))
        return None

    # else
    return resp.json()['accounts']
