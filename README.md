![alt text](https://miro.medium.com/max/7200/1*NNtzqHo1jW4bHowmkWn7uA.png)

# Airflow

My personal projects using Apache Airlfow to develop data pipeline.

---

## Prerequisites

python 3

pip 3

---

## Directories

These are default folders set to store dags, scripts and configuration file:

conf file: ~/airflow/airflow.cfg 

dags: ~/airflow/dags

scripts: ~/airflow/dags/etl_scripts

---

## Installing PostgreSQL

### Update your system

```bash
sudo apt -y update
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

### Type postgres user's password, in this case the password is "admin", but you can choose whatever you want

```bash
psql -c "alter user postgres with password 'admin'"
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

### Type the database user's password, in this case the password is "12345", but you can choose whatever you want

```bash
alter user dbuser with password '12345';
```

```bash
\q
```

### List created databases and then, exit

```bash
psql -l
```

```bash
exit
```

### Type exit again to go out from root

```bash
exit
```

---

## Installing and configuring Airflow

### Install libpq-dev and psycopg2 to connect to a database

```bash
sudo apt-get install libpq-dev
```

```bash
sudo pip3 install psycopg2
```

### Create a specific directory for Airflow

```bash
export AIRFLOW_HOME=~/airflow
```

### Install Apache Airflow

```bash
pip3 install apache-airflow
```

### Initialize database

```bash
airflow db init
```

### After initialization is done, create a user for Airflow WebServer. You can copy the script below and edit to put your own credentials.

```bash
airflow users create \
    --username admin \
    --firstname Michel \
    --lastname Lima \
    --role Admin \
    --email michelcorreialima@gmail.com
```

### Now, access Airflow configuration file.

```bash
cd ~/airflow
```

```bash
vim airflow.cfg
```

### Alter configurations inside the file. Search for the parameters below and change to the following values:

```bash
executor = LocalExecutor

sql_alchemy_conn = postgresql+psycopg2://user:password@host/database

load_examples = False
```

### Save and close airflow.cfg and then start webserver on port 80

```bash
airflow webserver -p 80
```

### Start Airflow Scheduler in another terminal window. Finally, all things are ready!

```bash
airflow scheduler
```

---

## References

### PostgreSQL installation

https://computingforgeeks.com/installing-postgresql-database-server-on-ubuntu/

### Airflow installation

https://airflow.apache.org/docs/apache-airflow/stable/start.html

### Airflow with Postgres

https://medium.com/data-hackers/primeiros-passos-com-o-apache-airflow-etl-f%C3%A1cil-robusto-e-de-baixo-custo-f80db989edae

https://medium.com/@taufiq_ibrahim/apache-airflow-installation-on-ubuntu-ddc087482c14

https://stackoverflow.com/questions/57668584/airflow-scheduler-does-not-appear-to-be-running-after-excute-a-task

### Airflow fails to start or check version

https://github.com/apache/airflow/issues/11965
