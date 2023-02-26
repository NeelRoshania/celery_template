import json
import logging

from celery_template import app, cparser
from celery_template.csv import read_csv
from celery_template.psql import connect_postgres
from celery.app.log import TaskFormatter
from celery.utils.log import get_task_logger
from celery.result import AsyncResult
from celery.signals import task_success, after_setup_task_logger

"""
    References
        - task requests, https://docs.celeryq.dev/en/stable/userguide/tasks.html#task-request
        - signals,  https://docs.celeryq.dev/en/stable/userguide/signals.html#signal-ref

"""
# logging configurations
LOGGER = get_task_logger(__name__) # this should call the logger celery_template.tasks

# signals

# define task logger and redirect to file
@after_setup_task_logger.connect
def setup_task_logger(logger, *args, **kwargs):
    LOGGER = logging.getLogger(__name__)
    LOGGER.handlers.clear()
    LOGGER.addHandler(logging.FileHandler(f'logs/{__name__}.log'))
    for handler in LOGGER.handlers:
        handler.setFormatter(TaskFormatter('%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s'))
    return None

# signal to handle task successes
@task_success.connect
def log_task_id(sender=None, result=None, **kwargs) -> tuple:
    print(f'{LOGGER.name}, handlers: {LOGGER.handlers}')
    LOGGER.info(f'task_id:{sender.request.id} - task completed with result: {result}') # can't get celery.utils.log.get_task_logger to work
    return None

# tasks

@app.task(bind=True)
def fetch_task_result(self, taskid: str) -> tuple:
    LOGGER.info(f'querying task: {taskid}') # can't get celery.utils.log.get_task_logger to work
    return AsyncResult(id=taskid, app=app)

@app.task(bind=True)
def fetch_backend_taskresult(self, taskid: str) -> tuple:

    """
        Fetch task_id result
            - result needs to be deserialized
                result = pickle.loads(fetch_backend_taskresult({task_id})[0][0])
    """
    LOGGER.info(f'querying task: {taskid}') # can't get celery.utils.log.get_task_logger to work

    # connect to psql
    conn_response = connect_postgres()
    
    if conn_response["connection-status"]:

        # Creating a cursor object using the cursor() method
        conn = conn_response['conn']
        cursor = conn.cursor()

        # Executing an MYSQL function using the execute() method
        cursor.execute(f'select result from celery_taskmeta where task_id = \'{taskid}\' limit 10;')

        # Fetch a single row using fetchone() method.
        data = cursor.fetchall()
        LOGGER.info(f'data: {data}, type: {type(data)}, len: {len(data)}')

        # Closing the connection
        conn.close()
        return data
    else:
        LOGGER.info(f'connection failed: {conn_response}')
        raise Exception(f'Failed to pass test - {conn_response}')

@app.task(bind=True)
def sort_list(self, fpath: str) -> dict:

    """

        task is packaged to perform bubble_sort 

    """
    def bubble_sort(arr: list) -> list:
        
        """
            bubble sort implementation
                - https://www.programiz.com/dsa/bubble-sort
        """ 

        # loop to access each array element
        if isinstance(arr, list):

            for i in range(len(arr)):

                # loop to compare array elements
                for j in range(0, len(arr) - i - 1):

                    # compare two adjacent elements - change > to < to sort in descending order
                    if arr[j] > arr[j + 1]:

                        # swapping elements if elements are not in the intended order
                        temp = arr[j]
                        arr[j] = arr[j+1]
                        arr[j+1] = temp
            
            return arr
        else:
            raise TypeError(f'argument of type {type(arr)} must be {type([])}: {arr}')
    
    """
        Sort one list object 
    """

    lsorted = []
    headers, *data = read_csv(file_loc=fpath)
    LOGGER.info(f'sorting data in: {fpath}')

    for row in data:
        l = json.loads(row[1])
        lsorted.append([
                        row[0],
                        bubble_sort(l)
                    ]
        )

    return {
        "task_description": 'single-sort',
        # "data": lsorted,
    }

@app.task(bind=True)
def sort_directory(self, fpaths: list) -> None:

    """
        Sort data across many files

    """

    fsorted = []

    for path in enumerate(fpaths):
        fsorted.append([
            path[1],
            sort_list(fpath=path[1])["data"]
            ]
        )

    return {
        "task_description": 'single-sort',
        # "data": fsorted,
    }

@app.task(bind=True)
def add(self, x, y):
    LOGGER.info(f'task.request:{dir(self.request)} - args=({x}, {y})')
    return x + y
