from celery import shared_task
from accounts.models import CostumeUser
from datetime import datetime, timedelta

@shared_task
def delete_unverified_users_task():
    expire_time = datetime.now() - timedelta(minutes=1)
    CostumeUser.objects.filter(is_verify=False).delete()
    print('SHEDULED-TASK: unverified users (for more than 10 minute) are deleted')
