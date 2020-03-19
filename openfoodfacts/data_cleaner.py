#!/usr/bin/env python3

from typing import List, Dict, Any, Generator


class DataCleaner:
    """ Manages the sorting and verification of data retrieved from the API before integration. """

    def __init__(self) -> None:
        """Constructor"""
        self.product_items_list: List[str, str] = [
            "nutriscore_grade",
            "product_name",
            "stores_tags",
            "_id",
            "categories",
            "url",
        ]

    def get_product(self, datas: Dict[str, Any], category: str) -> Generator:
        """ Sorts the data to keep only what is needed in the database """
        for data in datas["products"]:
            if self._product_is_valid(data):
                product: Dict = {
                    "id": data["_id"],
                    "Aliment": data["product_name"],
                    "Magasins": data["stores_tags"],
                    "Categories": category,
                    "Nutriscore": data["nutriscore_grade"].upper(),
                    "Url": data["url"],
                }
                yield product

    def _product_is_valid(self, product: Dict[str, Any]) -> bool:
        """ Verifies the presence of all the elements required for a product
        and if the stores_tags list is not empty """
        for field in self.product_items_list:
            if field not in product:
                return False
            elif len(product[field]) == 0:
                return False
        if not product["stores_tags"]:
            return False
        return True
