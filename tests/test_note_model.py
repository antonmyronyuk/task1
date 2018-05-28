import unittest

from app import app, db
from app.models import Note
from counter import count_unique_words


class TestNoteModel(unittest.TestCase):

    def setUp(self):
        # database in memory
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_validation(self):
        with self.assertRaises(ValueError):
            Note(text=None, unique_count=None)
        with self.assertRaises(ValueError):
            Note(text='', unique_count=0)
        with self.assertRaises(ValueError):
            Note(text='          ', unique_count=0)
        with self.assertRaises(ValueError):
            Note(text='a ' * 900, unique_count=1)  # long string

        # success
        self.assertTrue(Note(text='text', unique_count=1))

    def test_all_ordered(self):
        strings = ['  three,, words here', 'one', 'lol lol lol lol kek',
                   ' ....??... ', 'the biggest note in this test']

        for string in strings:
            db.session.add(Note(
                text=string,
                unique_count=count_unique_words(string)
            ))
        db.session.commit()

        notes_db = [
            (note.text, note.unique_count) for note in Note.ordered_all()
        ]

        # sort original notes
        notes_original = sorted(
            ((s, count_unique_words(s)) for s in strings),
            key=lambda item: item[1],  # by count
            reverse=True
        )

        self.assertEqual(notes_db, notes_original)
