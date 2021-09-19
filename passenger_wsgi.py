import os, sys
  
#project directory
sys.path.append('/home/o/oruchk91/oleg.uno/venv/lib/python3.8/site-packages')
sys.path.append('/home/o/oruchk91/oleg.uno')
  
#project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wc2.settings")
  
#start server
  
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
