# my_tennis_club/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_tennis_club.settings')

application = get_wsgi_application()
