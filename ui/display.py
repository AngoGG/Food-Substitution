#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-02-25
@note    0.0.1 (2020-02-25) : Init file
'''
from config.config import Config
from database.database import Database


class Display:
    ''' Class who will manage the UI display and interactions '''

    def __init__(self, database):
        self.database = database

    def display_menu(self):
        ''' '''
        print(
            'Bonjour utilisateur, bienvenue dans notre programme de substitution alimentaire Pur Beurre!\n',
        )
        print(
            'Que voulez-vous faire? \n',
            'Appuyez sur la touche de votre clavier correspondante à votre choix:\n',
            '1 - Remplacer un aliment par un substitut plus sain\n',
            '2 - Voir vos aliment déjà subsitués\n',
        )
        choix = input("Tapez votre choix: ")
        if int(choix) == 1:
            self.display_categories()
        else:
            print("Vous avez choisi d'afficher vos elements deja subsitues")
            input("")

    def display_categories(self):
        ''' '''
        print('\nVoici la liste des Catégories de produit disponible\n')
        n = 1
        for category in Config.CATEGORIES:
            print(f'{n} - {category}')
            n += 1
        choix = input('Selectionnez une categorie a afficher: ')
        if int(choix) <= len(Config.CATEGORIES):
            self.display_products(Config.CATEGORIES[int(choix) - 1])
        else:
            print("Le choix n'existe pas\n")
            self.display_categories()

    def display_products(self, category):
        ''' '''
        print(
            f'\nVoici la liste des Aliments a substitue pour le choix {category}\n',
        )
        n = 1
        products = self.database.get_product(category)
        for product in products:
            print (f'{n} - {product[1]}, Nutriscore = {product[2]}')
            n += 1
        choix = input("Sélectionner un aliment à substituer: ")
        if int(choix) <= n:
            self.display_substitute(products[int(choix)-1][0], products[int(choix)-1][1], category)
        else:
            print(f'Ayayaye : {choix} => {n}')

    def display_substitute(self, product_id, product_name, category):
        ''' '''
        substitute = self.database.get_substitute(category)
        print(
            f'\nPour le produit {product_name}, nous vous proposons le produit suivant en substitution:\n',
        )
        print(
            f'Nom du produit : {substitute[0][1]} \n' +
            f'Nutri-Score : {substitute[0][3]}\n' +   
            f'Magasins: {". ".join(substitute[1])}\n' +
            f'Lien vers la page OpenFoodFacts du produit : {str(substitute[0][2])}\n'
        )
        input("")


