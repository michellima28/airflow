# airflow
Personal projects using Apache Airlfow to develop data pipeline.

# prerequisites
I installed this application on Ubuntu 20.04 and to do so, first I installed PostgreSQL

# installing postgresql

# installing and configuring airflow
### update ubuntu packages
sudo su

cd ~

sudo apt-get update

### export environment variables
export SLUGIFY_USES_TEXT_UNIDECODE=yes

export LC_ALL=”en_US.UTF-8"

export LC_CTYPE=”en_US.UTF-8"

sudo dpkg-reconfigure locales

### install psycopg to connect to a database
sudo apt install python3-pip

sudo apt-get install libpq-dev

sudo pip3 install psycopg2

### create a specific directory for airflow
export AIRFLOW_HOME=/airflow

sudo mkdir $AIRFLOW_HOME

sudo chmod 777 $AIRFLOW_HOME

cd $AIRFLOW_HOME

### install airflow
pip3 install apache-airflow

### check airflow version
airflow version

### access airflow configuration file
vim $AIRFLOW_HOME/airflow.cfg

### alter configurations
executor = LocalExecutor

sql_alchemy_conn = postgresql+psycopg2://user:password@host/database

load_examples = False

### start database through airflow
airflow initdb

### start webserver on port 80
airflow webserver -p 80

### references
postgresql installation

https://computingforgeeks.com/installing-postgresql-database-server-on-ubuntu/

airflow installation and configuration

https://medium.com/data-hackers/primeiros-passos-com-o-apache-airflow-etl-f%C3%A1cil-robusto-e-de-baixo-custo-f80db989edae

https://medium.com/@taufiq_ibrahim/apache-airflow-installation-on-ubuntu-ddc087482c14

https://stackoverflow.com/questions/57668584/airflow-scheduler-does-not-appear-to-be-running-after-excute-a-task

