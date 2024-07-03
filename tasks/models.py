from django.db import models
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

# Create your models here.
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
    description     = models.TextField()
    created_at  = models.DateTimeField(default=timezone.now)
    updated_at  = models.DateTimeField(auto_now=True)
    status      = models.CharField(max_length=20, choices=TASK_STATUS, default='in-progress')
    owner       = models.ForeignKey(User, on_delete=models.CASCADE)

    # class Meta:
    #     ordering = ['-created_at']

    # def save(self, **kwargs):
    #     pass


    def __str__(self) -> str:
        """Return the title of the task."""
        return self.title
