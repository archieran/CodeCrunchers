from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Student = "S"
    Candidate = "C"
    Employer = "E"
    Faculty = "F"
    USER_TYPES = (
    (Student, "Student"),
    (Candidate, "Candidate"),
    (Employer, "Employer"),
    (Faculty, "Faculty"),
    )
    user_type = models.CharField(max_length=255, choices=USER_TYPES, default=Student)

    def __unicode__(self):
        return self.user.username
