# MODEL
from django.db import models
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


# Task Model
class Task(models.Model):
    """
    A model representing a task with a title, content, status, and timestamps.
    """
    TASK_STATUS = [
        ('completed', 'Completed'), 
        ('in-progress', 'In-progress')
    ]
    title       = models.CharField(max_length=100)
    content     = models.TextField()
    created_at  = models.DateTimeField(default=timezone.now)
    updated_at  = models.DateTimeField(auto_now=True)
    status      = models.CharField(max_length=20, choices=TASK_STATUS, default='in-progress')
    owner       = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    # def save(self, **kwargs):
    #     pass


    def __str__(self) -> str:
        """Return the title of the task."""
        return self.title



# Token Model
class Token(models.Model):
    key = models.CharField(
        max_length=40,  # Maximum length of 40 characters
        primary_key=True,
        validators=[
            MinLengthValidator(40),  # Minimum length of 40 characters
        ]
    )
    user    = models.OneToOneField(User, on_delete=models.CASCADE,                related_name='auth_token')
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
    

    def revoke_token(self):
        """
        Revokes the token, setting it to inactive.
        This approach is more robust than deleting the token immediately,
        as it allows for tracking the token's history. You can run a cron job 
        to delete tokens that have been inactive for more than a week.
        """
        self.is_active = False
        self.save()


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



