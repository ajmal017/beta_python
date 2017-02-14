import logging
from django.db import models
from weasyprint import HTML
from django.conf import settings
from io import BytesIO
from django.core.files.base import ContentFile
from main.settings import BASE_DIR
from functools import reduce
from main import constants
from retiresmartz.models import RetirementPlan
from statements import utils
logger = logging.getLogger(__name__)


class PDFStatement(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(null=True, blank=True)

    @property
    def date(self):
        return self.create_date.strftime('%Y-%m-%d_%H:%I:%S')

    def render_template(self, template_name=None):
        from django.template.loader import render_to_string
        template_name = template_name or self.default_template
        return render_to_string(template_name, {
            'object': self,
            'statement': self,
            'account': self.account,
            'client': self.client,
            'owner': self.client,
            'advisor': self.client.advisor,
            'firm': self.client.advisor.firm,
        })

    def render_pdf(self, template_name=None):
        html = self.render_template(template_name)
        # Have to source the images locally for WeasyPrint
        static_path = settings.STATICFILES_DIRS[0]
        html = html.replace('/static/', 'file://%s/' % static_path)
        html = html.replace('/media/', 'file://%s/media/' % BASE_DIR)
        pdf_builder = HTML(string=html)
        return pdf_builder.write_pdf()

    def save(self, *args, **kwargs):
        super(PDFStatement, self).save(*args, **kwargs)
        if not self.pdf:
            bio = BytesIO(self.render_pdf())
            self.pdf.save('%s.pdf' % self.account,
                          ContentFile(bio.getvalue()))

    @property
    def default_template(self):
        return None

    @property
    def client(self):
        return self.account.primary_owner

    class Meta:
        abstract = True
        ordering = ('-create_date', )


class StatementOfAdvice(PDFStatement):
    account = models.OneToOneField('client.ClientAccount', related_name='statement_of_advice')

    def __str__(self):
        return 'Statement of Advice for %s' % self.account

    @property
    def default_template(self):
        return "statements/statement_of_advice.html"


class RetirementStatementOfAdvice(PDFStatement):
    retirement_plan = models.OneToOneField('retiresmartz.RetirementPlan', related_name='statement_of_advice')

    def __str__(self):
        return 'Statement of Advice for %s' % self.retirement_plan

    @property
    def account(self):
        return None

    @property
    def client(self):
        return self.retirement_plan.client

    @property
    def default_template(self):
        return "statements/retirement_statement_of_advice/index.html"

    def render_template(self, template_name=None):
        from django.template.loader import render_to_string
        template_name = template_name or self.default_template
        plan = self.retirement_plan
        retirement_accounts = plan.retirement_accounts if plan.retirement_accounts else []

        retirement_income_graph = {
            'estimated': { 'y': 0, 'h': 100 },
            'target': { 'y': 30, 'h': 70 }
        }
        iraTypes = [
            constants.ACCOUNT_TYPE_IRA,
            constants.ACCOUNT_TYPE_ROTHIRA,
            constants.ACCOUNT_TYPE_SIMPLEIRA,
            constants.ACCOUNT_TYPE_SARSEPIRA,
        ]
        client_retirement_accounts = list(filter(lambda item: item['owner'] == 'self', retirement_accounts))
        partner_retirement_accounts = list(filter(lambda item: item['owner'] == 'partner', retirement_accounts))
        ira_retirement_accounts = filter(lambda item: item['acc_type'] in iraTypes, retirement_accounts)
        has_partner = self.client.is_married and plan.partner_data

        return render_to_string(template_name, {
            'object': self,
            'statement': self,
            'client': self.client,
            'owner': self.client,
            'advisor': self.client.advisor,
            'firm': self.client.advisor.firm,
            'plan': plan,
            'has_partner': has_partner,
            'partner_name': plan.partner_data['name'] if has_partner else '',
            'lifestyle_stars': range(plan.lifestyle + 2),
            'retirement_income_graph': retirement_income_graph,
            'sum_of_retirement_accounts': reduce(lambda acc, item: acc + item['balance'], retirement_accounts, 0),
            'sum_of_retirement_accounts_ira': reduce(lambda acc, item: acc + item['balance'], ira_retirement_accounts, 0),
            'lifestyle_box': utils.get_lifestyle_box(self.client),
            'client_retirement_accounts': client_retirement_accounts,
            'partner_retirement_accounts': partner_retirement_accounts,
            'waterfall_chart': utils.get_waterfall_chart(plan)
        })

class RecordOfAdvice(PDFStatement):
    account = models.ForeignKey('client.ClientAccount', related_name='records_of_advice')

    def __str__(self):
        return 'Record of Advice %s %s' % (self.account, self.date)

    @property
    def default_template(self):
        return "statements/record_of_advice.html"
