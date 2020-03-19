# #!/usr/bin/env python3

from typing import List, Tuple, Dict
import mysql.connector


class Database:
    """ Class that manages all program interactions with the database. """

    def __init__(self, host, user, passwd, db=None, charset="utf8"):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = db
        self.charset = charset
        self.connection = None

    def connect(self) -> None:
        """Database connection."""
        self.connection = mysql.connector.connect(
            host=self.host,
            db=self.database,
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

    def insert(self, query: str, values: Tuple = None, lastrowid=False) -> str:
        """Open Cursor, Execute the Insert and commit changes to the database.
        If lastrowid is True, returns it"""
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
        if lastrowid:
            store_id = cursor.lastrowid
            cursor.close()
            return store_id
        cursor.close()

    def get_categories(self) -> List:
        request = "SELECT category_name FROM category"
        return self.query(request)

    def get_product(self, category: str) -> Dict:
        """ Randomly get all products from the selected category and return the first 10 rows """
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
        """ For a given product, get get a healthier substitute from the same category  """

        substitute = self.select_substitute(category)
        return self.get_product_info(substitute[0][0])

    def select_substitute(self, category: str) -> Dict:
        """ Randomly retrieves a substitute from the category """
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
        """ Retrieves all the information available for a product """
        product_info_request = "SELECT * FROM product WHERE id = %s"
        return self.query(product_info_request, (product_id,))[0]

    def get_stores(self, product_id: str) -> List:
        """ Retrieves the list of all stores selling the product """
        product_stores_request = """SELECT s.store_name
            FROM store s
            INNER JOIN store_has_product shp ON s.id = shp.store_id
            WHERE shp.product_id = %s"""
        stores_list = []
        for store in self.query(product_stores_request, (product_id,)):
            stores_list.append(store[0])
        return stores_list

    def get_product_categories(self, product_id: str) -> List:
        """ Retrieves the list of all categories to which the product belongs """
        product_categories_request = """SELECT c.category_name
            FROM category c
            INNER JOIN category_has_product chp ON c.id = chp.category_id
            WHERE chp.product_id = %s"""
        categories_list = []
        for store in self.query(product_categories_request, (product_id,)):
            categories_list.append(store[0])
        return categories_list

    def add_favorite(self, product_id: str, substitute_id: str) -> None:
        """  Add a favorite in database (with the id of the product and its substitute) """
        add_favorite_request = "INSERT INTO substituted_product VALUES (%s, %s)"
        self.insert(add_favorite_request, (substitute_id, product_id))

    def get_favorites(self) -> Dict:
        """ Retrieves the list of all substituted products registered in the database """
        return self.query("SELECT * FROM substituted_product")

    def disconnect(self) -> None:
        """Close the database connection."""
        self.connection.close()

    def __del__(self):
        if self.connection is not None:
            self.disconnect()
