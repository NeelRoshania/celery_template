import pytest
import logging
import os

from celery_template.csv import read_csv, write_csv
from celery_template.tasks import sort_list, sort_directory

# usage: 
#   - pytest tests/scripts/test_sample.py
#   - pytest -v

LOGGER = logging.getLogger(__name__)

def generate_test_data(data_dir: str) -> None:

        """
            No reservation made to captures missing directories

        """
        import numpy as np

        LOGGER.info('generating test data')

        values_one = [[0, np.random.randint(1000, size=int(1e1)).tolist()]]
        values_many = [[i[0], np.random.randint(1000, size=int(1e1)).tolist()] for i in enumerate(range(10))]

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

def test_sort_row():
    
    test_dir = 'tests/data'
    tdata_files = generate_test_data(test_dir)

    res = sort_list(f'{test_dir}/testdata_singlelist_021923.csv')

    LOGGER.info(f'test complete - {res}') # doesn't work yet
    write_csv(file_loc=f'{test_dir}/results/test_sort_row.csv', data=res["data"])

    assert res["success"] == True

def test_sort_manyrows():
    
    test_dir = 'tests/data'
    tdata_files = generate_test_data(test_dir)

    res = sort_list(f'{test_dir}/testdata_many_021923.csv')

    LOGGER.info(f'test complete - {res}') # doesn't work yet
    write_csv(file_loc=f'{test_dir}/results/test_sort_manyrows.csv', data=res["data"])

    assert res["success"] == True

def test_sort_directory():
    
    test_dir = 'tests/data'
    tdata_files = generate_test_data(test_dir)

    res = sort_directory(tdata_files)

    LOGGER.info(f'test complete - {res}') # doesn't work yet
    write_csv(file_loc=f'{test_dir}/results/test_sort_directory.csv', data=res["data"])

    assert res["success"] == True