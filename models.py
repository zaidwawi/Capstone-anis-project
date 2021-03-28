import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from config import SQLALCHEMY_DATABASE_URI


'''
#App Config.
'''

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate (app, db)

#Connect to a local postgresql database

def setup_db(app, database_path=SQLALCHEMY_DATABASE_URI):
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
#Models.
'''

class Movies(db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.String, nullable=False)

    #The insert method 
    def insert(self):
        db.session.add(self)
        db.session.commit()
        #movie = Movies(titile=title, release_date=release_date)
        #movie.insert()

    #The update method
    def update(self):
        db.session.commit()
        #movie.title = 'New movie'
        #movie.update()

    #The delete method
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        #movie = Movies.query.filter(title=title)
        #movie.delete()

    #Formatted data
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def __repr__(self):
        return 'Movie ID: {self.id}, title: {self.title}'

class Actors (db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    
    #The insert method 
    def insert(self):
        db.session.add(self)
        db.session.commit()
        #movie = Actors(name=name, age=age, gender=gender)
        #movie.insert()

    #The update method
    def update(self):
        db.session.commit()
        #movie.title = 'New actor'
        #movie.update()

    #The delete method
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        #movie = Actors.query.filter(name=name)
        #movie.delete()

    #Formatted data
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return 'Actor ID: {self.id}, name: {self.name}'

