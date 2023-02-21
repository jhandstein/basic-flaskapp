import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user="root",
    passwd="root",
    database="testdatabase"
)

db_cursor = db.cursor()

# db_cursor.execute("CREATE DATABASE IF NOT EXISTS testdatabase")

# db_cursor.execute("CREATE TABLE Person (name VARCHAR(50) NOT NULL, age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")

db_cursor.execute('INSERT INTO Person (name, age) VALUES (%s, %s)', ('Sina', 15))
db.commit()
db_cursor.execute('SELECT * FROM Person')

for x in db_cursor:
    print(x)