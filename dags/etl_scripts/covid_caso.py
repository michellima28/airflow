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
gz_filepath = '{}/files/caso.csv.gz'.format(my_parent_folder)
csv_filepath = '{}/files/caso.csv'.format(my_parent_folder)

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
	df_covid_caso.to_sql('covid_caso', alchemy_engine, if_exists='replace', index=False)
	os.remove(csv_filepath)

	# create cursor and execure sql commands  
	cur = conn.cursor()
	cur.execute("""
				/*create schema*/
				create schema if not exists covid;

				/* drop table*/
				drop table if exists covid.covid_caso;

				/*create target table*/
				create table covid.covid_caso 
					(
					date_imported timestamp,	
	            	date date,
	            	state varchar(4),
	            	city varchar(200),
	            	place_type varchar(200),
	            	confirmed numeric,
	            	deaths numeric,
	            	order_for_place numeric,
	            	is_last varchar(80),
	            	estimated_population_2019 numeric,
	            	estimated_population numeric,
	            	city_ibge_code numeric,
	            	confirmed_per_100k_inhabitants float,
	            	death_rate float
                	);

				/* insert into target table*/               
				insert into covid.covid_caso
				select  current_timestamp as date_imported,
				        cast(date as date),
	    				state,
	    				city,
	    				place_type,
	    				confirmed,
	    				deaths,
	    				order_for_place,
	    				is_last,
	    				estimated_population_2019,
	    				estimated_population,
	    				city_ibge_code,
	    				confirmed_per_100k_inhabitants,
	    				death_rate 
				from 	public.covid_caso;

				/* drop stage table */
				drop table public.covid_caso;
            	""")
	conn.commit()
	conn.close()
						
except (yaml.YAMLError) as yaml_error:
	print("Could not load yaml error", yaml_error)
except (sqlalchemy.exc.SQLAlchemyError) as alchemy_error:
	print("Could not establish sqlalchemy connection", alchemy_error)
except (psycopg2.Error) as psyco_error:
	print("Could not establish psycopg2 connection", psyco_error)
    