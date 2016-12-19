import logging

import requests
from django.conf import settings
from django.db import models
from jsonfield.fields import JSONField

from common.structures import ChoiceEnum

logger = logging.getLogger(__name__)


class ErrorLog(models.Model):
    class ErrorSource(ChoiceEnum):
        WebApp = 1, 'WebApp'
        Backend = 2, 'Backend'
        FrontEnd = 3, 'FrontEnd'

        def __str__(self):
            return self.human_name

    source = models.IntegerField(choices=ErrorSource.choices())
    user = models.ForeignKey('main.User', blank=True, null=True,
                             related_name='logged_ui_errors')
    header = models.CharField(max_length=100)
    message = models.TextField()
    url = models.URLField()
    details = JSONField(blank=True, null=True)  # dict
    version = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    jira_ticket = models.ForeignKey('JiraTicket', blank=True, null=True)

    def __str__(self):
        msg = "{source}: {title}"
        if self.jira_ticket:
            msg += " ({jira_ticket})"
        return msg.format(source=self.get_source_display(),
                          title=self.header,
                          jira_ticket=self.jira_ticket)


class JiraTicket(models.Model):
    ticket = models.URLField(blank=True, null=True)
    header = models.CharField(max_length=100)
    message = models.TextField()
    task = models.CharField(max_length=100)

    class Meta:
        index_together = 'header', 'message'

    def __str__(self):
        return self.task

    @classmethod
    def create(cls, error: ErrorLog) -> 'JiraTicket':
        try:
            details = '\n'.join(
                '%s: %s' % (k, v) for k, v in error.details.items())
        except (AttributeError, TypeError):
            details = ''
        # TODO auth
        response = requests.post(
            url='https://betasmartz.atlassian.net/rest/api/2/issue',
            json={
                "fields": {
                    "project": {
                        "id": settings.JIRA_ERROR_PROJECT_ID,
                    },
                    "summary": error.header,
                    "description": error.message,
                    "issuetype": {
                        "id": settings.JIRA_ISSUE_TYPE_ID,
                    },
                    "labels": [
                        error.get_source_display(),
                    ],
                    "environment": details,
                }
            }
        )
        if response.status_code == 200:
            return cls.objects.create(message=error.message,
                                      ticket=response.content)
        logger.error('Cannot create a JIRA ticket %d(%s)',
                     response.status_code, response.content)
