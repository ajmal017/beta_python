from django.contrib import messages
from django.contrib.auth import (
    logout as auth_logout,
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    login as auth_views_login,
)
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


@never_cache
@csrf_protect
@sensitive_post_parameters()
def login(request, template_name='registration/login.html',
          authentication_form=AuthenticationForm,
          extra_context=None):

    # TODO: maybe to add expected user role (based on url) to extra_context 
    response = auth_views_login(request,
                                authentication_form=authentication_form,
                                extra_context=extra_context)

    user = request.user

    if user.is_authenticated():
        # custom extra checking 

        # TODO: temp temp temp
        # TODO: discuss "confirmation" feature
        # it should be deeply refactored in the first place
        # we need to (also) use "is_active" user flag for that stuff
        is_confirmed = (
            user.is_client and user.client.is_confirmed or
            user.is_advisor and user.advisor.is_confirmed or
            user.is_authorised_representative and
            user.authorised_representative.is_confirmed
        )

        if not is_confirmed:
            messages.error(request, 'Your account has not been confirmed yet.')
            form = authentication_form(request)
            context = {'form': form}

            return TemplateResponse(request, template_name, context)

        # custom redirect
        redirect_to = request.GET.get('next',
                                      reverse_lazy('client:app',
                                                   args=(user.client.id,))
                                      if user.is_client
                                      else reverse_lazy('advisor:overview')
                                      if user.is_advisor
                                      else reverse_lazy('firm:overview')
                                      if user.is_authorised_representative
                                      else None)

        if redirect_to:
            response = HttpResponseRedirect(redirect_to)

    return response


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))
