from django.contrib.auth.models import BaseUserManager


class CostumeUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("!!! need your email to create account !!!")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
