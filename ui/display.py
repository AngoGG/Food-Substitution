# #!/usr/bin/env python3

from config.config import Config


class Display:
    """ Class who will manage the UI display and interactions """

    def __init__(self, database):
        self.database = database

    def display_menu(self):
        """ """
        print(
            "Bonjour utilisateur, bienvenue dans notre programme "
            + "de substitution alimentaire Pur Beurre!",
        )
        print(
            "Que voulez-vous faire?\n",
            "Appuyez sur la touche de votre clavier correspondante à votre choix:\n",
            "1 - Remplacer un aliment par un substitut plus sain\n",
            "2 - Voir vos aliment déjà subsitués\n",
        )
        choix = input("Tapez votre choix: ")
        if choix != "":
            if choix == "1":
                self.display_categories()
            elif choix == "2":
                self.display_favorites()
            else:
                print("Le choix n'existe pas\n")
        else:
            print("Veuillez faire un choix\n")

    def display_categories(self):
        """ """
        print("\nVoici la liste des Catégories de produit disponible:")
        n = 1
        for category in self.database.get_categories():
            print(f"{n} - {category[0]}")
            n += 1
        choix = input("Selectionnez une categorie à afficher: ")
        try:
            int(choix)
            if int(choix) <= len(Config.CATEGORIES) and int(choix) != 0:
                self.display_products(Config.CATEGORIES[int(choix) - 1])
            else:
                print("Le choix n'existe pas\n")
                self.display_categories()
        except ValueError:
            print("Le choix n'existe pas\n")
            self.display_categories()

    def display_products(self, category):
        """ """
        print(f"\nVoici la liste des Aliments a substituer pour le choix {category}:",)
        n = 1
        products = self.database.get_product(category)
        for product in products:
            print(f"{n} - {product[1]}, Nutriscore = {product[3]}")
            n += 1
        choix = input("Sélectionner un aliment à substituer: ")
        try:
            if int(choix) <= len(products) and int(choix) != 0:
                self.display_product_infos(products[int(choix) - 1], category)
            else:
                print("Le choix n'existe pas\n")
                self.display_products(category)
        except ValueError:
            print("Le choix n'existe pas\n")
            self.display_categories()

    def display_product_infos(self, product, category):
        product_stores = self.database.get_stores(str(product[0]))
        product_categories = self.database.get_product_categories(str(product[0]))
        print(
            f"\nVous avez sélectionné {product[1]}, voici les informations sur ce produit:",
        )
        print(
            f"Nutri-Score : {product[3]}\n"
            + f'Catégories: {", ".join(product_categories)}\n'
            + f'Magasins: {", ".join(product_stores)}\n'
            + f"Lien vers la page OpenFoodFacts du produit : {str(product[2])}\n"
        )
        print(
            "Tapez 1 pour remplacer cet aliment par un substitut plus sain",
            "\nTapez 2 pour revenir à la sélection des catégories\n",
        )
        choix = input("")
        if choix == "1":
            self.display_substitute(product[0], product[1], category)
        elif choix == "2":
            self.display_categories()
        else:
            print("Le choix n'existe pas\n")

    def display_substitute(self, product_id, product_name, category):
        """ """
        substitute = self.database.get_substitute(category)
        substitute_stores = self.database.get_stores(str(substitute[0]))
        substitute_categories = self.database.get_product_categories(str(substitute[0]))
        print(
            f"\nPour le produit {product_name}, nous vous proposons "
            + "le produit suivant en substitution:\n",
        )
        print(
            f"Nom du produit : {substitute[1]} \n"
            + f"Nutri-Score : {substitute[3]}\n"
            + f'Catégories: {", ".join(substitute_categories)}\n'
            + f'Magasins: {", ".join(substitute_stores)}\n'
            + f"Lien vers la page OpenFoodFacts du produit : {str(substitute[2])}\n"
        )
        print(
            "Tapez 1 pour enregistrer ce substitut dans vos favoris",
            "\nTapez 2 pour revenir au menu\n",
        )
        choix = input("")
        if choix == "1":
            self.database.add_favorite(substitute[0], product_id)
            print("Substitution enregistrée dans les favoris, retour au menu \n")
            self.display_menu()
        elif choix == "2":
            self.display_categories()
        else:
            print("Le choix n'existe pas\n")

    def display_favorites(self):
        """ """
        favorites = self.database.get_favorites()
        print(
            "Voici vos substitutions enregistrées dans vos favoris: "
            + "Aliment[Nutriscore] => Substitut[Nutriscore]\n"
        )
        n = 1
        for favorite in favorites:
            product_infos = self.database.get_product_info(favorite[0])
            substitute_infos = self.database.get_product_info(favorite[1])
            print(
                f"{n} - {product_infos[1]}[Nutriscore {product_infos[3]}] =>",
                f"{substitute_infos[1]}[Nutriscore {substitute_infos[3]}]",
            )
            n += 1
        print("\nTapez une touche pour revenir au menu\n",)
        choix = input("")
        if choix:
            self.display_menu()

