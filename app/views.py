from flask import render_template

from app import app
from .models import Note


"""
According to task I decided not to give notes to the render_template 
function as a parameter. All the notes will be requested dynamically
with using ajax on a client. Furthermore, I will not use constructions
like this '{{ }}' and this '{% %}' in HTML page to improve performance
and follow KISS principle

UPD: Oops, I had some misunderstanding, I've though that 'Постарайтесь
избежать больших шаблонов сайтов' means not use html templates, but it 
really means other

Templates is the easiest way to do this task
"""
@app.route('/')
@app.route('/notes')
def notes():
    """
    Page with notes which are ordered by
    number of unique words in each note
    """
    return render_template('notes.html', notes=Note.all_ordered())


@app.route('/add_note')
def add_note():
    """
    Page with form for adding a new note
    """
    return render_template('add_note.html')
