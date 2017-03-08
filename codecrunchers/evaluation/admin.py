from django.contrib import admin
from .models import Problem, TestCase, Submission
# Register your models here.

class TestCaseInline(admin.StackedInline):
    #To show Test cases tab inside Problem
    model = TestCase

class SubmissionInline(admin.StackedInline):
    model = Submission
class ProblemAdmin(admin.ModelAdmin):

    list_display = ['title', 'difficulty', 'reward_points','start_time', 'end_time', 'is_archived', 'is_active', 'creator']
    #To show Test cases tab inside problem
    inlines = [
        TestCaseInline,
        SubmissionInline,
    ]

class TestcaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'problem','input_sequence', 'output_sequence' ,'score', 'is_sample']

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['sub_made_by', 'prob', 'submitted_code', 'achieved_score', 'total_memory_used', 'total_execution_time', 'lang']
admin.site.register(Problem, ProblemAdmin)
admin.site.register(TestCase, TestcaseAdmin)
admin.site.register(Submission, SubmissionAdmin)