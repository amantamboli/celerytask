from __future__ import absolute_import,unicode_literals  
import os
from celery import Celery  
from django.conf import settings  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangotask.settings')  

app = Celery('djangotask')  
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')  
app.conf.broker_connection_retry_on_startup = True
app.conf.broker_url = 'redis://localhost:6379/0'

# Load task modules from all registered Django apps.  
app.autodiscover_tasks()  
  
@app.task(bind=True)  
def debug_task(self):  
    print(f'Request: {self.request!r}')  

# celery -A djangotask flower
# celery -A djangotask.celery worker -P eventlet -l INFO
