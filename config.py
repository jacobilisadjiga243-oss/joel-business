import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une-cle-tres-secrete-pour-joel-business'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///boutique.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
