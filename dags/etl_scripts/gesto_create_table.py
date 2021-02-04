# import psycopg2 module
import psycopg2

# set postgresql connection and run sql script
try:
    connection = psycopg2.connect(user = "dbuser",
                                  password = "12345",
                                  host = "localhost",
                                  port = "5432",
                                  database = "testdb")

    cursor = connection.cursor()
    # create schema 
    cursor.execute("""create schema if not exists gesto;""")

    # create table
    cursor.execute("""create table if not exists gesto.contas (
	email varchar(200)
  , name varchar(200)
  , data varchar(50)
  , valor integer
  , procedimento varchar(200)
  , tipo varchar(200)
  , prestador varchar(200)
  , observacao varchar(200)
  , competencia date
);""")

    connection.commit()
    print("SQL command executed sucessfully!")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")