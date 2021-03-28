import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import sys
import traceback
from models import Movies, Actors, app, db
from config import SQLALCHEMY_DATABASE_URI
import json 

from auth.auth import AuthError, requires_auth


AUTH0_CALLBACK_URL = 'http://http://0.0.0.0:8080/'
AUTH0_CLIENT_ID = '3R7wm6VXWZCYCY0W9wQ7rfwV4dfQX4ru'


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  #Set up CORS. Allow '*' for origins.
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  #Using the after request decorator to se Access-Control-Allow
  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

  #Endpoint : Welcome
  @app.route('/')
  def Welcome():
    return 'Udacity final project'


  #Endpoint to handle GET request
  @app.route('/Movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(jwt):

    movies = Movies.query.all()
    if len(movies) == 0:
      abort(404)
    
    formatted_movies = [mov.format() for mov in movies]
    return jsonify({
      'success': True,
      'movies': formatted_movies
     
    }), 200
  

  #Endpoint to handle GET request
  @app.route('/Actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(jwt):
    actors = Actors.query.all()
    if len(actors) == 0:
      abort(404)
    
    formatted_actors = [act.format() for act in actors]
    return jsonify ({
      'success': True,
      'actors': formatted_actors
    }), 200


  #Endpoint to handle POST request for movies
  @app.route('/Movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movies(jwt):

    data = request.get_json()
    if 'title' not in data :
      abort(422)
    if 'release_date' not in data :
      abort(422)
    
    new_title = data.get('title')
    new_release_date = data.get('release_date')

    try :
      new_movie = Movies(
        title = new_title,
        release_date = new_release_date
      )
      new_movie.insert()
    except : 
      abort(422)
    
    
    return jsonify({
      'success': True,
      'movie': new_movie.format()
    }), 200

  
  #Endpoint to handle DELETE request for movies
  @app.route('/Movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt, id):
    try:
      movie_to_delete = Movies.query.get(id)
      movie_to_delete.delete()
      id = movie_to_delete.id
      return jsonify({
        'success': True,
        'deleted': id
      }), 200
    except :
      abort(422)


  #Endpoint to handle UPDATE request for movies
  @app.route('/Movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(jwt, id):

    movie_to_update= Movies.query.get(id)
    if movie_to_update is None:
      abort(404)

    data = request.get_json()
    if 'title' in data:
      if data.get('title') is None :
        abort (400)
      movie_to_update.title = data.get('title')

    if 'release_date' in data :
      if data.get('release_date') is None :
        abort(400)
      movie_to_update.release_date = data.get('release_date')
    
    try : 
      movie_to_update.update()

      return jsonify({
        'success': True,
        'movie': movie_to_update.format()
      }), 200
    except :
      abort (422)
    

  #Endpoint to handle POST request for actors
  @app.route('/Actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actors(jwt):
    data = request.get_json()
    if 'name' not in data:
      abort(422)
    if 'age' not in data:
      abort(422)
    if 'gender' not in data: 
      abort(422)
    
    try:
      new_actor = Actors(
        name = data.get('name'),
        age = data.get('age'),
        gender = data.get('gender')
      )
      new_actor.insert()
    except :
      abort(422)
    
    return jsonify({
      'success': True,
      'actor': new_actor.format()
    }), 200


  #Endpoint to handle DELETE request for actors
  @app.route('/Actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt, id):
    try:
      actor = Actors.query.filter(Actors.id == id).one_or_none()
      actor.delete()
      return jsonify({
        'success': True,
        'deleted': id
      }), 200
    except :
      abort(422)


  #Endpoint to handle UPDATE request for actors
  @app.route('/Actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(jwt, id):

    actor_to_update = Actors.query.get(id)
    if actor_to_update is None :
      abort(404)
    
    data = request.get_json()
    if 'name' in data :
      if data.get('name') is None :
        abort (400)
      actor_to_update.name = data.get('name')
    
    if 'age' in data:
      if data.get('age') is None :
        abort (400)
      actor_to_update.age = data.get('age')
    
    if 'gender' in data:
      if data.get('gender') is None :
        abort(400)
      actor_to_update.gender = data.get('gender')

    try:
      actor_to_update.update()
    except:
      abort (422)

    return jsonify({
      'success': True,
      'actor': actor_to_update.format(),
    }), 200
    

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": 'Bad Request'
                    }), 400
    

  @app.errorhandler(404)
  def not_found(error):
     return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                    "success": False,
                    "error": 422,
                    "message": 'Unprocessable entity'
                    }), 422

  @app.errorhandler(AuthError)
  def auth_error(error):
      return jsonify({
          "success": False,
          "error": error.status_code,
          "message": error.error['description']
      }), error.status_code

      
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)