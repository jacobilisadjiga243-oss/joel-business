import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une-cle-tres-secrete-pour-joel-business'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///boutique.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'images')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 Mo pour les photos de telephone
