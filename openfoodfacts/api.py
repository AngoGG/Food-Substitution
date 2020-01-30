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
from typing import TextIO

class Api:
    """ Manages interactions with OpenFoodFact API """

    def __init__(self):
        self.base_url : str= "https://world.openfoodfacts.org/cgi/search.pl"
        self.payloads : dict = {
            "action": "process",
            "search_tag": "categories",
            "tag_0" : "Boissons",
            "sort_by": "unique_scans_n",
            "countries": "France",
            "page": 1,
            "page_size": 1,
            "json": 1
        }
        self.json_dir : str = environ.get("JSON_DIR")

    def request(self) -> dict:
        """ Get data from API, return json with results """
        
        response = requests.get(self.base_url, params=self.payloads)
        return(response.json())
        
    def get_products(self) -> TextIO:
        """ Sorts the data to keep only what is needed in the database """

        result = self.request()
        self.save_data_as_json_file(result, 'result.json')

        data = []
        for product in result['products']:
            if ('nutriscore_grade' in product):
                data.append({"id" : product['_id'], "Aliment" : product['product_name'], "Magasins" : product['stores_tags'], "Catégories" : product['categories'], "Nutriscore" : product['nutriscore_grade'], "Url" : product['url']}) 
        self.save_data_as_json_file(data, 'products.json')
    
    def save_data_as_json_file(self, data, file) -> None:
        """ All in method title"""

        with open(f'{self.json_dir}/{file}', 'w') as outfile:
            json.dump(data, outfile)