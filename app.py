#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-01-16
@note    0.0.1 (2020-01-16) : Init file
'''

import time
from os import environ
from openfoodfacts.api import Api
from openfoodfacts.datas_cleaner import DatasCleaner
from database.database import Database
from database.setup_database import SetupDatabase
from database.populate import Populate
from typing import BinaryIO
from config.config import Config
from ui.display import Display


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
        self.ui: Display = Display()
        self.setup_database: SetupDatabase = SetupDatabase(self.database)
        self.clean_datas: DatasCleaner = DatasCleaner()

    def main(self) -> None:
        start: float = time.time()
        for category in Config.CATEGORIES:
            self.database.connect()
            if Config.TABLES_CREATION:
                self.setup_database.delete_tables()
                self.setup_database.create_tables()
                Config.TABLES_CREATION = False
            result = self.api.get_datas(category)
            for product in self.clean_datas.get_product(result):
                Populate(self.database, product)
            self.database.disconnect()
        end: float = time.time()
        print(f'Temps de traitement {end - start:.2f} sec.')
        os.system('clear')
        program_loop = True
        while program_loop:
            self.ui.display_menu()


def main() -> None:
    app: App = App()
    app.main()


if __name__ == '__main__':
    main()
