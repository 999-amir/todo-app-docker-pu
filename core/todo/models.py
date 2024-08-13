from django.db import models
from accounts.models import ProfileModel


class TodoModel(models.Model):
    LEVELS = (("green", "easy"), ("orange", "medium"), ("red", "hard"))

    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, default="easy", choices=LEVELS)
    job = models.TextField(max_length=200)
    is_done = models.BooleanField(default=False)
    dead_end = models.DateField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.profile)

    def get_snippet(self):
        return self.job[:20]
