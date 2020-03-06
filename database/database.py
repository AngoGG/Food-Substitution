#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-01-29
@note    0.0.1 (2020-01-29) : Init file
'''

import random
import time
import mysql.connector
from os import environ
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

    def get_product(self, category):
        ''' get all products from the selected category and return the first 10 rows '''
        request = "SELECT p.id, p.product_name, p.nutriscore_grade, c.category_name" + \
                    " FROM product p" + \
                    " LEFT JOIN category_has_product chp ON p.id = chp.product_id" + \
                    " LEFT JOIN category c ON chp.category_id = c.id" + \
                    f" WHERE c.category_name = '{category}'" + \
                    " AND nutriscore_grade > 'C' " + \
                    "LIMIT 10"
        return self.query(request)

    def get_substitute(self, category):
        ''' For a given product, get all products with the same category and return one  '''

        substitute = self.select_substitute(category)
        substitute_infos = self.get_substitute_infos(substitute)
        substitute_infos.append(self.get_substitute_stores(substitute))
        return substitute_infos
    
    def select_substitute(self, category):
        ''' '''
        category_id_request = "SELECT id " + \
                    " FROM category" + \
                    f" WHERE category_name = '{category}'"
        category_id = self.query(category_id_request)
        category_products_id_request = "SELECT p.id" + \
                            " FROM product p" + \
                            " INNER JOIN category_has_product chp ON p.id = chp.product_id" + \
                            f" WHERE chp.category_id = '{category_id[0][0]}'" + \
                            " AND p.nutriscore_grade <= 'C' "
        products_in_category = self.query(category_products_id_request)
        return random.choice(products_in_category)

    def get_substitute_infos(self, substitute_id):
        ''' '''
        substitute_info_request = f"SELECT * FROM product WHERE id = '{substitute_id[0]}'" 
        return self.query(substitute_info_request)

    def get_substitute_stores(self, substitute_id):
        ''' '''
        substitute_stores_request = "SELECT s.store_name" + \
                                    " FROM store s" + \
                                    " INNER JOIN store_has_product shp ON s.id = shp.store_id" + \
                                    f" WHERE shp.product_id = '{substitute_id[0]}'"
        stores_list= []
        for store in self.query(substitute_stores_request):
            stores_list.append(store[0])
        return stores_list

    def disconnect(self):
        '''Close the database connection.'''
        self.connection.close()

    def __del__(self):
        if self.connection is not None:
            self.disconnect()