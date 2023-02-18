import argparse
import logging

from celery_template import app
from celery_template.tasks import add
from kombu.exceptions import OperationalError

"""

    Celery task execution
        - single tasks
        - grouped tasks

        - timed executions

"""


def run_script(args):

    LOGGER = logging.getLogger(__name__) # will call the __main__ logger, which defaults to the logger defined in celery_template.__init__.py

    LOGGER.info('starting tasks')

    # catch operational errors - perhaps cannot send message to worker
    try:
        res = add.apply_async(args=(5, 7), queue='celery_template_queue')
    except OperationalError as e: 
        LOGGER.debug(f'app:{app} - failed to execute tasks - {e}')

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, action="store", default="conf/config.yaml", nargs="?")
    parser.add_argument("--optional", "-o", action="store", type=str, default=8000)
    args = parser.parse_args()

    run_script(args)

    

    
