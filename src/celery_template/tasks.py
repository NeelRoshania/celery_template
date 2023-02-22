import time
import json

from celery_template import app
from celery_template.csv import read_csv
from celery.utils.log import get_task_logger
from celery.result import AsyncResult

LOGGER = get_task_logger(__name__) # this should call the logger celery_template.tasks
# LOGGER = logging.getLogger(__name__) # this should call the logger celery_template.tasks

@app.task(bind=True)
def fetch_task_result(self, taskid: str) -> tuple:
    LOGGER.info(f'querying task: {taskid}') # can't get celery.utils.log.get_task_logger to work
    return AsyncResult(id=taskid, app=app)

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
    start_time = time.time()
    lsorted = []
    headers, *data = read_csv(file_loc=fpath)
    
    for row in data:
        l = json.loads(row[1])
        lsorted.append([
                        row[0],
                        bubble_sort(l)
                    ]
        )
    
    end_time = time.time()

    return {
        "task_description": 'single-sort',
        "start_time": start_time,
        "end_time": end_time,
        "data": lsorted,
        "success": True
    }

@app.task(bind=True)
def sort_directory(self, fpaths: list) -> None:

    """
        Sort data across many files

    """

    start_time = time.time()
    fsorted = []

    for path in enumerate(fpaths):
        # LOGGER.info(f'sorting data in: {path[1]}')
        fsorted.append([
            path[1],
            sort_list(fpath=path[1])["data"]
            ]
        )

    end_time = time.time()

    return {
        "task_description": 'single-sort',
        "start_time": start_time,
        "end_time": end_time,
        "data": fsorted,
        "success": True
    }

@app.task(bind=True)
def add(self, x, y):
    # logger.info(f'task_id:{self.request.id}, task_group:{self.request.group} - args=({x}, {y})') # can't get celery.utils.log.get_task_logger to work
    LOGGER.info(f'args=({x}, {y})') # can't get celery.utils.log.get_task_logger to work
    return x + y
