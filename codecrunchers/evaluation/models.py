from __future__ import unicode_literals
from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User
from codeconsole.models import ConsoleLanguage
from django.utils import timezone

# Create your models here.
class Topic(models.Model):
    topic_name = models.CharField(max_length = 255, verbose_name = "Topic")

    def __unicode__(self):
        return self.topic_name

class Contest(models.Model):
    title = models.CharField(max_length=255, verbose_name="Contest title")
    description = models.TextField(verbose_name="Description")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Contest Creator")
    start_time = models.DateTimeField(verbose_name="Start time")
    end_time = models.DateTimeField(verbose_name="End time")
    is_active = models.BooleanField(default=False, verbose_name="Active")

    def __str__(self):
        return self.title
    def clean(self):
        if self.start_time > self.end_time:
             raise ValidationError("Start Time cannot be greater than End Time")
        super(Contest,self).clean()

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
    topic = models.ForeignKey(Topic, on_delete=None, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Problem creator")
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name="Title")
    desc = models.TextField(max_length=65535, null=False, blank=False, verbose_name="Description")
    model_solution = models.TextField(verbose_name="Model solution")
    constraints = models.TextField(max_length=255, verbose_name="Constraints")
    input_format = models.TextField(max_length=255, verbose_name="Input format")
    output_format = models.TextField( max_length=255, verbose_name="Output format")
    startup_code = models.TextField(max_length=65535, verbose_name="Initial code")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    difficulty = models.CharField(choices=PROB_DIFFICULTY_LEVELS, max_length=255, default=Easy)
    reward_points = models.IntegerField(default=100, null=False, blank=False, verbose_name="Reward points")
    contest = models.ManyToManyField(Contest, blank=True)
    def __unicode__(self):
        return self.title
    def get_difficulty_verbose(self):
        return dict(self.PROB_DIFFICULTY_LEVELS).get(self.difficulty)

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, verbose_name="Problem")
    input_sequence = models.TextField(verbose_name="Expected Input")
    output_sequence = models.TextField(verbose_name="Expected output")
    score = models.IntegerField()
    is_sample = models.BooleanField(verbose_name="Sample test case", default=False)

    def __unicode__(self):
        return str(self.problem) + " TC ID: " +str(self.id)

class LiveCode(models.Model):
    live_user = models.OneToOneField(User)
    console_data = models.TextField(verbose_name="Code")
    console_lang = models.ForeignKey(ConsoleLanguage)

class Submission(models.Model):
    sub_made_by = models.ForeignKey(User, verbose_name="User")
    prob = models.ForeignKey(Problem, verbose_name="Problem")
    submitted_code = models.TextField(verbose_name="Submitted code")
    achieved_score = models.IntegerField(verbose_name="Achieved score")
    total_memory_used = models.FloatField(verbose_name="Total memory used")
    total_execution_time = models.FloatField(verbose_name="Total execution time")
    lang = models.ForeignKey(ConsoleLanguage)
    attempted = models.DateTimeField(verbose_name="Attempted")
    contest = models.ForeignKey(Contest, verbose_name="Contest_ID", null=True, blank=True)
    # class Meta:
    #     unique_together = ('sub_made_by', 'prob')
    def __unicode__(self):
        return self.prob.title + " by " + self.sub_made_by.username

class TestCaseResult(models.Model):
    PASS = "P"
    FAIL = "F"
    STATUS_CHOICES = (
        (PASS, "PASS"),
        (FAIL, "FAIL"),
    )
    submission = models.ForeignKey(Submission, verbose_name="Submission")
    test_case = models.ForeignKey(TestCase, verbose_name="Test_Case")
    status = models.CharField(choices=STATUS_CHOICES, verbose_name="Status", max_length=1, default=FAIL)
    time_submitted = models.DateTimeField(verbose_name="Time_Stamp", default=timezone.now)

    # class Meta:
       # unique_together = ['submission', 'test_case']
class ContestParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, verbose_name="Contest")
    achieved_score = models.IntegerField(default=0, verbose_name="Achieved Score")

    class Meta:
        unique_together = [
            'user',
            'contest',
        ]
    def __unicode__(self):
        return str(self.contest)