#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-01-16
@note    0.0.1 (2020-01-16) : Init file
'''

import requests
import time
import os
from os import environ
from openfoodfacts.api import Api
from database.database import Database
from typing import BinaryIO
from config.config import Config
from ui.ui import Ui


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
        self.ui: Ui = Ui()

    def main(self) -> None:
        start: float = time.time()
        for category in Config.CATEGORIES:
            self.database.connect()
            if Config.TABLES_CREATION:
                self.database.delete_tables()
                self.database.create_tables()
                Config.TABLES_CREATION = False
            for product in self.api.get_products(category):
                self.database.populate_from_json(product)
            self.database.disconnect()
        end: float = time.time()
        # print(f'Temps de traitement {end - start:.2f} sec.')
        os.system('clear')
        program_loop = True
        while program_loop:
            self.ui.display_menu()


def main() -> None:
    app: App = App()
    app.main()


if __name__ == '__main__':
    main()
