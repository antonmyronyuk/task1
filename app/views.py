from flask import (
    render_template, request, jsonify, escape
)

from app import app, db
from .models import Note
from counter import count_unique_words

"""
I think templates are good solution for this task, because
we don't need to build SPA (according to the task description
site should contain two pages: one with adding form, second
shows all the notes, so we don't need to build real-time 
notes adding without refreshing of the page on a client).
But you can add multiple notes on adding page without refreshing
of the page (client sends ajax request to the server and shows if
adding was successful). Also notes deleting works without refreshing
of the page (client also sends ajax request and clear notes section).
"""


@app.route('/', methods=['GET'])
@app.route('/notes/', methods=['GET'])
def notes_get():
    """
    Page with notes which are ordered by
    number of unique words in each note
    """
    return render_template(
        'notes.html',
        notes=Note.ordered_all(),
        title='Sorted notes'
    )


@app.route('/notes/add/', methods=['GET'])
def notes_add_get():
    """
    Page with form for adding a new note
    """
    return render_template(
        'add_note.html',
        title='Add new note'
    )

# #############################################
# ######              API          ############
# #############################################


@app.route('/api/notes', methods=['DELETE'])
def notes_delete():
    """
    Delete all the notes from database
    """
    rows_deleted = Note.query.delete()
    db.session.commit()
    return jsonify(
        {'status': 'OK - {0} rows was deleted'.format(rows_deleted)}
    ), 200


@app.route('/api/notes', methods=['POST'])
def note_post():
    """
    Add new note to database
    """
    try:
        text = request.form['text']
    except KeyError:
        return jsonify({'status': 'there is no text field in the note'}), 400

    try:
        note = Note(
            # text will be escaped automatically while rendering
            text=text,
            unique_count=count_unique_words(text)
        )
    except ValueError as e:  # failed validation
        return jsonify({'status': str(e)}), 400
    else:
        db.session.add(note)
        db.session.commit()

    # return created item (helpful while testing server from console)
    return jsonify(
        {
            'status': 'OK - created a new note',
            'note': {
                'id': note.id,
                'text': note.text,
                'unique_count': note.unique_count
            }
        }
    ), 201
