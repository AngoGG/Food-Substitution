# #!/usr/bin/env python3
'''
SDQ: docstring vide/inutile, à compléter ; idem partout
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-01-16
@note    0.0.1 (2020-01-16) : Init file
'''

# SDQ: penser à trier les imports comme suit
# 1. Les modules de la stdlib (from puis import) par ordre alphabétique
# 2. les modules installés par PyPI (from puis import) par ordre alphabétique
# 3. Les modules internes (from puis import) par ordre alphabétique
# Idem dans tous les autres fichiers

# On dirait que tu n'as pas lancé black, j'ai eu des modifs automatiques
# dans quasiment tous les fichiers

from os import environ
from typing import BinaryIO
import time
import os
import click
from config.config import Config
from database.database import Database
from database.populate import Populate
from database.setup_database import SetupDatabase
from openfoodfacts.api import Api
from openfoodfacts.datas_cleaner import DatasCleaner
from ui.display import Display


class App:
    ''' Main Class '''  # SDQ: manque la docstring

    def __init__(self, build_database: bool) -> None:
        self.api: Api = Api()
        self.database: Database = Database(
            environ['HOST'],
            environ['USER'],
            environ['PASSWORD'],
            environ['DATABASE'],
        )
        self.setup_database: SetupDatabase = SetupDatabase(self.database)
        self.clean_datas: DatasCleaner = DatasCleaner()
        self.populate: Populate = Populate(self.database)
        self.ui: Display = Display(self.database)
        self.build_database = build_database

    def main(self) -> None:
        # SDQ: et la docstring ?
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
        program_loop = True
        while program_loop:  # pourquoi pas `while True:` directement ?
            self.ui.display_menu()
        self.database.disconnect()


@click.command()
@click.option("-b", "--build", is_flag=True, help="To create and fill tables")
def main(build) -> None:
    # Et la docstring ? A noter que cette docstring est le message d'aide
    # de ton programme quand tu fais python app.py --help donc à détailler
    # fortement
    app: App = App(build)
    app.main()


if __name__ == '__main__':
    main()
