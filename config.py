import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une-cle-tres-secrete-pour-joel-business'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///boutique.db'
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'images')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
