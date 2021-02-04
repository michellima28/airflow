from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator

default_args = {
   'owner': 'michel_lima',
   'depends_on_past': True,
   'start_date': datetime(2020, 8, 18),
   'retries': 0,
   }

with DAG(
   'public_products-update',
   schedule_interval=timedelta(minutes=1),
   catchup=False,
   default_args=default_args
   ) as dag:

   t1 = BashOperator(
   task_id='truncate_table',
   bash_command="""
   cd ~/airflow/dags/etl_scripts/
   python3 public_truncate_products.py
   """)

   t2 = BashOperator(
   task_id='insert_into',
   bash_command="""
   cd ~/airflow/dags/etl_scripts/
   python3 public_insert_products_data.py
   """)

t1 >> t2
