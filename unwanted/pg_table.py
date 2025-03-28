import os

import psycopg2

# connection = psycopg2.connect(host="localhost", dbname="movies", user="postgres", password="123456789", port="5432")
# os.environ['PGSERVICEFILE'] =
print(os.environ["PGSERVICEFILE"])
# print(os.path.relpath('{dir}\\pg_service.conf'.format(dir=os.getcwd())))
connection = psycopg2.connect(service="my_service")
cursor = connection.cursor()


# cursor.execute("SELECT * FROM movies")
# cursor.execute("SELECT genre FROM movies")
# cursor.execute("SELECT genre FROM movies WHERE genre='Romance'")
cursor.execute(f"SELECT genre FROM movies_backup WHERE genre=%(gen)s", {"gen": 'Romance', })
# cursor.execute(f"SELECT genre FROM movies_backup WHERE genre='Rom'",)
print(cursor.fetchall())

