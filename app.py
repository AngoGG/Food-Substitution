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
from openfoodfact.api import Api

class App:
    ''' Main Class '''

    def __init__(self) -> None:
        self.api: Api = Api()

    def main(self) -> None:   
        self.api.get_products()

def main() -> None:
    app: App = App()
    app.main()

if __name__ == '__main__':
    main()