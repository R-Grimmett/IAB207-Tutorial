from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination, Comment
from .forms import CommentForm, DestinationForm
from . import db

destbp = Blueprint('destination', __name__, url_prefix='/destinations')

@destbp.route('/<id>')
def show(id):
  destination = db.session.scalar(db.select(Destination).where(Destination.id == id))
  commentForm = CommentForm()
  return render_template('destinations/show.html', destination=destination, form=commentForm)

@destbp.route('/<id>/comment', methods = ['GET', 'POST'])
def comment(id):
  form = CommentForm()
  # Get the id of the destination that the comment is being made on
  destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
  if form.validate_on_submit():
    comment = Comment(text = form.text.data, destination = destination)
    db.session.add(comment)
    db.session.commit()
    print(f"The following comment has been posted: {form.text.data}")
  return redirect(url_for('destination.show', id=id))

@destbp.route('/create', methods = ['GET', 'POST'])
def create():
  print('Method type: ', request.method)
  form = DestinationForm()
  if form.validate_on_submit():
    destination = Destination(name = form.name.data, 
                              description = form.description.data,
                              image = form.image.data,
                              currency=form.currency.data)
    # Add new destination to the database
    db.session.add(destination)
    db.session.commit() 
    print('Successfully created new travel destination', 'success')
    # implement the PRG pattern to avoid duplicate form submissions
    # "The golden rule is: Always end the handling of a POST request with a redirect"
    return redirect(url_for('destination.create'))
  return render_template('destinations/create.html', form=form)


