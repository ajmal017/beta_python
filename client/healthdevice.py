from client.models import HealthDevice
from django.conf import settings
from datetime import datetime, timedelta
from support.models import SupportRequest
from main.settings import FITBIT_SETTINGS
import base64
import urllib.request as urllib2
import urllib
import json

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
    print(res)
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
        healthdevice.token = res['access_token']
        healthdevice.refresh_token = res['refresh_token']
        healthdevice.expires_at = datetime.now() + timedelta(seconds=int(res['expires_in']))
        healthdevice.meta = {
            'scope': res['scope'],
            'token_type': res['token_type'],
            'user_id': res['user_id']
        }
        healthdevice.save()
        print(res)
        return True
    except urllib2.URLError as e:
        print(e.code)
        print(e.read())
        return False


def fitbit_get_data(healthdevice):
    #This is the Fitbit URL
    profile_url = '{}/1/user/-/profile.json'.format(FITBIT_SETTINGS['API_BASE'])
    activity_url = '{}/1/user/-/activities/goals/daily.json'.format(FITBIT_SETTINGS['API_BASE'])

    try:
        #Start the request
        req = urllib2.Request(profile_url)
        req.add_header('Authorization', 'Bearer ' + healthdevice.token)
        res = get_json_response(req)
        if fitbit_should_refresh_token(res):
            fitbit_refresh_token(healthdevice)
            res = get_json_response(req)

        height = float(res['user']['height'])
        weight = float(res['user']['weight'])
        h_mul = 0.3048 if res['user']['heightUnit'] == 'en_US' else 1 # feet to cm
        w_mul = 0.453592 if res['user']['weightUnit'] == 'en_US' else 1 # oz to kg

        req = urllib2.Request(activity_url)
        req.add_header('Authorization', 'Bearer ' + healthdevice.token)
        response = urllib2.urlopen(req)
        full_response = response.read()
        res = json.loads(full_response.decode("utf-8"))

        activeMinutes = res['goals']['activeMinutes']

        return {
            'id': healthdevice.id,
            'height': round(height / h_mul, 1),
            'weight': round(weight / w_mul, 1),
            'daily_exercise': activeMinutes
        }
    except urllib2.URLError as e:
        print(e.code)
        print(e.read())
        return None
