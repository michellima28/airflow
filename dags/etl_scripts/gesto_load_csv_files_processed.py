# import psycopg2 module
import psycopg2

# set postgresql connection and run sql script
try:
    connection = psycopg2.connect(user = "dbuser",
                                  password = "12345",
                                  host = "localhost",
                                  port = "5432",
                                  database = "localdb")

    cursor = connection.cursor()

    # truncate
    cursor.execute("""truncate table gesto.contas;""")
    connection.commit()

    # insert
    cursor.execute("""
                    insert into gesto.contas
                    select email 
                        , "name"
                        , "Data" 
                        , cast(valor as integer) as valor  
                        , procedimento 
                        , tipo 
                        , prestador 
                        , observacao 
                        , to_date(competencia, 'dd/mm/yyyy') as competencia 
                    from   public.contas;
                   """)
    connection.commit()

    # drop
    cursor.execute("""drop table public.contas;""")
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