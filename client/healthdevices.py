from client.models import HealthDevice
from datetime import datetime, timedelta
from support.models import SupportRequest
from main.settings import FITBIT_SETTINGS
import base64
import urllib.request as urllib2
import urllib
import json

# def create_access_token(request):
#     user = SupportRequest.target_user(request)
#     provider_type = request.data.get('provider', None)
#     data = request.data.get('data', None)
#
#     provider_types = list(map(lambda item: item[0], HealthDevice.ProviderType.choices()))
#     if provider_type not in provider_types:
#         return { 'error': 'Unknown provider' }
#
#     try:
#         healthdevice = user.client.health_device
#     except:
#         healthdevice = HealthDevice(client=user.client, provider=provider_type)
#
#     if provider_type == HealthDevice.ProviderType.FITBIT.value:
#         healthdevice.provider = provider_type
#         healthdevice = store_fitbit(healthdevice, data)
#         healthdevice.save()
#         return 'ok'
#
#     return { 'error': 'Not yet implemented' }
#
# def store_fitbit(healthdevice, data):
#     authd_client = fitbit.Fitbit(FITBIT_SETTINGS['CLIENT_ID'], FITBIT_SETTINGS['CLIENT_SECRET'],
#                                  access_token=healthdevice.token)
#     res = authd_client.client.fetch_access_token(data['code'])
#     print(res)
#     healthdevice.token = res['access_token']
#     healthdevice.expires_at = datetime.now() + timedelta(seconds=int(res['expires_in']))
#     healthdevice.meta = {
#         'scope': res['scope'],
#         'token_type': res['token_type'],
#         'user_id': res['user_id']
#     }
#     return healthdevice

def get_data(request):
    user = SupportRequest.target_user(request)
    try:
        healthdevice = user.client.health_device
    except:
        return None
    if healthdevice.provider == HealthDevice.ProviderType.FITBIT.value:
        return get_fitbit(healthdevice)

    return None

def get_fitbit(healthdevice):
    #This is the Fitbit URL
    profile_url = "https://api.fitbit.com/1/user/-/profile.json"

    #Start the request
    req = urllib2.Request(profile_url)

    req.add_header('Authorization', 'Bearer ' + healthdevice.token)

    #Fire off the request
    try:
        response = urllib2.urlopen(req)
        full_response = response.read()
        print(full_response)
        res = json.loads(full_response.decode("utf-8"))
        return {
            'id': healthdevice.id,
            'height': res['user']['height'],
            'weight': res['user']['weight']
        }
    except urllib2.URLError as e:
        print(e.code)
        print(e.read())
        return None
