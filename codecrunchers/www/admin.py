import user
from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'user_type']
    def username(self, instance):
        return instance.user.username
admin.site.register(Profile, ProfileAdmin)




# class TestCaseResultAdmin(admin.ModelAdmin):
#     list_display = ['submission','test_case','status']
# admin.site.register(TestCaseResult, TestCaseResultAdmin)