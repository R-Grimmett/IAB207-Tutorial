from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from . import db

from .models import Destination

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    destinations = db.session.scalars(db.select(Destination)).all()
    return render_template('index.html', destinations=destinations)


@mainbp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print("SEARCH QUERY: " + request.args['search'])
        query = "%" + request.args['search'] + "%"
        destinations = db.session.scalars(db.select(Destination).where(Destination.description.like(query)))
        return render_template('index.html', destinations=destinations)
    else:
        return redirect(url_for('main.index'))
