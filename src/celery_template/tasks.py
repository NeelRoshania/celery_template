import celery

from celery_template import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

print(f'logger: {logger.name}')

#@celery.signals.after_setup_logger.connect
#def on_after_setup_logger(**kwargs):
#    logger = logging.getLogger('celery')
#    logger.propagate = True
#    logger = logging.getLogger('celery.app.trace')
#    logger.propagate = True

@app.task(bind=True)
def add(self, x, y):
    logger.info(f'task_id: {self.request.id}: adding ({x}, {y})') # this logs to worker server, not file...yet
    return x + y

@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers):
    return sum(numbers)
