# #!/usr/bin/env python3

from typing import List, Tuple
import mysql.connector


class Database:
    def __init__(self, host, user, passwd, db=None, charset="utf8"):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.connection = None

    def connect(self) -> None:
        """Database connection."""
        self.connection = mysql.connector.connect(
            host=self.host,
            db=self.db,
            user=self.user,
            passwd=self.passwd,
            charset=self.charset,
        )

    def query(self, query: str, values: Tuple = None) -> None:
        """Open Cursor, Execute the Query and return result."""
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insert(self, query: str, values: Tuple = None, lastrowid=False):
        """Open Cursor, Execute the Insert and commit changes to the database."""
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
        if lastrowid:
            store_id = cursor.lastrowid
            cursor.close()
            return store_id
        else:
            cursor.close()

    def get_product(self, category: str) -> Dict:
        """ get all products from the selected category and return the first 10 rows """
        request = """ SELECT p.id, p.product_name, p.url, p.nutriscore_grade, c.category_name
            FROM product p
            LEFT JOIN category_has_product chp ON p.id = chp.product_id
            LEFT JOIN category c ON chp.category_id = c.id
            WHERE c.category_name = %s
            AND nutriscore_grade > 'C' 
            ORDER BY RAND() 
            LIMIT 10"""
        return self.query(request, (category,))

    def get_substitute(self, category: str) -> str:
        """ For a given product, get all products with the same category and return one  """

        substitute = self.select_substitute(category)
        return self.get_product_info(substitute[0][0])

    def select_substitute(self, category: str) -> Dict:
        """ """
        category_id_request = "SELECT id FROM category WHERE category_name = %s"
        category_id = self.query(category_id_request, (category,))
        category_products_id_request = """SELECT p.id
            FROM product p
            INNER JOIN category_has_product chp ON p.id = chp.product_id
            WHERE chp.category_id = %s
            AND p.nutriscore_grade <= 'C'
            ORDER BY RAND()
            LIMIT 1 """

        return self.query(category_products_id_request, (category_id[0][0],))

    def get_product_info(self, product_id: str) -> Dict:
        """ """
        product_info_request = "SELECT * FROM product WHERE id = %s"
        return self.query(product_info_request, (product_id,))[0]

    def get_stores(self, product_id: str) -> List:
        """ """
        product_stores_request = """SELECT s.store_name
            FROM store s
            INNER JOIN store_has_product shp ON s.id = shp.store_id
            WHERE shp.product_id = %s"""
        stores_list = []
        for store in self.query(product_stores_request, (product_id,)):
            stores_list.append(store[0])
        return stores_list

    def get_categories(self, product_id: str) -> List:
        """ """
        product_categories_request = """SELECT c.category_name
            FROM category c
            INNER JOIN category_has_product chp ON c.id = chp.category_id
            WHERE chp.product_id = %s"""
        categories_list = []
        for store in self.query(product_categories_request, (product_id,)):
            categories_list.append(store[0])
        return categories_list

    def add_favorite(self, product_id: str, substitute_id: str) -> None:
        """ """
        add_favorite_request = "INSERT INTO substituted_product VALUES (%s, %s)"
        self.insert(add_favorite_request, (substitute_id, product_id))

    def get_favorites(self) -> Dict:
        """ """
        return self.query("SELECT * FROM substituted_product")

    def disconnect(self) -> None:
        """Close the database connection."""
        self.connection.close()

    def __del__(self):
        if self.connection is not None:
            self.disconnect()
