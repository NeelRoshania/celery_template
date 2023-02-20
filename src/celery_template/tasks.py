import time
import json

from celery_template import app
from celery_template.csv import read_csv
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__) # this should call the logger celery_template.tasks
# logger = logging.getLogger(__name__) # this should call the logger celery_template.tasks

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
    
    
    """
        Sort one list object
    """
    start_time = time.time()
    
    arr = read_csv(file_loc=fpath)
    res = bubble_sort(arr)
    
    end_time = time.time()

    return {
        "task_description": 'single-sort',
        "start_time": start_time,
        "end_time": end_time,
        "res": res
    }

@app.task(bind=True)
def sort_lists(self, dir: list) -> None:

    """
        Sort multiple list objects
    """

    start_time = time.time()
    res = []

    for i in enumerate(dir):
        res.append(sort_list(i[1]))

    end_time = time.time()

    return {
        "task_description": 'nested-sort',
        "start_time": start_time,
        "end_time": end_time,
        "res": res
    }

@app.task(bind=True)
def add(self, x, y, arr):
    # logger.info(f'task_id:{self.request.id}, task_group:{self.request.group} - args=({x}, {y})') # can't get celery.utils.log.get_task_logger to work
    logger.info(f'args=({x}, {y}, {arr})') # can't get celery.utils.log.get_task_logger to work
    return x + y
