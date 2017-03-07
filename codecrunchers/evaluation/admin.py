from django.contrib import admin
from .models import Problem, TestCase
# Register your models here.
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'reward_points','start_time', 'end_time', 'is_archived', 'is_active', 'creator']

class TestcaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'problem','input_sequence', 'output_sequence' ,'score', 'is_sample']
admin.site.register(Problem, ProblemAdmin)
admin.site.register(TestCase, TestcaseAdmin)