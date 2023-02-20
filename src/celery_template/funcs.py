import logging
import os
from celery_template.csv import write_csv

LOGGER = logging.getLogger(__name__) # this calls the celery_template.funcs logger - which logs to worker node instance

def generate_test_data(data_dir: str) -> None:

        """
            No reservation made to captures missing directories

        """
        import numpy as np

        LOGGER.info('generating test data')

        values_one = [[0, np.random.randint(1000, size=int(5e3)).tolist()]]
        values_many = [[i[0], np.random.randint(1000, size=int(5e3)).tolist()] for i in enumerate(range(10))]

        write_csv(
            file_loc=f'{data_dir}/testdata_singlelist_021923.csv', 
            data=values_one, 
            schema=['record_id', 'data']
        )

        write_csv(
            file_loc=f'{data_dir}/testdata_many_021923.csv', 
            data=values_many, 
            schema=['record_id', 'data']
        )

        return [f'{data_dir}/{f}' for f in os.listdir('tests/data') if f.endswith('.csv')]