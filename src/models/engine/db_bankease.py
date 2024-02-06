#!/usr/bin/python3

from models.engine.db_handler import DatabaseHandler


class DB_BankEase:
    """Connection to MySQL database and save to Json Storage."""
    db_handler = DatabaseHandler()

    @classmethod
    def save_update(cls, user):
        """Save the user's info to both storage (database and JSON file)."""
        cls.db_handler.save_update(user)
        """
        cursor = cls.connection.cursor()
        update_query = '''
        UPDATE users
        SET balance = %s,
        transaction_history = JSON_ARRAY_APPEND(transaction_history, '$', %s)
        WHERE id = %s and account_number = %s
        '''
        cursor.execute(update_query, (
            cls.balance, cls.transaction_history, cls.id, cls.account_number
            ))
        cls.connection.commit()
        cursor.close()

        # Update information in the JSON file
        users = cls.load_users()
        # Find the user's data in the list and update it
        for user_data in users:
            if user_data["id"] == cls.id:
                user_data["balance"] = cls.balance
                user_data["transaction_history"].append(cls.transaction_history)

        # Save the updated user data back to the JSON file
        with open("../user_data.json", "w") as file:
            for user_data in users:
                json.dump(user_data, file)
                file.write("\n")

        cls.connection.close()
        """
