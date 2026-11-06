"""
WSGI config for AnyLearn Labs project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anylearn_labs.settings')

application = get_wsgi_application()
