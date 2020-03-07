#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-03-05
@note    0.0.1 (2020-03-05) : Init file
'''

import mysql.connector
from mysql.connector import errorcode
from .config import Config


class SetupDatabase:
    def __init__(self, database) -> None:
        self.database = database


    def create_tables(self):
        cursor = self.database.connection.cursor()
        for table_name in Config.TABLES:
            table_description = Config.TABLES[table_name]
            try:
                print(
                    "Creating table {}: ".format(table_name),
                    end='',
                    flush=True,
                )
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.", flush=True)
                else:
                    print(err.msg, flush=True)
            else:
                print("OK", flush=True)
        cursor.close()

    def delete_tables(self):
        cursor = self.database.connection.cursor()
        try:
            print("Deleting tables: ", end='', flush=True)
            cursor.execute(
                'DROP TABLE category, category_has_product, product, store, store_has_product, substituted_product;'
            )
        except mysql.connector.Error as err:
            print(err.msg, flush=True)
        else:
            print("OK", flush=True)
        cursor.close()
