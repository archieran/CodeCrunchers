from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ConsoleLanguage(models.Model):
    lang_code = models.CharField(max_length=255, unique=True, verbose_name="Code", help_text="Code of language for Hackerrank API")
    lang = models.CharField(max_length=255, unique=True, verbose_name="Language", help_text="Name of language")
    ace_file_name = models.CharField(max_length=255, verbose_name="Editor filename", help_text="Name of ace editor file for syntax highlighting")
    is_active = models.BooleanField(default=False, verbose_name="Active")

    class Meta:
        pass

    def __unicode__(self):
        return self.lang

class SavedCode(models.Model):
    code = models.TextField(verbose_name="Code", help_text="Code committed by the user")
    user = models.ForeignKey(User, on_delete=None, help_text="Writer of the code", verbose_name="Coder")
    time_saved = models.DateTimeField(verbose_name="Last saved", help_text="Time of last code backup", default=timezone.now)
    def __unicode__(self):
        return self.user.username

