#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-03-05
@note    0.0.1 (2020-03-05) : Init file
'''

import mysql.connector

class Populate:
    
    def __init__(self, database) -> None:
        self.database = database
        self.store_list = []
        self.category_list = []

    def insert_datas(self, product):
        ''' '''
        product_name = product['Aliment'].replace('"', '""')
        if not self.database.query(
            f"SELECT * from product WHERE product_name = \"{product_name}\""
        ):
            self.database.insert(
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
                store_id = self.database.insert(
                    f"INSERT INTO store (store_name)  VALUES (\"{store}\");",
                    lastrowid=True,
                )
                yield store_id
            else:
                store_id = self.database.query(
                    f"SELECT id from store WHERE store_name = \"{store}\";"
                )
                yield store_id[0][0]

    def _populate_store_has_product(self, store_id, product_id):
        self.database.insert(
            f"INSERT INTO store_has_product VALUES ({store_id}, \"{product_id}\");"
        )

    def populate_categories(self, categories):     
        categories.replace(", ", ",")
        for category in categories.split(","):
            new_category = category.lstrip()
            if new_category not in self.category_list:
                if "en:" not in category:
                    self.category_list.append(new_category)
                    category_id = self.database.insert(
                        f"INSERT INTO category (category_name)  VALUES (\"{new_category}\");",
                        lastrowid=True,
                    )
                    yield category_id
            else:
                category_id = self.database.query(
                    f"SELECT id from category WHERE category_name = \"{new_category}\";"
                )
                yield category_id[0][0]

    def _populate_category_has_product(self, category_id, product_id):
        self.database.insert(
            f"INSERT INTO category_has_product VALUES ({category_id}, \"{product_id}\");"
        )

