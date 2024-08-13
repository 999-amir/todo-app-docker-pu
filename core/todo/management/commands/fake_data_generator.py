from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import datetime
from accounts.models import CostumeUser, ProfileModel
from todo.models import TodoModel

level = ['green', 'orange', 'red']
is_done = [True, False]


class Command(BaseCommand):
    help = 'generate 10 fake user + 10 todo task for each user'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        for _ in range(10):
            user = CostumeUser.objects.create_user(email=self.fake.email(), password='Aaa123##')
            user.is_verify = True
            user.save()
            profile = ProfileModel.objects.get(user=user)
            profile.f_name, profile.l_name = self.fake.first_name(), self.fake.last_name()
            profile.description = self.fake.paragraph(nb_sentences=5)
            profile.save()

            for _ in range(10):
                TodoModel.objects.create(profile=profile, level=random.choice(level),
                                         job=self.fake.paragraph(nb_sentences=3),
                                         is_done=random.choice(is_done), dead_end=datetime.now())
