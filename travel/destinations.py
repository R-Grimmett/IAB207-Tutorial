from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination, Comment
from .forms import CommentForm, DestinationForm
from . import db
import os
from werkzeug.utils import secure_filename

destbp = Blueprint('destination', __name__, url_prefix='/destinations')


@destbp.route('/<id>')
def show(id):
    destination = db.session.scalar(db.select(Destination).where(Destination.id == id))
    commentForm = CommentForm()
    return render_template('destinations/show.html', destination=destination, form=commentForm)


@destbp.route('/<id>/comment', methods=['GET', 'POST'])
def comment(id):
    form = CommentForm()
    # Get the id of the destination that the comment is being made on
    destination = db.session.scalar(db.select(Destination).where(Destination.id == id))
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, destination=destination)
        db.session.add(comment)
        db.session.commit()
        print(f"The following comment has been posted: {form.text.data}")
    return redirect(url_for('destination.show', id=id))


@destbp.route('/create', methods=['GET', 'POST'])
def create():
    print('Method type: ', request.method)
    form = DestinationForm()
    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        destination = Destination(name=form.name.data,
                                  description=form.description.data,
                                  image=db_file_path,
                                  currency=form.currency.data)
        # Add new destination to the database
        db.session.add(destination)
        db.session.commit()
        print('Successfully created new travel destination', 'success')
        # implement the PRG pattern to avoid duplicate form submissions
        # "The golden rule is: Always end the handling of a POST request with a redirect"
        return redirect(url_for('destination.create'))
    return render_template('destinations/create.html', form=form)

def check_upload_file(form):
  # Retrieve file data from the create form in forms.py
  fp = form.image.data
  filename = fp.filename
  # Get the current path of the module file and store image relative to this path
  BASE_PATH = os.path.dirname(__file__)
  # Upload file location
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  # Store relative path in the DB as image location in HTML
  db_upload_path = '/static/image' + secure_filename(filename)
  # Save image and return relative path for DB storage
  fp.save(upload_path)
  return db_upload_path
