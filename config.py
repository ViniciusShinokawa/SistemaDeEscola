
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/escola')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
