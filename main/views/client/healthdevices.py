from client import healthdevice
from client.models import HealthDevice
from datetime import datetime, timedelta
from django.shortcuts import render
from support.models import SupportRequest

def fitbit(request):
    user = SupportRequest.target_user(request)
    code = request.GET.get('code', None)
    status = False
    if code is not None:
        status = healthdevice.fitbit_connect(user.client, code)

    context = {
        'provider': HealthDevice.ProviderType.FITBIT.value,
        'status': status
    }
    return render(request, 'healthdevices/fitbit.html', context)

def google_fit(request):
    user = SupportRequest.target_user(request)
    code = request.GET.get('code', None)
    status = False
    if code is not None:
        status = healthdevice.googlefit_connect(user.client, code)

    context = {
        'provider': HealthDevice.ProviderType.GOOGLE_FIT.value,
        'status': status
    }
    return render(request, 'healthdevices/google_fit.html', context)
