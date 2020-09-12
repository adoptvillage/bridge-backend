from flask import Flask
import app
from config import get_env_config
import firebase_admin
from firebase_admin import credentials, firestore
from flask_sqlalchemy import SQLAlchemy
import os
import pyrebase

def create_app(config_filename: str) -> Flask:
    
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///local_data.db"
    app.url_map.strict_slashes = False
    
    
    # config = {
    #     "apiKey": os.getenv("API_KEY"),
    #     "authDomain": "bridge-3f39b.firebaseapp.com",
    #     "databaseURL": "https://bridge-3f39b.firebaseio.com",
    #     "storageBucket": "bridge-3f39b.appspot.com"
    #     }
    
    
    # firebase = pyrebase.initialize_app(config)
    
    cred = credentials.Certificate('firebase_credentials.json')
    firebase_admin.initialize_app(cred)
    
    from app.apis import api
    api.init_app(app)
    
    from app.database.sqlalchemy_extension import db
    db.init_app(app)
    
    # from app.database.firebase import firebase_db
    # firebase_db = firestore.client()
    
    return app

application = create_app(get_env_config())


@application.before_first_request
def create_tables():
    from app.database.sqlalchemy_extension import db

    db.create_all()

if __name__ == "__main__":
    application.run(port=5000)
