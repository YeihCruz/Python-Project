import psycopg2

conn = psycopg2.connect(host="localhost", port=5432, dbname="postgres", user="postgres", password="damisela")
conn.autocommit = True
cur = conn.cursor()
cur.execute("SELECT 1 FROM pg_database WHERE datname = 'AgenciaSegurosPython'")
if not cur.fetchone():
    cur.execute('CREATE DATABASE "AgenciaSegurosPython"')
    print("Database created")
else:
    print("Database already exists")
cur.close()
conn.close()
