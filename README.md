# Wingz Ride Backend
Payment Gateway integrating multiple methods.

## Prerequisites
- Python 3.13.2
- Django 5.0.4
- DRF 3.16.0
- PostgreSQL 16.8

## Things to do after cloning the project on Github
1. Create virtual environment:
    - you can use virtualenv or pip, but what I can recommend is to use Conda
2. Create a PostgreSQL database:
    - create a .env file then copy variables in .env-example
    - add values for DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST and DATABASE_PORT after creating database
3. Run `python manage.py migrate` command.
4. Run `python manage.py creatsuperuser` command to create a superuser account.
5. Install Postman application.
6. Import collections and environments using the json files under postman directory.