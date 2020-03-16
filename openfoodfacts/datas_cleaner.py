#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-03-05
@note    0.0.1 (2020-03-05) : Init file
'''
import json
import requests
from os import environ
from pathlib import Path
from typing import List, Dict, Any, BinaryIO, Generator


class DatasCleaner:  # Pas de s à data en anglais, idem partout, donc
    def __init__(self,) -> None:
        '''Constructor'''
        self.product_items_list: List[str, str] = [
            'nutriscore_grade',
            'product_name',
            'stores_tags',
            '_id',
            'categories',
            'url',
        ]

    def get_product(self, datas) -> Generator:
        """ Sorts the data to keep only what is needed in the database """
        for data in datas['products']:
            if self._product_is_valid(data):
                product: Dict = {
                    "id": data['_id'],
                    "Aliment": data['product_name'],
                    "Magasins": data['stores_tags'],
                    "Categories": data['categories'],
                    "Nutriscore": data['nutriscore_grade'].upper(),
                    "Url": data['url'],
                }
                yield product

    def _product_is_valid(self, product: Dict[str, Any]) -> bool:
        ''' Verifies the presence of all the elements required for a product and if the stores_tags list is not empty '''
        for field in self.product_items_list:
            if field not in product:
                return False
            elif len(product[field]) == 0:
                return False
        if not product['stores_tags']:
            return False
        return True
