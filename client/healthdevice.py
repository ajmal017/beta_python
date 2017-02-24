from client.models import HealthDevice
from django.conf import settings
from datetime import datetime, timedelta
from support.models import SupportRequest
from main.settings import FITBIT_SETTINGS, GOOGLEFIT_SETTINGS, MICROSOFTHEALTH_SETTINGS
from apiclient.discovery import build
from oauth2client.client import OAuth2Credentials, OAuth2WebServerFlow
from MicrosoftHealth import MHOauth2Client, MH
from MicrosoftHealth.Exceptions import *
from functools import reduce
import base64
import urllib.request as urllib2
from urllib.parse import quote_plus
import urllib
import json
import httplib2
import pytz
from tzlocal import get_localzone

def get_json_response(req):
    response = urllib2.urlopen(req)
    full_response = response.read()
    return json.loads(full_response.decode("utf-8"))


def get_data(client):
    try:
        healthdevice = client.health_device
    except:
        return None
    if healthdevice.provider == HealthDevice.ProviderType.FITBIT.value:
        return fitbit_get_data(healthdevice)
    if healthdevice.provider == HealthDevice.ProviderType.GOOGLE_FIT.value:
        return googlefit_get_data(healthdevice)
    if healthdevice.provider == HealthDevice.ProviderType.MICROSOFT_HEALTH.value:
        return microsofthealth_get_data(healthdevice)

    return None


# FITBIT module
def fitbit_connect(client, code):
    try:
        healthdevice = client.health_device
    except:
        healthdevice = HealthDevice(client=client)

    token_url = '{}/oauth2/token'.format(FITBIT_SETTINGS['API_BASE'])

    #Form the data payload
    body_text = {'code' : code,
                'redirect_uri' : '{}/oauth2/health-devices/fitbit/'.format(settings.SITE_URL),
                'client_id' : FITBIT_SETTINGS['CLIENT_ID'],
                'grant_type' : 'authorization_code'}

    return fitbit_save_fields(healthdevice, token_url, body_text)


def fitbit_refresh_token(healthdevice):
    token_url = '{}/oauth2/token'.format(FITBIT_SETTINGS['API_BASE'])
    #Form the data payload
    body_text = {'grant_type' : 'refresh_token',
                 'refresh_token' : healthdevice.refresh_token,
                 'expires_in': FITBIT_SETTINGS['EXPIRES_IN']}

    return fitbit_save_fields(healthdevice, token_url, body_text)


def fitbit_get_redirect_uri():
    url = 'https://www.fitbit.com/oauth2/authorize'
    scope = '%20'.join([
        'activity',
        'profile',
        'weight'
    ])
    query = '&'.join([
        'response_type=code',
        'client_id={}'.format(FITBIT_SETTINGS['CLIENT_ID']),
        'redirect_uri={}%2Foauth2%2Fhealth-devices%2Ffitbit%2F'.format(settings.SITE_URL),
        'scope={}'.format(scope),
        'expires_in={}'.format(FITBIT_SETTINGS['EXPIRES_IN'])
    ])
    return '{}?{}'.format(url, query)


def fitbit_should_refresh_token(res):
    return 'success' in res and not res['success'] and res['errors']['errorType'] == 'expired_token'


def fitbit_save_fields(healthdevice, url, body_text):
    body_url_encoded = urllib.parse.urlencode(body_text)

    #Start the request
    req = urllib2.Request(url, body_url_encoded.encode('utf-8'))

    #Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
    req.add_header('Authorization', bytes('Basic ', 'utf-8') + base64.b64encode(bytes(FITBIT_SETTINGS['CLIENT_ID'] + ":" + FITBIT_SETTINGS['CLIENT_SECRET'], 'utf-8')))
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')

    #Fire off the request
    try:
        res = get_json_response(req)
        healthdevice.provider = HealthDevice.ProviderType.FITBIT.value
        healthdevice.access_token = res['access_token']
        healthdevice.refresh_token = res['refresh_token']
        healthdevice.expires_at = datetime.now() + timedelta(seconds=int(res['expires_in']))
        healthdevice.meta = {
            'scope': res['scope'],
            'token_type': res['token_type'],
            'user_id': res['user_id']
        }
        healthdevice.save()
        return True
    except urllib2.URLError as e:
        print(e.code)
        print(e.read())
        return False


def fitbit_get_data(healthdevice):
    #These are the Fitbit URLs
    profile_url = '{}/1/user/-/profile.json'.format(FITBIT_SETTINGS['API_BASE'])
    activity_url = '{}/1/user/-/activities/goals/daily.json'.format(FITBIT_SETTINGS['API_BASE'])

    try:
        #Start the request
        req = urllib2.Request(profile_url)
        req.add_header('Authorization', 'Bearer ' + healthdevice.access_token)
        res = get_json_response(req)
        if fitbit_should_refresh_token(res):
            fitbit_refresh_token(healthdevice)
            res = get_json_response(req)

        height = float(res['user']['height'])
        weight = float(res['user']['weight'])
        h_mul = 0.3048 if res['user']['heightUnit'] == 'en_US' else 1 # feet to cm
        w_mul = 0.453592 if res['user']['weightUnit'] == 'en_US' else 1 # oz to kg

        req = urllib2.Request(activity_url)
        req.add_header('Authorization', 'Bearer ' + healthdevice.access_token)
        response = urllib2.urlopen(req)
        full_response = response.read()
        res = json.loads(full_response.decode("utf-8"))

        active_minutes = res['goals']['activeMinutes']

        return {
            'id': healthdevice.id,
            'height': round(height / h_mul, 1),
            'weight': round(weight / w_mul, 1),
            'daily_exercise': active_minutes
        }
    except urllib2.URLError as e:
        print(e.code)
        print(e.read())
        return None


# Google Fit module
google_scopes = [
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.body.read',
    'https://www.googleapis.com/auth/fitness.body.write',
    'https://www.googleapis.com/auth/fitness.reproductive_health.read',
]

def googlefit_get_redirect_uri():
    url = 'https://accounts.google.com/o/oauth2/v2/auth'
    query = '&'.join([
        'prompt=consent',
        'response_type=code',
        'client_id={}'.format(GOOGLEFIT_SETTINGS['CLIENT_ID']),
        'redirect_uri={}/oauth2/health-devices/google-fit/'.format(settings.SITE_URL),
        'scope={}'.format('+'.join(google_scopes)),
        'access_type=offline'
    ])
    return '{}?{}'.format(url, query)


def googlefit_connect(client, code):
    try:
        healthdevice = client.health_device
    except:
        healthdevice = HealthDevice(client=client)

    flow = OAuth2WebServerFlow(GOOGLEFIT_SETTINGS['CLIENT_ID'],
                               GOOGLEFIT_SETTINGS['CLIENT_SECRET'],
                               google_scopes,
                               '{}/oauth2/health-devices/google-fit/'.format(settings.SITE_URL))
    try:
        credentials = flow.step2_exchange(code)

        healthdevice.provider = HealthDevice.ProviderType.GOOGLE_FIT.value
        healthdevice.access_token = credentials.access_token
        healthdevice.refresh_token = credentials.refresh_token
        healthdevice.expires_at = credentials.access_token_expiry
        healthdevice.meta = {}
        healthdevice.save()
        return True
    except:
        return False


def to_nano_epoch(dt):
    return int(round(dt.timestamp() * 1000000000))


def googlefit_get_data(healthdevice):
    height_source = 'derived:com.google.height:com.google.android.gms:merge_height'
    weight_source = 'derived:com.google.weight:com.google.android.gms:merge_weight'
    activity_source = 'derived:com.google.activity.segment:com.google.android.gms:merge_activity_segments'
    # The ID is formatted like: "startTime-endTime" where startTime and endTime are
    # 64 bit integers (epoch time with nanoseconds).
    DATA_SET = "0-{}".format(to_nano_epoch(datetime.now()))

    credentials = OAuth2Credentials(healthdevice.access_token,
                      GOOGLEFIT_SETTINGS['CLIENT_ID'],
                      GOOGLEFIT_SETTINGS['CLIENT_SECRET'],
                      healthdevice.refresh_token,
                      healthdevice.expires_at,
                      'https://accounts.google.com/o/oauth2/token', # token_uri
                      None) # user_agent

    http = httplib2.Http()
    http = credentials.authorize(http)
    fitness_service = build('fitness', 'v1', http=http, cache_discovery=False)

    res = fitness_service.users().dataSources().datasets(). \
              get(userId='me', dataSourceId=height_source, datasetId=DATA_SET, limit=1). \
              execute()
    height = res['point'][0]['value'][0]['fpVal'] * 100 if len(res['point']) > 0 else 0

    res = fitness_service.users().dataSources().datasets(). \
              get(userId='me', dataSourceId=weight_source, datasetId=DATA_SET, limit=1). \
              execute()
    weight = res['point'][0]['value'][0]['fpVal'] if len(res['point']) > 0 else 0

    activity_data_set = '{}-{}'.format(to_nano_epoch(datetime.now() - timedelta(days=7)), to_nano_epoch(datetime.now()))
    res = fitness_service.users().dataSources().datasets(). \
              get(userId='me', dataSourceId=activity_source, datasetId=activity_data_set). \
              execute()
    if len(res['point']) > 0:
        daily_exercise = reduce((lambda acc, item: acc + int(item['endTimeNanos'])-int(item['startTimeNanos'])), res['point'], 0) / 7
    else:
        daily_exercise = 0

    return {
        'id': healthdevice.id,
        'height': round(height, 1),
        'weight': round(weight, 1),
        'daily_exercise': round(daily_exercise / (1000000000 * 60)) # nano sec to minutes
    }


# Microsoft Health Module
microsoft_scopes = [
    'mshealth.ReadProfile',
    'mshealth.ReadActivityHistory',
]

microsoft_redirect_uri = '{}/oauth2/health-devices/microsoft-health/'.format(settings.SITE_URL)
def microsofthealth_get_redirect_uri():
    url = 'https://login.live.com/oauth20_authorize.srf'
    query = '&'.join([
        'response_type=code',
        'client_id={}'.format(MICROSOFTHEALTH_SETTINGS['CLIENT_ID']),
        'redirect_uri={}'.format(microsoft_redirect_uri),
        'scope={}'.format('+'.join(microsoft_scopes))
    ])
    return '{}?{}'.format(url, query)


def microsofthealth_connect(client, code):
    try:
        healthdevice = client.health_device
    except:
        healthdevice = HealthDevice(client=client)

    mh_oauth_object = MHOauth2Client(client_id = MICROSOFTHEALTH_SETTINGS['CLIENT_ID'],
                                   client_secret = MICROSOFTHEALTH_SETTINGS['CLIENT_SECRET'])

    try:
        token_info = mh_oauth_object.fetch_access_token(code, redirect_uri=microsoft_redirect_uri)
        print(token_info)
        healthdevice.provider = HealthDevice.ProviderType.MICROSOFT_HEALTH.value
        healthdevice.access_token = token_info['access_token']
        if 'refresh_token' in token_info:
            healthdevice.refresh_token = token_info['refresh_token']
        healthdevice.expires_at = datetime.now() + timedelta(seconds=int(token_info['expires_in']))
        healthdevice.meta = {
            'user_id': token_info['user_id']
        }
        healthdevice.save()
        return True
    except:
        return False


def microsofthealth_get_data(healthdevice):
    local_tz = get_localzone()
    dt_start = datetime.now() - timedelta(days=7)
    activity_url = '/v1/me/Summaries/daily?startTime={}Z'.format(dt_start.isoformat())
    try:
        mh_object = MH(microsoft_health_key = MICROSOFTHEALTH_SETTINGS['CLIENT_ID'],
                      microsoft_health_secret = MICROSOFTHEALTH_SETTINGS['CLIENT_SECRET'],
                      access_token = healthdevice.access_token,
                      refresh_token = healthdevice.refresh_token)
        profile = mh_object.user_profile_get(user_id=healthdevice.meta['user_id'])

        height = float(profile['height']) / 10
        weight = float(profile['weight']) / 1000
        daily_summary = mh_object.make_request(mh_object.API_ENDPOINT + activity_url)
        total_seconds = reduce(lambda acc, item: acc + (item['activeHours'] * 3600 if 'activeHours' in item else 0) + (item['activeSeconds'] if 'activeSeconds' in item else 0), daily_summary['summaries'], 0)
        return {
            'id': healthdevice.id,
            'height': round(height, 1),
            'weight': round(weight, 1),
            'daily_exercise': total_seconds / 60
        }
    except HTTPNotFound as e:
        return e
