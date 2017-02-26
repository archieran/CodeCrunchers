from __future__ import unicode_literals

from django.db import models

class ConsoleLanguages(models.Model):
    lang_code = models.CharField(max_length=255, unique=True)
    lang = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.lang
