import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.password = 'root'
        self.user = 'shrut'
        self.database_path = "postgres://{}:{}@{}/{}".format(self.user, self.password,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions_by_page(self):
        res = self.client().get('/questions?page=2000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'not found')

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))      

    def test_delete_questions_by_id(self):
        res = self.client().delete('/questions/13')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertTrue(data['total_questions'])

    def test_delete_questions_by_wrong_id(self):
        res = self.client().delete('/questions/1900')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422) 
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')
        

    def test_post_question(self):
        new_question = {
            'question': 'a',
            'answer': 'b',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_post_question_wrong_data(self):
        new_question = {
            'question':'',
            'answer': 'b',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422) 
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable') 

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_get_questions_by_wrong_category(self):
        res = self.client().get('/categories/90/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'not found')

    def test_search_question(self):
        search= {
            'searchTerm' : 'what'
        }
        res = self.client().post('/questions/search', json = search)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['current_category']))

    def test_search_wrong_question(self):
        search= {
            'searchTerm' : ''
        }
        res = self.client().post('/questions/search', json = search)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'not found')
        
    def test_quiz(self):
        quiz = {
            'previous_questions' : [],
            'quiz_category' :{
                'type':'click',
                'id':0
            }
        }
        res = self.client().post('/quizzes', json = quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    def test_quiz_wrong(self):
        quiz = {
            'previous_questions' : [],
            'quiz_category' :{
                'type':'',
                'id':0
            }
        } 
        res = self.client().post('/quizzes', json = quiz)
        data = json.loads(res.data) 
        self.assertEqual(res.status_code, 422) 
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')  
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()