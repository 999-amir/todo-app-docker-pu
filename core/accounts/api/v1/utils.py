from django.conf import settings
from mail_templated import EmailMessage
import threading



class EmailThreading(threading.Thread):
    def __init__(self, email_obj):
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send()


def send_threading_email(tpl_file_directory, data, to_user):
    email_obj = EmailMessage(tpl_file_directory, data, settings.EMAIL_HOST_USER, [to_user])
    EmailThreading(email_obj).start()
