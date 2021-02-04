# import psycopg2 module
import psycopg2

# set postgresql connection and run sql script
try:
    connection = psycopg2.connect(user = "dbuser",
                                  password = "12345",
                                  host = "localhost",
                                  port = "5432",
                                  database = "localdb")

    # init cursor method
    cursor = connection.cursor()

    # query
    sql_query = '''create table public.products (id numeric
                                               , name varchar(150)
                                               , price decimal(15,2)
                                                 );'''

    # execute query
    cursor.execute(sql_query)
    connection.commit()
    print("Table created sucessfully!")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            