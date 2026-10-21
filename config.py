import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une-cle-tres-secrete-pour-joel-business'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///boutique.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Configuration pour l'upload d'images
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'images')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # Limite à 5 Mo
