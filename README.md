# Udacity FSND final project : Capstone

## Motivation for project

This project is the result of four months that I've passed trying to learn how to become a full stack web developer ! 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects.

Initializing :

```bash
python3 -m venv env
```

Activating :

```bash
source env/bin/activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/starter/` directory and running:

```bash
pip3 install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Create local database

Create a local database then run Database Migrations :

```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Running the server

From within the `starter/` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

## API Reference

# Error Handling :

Errors are returned as JSON objects in the following format:

```bash
{
    "success": False,
    "error": 404,
    "message":"resource not found"
}
```

# Endpoints

1. GET '/Movies'

- Returns a list of movies 
- When successeful it returns 200 and the following dictionaary :
```bash
{
    'success': True,
    'movies': formatted_movies
}
```
2. POST '/Movies'

- Creates a new movie in the database
- Request Arguments: {title:string, release_date:string}
- Example response:

```bash
{
    "success": true
    "movie": new_movie.format(), 
}
```
3. DELETE '/Movies'

- Delete a movie from the database
- Request Arguments: {movie_id:integer}
- Example response:

```bash
{
    "success": true
    "deleted": movie_to_delete.id, 
}
```
4. UPDATE '/Movies'

- Update a movie in the database
- Request Arguments: {movie_id:integer}
- Example response:

```bash
{
    "success": true
    "movie": movie_to_update.format(), 
}
```

5. GET '/Actors'

- Returns a list of actors 
- When successeful it returns 200 and the following dictionaary :
```bash
{
    'success': True,
    'movies': formatted_actors
}
```
6. POST '/Actors'

- Creates a new actor in the database
- Request Arguments: {name:string, age:string, gender:string}
- Example response:

```bash
{
    "success": true
    "movie": new_actor.format(), 
}
```
7. DELETE '/Actors'

- Delete an actor from the database
- Request Arguments: {actor_id:integer}
- Example response:

```bash
{
    "success": true
    "deleted": id, 
}
```
8. UPDATE '/Actors'

- Update an actor in the database
- Request Arguments: {actor_id:integer}
- Example response:

```bash
{
    "success": true
    "movie": actor_to_update.format(), 
}
```

## Roles and Permissions 

1. Casting Assistant 
- Can view actors and movies

2. Casting Director 
- All permessions a Casting Assistant has
- Add or delete an actor from the database
- Modify actors or movies

3. Executive Producer 
- All permessions a Casting Director has 
- Add or delete a movie from the database

## Testing 

To run the tests, run
```
createdb <database_name>
python test_app.py
```



