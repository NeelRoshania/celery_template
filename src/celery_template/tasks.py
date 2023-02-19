import celery
import logging

from celery_template import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__) # this should call the logger celery_template.tasks

@app.task(bind=True)
def add(self, x, y):
    logger.info(f'task_id:{self.request.id}, task_group:{self.request.group} - args=({x}, {y})') # can't get celery.utils.log.get_task_logger to work
    # logger.info(f'args=({x}, {y})') # can't get celery.utils.log.get_task_logger to work
    return x + y

@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers):
    return sum(numbers)
