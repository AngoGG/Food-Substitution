import json
import requests

class Api:
    """ Manages interactions with OpenFoodFact API """

    def __init__(self):
        self.base_url = "https://world.openfoodfacts.org/cgi/search.pl"
        self.payloads = {
            "action": "process",
            "search_tag": "categories",
            "tag_0" : "Boissons",
            "sort_by": "unique_scans_n",
            "countries": "France",
            "page": 1,
            "page_size": 1,
            "json": 1
        }

    def request(self):
        """ Get data from API, return json with results """
        response = requests.get(self.base_url, params=self.payloads)
        return(response.json())
        
    def get_products(self):
        """ Sorts the data to keep only what is needed in the database """
        result = self.request()
        self.save_data_as_json_file(result, 'result.json')

        data = []
        for product in result['products']:
            if ('nutriscore_grade' in product):
                data.append({"id" : product['_id'], "Aliment" : product['product_name'], "Magasins" : product['stores_tags'], "Catégories" : product['categories'], "Nutriscore" : product['nutriscore_grade']}) 
        self.save_data_as_json_file(data, 'products.json')
    
    def save_data_as_json_file(self, data, file):
        """ All in method title"""

        with open(f'json/{file}', 'w') as outfile:
            json.dump(data, outfile)