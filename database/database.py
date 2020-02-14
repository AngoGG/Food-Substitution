#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-01-29
@note    0.0.1 (2020-01-29) : Init file
'''

import mysql.connector
from os import environ
from mysql.connector import errorcode
from database.config import Config


class Database:
    def __init__(self, host, user, passwd, db=None, charset="utf8"):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.connection = None
        self.category_list = []

    def connect(self):
        '''Database connection.'''
        self.connection = mysql.connector.connect(
            host=self.host,
            db=self.db,
            user=self.user,
            passwd=self.passwd,
            charset=self.charset,
        )

    def query(self, query):
        '''Open Cursor, Execute the Query and return result.'''
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insert(self, query):
        '''Open Cursor, Execute the Insert and commit changes to the database.'''
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()

    def disconnect(self):
        '''Close the database connection.'''
        self.connection.close()

    def __del__(self):
        if self.connection is not None:
            self.disconnect()

    def create_tables(self):
        cursor = self.connection.cursor()
        for table_name in Config.TABLES:
            table_description = Config.TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
        cursor.close()

    def populate_from_json(self, json):

        for product in json:
            self.insert(
                f"INSERT INTO product VALUES ({product['id']}, \"{product['Aliment']}\", \"{product['Url']}\", \"{product['Nutriscore']}\");"
            )
            self.populate_caterogies(product['Categories'])

    def populate_caterogies(self, categories):
        for category in categories.split(", "):
            if category not in self.category_list:
                if "en:" not in category:
                    self.category_list.append(category)
                    print(self.category_list)
                    self.insert(
                        f"INSERT INTO category (category_name)  VALUES (\"{category}\");"
                    )

    def populate_stores(self):
        pass

