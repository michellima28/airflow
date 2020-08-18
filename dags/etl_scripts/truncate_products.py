# import psycopg2 module
import psycopg2

# set postgresql connection and run sql script
try:
    connection = psycopg2.connect(user = "dbuser",
                                  password = "Y@smin2019",
                                  host = "localhost",
                                  port = "5432",
                                  database = "testdb")

    cursor = connection.cursor()

    # truncate table
    cursor.execute("TRUNCATE airflow_data.products;")
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
            