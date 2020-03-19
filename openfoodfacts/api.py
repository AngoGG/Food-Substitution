#!/usr/bin/env python3

from os import environ
from typing import List, Dict, Any
import json
import requests


class Api:
    """ Manages interactions with OpenFoodFact API """

    def __init__(self):
        self.base_url: str = "https://world.openfoodfacts.org/cgi/search.pl"
        self.payloads: Dict = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": "Chips",
            "sort_by": "unique_scans_n",
            "countries": "France",
            "purchase_places": "France",
            "page": 1,
            "page_size": 300,
            "json": 1,
        }
        self.json_dir: str = environ.get("JSON_DIR")

    def request(self) -> Dict:
        """ Get data from API, return json with results """
        response = requests.get(self.base_url, params=self.payloads)
        return response.json()

    def get_data(self, category: str) -> Dict:
        """ Gets data from the given category and returns it"""
        self.payloads["tag_0"] = category
        result = self.request()
        return result

    def save_data_as_json_file(self, data: List[Dict[str, Any]], file: str) -> None:
        """ All in method title"""
        with open(f"{self.json_dir}/{file}", "w") as outfile:
            json.dump(data, outfile)
