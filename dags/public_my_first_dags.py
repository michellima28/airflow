from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator

default_args = {
   'owner': 'michel_lima',
   'depends_on_past': False,
   'start_date': datetime(2019, 1, 1),
   'retries': 0,
   }

with DAG(
   'public-my-first-dag',
   schedule_interval=timedelta(minutes=1),
   catchup=False,
   default_args=default_args
   ) as dag:

   t1 = BashOperator(
   task_id='first_etl',
   bash_command="""
   cd ~/airflow/dags/etl_scripts/
   python3 public_my_first_etl_script.py
   """)

   t2 = BashOperator(
   task_id='second_etl',
   bash_command="""
   cd ~/airflow/dags/etl_scripts/
   python3 public_my_second_etl_script.py
   """)

t1 >> t2
      