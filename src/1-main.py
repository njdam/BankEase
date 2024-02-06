#!/usr/bin/python3

import json
from models.user import User, authenticate_user


# Assuming you have an instance of User, for example, user1
if __name__ == "__main__":
    '''
    def authenticate_user():
        while True:
            try:
                username = User.get_valid_username()
                password = User.get_valid_password()
                try:
                    user = User.signin(username, password)
                    return user
                except AuthenticationError as e:
                    print(f"{e} Please try again!")
            except KeyboardInterrupt:
                print("\nThank you for visiting us!")
                print("Exiting............")
                exit()'''

    user1 = authenticate_user()
    if user1:
        # Perform actions on the user instance
        deposit_amount = input("Enter amount to deposit: ")
        user1.deposit(deposit_amount)

        withdraw_amount = input("Enter amount to withdraw: ")
        user1.withdraw(withdraw_amount)
    else:
        print("User not found.")

        # Transfer example (assuming you have another user instance called user2)
    user2 = authenticate_user()
    if user2:
        transfer_amount = input("Enter amount to transfer: ")
        user1 = input("Enter username of reciever: ")
        user2.transfer(user1, transfer_amount)

        user_info = User.load_users()
        print("\nUpdated User Information:")
        print(json.dumps(user_info, indent=2))
    else:
        print("User not found.")
