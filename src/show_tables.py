#!/usr/bin/python3

from models.engine.db_connector import connect_to_mysql


connection = connect_to_mysql()
cursor = connection.cursor()


cursor.execute("SELECT * FROM users")

result = cursor.fetchall()

for row in result:
    print(row)

# Commit the change to the database
connection.commit()
connection.close()
