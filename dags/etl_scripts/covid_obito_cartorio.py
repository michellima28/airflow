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
gz_filepath = '{}/files/obito_cartorio.csv.gz'.format(my_parent_folder)
csv_filepath = '{}/files/obito_cartorio.csv'.format(my_parent_folder)

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
	df_covid_caso.to_sql('obito_cartorio', alchemy_engine, if_exists='replace', index=False)
	os.remove(csv_filepath)

	# create cursor and execure sql commands  
	cur = conn.cursor()
	cur.execute("""
				/*create schema*/
				create schema if not exists covid;

				/* drop table*/
				drop table if exists covid.obito_cartorio;

				/*create target table*/
				create table covid.obito_cartorio
					(
					date_imported timestamp,	
	            	date date,
	            	state varchar(4),
	            	epidemiological_week_2019 numeric,
	            	epidemiological_week_2020 numeric,
	            	deaths_indeterminate_2019 numeric,
	            	deaths_respiratory_failure_2019 numeric,
	            	deaths_others_2019 numeric,
	            	deaths_pneumonia_2019 numeric,
	            	deaths_septicemia_2019 numeric,
	            	deaths_sars_2019 numeric,
	            	deaths_covid19 numeric,
	            	deaths_indeterminate_2020 numeric,
	            	deaths_respiratory_failure_2020 numeric,
	            	deaths_others_2020 numeric,
	            	deaths_pneumonia_2020 numeric,
	            	deaths_septicemia_2020 numeric,
	            	deaths_sars_2020 numeric,
	            	deaths_total_2019 numeric,
	            	deaths_total_2020 numeric,
	            	new_deaths_indeterminate_2019 numeric,
	            	new_deaths_respiratory_failure_2019 numeric,
	            	new_deaths_others_2019 numeric,
	            	new_deaths_pneumonia_2019 numeric,
	            	new_deaths_septicemia_2019 numeric,
	            	new_deaths_sars_2019 numeric,
	            	new_deaths_covid19 numeric,
	            	new_deaths_indeterminate_2020 numeric,
	            	new_deaths_respiratory_failure_2020 numeric,
	            	new_deaths_others_2020 numeric,
	            	new_deaths_pneumonia_2020 numeric,
	            	new_deaths_septicemia_2020 numeric,
	            	new_deaths_sars_2020 numeric,
	            	new_deaths_total_2019 numeric,
	            	new_deaths_total_2020 numeric
                	);

				/* insert into target table*/               
				insert into covid.obito_cartorio
				select  current_timestamp as date_imported,
				        cast(date as date),
				        state,
				        epidemiological_week_2019,
				        epidemiological_week_2020,
				        deaths_indeterminate_2019,
				        deaths_respiratory_failure_2019,
				        deaths_others_2019,
				        deaths_pneumonia_2019,
				        deaths_septicemia_2019,
				        deaths_sars_2019,
				        deaths_covid19,
				        deaths_indeterminate_2020,
				        deaths_respiratory_failure_2020,
				        deaths_others_2020,
				        deaths_pneumonia_2020,
				        deaths_septicemia_2020,
				        deaths_sars_2020,
				        deaths_total_2019,
				        deaths_total_2020,
				        new_deaths_indeterminate_2019,
				        new_deaths_respiratory_failure_2019,
				        new_deaths_others_2019,
				        new_deaths_pneumonia_2019,
				        new_deaths_septicemia_2019,
				        new_deaths_sars_2019,
				        new_deaths_covid19,
				        new_deaths_indeterminate_2020,
				        new_deaths_respiratory_failure_2020,
				        new_deaths_others_2020,
				        new_deaths_pneumonia_2020,
				        new_deaths_septicemia_2020,
				        new_deaths_sars_2020,
				        new_deaths_total_2019,
				        new_deaths_total_2020
				from 	public.obito_cartorio;

				/* drop stage table */
				drop table public.obito_cartorio;
            	""")
	conn.commit()
	conn.close()
						
except (yaml.YAMLError) as yaml_error:
	print("Could not load yaml error", yaml_error)
except (sqlalchemy.exc.SQLAlchemyError) as alchemy_error:
	print("Could not establish sqlalchemy connection", alchemy_error)
except (psycopg2.Error) as psyco_error:
	print("Could not establish psycopg2 connection", psyco_error)
    