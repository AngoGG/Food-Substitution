# #!/usr/bin/env python3
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
        request = "SELECT p.id, p.product_name, p.url, p.nutriscore_grade, c.category_name" + \
                    " FROM product p" + \
                    " LEFT JOIN category_has_product chp ON p.id = chp.product_id" + \
                    " LEFT JOIN category c ON chp.category_id = c.id" + \
                    f" WHERE c.category_name = '{category}'" + \
                    " AND nutriscore_grade > 'C' " + \
                    " ORDER BY RAND() " + \
                    " LIMIT 10"
        return self.query(request)

    def get_substitute(self, category):
        ''' For a given product, get all products with the same category and return one  '''

        substitute = self.select_substitute(category)
        return self.get_substitute_infos(substitute[0][0])
    
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
                            " AND p.nutriscore_grade <= 'C' " + \
                            " ORDER BY RAND() " + \
                            " LIMIT 1"

        return self.query(category_products_id_request)

    def get_substitute_infos(self, substitute_id):
        ''' '''
        substitute_info_request = f"SELECT * FROM product WHERE id = '{substitute_id}'"
        return self.query(substitute_info_request)[0]

    def get_stores(self, product_id):
        ''' '''
        product_stores_request = "SELECT s.store_name" + \
                                    " FROM store s" + \
                                    " INNER JOIN store_has_product shp ON s.id = shp.store_id" + \
                                    f" WHERE shp.product_id = '{product_id}'"
        stores_list= []
        for store in self.query(product_stores_request):
            stores_list.append(store[0])
        return stores_list
    
    def get_categories(self, product_id):
        ''' '''
        product_categories_request = "SELECT c.category_name" + \
                                    " FROM category c" + \
                                    " INNER JOIN category_has_product chp ON c.id = chp.category_id" + \
                                    f" WHERE chp.product_id = '{product_id}'"
        categories_list= []
        for store in self.query(product_categories_request):
            categories_list.append(store[0])
        return categories_list
    
    def add_favorite(self, product_id, substitute_id):
        ''' '''
        add_favorite_request = f"INSERT INTO substituted_product VALUES ('{substitute_id}', '{product_id}')"
        self.insert(add_favorite_request)
    
    def get_favorites(self):
        ''' '''
        return self.query("SELECT * FROM substituted_product")


    def disconnect(self):
        '''Close the database connection.'''
        self.connection.close()

    def __del__(self):
        if self.connection is not None:
            self.disconnect()