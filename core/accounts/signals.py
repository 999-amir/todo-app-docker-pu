from django.db.models.signals import post_save, post_delete
from .models import CostumeUser, ProfileModel
from django.dispatch import receiver


@receiver(post_save, sender=CostumeUser)
def create_profile(sender, **kwargs):
    """
    this function will create profile after user created
    """
    user = kwargs["instance"]
    if kwargs["created"]:
        ProfileModel.objects.create(user=user)


@receiver(post_delete, sender=ProfileModel)
def delete_user(sender, **kwargs):
    """
    this function will delete user after Profile deleted
    """
    profile = kwargs["instance"]
    profile.user.delete()
