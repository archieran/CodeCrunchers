from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from codeconsole.models import ConsoleLanguage

# Create your models here.
class Topic(models.Model):
    topic_name = models.CharField(max_length = 255, verbose_name = "Topic")

    def __unicode__(self):
        return self.topic_name

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
    reward_points = models.IntegerField(default=100, null=False, blank=False, verbose_name="Reward points")
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
    total_memory_used = models.IntegerField(verbose_name="Total memory used")
    total_execution_time = models.IntegerField(verbose_name="Total execution time")
    lang = models.ForeignKey(ConsoleLanguage)
    attempted = models.DateTimeField(verbose_name="Attempted")
    class Meta:
        unique_together = ('sub_made_by', 'prob')
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

    class Meta:
        unique_together = ['submission', 'test_case']