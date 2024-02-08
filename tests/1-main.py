#!/usr/bin/python3

import json
from models.users import User


# Assuming you have an instance of User, for example, user1
if __name__ == "__main__":
    try:
        '''
        User.signup()
        user1 = User.signin()
        if user1:
            # Perform actions on the user instance
            deposit_amount = input("Enter amount to deposit: ")
            account1 = user1.get_account()
            account1.deposit(deposit_amount)

            withdraw_amount = input("Enter amount to withdraw: ")
            account1.withdraw(withdraw_amount)
        else:
            print("User not found.")
        '''

        # Transfer example (assuming you have another user instance called user2)
        user2 = User.signin()
        if user2:
            transfer_amount = input("Enter amount to transfer: ")
            recipient = input("Enter Account number of reciever: ")
            account2 = user2.get_account()
            account2.transfer(recipient, transfer_amount)

            account = account2.get_account_by_account_number(recipient)
            user_info = account.get_account_by_user_id(account.user_id)
            print("\nUpdated User Information:")
            print(json.dumps(user_info, indent=2))
        else:
            print("User not found.")

    except Exception:
        raise Exception("Failed to Work Smoothly from main file!")

    finally:
        User.disconnect()
