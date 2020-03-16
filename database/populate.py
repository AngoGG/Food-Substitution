#!/usr/bin/env python3

import mysql.connector


class Populate:
    def __init__(self, database) -> None:
        self.database = database
        self.store_list = []
        self.category_list = []

    def insert_datas(self, product: Dict) -> None:
        """ """
        product_name = product["Aliment"].replace('"', '""')
        if not self.database.query(
            "SELECT * from product WHERE product_name = %s", (product_name,),
        ):
            self.database.insert(
                "INSERT INTO product VALUES (%s, %s, %s, %s);",
                (product["id"], product_name, product["Url"], product["Nutriscore"]),
            )
            for store_id in self.populate_stores(product["Magasins"]):
                self._populate_store_has_product(store_id, product["id"])

            for category_id in self.populate_categories(product["Categories"]):
                self._populate_category_has_product(category_id, product["id"])

    def populate_stores(self, stores: List) -> Generator:
        for store in list(set(stores)):
            if store not in self.store_list:
                self.store_list.append(store)
                store_id = self.database.insert(
                    "INSERT INTO store(store_name) VALUES (%s);",
                    (store,),
                    lastrowid=True,
                )
                yield store_id
            else:
                store_id = self.database.query(
                    "SELECT id from store WHERE store_name = %s;", (store,)
                )
                yield store_id[0][0]

    def _populate_store_has_product(self, store_id: str, product_id: str) -> None:
        self.database.insert(
            "INSERT INTO store_has_product VALUES (%s, %s);", (store_id, product_id),
        )

    def populate_categories(self, categories: List) -> Generator:
        categories.replace(", ", ",")
        for category in categories.split(","):
            new_category = category.lstrip()
            if new_category not in self.category_list:
                if "en:" not in category:
                    self.category_list.append(new_category)
                    category_id = self.database.insert(
                        "INSERT INTO category (category_name)  VALUES (%s);",
                        (new_category,),
                        lastrowid=True,
                    )
                    yield category_id
            else:
                category_id = self.database.query(
                    "SELECT id from category WHERE category_name = %s;",
                    (new_category,),
                )
                yield category_id[0][0]

    def _populate_category_has_product(self, category_id: str, product_id: str) -> None:
        self.database.insert(
            "INSERT INTO category_has_product VALUES (%s, %s);",
            (category_id, product_id),
        )

