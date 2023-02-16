import configparser
import logging
import logging.config

from celery import Celery
from kombu import Queue, Exchange

# setup
logging.config.fileConfig('conf/logging.conf', defaults={'fileHandlerLog': 'logs/celery_template.log'})
LOGGER = logging.getLogger(__name__)
cparser = configparser.ConfigParser() # objects to make available when this package is imported

## configuration: read from configparser - https://docs.celeryq.dev/en/stable/userguide/configuration.html
class CeleryConfig:
    broker_url =  "pyamqp://guest@localhost//"
    result_backend = "db+postgresql://celery_user:celery_pass@localhost/celery_db"
    include = ["celery_template.tasks"]
    event_queue_expires = 3600
    task_queues = (
            Queue("default", Exchange("default"), routing_key="default"),
            Queue("celery_template_queue", Exchange("celery_template_queue"), routing_key="ctq")
    )

# start application
app = Celery('tasks')

# set app configuration
app.config_from_object(CeleryConfig)
