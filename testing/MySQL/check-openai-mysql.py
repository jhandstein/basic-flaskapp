import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user="root",
    passwd="root",
    database="openai_mysql"
)

db_cursor = db.cursor()

db_cursor.execute('SELECT * FROM openai_requests')

for x in db_cursor:
    print(x)