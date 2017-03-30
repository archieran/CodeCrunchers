from django.contrib import admin
from .models import Problem, TestCase, Submission, Topic, Contest
from jet.admin import CompactInline
# Register your models here.

class TestCaseInline(CompactInline):
    #To show Test cases tab inside Problem
    model = TestCase

class SubmissionInline(CompactInline):
    model = Submission
class ProblemInline(CompactInline):
    model = Problem
    
class ProblemAdmin(admin.ModelAdmin):

    list_display = ['title', 'difficulty', 'reward_points','start_time', 'end_time', 'is_practice', 'is_active', 'creator']
    #To show Test cases tab inside problem
    inlines = [
        TestCaseInline,
        SubmissionInline,
    ]
    list_filter = ['difficulty', 'is_active', 'is_practice']
    search_fields = ['title','creator__username']

class TestcaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'problem','input_sequence', 'output_sequence' ,'score', 'is_sample']
    list_filter = ['is_sample']
    search_fields = ['problem__title']

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['sub_made_by', 'prob', 'submitted_code', 'achieved_score', 'total_memory_used', 'total_execution_time', 'lang', 'attempted']
    list_filter = ['lang__lang']
    search_fields = ['sub_made_by__username', 'prob__title']

class TopicAdmin(admin.ModelAdmin):
    list_display = ['topic_name']
    search_fields = ['topic_name']
    inlines = [
        ProblemInline
    ]

class ContestAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','description','creator','start_time','end_time','is_active']
    list_filter = ['creator','is_active']
    search_fields = ['creator','title','description']

admin.site.register(Topic, TopicAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(TestCase, TestcaseAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Contest, ContestAdmin)