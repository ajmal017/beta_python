from __future__ import absolute_import, unicode_literals
from .celery import app
from retiresmartz import models

@app.task
def send_plan_agreed_email_task(plan_id):
    """
    Send email to notify the plan is agreed along with the SOA attached.
    (called asynchronosly via Celery)
    """
    models.RetirementPlan._send_plan_agreed_email(plan_id)
