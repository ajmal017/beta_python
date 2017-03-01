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
    return render(request, 'healthdevice.html', context)

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
    return render(request, 'healthdevice.html', context)

def microsoft_health(request):
    user = SupportRequest.target_user(request)
    code = request.GET.get('code', None)
    status = False
    if code is not None:
        status = healthdevice.microsofthealth_connect(user.client, code)

    context = {
        'provider': HealthDevice.ProviderType.MICROSOFT_HEALTH.value,
        'status': status
    }
    return render(request, 'healthdevice.html', context)

def under_armour(request):
    user = SupportRequest.target_user(request)
    code = request.GET.get('code', None)
    status = False
    if code is not None:
        status = healthdevice.underarmour_connect(user.client, code)

    context = {
        'provider': HealthDevice.ProviderType.UNDERARMOUR.value,
        'status': status
    }
    return render(request, 'healthdevice.html', context)

def jawbone(request):
    user = SupportRequest.target_user(request)
    code = request.GET.get('code', None)
    status = False
    if code is not None:
        status = healthdevice.jawbone_connect(user.client, code)

    context = {
        'provider': HealthDevice.ProviderType.JAWBONE.value,
        'status': status
    }
    return render(request, 'healthdevice.html', context)
