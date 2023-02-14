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
    # print('lol')
    print(f'{self.request.id}: additing {x} and {y}')
    logger.info(f'{self.request.id}: adding ({x}, {y})')
    return x + y

@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers):
    return sum(numbers)
