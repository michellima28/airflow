import sqlalchemy
import yaml
import os
import psycopg2
import gzip
import shutil
import glob
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

# path variables
my_folder = os.getenv('PWD')
my_parent_folder = Path(my_folder).parent
gz_filepath = '{}/files/boletim.csv.gz'.format(my_parent_folder)
csv_filepath = '{}/files/boletim.csv'.format(my_parent_folder)

try:
	# load yml file values and pass values to variables
	creds = yaml.safe_load(open('{}/config/credentials.yml'.format(my_parent_folder)))
	v_host = creds['postgresql']['y_hostname']
	v_database = creds['postgresql']['y_database']
	v_user = creds['postgresql']['y_username']
	v_password = creds['postgresql']['y_password']
	v_port = creds['postgresql']['y_port']

	# database connection with sqlalchemy
	alchemy_engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(v_user, 
                                                                    	v_password, 
																		v_host, 
																		v_port, 
																		v_database))

	# database connection with psycopg2
	conn = psycopg2.connect(host=v_host,
                        	dbname=v_database,
                        	user=v_user,
                        	password=v_password,
                        	port=v_port)

	# extract .csv.gz file to .csv
	if os.path.isfile(gz_filepath) is True:
		with gzip.open(gz_filepath, 'rb') as f_in:
			with open(csv_filepath, 'wb') as f_out:
				shutil.copyfileobj(f_in, f_out)

	# copy csv file to pandas, load to postgresql and then remove it
	p_file = glob.glob(csv_filepath)
	dfs = [pd.read_csv(f, sep=",") for f in p_file]
	df_covid_caso = pd.concat(dfs,ignore_index=True)
	df_covid_caso.to_sql('boletim', alchemy_engine, if_exists='replace', index=False)
	os.remove(csv_filepath)

	# create cursor and execure sql commands  
	cur = conn.cursor()
	cur.execute("""
				/*create schema*/
				create schema if not exists covid;

				/* drop table*/
				drop table if exists covid.boletim;

				/*create target table*/
				create table covid.boletim 
					(
					date_imported timestamp,	
	            	date date,
	            	notes text,
					state varchar(10),
	            	url text
                	);

				/* insert into target table*/               
				insert into covid.boletim
				select  current_timestamp as date_imported,
				        cast(date as date),
	    				notes,
	    				state,
	    				url
				from 	public.boletim;

				/* drop stage table */
				drop table public.boletim;
            	""")
	conn.commit()
	conn.close()
						
except (yaml.YAMLError) as yaml_error:
	print("Could not load yaml error", yaml_error)
except (sqlalchemy.exc.SQLAlchemyError) as alchemy_error:
	print("Could not establish sqlalchemy connection", alchemy_error)
except (psycopg2.Error) as psyco_error:
	print("Could not establish psycopg2 connection", psyco_error)
    