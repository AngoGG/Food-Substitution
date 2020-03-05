#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-01-20
@note    0.0.1 (2020-01-20) : Init file
'''
import json
import requests
from os import environ
from pathlib import Path
from typing import List, Dict, Any, BinaryIO, Generator


class Api:
    """ Manages interactions with OpenFoodFact API """

    def __init__(self):
        self.base_url: str = "https://world.openfoodfacts.org/cgi/search.pl"
        self.payloads: dict = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": 'Chips',
            "sort_by": "unique_scans_n",
            "countries": "France",
            "purchase_places": "France",
            "page": 1,
            "page_size": 20,
            "json": 1,
        }
        self.json_dir: str = environ.get("JSON_DIR")

    def request(self) -> dict:
        """ Get data from API, return json with results """
        response = requests.get(self.base_url, params=self.payloads)
        return response.json()
    
    def get_datas(self, category):
        self.payloads['tag_0'] = category
        result = self.request()
        return result

    def save_data_as_json_file(
        self, data: List[Dict[str, Any]], file: str
    ) -> None:
        """ All in method title"""
        with open(f'{self.json_dir}/{file}', 'w') as outfile:
            json.dump(data, outfile)
