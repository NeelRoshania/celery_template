import configparser
import logging
import logging.config

from celery import Celery

# setup
logging.config.fileConfig('conf/logging.conf', defaults={'fileHandlerLog': 'logs/celery_template.log'})

# objects to make available when this package is imported
cparser = configparser.ConfigParser()

# celery app
app = Celery(
    'tasks', 
    broker = 'pyamqp://guest@localhost//',
    include = ['celery_template.tasks'],
    backend = 'db+postgresql://celery_user:celery_pass@localhost/celery_db'
    )

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

# # __all__ applies to the situation where from foo.bar import *
# __all__ = [
#     'logger'
# ]
