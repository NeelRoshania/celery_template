import argparse
import logging
import json
import numpy as np
from celery_template import app
from celery_template.tasks import add, sort_list, sort_lists
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
        svalues = json.dumps(values.tolist()) # Data transferred between clients and workers needs to be serialized - https://docs.celeryq.dev/en/stable/userguide/calling.html#serializers

        # tasks to run
        # t1 = add.apply_async(args=[5, 7, svalues], queue='celery_template_queue')
        t2 = sort_list.apply_async(args=[svalues], queue='celery_template_queue')
        t3 = sort_lists.apply_async(args=[svalues], queue='celery_template_queue')

        LOGGER.info(f'tasks complete')


    except OperationalError as e: 
        LOGGER.error(f'app:{app} - failed to execute tasks - {e}')

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, action="store", default="conf/config.yaml", nargs="?")
    parser.add_argument("--optional", "-o", action="store", type=str, default=8000)
    args = parser.parse_args()

    single_task(args)

    

    
