import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import create_app
from models import setup_db, Movies, Actors


Acces_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRsUG0zaG1UNm1odGhOOHEtU0dwUSJ9.eyJpc3MiOiJodHRwczovL3Rlc3Qtbm8tMS5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDQxNTYyNzExODkyNTU5MjA3MzMiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYxNjQ1MjkwMSwiZXhwIjoxNjE2NDYwMTAxLCJhenAiOiIzUjd3bTZWWFdaQ1lDWTBXOXdRN3Jmd1Y0ZGZRWDRydSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.UrkoRBuEoKxG1DcnUjMWmlxG7Y0fMu7ZNYFJoKv_G5Qdm37IkljgKUyI44DYwE6BzY10Eym6vuqGXAwLy3hw8Ku6gveaWI5RQcddd8BNgeCgzOoIVM3dQYoRAQMgEe86buqR9hbaAIOG9ciajgN5NWWx62FQQouSdWOqpC-PjkcoAwfGJBQiYYXTM-OZvLrJNdppCb-F-8z6KcSR5fJe74BPxUGx5XLxTMCVBDB8aj25t1hvHC2CnG-off9QSGIvr4SD6MizYdlG8TPk0xMhc36hsUvqeEEl1u1Y_jcgm07RW1p6_OYpWxeTKqS4bNerq3NdumjmUGeraff7KwlFhg'


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "caps_base"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.exec_prod = Acces_token
        self.app.config['TESTING'] = True

        self.new_movie = {
            "title": "Titanic",
            "release_date": "1997",
        }
        self.update_movie = {
            "title": "This movie is updated"
        }
        self.new_actor = {
            "name":"Anis",
            "age": "26",
            "gender":"male"
        }
        self.update_actor = {
            "name":"Name-Updated"
        }
        
    def tearDown(self):
        """Executed after reach test"""
        pass

    #This test is for getting the movie                              
    def test_get_movies(self):
        res = self.client().get('/Movies', 
                                    headers={
                                        "Authorization": "Bearer " + self.exec_prod
                                    })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #This test is for getting the actors                              
    def test_get_actors(self):
        res = self.client().get('/Actors',
                                    headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # #This test is for creating a new movie                             
    def test_create_new_movie(self):
        res = self.client().post('/Movies',
                                    headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    },
                                    json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # #This test is for deleting a movie                                 
    def test_delete_movie(self):
        #We will create a movie that will be deleted in the test 
        create_movie = {
            'title' : 'This is a delete test movie',
            'release_date' : '2000'
                        } 
        res = self.client().post('/Movies',headers={
                                            'Authorization': 'Bearer ' + self.exec_prod
                                                    }, json = create_movie)
        data = json.loads(res.data)
        movie_id= data['movie']['id']
        #Now we will execute the test for deleting the 'create_movie'
        res = self.client().delete('/Movies/{}'.format(movie_id), headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                                                            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # #This test is for updating a movie
    def test_update_movie(self):
        #We will create a movie to update later in the test
        create_movie = {
            'title': 'This an update test movie',
            'release_date':'1990'
                        }
        res = self.client().post('/Movies', headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    }, json = create_movie)
        data = json.loads(res.data)
        movie_id= data['movie']['id']
        #We will execute the test for update
        update_movie = self.update_movie
        res = self.client().patch('/Movies/{}'.format(movie_id), headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    }, json = update_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # #This test is for adding a new actor
    def test_create_new_actor(self):
        res = self.client().post('/Actors',
                                    headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    }, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # #This test is for deleting an actor
    def test_delete_actor(self):
        create_actor = {
            'name': 'Test_name',
            'age': '30',
            'gender': 'Male'
        }
        res = self.client().post('/Actors', headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    }, json = create_actor)
        data = json.loads(res.data)
        actor_id= data['actor']['id']
        res = self.client().delete('/Actors/{}'.format(actor_id),  headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # #This test is for updating an actor
    def test_update_actor(self):
        create_actor = {
            'name': 'Name-Non-Updated',
            'age': '30',
            'gender': 'Male'
        }
        res = self.client().post('/Actors', headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    } ,json = create_actor)
        data = json.loads(res.data)
        actor_id= data['actor']['id']
        update_actor = self.update_actor
        res = self.client().patch('/Actors/{}'.format(actor_id), headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    },json = update_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == "__main__":
    unittest.main()