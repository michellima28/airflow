# Airflow

My personal projects using Apache Airlfow to develop data pipeline.

---

## Prerequisites

Ubuntu 20.04

PostgreSQL

Python 3

---

## Directories

These are default folders set to store dags, scripts and configuration file:

conf file: /root/airflow/airflow.cfg 

dags: /root/airflow/dags

scripts: /root/airflow/dags/etl_scripts

---

## Installing PostgreSQL

### Update your system

```bash
sudo apt update
```

```bash
sudo apt -y upgrade
```

### Install PostgreSQL Database Server

```bash
sudo apt install postgresql postgresql-client
```

### Check if server is running

The service is automatically started upon installation, you can confirm if it is running with the command:

```bash
systemctl status postgresql.service
```

### Update PostgreSQL admin user's password

```bash
sudo su - postgres
```

```bash
psql -c "alter user postgres with password 'your_password'"
```

### Try creating a test database and user

```bash
createuser dbuser
```

```bash
createdb testdb -O dbuser
```

```bash
psql testdb
```

```bash
alter user dbuser with password 'StrongPassword';
```

```bash
\q
```

### List created databases

```bash
psql -l
```

## Installing and configuring Airflow

### Update Ubuntu packages

```bash
sudo su -
```
```bash
cd /
```

```bash
sudo apt-get update
```

### Export environment variables

```bash
export SLUGIFY_USES_TEXT_UNIDECODE=yes
```

```bash
export LC_ALL=”en_US.UTF-8"
```

```bash
export LC_CTYPE=”en_US.UTF-8"
```

```bash
sudo dpkg-reconfigure locales
```

### Install psycopg to connect to a database

```bash
sudo apt install python3-pip
```

```bash
sudo apt-get install libpq-dev
```
```bash
sudo pip3 install psycopg2
```

### Create a specific directory for Airflow

```bash
export AIRFLOW_HOME=/root/airflow
```

```bash
sudo mkdir $AIRFLOW_HOME
```

```bash
sudo chmod 777 $AIRFLOW_HOME
```

```bash
cd $AIRFLOW_HOME
```

# Install Airflow

```bash
pip3 install apache-airflow
```

### Check Airflow version

```bash
airflow version
```

### Access Airflow configuration file

```bash
vim $AIRFLOW_HOME/airflow.cfg
```

### Alter configurations

```bash
executor = LocalExecutor
sql_alchemy_conn = postgresql+psycopg2://user:password@host/database
load_examples = False
```

### Start database through Airflow

```bash
airflow initdb
```

### Start webserver on port 80

```bash
airflow webserver -p 80
```
---

## References

### PostgreSQL installation

https://computingforgeeks.com/installing-postgresql-database-server-on-ubuntu/

### Airflow installation and configuration

https://medium.com/data-hackers/primeiros-passos-com-o-apache-airflow-etl-f%C3%A1cil-robusto-e-de-baixo-custo-f80db989edae

https://medium.com/@taufiq_ibrahim/apache-airflow-installation-on-ubuntu-ddc087482c14

https://stackoverflow.com/questions/57668584/airflow-scheduler-does-not-appear-to-be-running-after-excute-a-task
