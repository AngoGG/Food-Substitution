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
        products = self.api.get_products()
        self.database.connect()
        self.database.create_tables()
        self.database.populate_from_json(products)
        self.database.disconnect()


def main() -> None:
    app: App = App()
    app.main()


if __name__ == '__main__':
    main()
