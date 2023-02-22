import argparse
import logging
import os

from celery_template import app
from celery_template.funcs import generate_test_data
from celery_template.tasks import add, sort_list, sort_directory
from celery_template.csv import read_csv, write_csv
from kombu.exceptions import OperationalError

"""

    Celery task execution
        - single tasks
        - grouped tasks

        - timed executions

"""

logging.config.fileConfig('conf/logging.conf', disable_existing_loggers=False, defaults={'fileHandlerLog': f'logs/{__name__}.log'})
LOGGER = logging.getLogger(__name__) # this will call the logger __main__ which will log to that referenced in python_template.__init__

def sequential_tasks(fpath: str, fpaths: str) -> None:

    LOGGER.info('starting tasks')

    # catch operational errors - perhaps cannot send message to worker
    try:

        # celery tasks expect serialized arguments, not objects - https://docs.celeryq.dev/en/stable/userguide/calling.html#serializers
        t1 = add.apply_async(args=[5, 7], queue='celery_template_queue')
        t2 = sort_list.apply_async(args=[fpath], queue='celery_template_queue')
        t3 = sort_directory.apply_async(args=[fpaths], queue='celery_template_queue')

        LOGGER.info(f'tasks submitted')

    except OperationalError as e: 
        LOGGER.error(f'app:{app} - failed to execute tasks - {e}')

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, action="store", default="conf/config.yaml", nargs="?")
    parser.add_argument("--optional", "-o", action="store", type=str, default=8000)
    args = parser.parse_args()

    # prepare data
    data_dir = r'tests/data'
    data_files = generate_test_data(data_dir=data_dir)
    LOGGER.info(f'test data: {data_files}')

    # run tasks
    sequential_tasks(fpath=data_files[0], fpaths=data_files)

    

    
