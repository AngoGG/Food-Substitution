#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-01-29
@note    0.0.1 (2020-01-29) : Init file
'''

import time
import mysql.connector
from os import environ
from mysql.connector import errorcode
from config.config import Config
from typing import List


class Database:
    def __init__(self, host, user, passwd, db=None, charset="utf8"):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.connection = None
        self.category_list = []
        self.store_list = []

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

    def insert(self, query, lastrowid=False):
        '''Open Cursor, Execute the Insert and commit changes to the database.'''
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        if lastrowid:
            store_id = cursor.lastrowid
            cursor.close()
            return store_id
        else:
            cursor.close()

    def disconnect(self):
        '''Close the database connection.'''
        self.connection.close()

    def create_tables(self):
        cursor = self.connection.cursor()
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
        cursor = self.connection.cursor()
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

    def populate_from_json(self, product):
        ''' '''
        product_name = product['Aliment'].replace('"', '""')
        if not self.query(
            f"SELECT * from product WHERE product_name = \"{product_name}\""
        ):
            self.insert(
                f"INSERT INTO product VALUES ({product['id']}, \"{product_name}\", \"{product['Url']}\", \"{product['Nutriscore']}\");"
            )
            for store_id in self.populate_stores(product['Magasins']):
                self._populate_store_has_product(store_id, product['id'])

            for category_id in self.populate_categories(product['Categories']):
                self._populate_category_has_product(category_id, product['id'])

    def populate_stores(self, stores):
        for store in list(set(stores)):
            if store not in self.store_list:
                self.store_list.append(store)
                store_id = self.insert(
                    f"INSERT INTO store (store_name)  VALUES (\"{store}\");",
                    lastrowid=True,
                )
                yield store_id
            else:
                store_id = self.query(
                    f"SELECT id from store WHERE store_name = \"{store}\";"
                )
                yield store_id[0][0]

    def _populate_store_has_product(self, store_id, product_id):
        self.insert(
            f"INSERT INTO store_has_product VALUES ({store_id}, \"{product_id}\");"
        )

    def populate_categories(self, categories):
        categories.replace(", ", ",")
        for category in categories.split(","):
            new_category = category.lstrip()
            if new_category not in self.category_list:
                if "en:" not in category:
                    self.category_list.append(new_category)
                    category_id = self.insert(
                        f"INSERT INTO category (category_name)  VALUES (\"{new_category}\");",
                        lastrowid=True,
                    )
                    yield category_id
            else:
                category_id = self.query(
                    f"SELECT id from category WHERE category_name = \"{new_category}\";"
                )
                yield category_id[0][0]

    def _populate_category_has_product(self, category_id, product_id):
        self.insert(
            f"INSERT INTO category_has_product VALUES ({category_id}, \"{product_id}\");"
        )

    def __del__(self):
        if self.connection is not None:
            self.disconnect()
