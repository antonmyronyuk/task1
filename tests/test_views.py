import unittest
import json

from app import app, db
from app.models import Note
from counter import count_unique_words


class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        # database in memory
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_notes_get(self):
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)
        res = self.app.get('/notes')
        self.assertEqual(res.status_code, 200)

    def test_notes_add_get(self):
        res = self.app.get('/notes/add')
        self.assertEqual(res.status_code, 200)

    def test_notes_delete(self):
        strings = ['one', 'two', 'three', 'four']

        for string in strings:
            db.session.add(Note(
                text=string,
                unique_count=count_unique_words(string)
            ))
        db.session.commit()
        self.assertEqual(len(Note.ordered_all()), len(strings))

        res = self.app.delete('/api/notes')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(Note.ordered_all()), 0)

    def test_notes_post(self):
        # no text field
        res = self.app.post('/api/notes', data={'txt': 'text'})
        self.assertEqual(res.status_code, 400)

        # empty text field
        res = self.app.post('/api/notes', data={'text': ''})
        self.assertEqual(res.status_code, 400)

        # spaces in text field
        res = self.app.post('/api/notes', data={'text': '      '})
        self.assertEqual(res.status_code, 400)

        # too large text field
        res = self.app.post('/api/notes', data={'text': 'a ' * 600})
        self.assertEqual(res.status_code, 400)

        # add valid note
        res = self.app.post('/api/notes', data={'text': 'Hello World!'})
        self.assertEqual(res.status_code, 201)
        res = self.app.post('/api/notes', data={'text': 'Hello Humans!'})
        self.assertEqual(res.status_code, 201)

        # check if notes were added to database
        self.assertEqual(len(Note.ordered_all()), 2)


