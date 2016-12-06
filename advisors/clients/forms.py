from __future__ import unicode_literals

from django import forms

from client.models import EmailInvite

from main.models import User

class EmailInviteForm(forms.ModelForm):
    class Meta:
        model = EmailInvite
        fields = 'first_name', 'middle_name', 'last_name', 'email', 'reason'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                u'Email "%(email)s" is already in use',
                params={'email': email},
            )
        if EmailInvite.objects.filter(email=email).exists():
            raise forms.ValidationError(
                u'Invitation has already been sent to "%(email)s"',
                params={'email': email},
            )
        return email
