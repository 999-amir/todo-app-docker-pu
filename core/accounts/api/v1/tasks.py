from celery import shared_task
from django.conf import settings
from mail_templated import EmailMessage


@shared_task
def send_email_task(tpl_file_directory, data, to_user):
    email_obj = EmailMessage(
        tpl_file_directory, data, settings.EMAIL_HOST_USER, [to_user]
    )
    email_obj.send()
