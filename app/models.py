from sqlalchemy import desc

from app import db


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    # there will be stored count of unique words in note, it is very
    # convenient: we can get sorted notes directly from database
    unique_count = db.Column(db.Integer, index=True)

    @classmethod
    def all_ordered(cls):
        """
        get all notes, ordered by number of unique words
        """
        return Note.query.order_by(Note.unique_count.desc())

