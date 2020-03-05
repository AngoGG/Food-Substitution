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

    def __init__(self):
        pass

    def display_menu(self):
        ''' '''
        print(
            'Bonjour utilisateur, bienvenue dans notre programme de substitution alimentaire Pur Beurre!',
        )
        print(
            'Que voulez-vous faire? ',
            'Appuyez sur la touche de votre clavier correspondante à votre choix\n',
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
        # Query sur category = category et product nutriscore_grade = E ou D pour pouvoir trouver facilement un resultat
        # Afficher ici les 5 premiers résultats
        # Dans class Database, faire une methode get_products dans laquelle on enverra la catégorie récupérée
        print(
            f'\nVoici la liste des Aliments a substitue pour le choix {category}',
        )
        print(
            ' 1- Aliment 1 \n', '2- Aliment 2\n', '3- Aliment 3\n',
        )
        input("")
