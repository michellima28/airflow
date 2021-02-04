# import psycopg2 module
import psycopg2

# set postgresql connection and run sql script
try:
    connection = psycopg2.connect(user = "dbuser",
                                  password = "12345",
                                  host = "localhost",
                                  port = "5432",
                                  database = "testdb")

    # init cursor method
    cursor = connection.cursor()

    # query
    sql_query = '''insert into airflow_data.products (id, name, price)
                   values (17, 'smart tv sony', 3000);'''

    # execute query
    cursor.execute(sql_query)
    connection.commit()
    print("Data inserted sucessfully!")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            