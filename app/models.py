from sqlalchemy.orm import validates

from app import db


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    # there will be stored count of unique words in note, it is very
    # convenient: we can get sorted notes directly from database
    unique_count = db.Column(db.Integer, index=True)

    # I have decided to set note text max size to 500 chars
    # on this development stage to avoid db overloading
    # http://docs.sqlalchemy.org/en/latest/orm/mapped_attributes.html
    @validates('text')
    def validate_text(self, key, value):
        print('key: {0}, value: {1}'.format(key, value))
        if value is None:
            raise ValueError('Note should contain text!')
        if not value.strip(' '):  # if there are no non-space chars
            raise ValueError(
                'Note text should contain at least one non-space character'
            )
        if len(value) > 500:
            raise ValueError('Note text should contain up to 500 chars!')
        return value

    @classmethod
    def all_ordered(cls):
        """
        get all notes, ordered by number of unique words
        """
        return cls.query.order_by(Note.unique_count.desc())

