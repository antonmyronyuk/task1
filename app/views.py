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
notes adding without refreshing of the page on a client)
"""


@app.route('/', methods=['GET'])
@app.route('/notes', methods=['GET'])
def notes_get():
    """
    Page with notes which are ordered by
    number of unique words in each note
    """
    return render_template(
        'notes.html',
        notes=Note.all_ordered(),
        title='Sorted notes'
    )


@app.route('/notes', methods=['DELETE'])
def notes_delete():
    """
    Delete all the notes from database
    """
    Note.query.delete()
    db.session.commit()
    return jsonify({'status': 'OK'}), 200


@app.route('/add_note', methods=['GET'])
def add_note_get():
    """
    Page with form for adding a new note
    """
    return render_template(
        'add_note.html',
        title='Add new note'
    )


@app.route('/notes', methods=['POST'])
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

    print(note.id)
    return jsonify({'status': 'OK'}), 200
