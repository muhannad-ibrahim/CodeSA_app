import os
import platform
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_processor.settings')

app = Celery('task_processor')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Use solo pool on Windows for better stability
if platform.system() == 'Windows':
    app.conf.update(
        broker_connection_retry_on_startup=True,
        worker_pool='solo',
        worker_concurrency=1
    )

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 