from django.db import models

# Create your models here.
# MODEL
from django.contrib.auth.models import User

# PERFORMANCE
from django.utils.translation import gettext_lazy as _

# ENCRYPTION
import binascii
import os

# TIME
from django.utils import timezone
from datetime import timedelta

# VALIDATORS
from django.core.validators import MinLengthValidator




# Token Model
class Token(models.Model):
    key = models.CharField(
        max_length=40,  # Maximum length of 40 characters
        primary_key=True,
        validators=[
            MinLengthValidator(40),  # Minimum length of 40 characters
        ]
    )
    user    = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_token')
    created_at  = models.DateTimeField(auto_now_add=True)
    is_active   = models.BooleanField(default=True, blank=True)
    expires_at  = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()

        if self.expires_at is None:
            self.expires_at = timezone.now() + timedelta(days=7) #Token expires in 7days

        super().save(*args, **kwargs)


    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()
    

    def revoke_token(self, delete=False):
        """
        Revokes the token, setting it to inactive.
        This approach is more robust than deleting the token immediately,
        as it allows for tracking the token's history. You can run a cron job 
        to delete tokens that have been inactive for more than a week.
        """
        self.is_active = False
        self.save()

        if delete:
            self.delete()


    def expire_token(self, expire_at):
        """
        Set the expiration time for the token. 
        This will overwrite the default expiration time in days.

        eg: expire_token(10), would expire token 10days from now.
        """

        try:
            expire_at = int(expire_at)
            self.expires_at = timezone.now() + timedelta(days=expire_at)
            self.save()
        except ValueError:
            print('Error: expire_at value must be an integer type')
        

    @property
    def is_expired(self):
        """Checks if the token has expired."""
        return timezone.now() > self.expires_at if self.expires_at else False


    def __str__(self) -> str:
        return f'{self.key}'       



