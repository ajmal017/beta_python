from rest_framework import permissions

from main.models import (
    Advisor, Client, #Firm, Company,
)


class IsAdvisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.is_advisor


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.is_client


class IsAdvisorOrClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated() and 
                (request.user.is_advisor or request.user.is_client))


# RESERVED
class IsMyAdvisorCompany(IsAdvisor):
    """
    Note: user is supposed to be Advisor only
    (could be extrended later)
    """
    def has_permission(self, request, view):
        user = request.user

        if not user.is_advisor:
            return True

        advisor = user.advisor

        if not advisor.company:
            # advisor should be associated with an advisor company
            return False

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user.is_advisor:
            return True

        advisor = user.advisor

        if isinstance(obj, Advisor):
            return obj.company == advisor.company

        #if isinstance(obj, Company):
        #    return obj == advisor.company

        if isinstance(obj, Client):
            # "get_clients" supposed to be role-awared
            try:
                advisor.get_clients().get(pk=obj.pk)
                return True
            except Client.DoesNotExist:
                return False

        #if isinstance(obj, Household):
        #    # "get_households" supposed to be role-awared
        #    try:
        #        advisor.get_households().get(pk=obj.pk)
        #        return True
        #    except Household.DoesNotExist:
        #        return False

        #if isinstance(obj, Portfolio):
        #    # "get_portfolios" supposed to be role-awared
        #    try:
        #        advisor.get_portfolios().get(pk=obj.pk)
        #        return True
        #    except Portfolio.DoesNotExist:
        #        return False

        else:
            # reserved
            pass


# RESERVED
class IsMyAdvisorCompanyCustom(IsMyAdvisorCompany):
    """
    Helper to be used for viewsets passing custom "object"

    Note: user is supposed to be Advisor only
    (could be extrended later)
    """
    def __init__(self, obj=None, *args, **kwargs):
        super(IsMyAdvisorCompanyCustom, self).__init__(*args, **kwargs)
        if obj:
            self.obj = obj

    def has_permission(self, request, view):
        if hasattr(self, 'obj'):
            return super(IsMyAdvisorCompanyCustom, self) \
                .has_object_permission(request, view, self.obj)

        return True

    def has_object_permission(self, request, view, obj):
        if hasattr(self, 'obj'):
            return True # already checked above (see "has_permission" function)

        return super(IsMyAdvisorCompanyCustom, self) \
            .has_object_permission(request, view, obj)


# RESERVED
def IsMyAdvisorCompanyCustomInit(obj):
    """
    Generate permission class with custom attributes.
    Supposed to be used for view sets passing custom "object"

    PS. Let's keep it capitalized to mimic a class.
    """
    IsMyAdvisorCompanyCustomClass = type(
        'IsMyAdvisorCompanyNested',
        (IsMyAdvisorCompanyCustom,),
        {'obj': obj},
    )

    return IsMyAdvisorCompanyCustomClass