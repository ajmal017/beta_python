from django.shortcuts import render
from client.models import HealthDevice
from datetime import datetime, timedelta
from support.models import SupportRequest
from main.settings import FITBIT_SETTINGS
import base64
import urllib.request as urllib2
import urllib
import json

def connect_fitbit(request):
    user = SupportRequest.target_user(request)
    code = request.GET.get('code', None)
    status = False
    try:
        healthdevice = user.client.health_device
    except:
        healthdevice = HealthDevice(client=user.client)

    if code is not None:

        #This is the Fitbit URL
        TokenURL = "https://api.fitbit.com/oauth2/token"


        #Form the data payload
        BodyText = {'code' : code,
                    'redirect_uri' : 'http://local.betasmartz.com/oauth2/health-devices/fitbit/',
                    'client_id' : FITBIT_SETTINGS['CLIENT_ID'],
                    'grant_type' : 'authorization_code'}

        BodyURLEncoded = urllib.parse.urlencode(BodyText)
        print(BodyURLEncoded)

        #Start the request
        req = urllib2.Request(TokenURL,BodyURLEncoded.encode('utf-8'))

        #Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
        print(bytes('Basic ', 'utf-8') + base64.b64encode(bytes(FITBIT_SETTINGS['CLIENT_ID'] + ":" + FITBIT_SETTINGS['CLIENT_SECRET'], 'utf-8')))
        req.add_header('Authorization', bytes('Basic ', 'utf-8') + base64.b64encode(bytes(FITBIT_SETTINGS['CLIENT_ID'] + ":" + FITBIT_SETTINGS['CLIENT_SECRET'], 'utf-8')))
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')

        #Fire off the request
        try:
            response = urllib2.urlopen(req)
            FullResponse = response.read()
            print(FullResponse)
            res = json.loads(FullResponse.decode("utf-8"))
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
            status = True
        except urllib2.URLError as e:
            print(e.code)
            print(e.read())

    context = {
        'provider': HealthDevice.ProviderType.FITBIT.value,
        'status': status
    }
    return render(request, 'healthdevices/fitbit.html', context)
