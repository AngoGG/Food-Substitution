# coding: utf8
# #!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-01-16
@note    0.0.1 (2020-01-16) : Init file
'''

import click
import time
import os
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

    def __init__(self, build_db) -> None:
        self.api: Api = Api()
        self.database: Database() = Database(
            environ['HOST'],
            environ['USER'],
            environ['PASSWORD'],
            environ['DATABASE'],
        )
        self.setup_database: SetupDatabase = SetupDatabase(self.database)
        self.clean_datas: DatasCleaner = DatasCleaner()
        self.populate: Populate = Populate(self.database)
        self.ui: Display = Display(self.database)
        self.build_database = build_db

    def main(self) -> None:
        start: float = time.time()
        self.database.connect()
        if self.build_database:
            self.setup_database.delete_tables()
            self.setup_database.create_tables()
            for category in Config.CATEGORIES:
                result = self.api.get_datas(category)
                for product in self.clean_datas.get_product(result):
                    self.populate.insert_datas(product)      
            end: float = time.time()
            print(f'Temps de traitement {end - start:.2f} sec.')
        #os.system('cls')
        program_loop = True
        while program_loop:
            self.ui.display_menu()
        self.database.disconnect()

@click.command()
@click.option(
    "-b",
    "--build",
    is_flag=True,
    help="To create and fill tables"
)

def main(build) -> None:
    app: App = App(build)
    app.main()


if __name__ == '__main__':
    main()
