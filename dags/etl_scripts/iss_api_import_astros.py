import yaml
import os
import psycopg2
import pandas as pd
from pathlib import Path
from iss_api_get_astros import df

# path variables
my_folder = os.getenv('PWD')
my_parent_folder = Path(my_folder).parent

try:
    # load yaml file values and pass values to variables
    creds = yaml.safe_load(open('{}/config/credentials.yml'.format(my_parent_folder)))
    hostname = creds['postgresql']['hostname']
    database = creds['postgresql']['database']
    username = creds['postgresql']['username']
    password = creds['postgresql']['password']
    port = creds['postgresql']['port']

    # perform connection string
    conn_string = 'postgres://{}:{}@{}/{}'.format(username, password, hostname, database)

    # export pandas dataframe to csv file
    df.to_csv('{}/files/iss_get_astros.csv'.format(my_parent_folder), index=False, header=False)

    # sql script
    query = '''
            /* create schema if not exists */
            create schema if not exists iss;

            /* create table */
            create table if not exists iss.astronauts (
	            index numeric, 
                snapshot_date timestamp, 
                craft varchar(30), 
                name varchar(150)
            );
    '''

    # establish connection and importing data to postgres
    print('staring loading data into iss.astronauts...')
    pg_conn = psycopg2.connect(conn_string)
    cur = pg_conn.cursor()
    cur.execute(query)
    file = open(r'{}/files/iss_get_astros.csv'.format(my_parent_folder), 'r')
    cur.copy_from(file, 'iss.astronauts', sep=',')
    os.remove('{}/files/iss_get_astros.csv'.format(my_parent_folder))
    pg_conn.commit()
    file.close()
    cur.close()
    pg_conn.close()
    print('finished sucessfully!')

except (yaml.YAMLError) as yaml_error:
	print("Could not load yaml error", yaml_error)
except (psycopg2.Error) as psyco_error:
	print("Could not establish psycopg2 connection", psyco_error)
