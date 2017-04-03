from django.contrib import admin
from .models import ConsoleLanguage, SavedCode
# Register your models here.
class ConsoleAdmin(admin.ModelAdmin):
    list_display = ['lang', 'is_active']
    list_filter = ['is_active']

class SavedCodeAdmin(admin.ModelAdmin):
    list_display = ['user','code', 'time_saved']
admin.site.register(ConsoleLanguage, ConsoleAdmin)
admin.site.register(SavedCode, SavedCodeAdmin)
