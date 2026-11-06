"""
ASGI config for AnyLearn Labs project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anylearn_labs.settings')

application = get_asgi_application()
