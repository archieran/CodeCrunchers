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
    title = models.CharField(max_length=255, verbose_name="Contest title", help_text="Title of the contest")
    description = models.TextField(verbose_name="Description")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Contest Creator", help_text="The user who created the contest")
    start_time = models.DateTimeField(verbose_name="Start time", help_text="Start time of the contest")
    end_time = models.DateTimeField(verbose_name="End time", help_text="End time of the contest")
    is_active = models.BooleanField(default=False, verbose_name="Active", help_text="Is the contest active?")

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
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Problem creator", help_text="The user who created the problem")
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name="Title", help_text="Title of the problem")
    desc = models.TextField(max_length=65535, null=False, blank=False, verbose_name="Description",help_text="Brief description of the problem")
    model_solution = models.TextField(verbose_name="Model solution", help_text="Working solution for the problem in any language")
    constraints = models.TextField(max_length=255, verbose_name="Constraints", help_text="Any constraints or steps to solve the problem")
    input_format = models.TextField(max_length=255, verbose_name="Input format", help_text="Input the program will read")
    output_format = models.TextField( max_length=255, verbose_name="Output format", help_text="Output the program will give")
    startup_code = models.TextField(max_length=65535, verbose_name="Initial code", help_text="Initial code to begin with")
    is_active = models.BooleanField(default=True, verbose_name="Active", help_text="Indicates whether the problem is active")
    difficulty = models.CharField(choices=PROB_DIFFICULTY_LEVELS, max_length=255, default=Easy, help_text="Difficulty level of the problem")
    reward_points = models.IntegerField(default=100, null=False, blank=False, verbose_name="Reward points", help_text="Maximum experience points for the  problem")
    contest = models.ManyToManyField(Contest, blank=True, help_text="Contests to which the problem belongs")
    def __unicode__(self):
        return self.title
    def get_difficulty_verbose(self):
        return dict(self.PROB_DIFFICULTY_LEVELS).get(self.difficulty)

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, verbose_name="Problem", help_text="Problem to which the test case belongs")
    input_sequence = models.TextField(verbose_name="Expected Input", help_text="The input that the program shall read")
    output_sequence = models.TextField(verbose_name="Expected output", help_text="The output expected to be generated from the code")
    score = models.IntegerField(help_text="Weightage for the testcase")
    is_sample = models.BooleanField(verbose_name="Sample test case", default=False, help_text="Indicates whether the testcase is a sample or graded. Checked indicates Sample")

    def __unicode__(self):
        return str(self.problem) + " TC ID: " +str(self.id)

class LiveCode(models.Model):
    live_user = models.OneToOneField(User)
    console_data = models.TextField(verbose_name="Code")
    console_lang = models.ForeignKey(ConsoleLanguage)

class Submission(models.Model):
    sub_made_by = models.ForeignKey(User, verbose_name="User", help_text="The user who made the sunmission")
    prob = models.ForeignKey(Problem, verbose_name="Problem", help_text="Submission made for the problem")
    submitted_code = models.TextField(verbose_name="Submitted code", help_text="Code submitted by the user")
    achieved_score = models.IntegerField(verbose_name="Achieved score", help_text="Score achieved for the submission")
    total_memory_used = models.FloatField(verbose_name="Total memory used", help_text="Total memory used for the submission")
    total_execution_time = models.FloatField(verbose_name="Total execution time", help_text="Total execution time for the submission")
    lang = models.ForeignKey(ConsoleLanguage, help_text="Language in which the submission was made")
    attempted = models.DateTimeField(verbose_name="Attempted", help_text="When the submission was made")
    contest = models.ForeignKey(Contest, verbose_name="Contest_ID", null=True, blank=True, help_text="Contest for which the submission was made. Can be empty")
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
    submission = models.ForeignKey(Submission, verbose_name="Submission", help_text="Submission to which the result belongs")
    test_case = models.ForeignKey(TestCase, verbose_name="Test_Case", help_text="The test case")
    status = models.CharField(choices=STATUS_CHOICES, verbose_name="Status", max_length=1, default=FAIL, help_text="Status indicating the result of the test case")
    time_submitted = models.DateTimeField(verbose_name="Time_Stamp", default=timezone.now, help_text="Time when the test case was executed")

    # class Meta:
       # unique_together = ['submission', 'test_case']
class ContestParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User", help_text="Contest Participant")
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, verbose_name="Contest", help_text="Contest")
    achieved_score = models.IntegerField(default=0, verbose_name="Achieved Score", help_text="Score achieved by the Participant")

    class Meta:
        unique_together = [
            'user',
            'contest',
        ]
    def __unicode__(self):
        return str(self.contest)