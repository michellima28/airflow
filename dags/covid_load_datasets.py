from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator

default_args = {
   'owner': 'michel_lima',
   'depends_on_past': False,
   'start_date': datetime(2020, 11, 11),
   'retries': 0,
   }

with DAG(
   'covid-load-datasets',
   schedule_interval=timedelta(minutes=15),
   catchup=False,
   default_args=default_args
   ) as dag:

   t1 = BashOperator(
   task_id='caso',
   bash_command="""
   cd ~/airflow/dags/etl_scripts/
   python3 covid_caso.py
   """)

   t2 = BashOperator(
   task_id='boletim',
   bash_command="""
   cd ~/airflow/dags/etl_scripts/
   python3 covid_boletim.py
   """)

t1 >> t2
