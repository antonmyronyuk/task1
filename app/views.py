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
@app.route('/')
@app.route('/notes')
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


@app.route('/notes/add', methods=['GET'])
def add_note_get():
    """
    Page with form for adding a new note
    """
    return render_template(
        'add_note.html',
        title='Add new note'
    )


@app.route('/notes/add', methods=['POST'])
def add_node_post():
    text = request.form['text']
    print(text)
    try:
        note = Note(
            # text will be escaped automatically while rendering
            text=text,
            unique_count=count_unique_words(text)
        )
        db.session.add(note)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'status': 'bad note text'}), 400

    return jsonify({'status': 'OK'}), 200


