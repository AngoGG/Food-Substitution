#!/usr/bin/env python3

from os import environ
import time
import click
from config.config import Config
from database.database import Database
from database.populate import Populate
from database.setup_database import SetupDatabase
from openfoodfacts.api import Api
from openfoodfacts.data_cleaner import DataCleaner
from ui.display import Display


class App:
    """ Manages the entire program process,
    creates and fills tables if required,
    launches the program menu.
    """

    def __init__(self, build_database: bool) -> None:
        self.api: Api = Api()
        self.database: Database = Database(
            environ["HOST"], environ["USER"], environ["PASSWORD"], environ["DATABASE"]
        )
        self.setup_database: SetupDatabase = SetupDatabase(self.database)
        self.clean_datas: DataCleaner = DataCleaner()
        self.populate: Populate = Populate(self.database)
        self.ui: Display = Display(self.database)
        self.build_database = build_database

    def run(self) -> None:
        start: float = time.time()
        self.database.connect()
        if self.build_database:
            self.setup_database.delete_tables()
            self.setup_database.create_tables()
            for category in Config.CATEGORIES:
                result = self.api.get_data(category)
                for product in self.clean_datas.get_product(result, category):
                    self.populate.insert_datas(product)
            end: float = time.time()
            print(f"Temps de traitement {end - start:.2f} sec.\n")
        program_loop = True
        while program_loop:
            self.ui.display_menu()
        self.database.disconnect()


@click.command()
@click.option("-b", "--build", is_flag=True, help="To create and fill tables")
def main(build=None) -> None:
    """ This program interacts with the Open Food Facts API to retrieve the food,
    in order to provide the user with the ability to choose a healthier alternative
    in the same category for a given food.
    There are 3 main functions:
    - API data retrieval,
    - data sorting and database integration,
    - and the substitute choice interface
    """
    app: App = App(build)
    app.run()


if __name__ == "__main__":
    main()
