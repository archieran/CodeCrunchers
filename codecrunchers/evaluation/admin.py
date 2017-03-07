from django.contrib import admin
from .models import Problem
# Register your models here.
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'start_time', 'end_time', 'is_archived', 'is_active', 'creator']

admin.site.register(Problem, ProblemAdmin)