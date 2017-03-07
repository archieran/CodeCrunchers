from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Problem(models.Model):
    Expert = "X"
    Hard = "H"
    Easy = "E"
    Medium = "M"
    PROB_DIFFICULTY_LEVELS = (
        (Easy, "Easy"),
        (Medium, "Medium"),
        (Hard, "Hard"),
        (Expert, "Expert"),
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Problem creator")
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name="Title")
    desc = models.CharField(max_length=65535, null=False, blank=False, verbose_name="Description")
    model_solution = models.CharField(max_length=65535, verbose_name="Model solution")
    constraints = models.CharField(max_length=255, verbose_name="Constraints")
    input_format = models.CharField(max_length=255, verbose_name="Input format")
    output_format = models.CharField( max_length=255, verbose_name="Output format")
    startup_code = models.CharField(max_length=65535, verbose_name="Initial code")
    start_time = models.DateTimeField(verbose_name="Problem start time")
    end_time = models.DateTimeField(verbose_name="Problem end time")
    is_archived = models.BooleanField(default=False, verbose_name="Archived")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    difficulty = models.CharField(choices=PROB_DIFFICULTY_LEVELS, max_length=255, default=Easy)
    def __unicode__(self):
        return self.title