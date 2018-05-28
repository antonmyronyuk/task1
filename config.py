import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # sqlite on localhost, postgres on heroku
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
