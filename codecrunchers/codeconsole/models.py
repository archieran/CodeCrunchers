from __future__ import unicode_literals

from django.db import models


class ConsoleLanguages(models.Model):
    lang_code = models.CharField("API code", max_length=255, unique=True)
    lang = models.CharField("language", max_length=255, unique=True)
    ace_file_name = models.CharField("editor filename", max_length=255)
    is_active = models.BooleanField("active", default=False)

    class Meta:
        pass

    def __unicode__(self):
        return self.lang
