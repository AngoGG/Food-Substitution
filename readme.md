# OpenClassrooms Project 5: Use OpenFoodFacts public data

## Setting up the database

<<<<<<< HEAD
In order to ensure the smooth running of the program there are 2 steps to follow: Create the database on your workstation and fill in the necessary information in the *.env* file in the directory in order to ensure the correct operation of the program:
=======
In order to ensure the smooth running of the program there are 2 steps to follow: Create the database on your workstation and fill in the necessary information in the .env file in the directory in order to ensure the correct operation of the program:
>>>>>>> 2f604bc8dbfa3a82d8a9d2278d56e7f97c0f9f49

**The default information is:**
- DATABASE=openfoodfacts
- HOST=localhost
- USER=root
- PASSWORD=root

## Setting up the environment 

The 2 prerequisites for the operation of the program are:
- Python 3.7 or higher
- pipenv

<<<<<<< HEAD
Prior to any program launch, set up the virtual environment with `pipenv install`

Then for a first run of the program: use  `pipenv run python app.py --build`  to create and fill the tables with data from the OpenFoodFacts API.

Once the database is in place, the program can be run simply with `pipenv run python app.py`
=======
Prior to any program launch, set up the virtual environment with pipenv install

Then for a first run of the program: use the pipenv run python app.py --build command to create and fill the tables with data from the OpenFoodFacts API.

Once the database is in place, the program can be run simply without any
>>>>>>> 2f604bc8dbfa3a82d8a9d2278d56e7f97c0f9f49
