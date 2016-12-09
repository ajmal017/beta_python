from __future__ import unicode_literals

from django import forms
from django.http import QueryDict
from django.utils.safestring import mark_safe

from advisors.models import ChangeDealerGroup, SingleInvestorTransfer, \
    BulkInvestorTransfer
from main.models import Firm, User, Section, Advisor


class ChangeDealerGroupForm(forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(required=False, widget=forms.SelectMultiple(attrs={"disabled": True}),
                                             queryset=None)

    class Meta:
        model = ChangeDealerGroup
        fields = ("advisor", "old_firm", "new_firm", "work_phone", "new_email", "letter_new_group",
                  "letter_previous_group", "signature", "clients")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        if "data" in kwargs:
            q = QueryDict('', mutable=True)
            q.update(kwargs["data"])
            initial = dict()
            initial["advisor"] = str(kwargs["initial"]["advisor"].pk)
            initial["old_firm"] = str(kwargs["initial"]["old_firm"].pk)
            q.update(initial)
            kwargs["data"] = q
        super(ChangeDealerGroupForm, self).__init__(*args, **kwargs)

        self.field_sections = [{"fields": ('new_firm', 'work_phone', 'new_email'),
                                "header": "New arrangements"},
                               {"fields": ('clients',),
                                "header": "Your current investors"},
                               {"fields": ('letter_previous_group',),
                                "header": "Previous Dealer Group Release Authorization",
                                "detail": mark_safe("A letter from your previous Dealer Group authorising the release "
                                                    "of your current investors. A template of this letter has been supplied, "
                                                    "This letter must be provided on the previous Dealer Group's "
                                                    "company letterhead. <a target='_blank' href='/static/docs/previous_dealer_group_release_authorization.pdf'>Example</a>")},
                               {"fields": ('letter_new_group',),
                                "header": "New Dealer Group Acceptance Authorization",
                                "detail": mark_safe("A letter from the new Dealer Group accepting the transfer of your "
                                                    "current investors. A template of this letter has been supplied. This letter"
                                                    "must be provided on the new Dealer Group's company letterhead. <a target='_blank' href='/static/docs/new_dealer_group_acceptance_authorization.pdf'>Example</a>")},
                               {"fields": ('signature',),
                                "header": "Advisor Signature",
                                "detail": mark_safe(
                                    "Please upload a signature approval by an Authorised Signatory of the new Dealer Group. <a target='_blank' href='/static/docs/advisor_signature_change_dealer_group.pdf'>Example</a>"),
                                }
                               ]
        self.fields["new_firm"].queryset = Firm.objects.exclude(pk=self.initial["old_firm"].pk)
        self.fields["clients"].queryset = self.initial["advisor"].clients

    def clean_new_email(self):
        email = self.cleaned_data["new_email"]
        if User.objects.exclude(pk=self.initial["advisor"].user.pk).filter(email=email).count():
            self._errors['new_email'] = "User with this email already exists"

        return email

    @property
    def sections(self):
        for section in self.field_sections:
            yield Section(section, self)


class SingleInvestorTransferForm(forms.ModelForm):
    class Meta:
        model = SingleInvestorTransfer
        fields = ("from_advisor", "to_advisor", "investor", "signatures",)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        if "data" in kwargs:
            q = QueryDict('', mutable=True)
            q.update(kwargs["data"])
            initial = dict()
            initial["from_advisor"] = str(kwargs["initial"]["from_advisor"].pk)
            q.update(initial)
            kwargs["data"] = q

        super(SingleInvestorTransferForm, self).__init__(*args, **kwargs)

        self.field_sections = [{"fields": ('to_advisor',),
                                "header": "To Advisor"},
                               {"fields": ('investor',),
                                "header": "Investor"},
                               {"fields": ('signatures',),
                                "header": "Signatures",
                                "detail": mark_safe("Signatures of the investor and the previous advisor: if this is "
                                                    "for a Joint Account the signature of the second  investor "
                                                    "is required. <a target='_blank' href='/static/docs/advisor_single_transferer_signatures.pdf'>Example</a>")},
                               ]

        self.fields["investor"].queryset = self.initial["from_advisor"].clients
        self.fields["to_advisor"].queryset = Advisor.objects.filter(firm=self.initial["from_advisor"].firm)

    @property
    def sections(self):
        for section in self.field_sections:
            yield Section(section, self)


class BulkInvestorTransferForm(forms.ModelForm):
    class Meta:
        model = BulkInvestorTransfer
        fields = ("from_advisor", "to_advisor", "investors", "signatures",)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        if "data" in kwargs:
            q = QueryDict('', mutable=True)
            q.update(kwargs["data"])
            initial = dict()
            initial["from_advisor"] = str(kwargs["initial"]["from_advisor"].pk)
            q.update(initial)
            kwargs["data"] = q

        super(BulkInvestorTransferForm, self).__init__(*args, **kwargs)

        self.field_sections = [{"fields": ('to_advisor',),
                                "header": "To Advisor"},
                               {"fields": ('investors',),
                                "detail": "You can select 2 or more investors for transfer",
                                "header": "Investors"},
                               {"fields": ('signatures',),
                                "header": "Signatures",
                                "detail": mark_safe("Signatures of the previous advisor and new advisor."
                                                    " <a target='_blank' href='/static/docs/advisor_bulk_transferer_signatures.pdf'>Example</a>")},
                               ]

        self.fields["investors"].queryset = self.initial["from_advisor"].clients
        self.fields["to_advisor"].queryset = Advisor.objects.filter(firm=self.initial["from_advisor"].firm)

    def clean_investors(self):
        investors = self.cleaned_data["investors"]
        if len(investors) < 2:
            self._errors["investors"] = "Please select 2 or more investors"
        return investors

    @property
    def sections(self):
        for section in self.field_sections:
            yield Section(section, self)
