#!/usr/bin/python3

import mysql.connector


def connect_to_mysql():
    return mysql.connector.connect(
            host="localhost",
            user="admin",
            password="   ",
            database="BankEase"
            )
