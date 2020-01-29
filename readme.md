# Open Classrooms Projet 5: Utilisez les données publiques de l'OpenFoodFacts

## Tableau Trello du projet
https://trello.com/b/3Kfg4uZT/oc-projet5-openfoodfacts (Work In Progress)

## Cahier des Charges

L'utilisateur est sur le terminal. Ce dernier lui affiche les choix suivants :

1. Quel aliment souhaitez-vous remplacer ?
2. Retrouver mes aliments substitués.

L'utilisateur sélectionne 1. Le programme pose les questions suivantes à l'utilisateur et ce dernier sélectionne les réponses :

- Sélectionnez la catégorie. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant et appuie sur entrée]
- Sélectionnez l'aliment. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant à l'aliment choisi et appuie sur entrée]
- Le programme propose un substitut, sa description, un magasin ou l'acheter (le cas échéant) et un lien vers la page d'Open Food Facts concernant cet aliment.
- L'utilisateur a alors la possibilité d'enregistrer le résultat dans la base de données.

## Fonctionnalités

- Recherche d'aliments dans la base Open Food Facts.
- L'utilisateur interagit avec le programme dans le terminal, mais si vous souhaitez développer une interface graphique vous pouvez,
- Si l'utilisateur entre un caractère qui n'est pas un chiffre, le programme doit lui répéter la question,
- La recherche doit s'effectuer sur une base MySql.

## Architecture Programme
**4 Classes + main:**
- Récupération données Open Food Facts
    - Requête API
    - Formattage json pour intégration en base de données
- Création Base de données
    - Création Base
    - Création Tables
    - Intégration Base de données
- Gestion Base de Données
    - Connexion
    - Requête
    - Mise en forme de la réponse
    - Update
    - Déconnexion
- Main:
    - Sélection choix (Nouveau Produit à substituer ou Affichage des éléments déjà substitués)
    - Choix 1, Nouveau Produits à substituer:
        - Sélection Catégorie (Chaque catégorie associée à un chiffre)
        - Sélection Aliment (Chaque aliment associé à un chiffre)
        - Proposition d'un substitut à l'aliment (Aliment, Description, Magasin ou acheter, lien Open Food Fact)
        - Proposition enregistrement du susbtitut en base pour l'utilisateur
    - Choix 2, Accès aux éléments déjà substitués par l'utilisateur:
        - Affichage catégories disponibles (seulement celles ou l'utilisateur a sauvegardé un substitut)
        - Affichage aliments sauvegardés par l'utilisateur
- Interface

## Champs API à récupérer

Exemple à analyser : 
- https://world.openfoodfacts.org/api/v0/product/5449000000996
- https://world.openfoodfacts.org/product/5449000000996/coca-cola

| Information     |     Champ API    |
| - |:-
| Aliment ID   |        _id        |
| Aliment     |        product_name        |
| Magasin ou acheter    |        stores_tags        |
| Lien OpenFoodFact    |        url        |
| nutriscore    |        nutriscore_grade        |
| Catégorie    |        categories        |