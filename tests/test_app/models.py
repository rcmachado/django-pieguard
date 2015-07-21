from __future__ import unicode_literals
from datetime import datetime
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        get_latest_by = 'created_at'
        permissions = (
            ('view_project', 'View project'),  # used by django-tastypie
        )

    def __unicode__(self):
        return self.name
