# airflow
Personal projects using Apache Airlfow to develop data pipeline.

## prerequisites
I installed this application on Ubuntu 20.04 and to do so, first I installed PostgreSQL

## installing postgresql

## installing and configuring airflow
### update ubuntu packages
sudo su
cd ~
sudo apt-get update

# export environment variables
export SLUGIFY_USES_TEXT_UNIDECODE=yes
export LC_ALL=”en_US.UTF-8"
export LC_CTYPE=”en_US.UTF-8"
sudo dpkg-reconfigure locales

# install psycopg to connect to a database
sudo apt install python3-pip
sudo apt-get install libpq-dev
sudo pip3 install psycopg2

# create a specific directory for airflow
export AIRFLOW_HOME=/airflow
sudo mkdir $AIRFLOW_HOME
sudo chmod 777 $AIRFLOW_HOME
cd $AIRFLOW_HOME

# install airflow
pip3 install apache-airflow

# check airflow version
airflow version

# access airflow configuration file
vim $AIRFLOW_HOME/airflow.cfg

# alter configurations
executor = LocalExecutor
sql_alchemy_conn = postgresql+psycopg2://dbuser:Y@smin2019@localhost/testdb
load_examples = False

# start database through airflow
airflow initdb

# start webserver on port 80
airflow webserver -p 80

