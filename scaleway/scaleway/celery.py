from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scaleway.settings")

app = Celery("scaleway")

# Load task settings from Django's settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks in all installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)