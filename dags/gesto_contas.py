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
   'gesto-contas-update',
   schedule_interval=timedelta(minutes=1),
   catchup=False,
   default_args=default_args
   ) as dag:

   t1 = BashOperator(
   task_id='create_table',
   bash_command="""
   cd ~/airflow/dags/etl_scripts/
   python3 gesto_create_table.py
   """)

   t2 = BashOperator(
   task_id='load_csv_raw_data',
   bash_command="""
   cd ~/airflow/dags/etl_scripts/
   python3 gesto_load_csv_files_raw.py
   """)

   t3 = BashOperator(
   task_id='load_csv_processed_data',
   bash_command="""
   cd ~/airflow/dags/etl_scripts/
   python3 gesto_load_csv_files_processed.py
   """)

t1 >> t2 >> t3
