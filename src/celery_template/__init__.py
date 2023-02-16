import configparser
import logging
import logging.config

from celery import Celery
from kombu import Queue, Exchange

# setup
logging.config.fileConfig('conf/logging.conf', defaults={'fileHandlerLog': 'logs/celery_template.log'})
# logger = logging.getLogger(__name__)

# objects to make available when this package is imported
cparser = configparser.ConfigParser()

## configuration: read from configparser - https://docs.celeryq.dev/en/stable/userguide/configuration.html
class CeleryConfig:
    broker_url =  "pyamqp://guest@localhost//"
    result_backend = "db+postgresql://celery_user:celery_pass@localhost/celery_db"
    include = ["celery_template.tasks"]
    event_queue_expires = 3600 

# start application
app = Celery(
        'tasks'
)

# set app configuration
app.config_from_object(CeleryConfig)

# # __all__ applies to the situation where from foo.bar import *
# __all__ = [
#     'logger'
# ]
