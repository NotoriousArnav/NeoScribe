from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from forms import Notebook
import imghdr
import time
import uuid
from db import db
from models import User, Page
from models import  Notebook as NotebookModel

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else "jpg")

main = Blueprint('main', __name__)

@main.route('/')
# @login_required
async def main_route():
    if current_user.is_anonymous:
        return render_template('landing_page.html')
    notebooks = NotebookModel.query.filter_by(author=current_user.id)
    return render_template(
        'index.html',
        user=current_user,
        notebooks=notebooks
    )

@main.get('/notebook/new')
@login_required
async def make_notebook():
    form = Notebook()
    return render_template(
        'new_notebook.html',
        user=current_user,
        form=form
    )

@main.post('/notebook/new')
@login_required
def notebook_create():
    name = request.form.get('name')
    desc = request.form.get('description')
    upload_user = current_user.id
    timestamp = time.time()

    new_notebook = NotebookModel(
            id = str(uuid.uuid4()),
            name = name,
            description = desc,
            timestamp = timestamp,
            author = upload_user
        )
    
    db.session.add(new_notebook)
    db.session.commit()

    return redirect(url_for('main.main_route'))