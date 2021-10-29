from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """few things to run before each test"""
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

    def test_homepage(self):
        """tests if board is in session, and if certain html elements are displayed on the requested page"""
        with self.client:
            resp = self.client.get('/')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('board', session)
            self.assertIn('<p>Your highscore is', html)
            self.assertIn('<button>Enter</button>', html)

    def test_post_score(self):
        """tests if highscore and num_plays are held in session"""
        with self.client:
            with self.client.session_transaction() as change_session:
                change_session['highscore'] = 50
                change_session['num_plays'] = 20

            resp = self.client.get('/')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['highscore'], 50)
            self.assertEqual(session['num_plays'], 20)

    def test_valid_guess(self):
        """tests if a user's guess is valid through a modified board in session"""
        with self.client:
            with self.client.session_transaction() as change_session:
                change_session['board'] = [
                    ['T', 'A', 'L', 'E', 'R'],
                    ['E', 'W', 'K', 'D', 'E'],
                    ['O', 'P', 'R', 'D', 'F'],
                    ['F', 'A', 'E', 'R', 'H'],
                    ['T', 'T', 'O', 'P', 'S'],
                ]
            guess = 'tale'
            resp = self.client.post('/process', data = {'guess' : guess })

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'ok')
    
    def test_invalid_guess(self):
        """test if word in invalid by not being on the modified board in session"""
        with self.client:
            with self.client.session_transaction() as change_session:
                change_session['board'] = [
                    ['T', 'A', 'L', 'E', 'R'],
                    ['E', 'W', 'K', 'D', 'E'],
                    ['O', 'P', 'R', 'D', 'F'],
                    ['F', 'A', 'E', 'R', 'H'],
                    ['T', 'T', 'O', 'P', 'S'],
                ]
        guess = 'sailor'       
        resp = self.client.post('/process', data = {'guess' : guess})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['result'], 'not-on-board')


    

