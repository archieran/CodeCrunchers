from django.contrib import admin
from .models import Profile
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'user_type']
    def username(self, instance):
        return instance.user.username

    pass
admin.site.register(Profile, ProfileAdmin)