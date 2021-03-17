from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator

default_args = {
   'owner': 'michel_lima',
   'depends_on_past': False,
   'start_date': datetime(2021, 3, 16),
   'retries': 0,
   }

with DAG(
   'iss-api-load-data',
   schedule_interval=timedelta(minutes=15),
   catchup=False,
   default_args=default_args
   ) as dag:

   t1 = BashOperator(
   task_id='get-astros',
   bash_command="""
   cd ~/airflow/dags/etl_scripts/
   python3 iss_api_get_astros.py
   """)

   t2 = BashOperator(
   task_id='import-astros',
   bash_command="""
   cd ~/airflow/dags/etl_scripts/
   python3 iss_api_import_astros.py
   """)

t1 >> t2
