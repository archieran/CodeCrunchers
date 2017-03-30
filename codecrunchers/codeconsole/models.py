from __future__ import unicode_literals

from django.db import models


class ConsoleLanguage(models.Model):
    lang_code = models.CharField(max_length=255, unique=True, verbose_name="Code", help_text="Code of language for Hackerrank API")
    lang = models.CharField(max_length=255, unique=True, verbose_name="Language", help_text="Name of language")
    ace_file_name = models.CharField(max_length=255, verbose_name="Editor filename", help_text="Name of ace editor file for syntax highlighting")
    is_active = models.BooleanField(default=False, verbose_name="Active")

    class Meta:
        pass

    def __unicode__(self):
        return self.lang
