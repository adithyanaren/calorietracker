"""
WSGI config for calorie_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
import os
import sys
from django.core.wsgi import get_wsgi_application

# Ensure the project path is added
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "calorie_tracker.settings")

application = get_wsgi_application()


