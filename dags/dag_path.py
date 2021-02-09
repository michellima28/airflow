from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
   'owner': 'michel_lima',
   'depends_on_past': False,
   'start_date': datetime(2019, 1, 1),
   'retries': 0,
   }

with DAG(
   'public-dag-path-test',
   schedule_interval=timedelta(minutes=1),
   catchup=False,
   default_args=default_args
   ) as dag:

   t1 = BashOperator(
   task_id='show_the_path',
   bash_command="""
   cd ~/airflow/dags/etl_scripts/
   python3 public_my_path.py
   """)
