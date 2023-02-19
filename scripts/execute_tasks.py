import argparse
import logging
import numpy as np
from celery_template import app
from celery_template.tasks import add, single_sort_task
from kombu.exceptions import OperationalError

"""

    Celery task execution
        - single tasks
        - grouped tasks

        - timed executions

"""

logging.config.fileConfig('conf/logging.conf', disable_existing_loggers=False, defaults={'fileHandlerLog': f'logs/{__name__}.log'})
LOGGER = logging.getLogger(__name__) # this will call the logger __main__ which will log to that referenced in python_template.__init__

def single_task(args):

    LOGGER.info('starting tasks')

    # catch operational errors - perhaps cannot send message to worker
    try:
        values = np.random.randint(1000, size=int(5e3))

        # tasks to run
        res = add.apply_async(args=(5, 7), queue='celery_template_queue')
        res = single_sort_task.apply_async(args=(values), queue='celery_template_queue')
        # res = single_sort_task.apply_async(args=(values), queue='celery_template_queue')

    except OperationalError as e: 
        LOGGER.error(f'app:{app} - failed to execute tasks - {e}')

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, action="store", default="conf/config.yaml", nargs="?")
    parser.add_argument("--optional", "-o", action="store", type=str, default=8000)
    args = parser.parse_args()

    single_task(args)

    

    
