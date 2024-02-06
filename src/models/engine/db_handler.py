#!/usr/bin/python3
"""Database Handler"""

import mysql.connector
import json


class DatabaseHandler:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="   ",
            database="BankEase",
        )

    def save_update(self, usr):
        """Save the user's info to both storage (database and JSON file)."""
        cursor = self.connection.cursor()
        update_query = '''
        UPDATE users
        SET balance = %s,
        transaction_history = JSON_ARRAY_APPEND(transaction_history, '$', %s)
        WHERE id = %s and account_number = %s
        '''
        transaction_json = json.dumps(usr.transaction_history)
        cursor.execute(update_query, (
            usr.balance, transaction_json, usr.id, usr.account_number
            ))
        self.connection.commit()
        cursor.close()

        # Update information in the JSON file
        users = usr.load_users()
        # Find the user's data in the list and update it
        for user_data in users:
            if user_data["id"] == usr.id:
                user_data["balance"] = usr.balance
                user_data["transaction_history"].append(usr.transaction_history)

        # Save the updated user data back to the JSON file
        with open("user_data.json", "w") as file:
            for user_data in users:
                json.dump(user_data, file)
                file.write("\n")

        self.connection.close()
