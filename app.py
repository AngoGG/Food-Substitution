#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-01-16
@note    0.0.1 (2020-01-16) : Init file
'''

import requests
from os import environ
from openfoodfacts.api import Api
from database.database import Database
from typing import BinaryIO
from config.config import Config


class App:
    ''' Main Class '''

    def __init__(self) -> None:
        self.api: Api = Api()
        self.database: Database() = Database(
            environ['HOST'],
            environ['USER'],
            environ['PASSWORD'],
            environ['DATABASE'],
        )

    def main(self) -> None:
        for category in Config.CATEGORIES:
            products = self.api.get_products(category)
            self.database.connect()
            if Config.TABLES_CREATED == False:
                self.database.delete_tables()
                self.database.create_tables()
                Config.TABLES_CREATED = True
            self.database.populate_from_json(products)
            self.database.disconnect()
                


def main() -> None:
    app: App = App()
    app.main()


if __name__ == '__main__':
    main()
