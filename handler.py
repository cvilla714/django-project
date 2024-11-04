import os
import sys

from django.core.wsgi import get_wsgi_application

# Set the Django settings module environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Add the project's root directory to the Python path
sys.path.append("/var/task")

# Initialize Django application
application = get_wsgi_application()

def lambda_handler(event, context):
    from mangum import Mangum
    # Initialize Mangum adapter for ASGI
    asgi_handler = Mangum(application)
    return asgi_handler(event, context)
