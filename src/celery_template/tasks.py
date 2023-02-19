import time

from celery_template import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__) # this should call the logger celery_template.tasks
# logger = logging.getLogger(__name__) # this should call the logger celery_template.tasks

@app.task(bind=True)
def single_sort_task(arr: list) -> dict:

    """
    Nested functions

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
    
    sorted_array = bubble_sort(arr)
    
    end_time = time.time()

    logger.info(
        {
            "task_description": 'single-sort',
            "start_time": start_time,
            "end_time": end_time

        }
    )

    return sorted_array

@app.task(bind=True)
def nested_sort_tasks(arrs: list) -> None:

    """
        Sort multiple list objects
    """

    start_time = time.time()

    for i in enumerate(arrs):
        single_sort_task(i[1][1])

    end_time = time.time()

    logger.info(
        {
            "task_description": 'nested-sort',
            "start_time": start_time,
            "end_time": end_time
        }
    )

@app.task(bind=True)
def add(self, x, y):
    # logger.info(f'task_id:{self.request.id}, task_group:{self.request.group} - args=({x}, {y})') # can't get celery.utils.log.get_task_logger to work
    logger.info(f'args=({x}, {y})') # can't get celery.utils.log.get_task_logger to work
    return x + y