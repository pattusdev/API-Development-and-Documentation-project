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
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "rwego", "admin123", 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            self.new_question = {
                "question": "Me",
                "answer": "You",
                "difficulty": "1",
                "category": "2"
            }
            self.new_question2 = {
                # ques to create error!
                "ques": "Me",
                "answer": "You",
                "difficulty": "1",
                "category": "2"
            }

            self.search_term = {
                'searchTerm': 'who'
            }
            self.search_term2 = {
                'searchTerm': ''
            }
            self.quiz = {
                'previous_questions': [],
                'quiz_category': {
                    'type': 'Science',
                    'id': '22'
                }
            }
            self.quiz2 = {
                'previous_questions': []
            }

    def tearDown(self):
        """Executed after reach test"""
        pass

    # testing pagination with respect of 10 question
    def test_selected_paginate_questions(self):
        resp = self.client().get('/questions')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    # testing error for not available page/beyond
    def test_404handler_beyond_valid_page(self):
        resp = self.client().get('/questions?page=30', json={'id': 1000})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page not found')

    # testing display all categories available
    def test_getAll_categories(self):
        resp = self.client().get('/categories')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    # testing error for no available category
    def test_404handler_category_not_found(self):
        resp = self.client().get('/categories/8000/questions')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page not found')

    # testing success remove question
    def test_remove_question(self):
        qts_no = 15
        resp = self.client().delete('/questions/{}'.format(qts_no))
        data = json.loads(resp.data)

        # question = Question.query.filter_by(id=id).one_or_none()
        # fro trivia_test...

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'], qts_no)
        # here the total question is from trivia db
        self.assertTrue(data['total_qts'])

    # testing error for question not found
    def test_422handler_question_notFound(self):
        qts_no = 11
        resp = self.client().delete('/questions/{}'.format(qts_no))
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable resources')

    # testing success for create new question
    def test_create_new_question(self):
        resp = self.client().post('/questions', json=self.new_question)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['new_question']))
        self.assertTrue(data['tot_questions'])

    # testing error for failed question creation
    def test_405handler_creation_notAllowed(self):
        resp = self.client().post('/questions', json=self.new_question2)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid method!')

    # testing finding a question
    def test_find_questions(self):
        resp = self.client().post('/questions/search', json=self.search_term)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['total_questions'])
        self.assertIsNotNone(data['questions'])

    # testing error to find a question
    def test_404handler_question_notFound(self):
        resp = self.client().post('/questions/search', json=self.search_term2)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page not found')

    # testing get questions by Category
    def test_get_questions_byCategory(self):
        cat = 2
        resp = self.client().get('/categories/{}/questions'.format(cat))
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['total_questions'])
        self.assertIsNotNone(data['questions'])
        self.assertTrue(data['current_category'])

    # testing error to get questions by category
    def test_404handler_questions_byCategory_notFound(self):
        cat = 500
        resp = self.client().get('/categories/{}/questions'.format(cat))
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page not found')

    # testing to start a quiz
    def test_start_quiz(self):
        resp = self.client().post('/quizzes', json=self.quiz)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    # testing error to start a quiz
    def test_422handler_error_toStart__quiz(self):
        resp = self.client().post('/quizzes', json=self.quiz2)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable resources')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
