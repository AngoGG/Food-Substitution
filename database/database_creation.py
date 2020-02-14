#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-01-29
@note    0.0.1 (2020-01-29) : Init file
'''
from __future__ import print_function

import mysql.connector
from os import environ
from mysql.connector import errorcode
from database.config import Config


class Creation:
    def __init__(self):
        self.connexion = mysql.connector.connect(
            host=environ.get['HOST'],
            user=environ.get['USER'],
            password=environ.get['PASSWORD'],
            database=None,
        )
        self.cursor = self.connexion.cursor()

    def create_database(self):
        try:
            self.cursor.execute(f'CREATE DATABASE {Config.DB_NAME}')
        except mysql.connector.Error as err:
            print(f'Failed creating database: {err}')
            exit(1)

        try:
            self.cursor.execute(f'USE {Config.DB_NAME}')
        except mysql.connector.Error as err:
            print(f'Database {Config.DB_NAME} does not exists.')
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                print(f'Database {Config.DB_NAME} created successfully.')
                self.connexion.database = DB_NAME
            else:
                print(err)
                exit(1)

    def create_table(self):
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        self.cursor.close()
        self.connexion.close()
