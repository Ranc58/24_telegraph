from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///stories.db'
