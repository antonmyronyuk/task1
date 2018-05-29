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
        self.assertEqual(res.headers['Content-Type'],
                         'text/html; charset=utf-8')

        res = self.app.get('/notes/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/html; charset=utf-8')

    def test_notes_add_get(self):
        res = self.app.get('/notes/add/')
        self.assertEqual(res.status_code, 200)

    def test_notes_delete(self):
        strings = ['one', 'two', 'three', 'four']

        # fill database
        for string in strings:
            db.session.add(Note(
                text=string,
                unique_count=count_unique_words(string)
            ))
        db.session.commit()
        self.assertEqual(len(Note.ordered_all()), len(strings))

        res = self.app.delete('/api/notes')
        self.assertEqual(res.status_code, 200)

        # check number of rows deleted
        msg = json.loads(res.data.decode())['status']
        self.assertEqual(msg, 'OK - {0} rows was deleted'.format(len(strings)))

        # check if really deleted
        self.assertEqual(len(Note.ordered_all()), 0)

        # deleting from empty table
        res = self.app.delete('/api/notes')
        self.assertEqual(res.status_code, 200)

        # check number of rows deleted
        msg = json.loads(res.data.decode())['status']
        self.assertEqual(msg, 'OK - 0 rows was deleted')

    def test_notes_post(self):
        # no text field
        res = self.app.post('/api/notes', data={'txt': 'text'})
        self.assertEqual(res.status_code, 400)
        msg = json.loads(res.data.decode())['status']
        self.assertEqual(msg, 'there is no text field in the note')

        # empty text field
        res = self.app.post('/api/notes', data={'text': ''})
        self.assertEqual(res.status_code, 400)
        msg = json.loads(res.data.decode())['status']
        self.assertEqual(msg, 'Note should contain text!')

        # spaces in text field
        res = self.app.post('/api/notes', data={'text': '      '})
        self.assertEqual(res.status_code, 400)
        msg = json.loads(res.data.decode())['status']
        self.assertEqual(msg, 'Note text should contain at '
                         + 'least one non-space character!')

        # too large text field
        res = self.app.post('/api/notes', data={'text': 'a ' * 600})
        self.assertEqual(res.status_code, 400)
        msg = json.loads(res.data.decode())['status']
        self.assertEqual(msg, 'Note text should contain up to 500 chars!')

        # add valid notes
        res = self.app.post('/api/notes', data={'text': 'Hello World!'})
        self.assertEqual(res.status_code, 201)
        msg = json.loads(res.data.decode())
        self.assertEqual(msg['status'], 'OK - created a new note')
        self.assertEqual(msg['note']['text'], 'Hello World!')
        self.assertEqual(msg['note']['unique_count'], 2)

        res = self.app.post('/api/notes', data={'text': 'Hello hello!'})
        self.assertEqual(res.status_code, 201)
        msg = json.loads(res.data.decode())
        self.assertEqual(msg['status'], 'OK - created a new note')
        self.assertEqual(msg['note']['text'], 'Hello hello!')
        self.assertEqual(msg['note']['unique_count'], 1)

        # check if notes were added to database
        notes = Note.ordered_all()
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0].text, 'Hello World!')
        self.assertEqual(notes[0].unique_count, 2)
        self.assertEqual(notes[1].text, 'Hello hello!')
        self.assertEqual(notes[1].unique_count, 1)


