#!/usr/bin/env python3
'''
@desc    description
@author  SDQ <sdq@afnor.org>
@version 0.0.1
@date    2020-01-20
@note    0.0.1 (2020-01-20) : Init file
'''
import json
import requests
from os import environ
from pathlib import Path
from typing import List, Dict, Any, BinaryIO


class Api:
    """ Manages interactions with OpenFoodFact API """

    def __init__(self):
        self.base_url: str = "https://world.openfoodfacts.org/cgi/search.pl"
        self.payloads: dict = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": "Boisson",
            "sort_by": "unique_scans_n",
            "countries": "France",
            "page": 1,
            "page_size": 1000,
            "json": 1,
        }
        self.product_items_list = [
            'nutriscore_grade',
            'product_name',
            'stores_tags',
            '_id',
            'categories',
            'url',
        ]
        self.json_dir: str = environ.get("JSON_DIR")

    def request(self) -> dict:
        """ Get data from API, return json with results """
        response = requests.get(self.base_url, params=self.payloads)
        return response.json()

    def get_products(self) -> List[Dict[str, Any]]:
        """ Sorts the data to keep only what is needed in the database """

        result = self.request()

        data = []
        for product in result['products']:
            if self._product_is_valid(product):
                data.append(
                    {
                        "id": product['_id'],
                        "Aliment": product['product_name'],
                        "Magasins": product['stores_tags'],
                        "Categories": product['categories'],
                        "Nutriscore": product['nutriscore_grade'].upper(),
                        "Url": product['url'],
                    }
                )
        self.save_data_as_json_file(data, 'products.json')
        return data

    def save_data_as_json_file(
        self, data: List[Dict[str, Any]], file: str
    ) -> None:
        """ All in method title"""
        with open(f'{self.json_dir}/{file}', 'w') as outfile:
            json.dump(data, outfile)

    def _product_is_valid(self, product: Dict[str, Any]) -> bool:
        ''' Verifies the presence of all the elements required for a product '''
        for field in self.product_items_list:
            if field not in product:
                return False
        return True
