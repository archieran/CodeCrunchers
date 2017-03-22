from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
def get_user_avatar_name(instance, filename):
    print filename
    parts = filename.split('.')
    extension = parts[-1]
    print extension
    new_name = 'profileimages/' + str(instance.user) + '.' + extension
    return new_name
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
    user_avatar = models.ImageField(upload_to = get_user_avatar_name, default='profileimages/anonymous.jpg')
    experience_points = models.IntegerField(default=0, verbose_name="Experience Points")
    def __unicode__(self):
        return self.user.username
