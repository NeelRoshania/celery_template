import logging
import os
from celery_template import cparser
from celery_template.csv import write_csv
from celery_template.psql import psql_connection

LOGGER = logging.getLogger(__name__) # this calls the celery_template.funcs logger - which logs to worker node instance

def connect_postgres() -> dict:

    # establishing the connection
    return psql_connection(
                    db=cparser.get('postgresql_credentials', 'database'),
                    usr=cparser.get('postgresql_credentials', 'user'),        
                    pswd=cparser.get('postgresql_credentials', 'password'), 
                    hst=cparser.get('postgresql_credentials', 'host'), 
                    prt=cparser.get('postgresql_credentials', 'port')
        )

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