from django.contrib import admin
from .models import ConsoleLanguage
# Register your models here.
class ConsoleAdmin(admin.ModelAdmin):
    list_display = ['lang', 'is_active']
admin.site.register(ConsoleLanguage, ConsoleAdmin)
