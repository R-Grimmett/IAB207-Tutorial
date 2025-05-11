from . import db
from datetime import datetime

# As all the data is stored in the DB we don't need __init__() functions
# Good practice to specify __tablename__

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), index = True, unique = True, nullable = False)
    emailid = db.Column(db.String(100), index = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    # Reference to the Comments that the User has made
    comments = db.relationship('Comment', backref = 'user')

    def __repr__(self):
        return f"Name : {self.name}"

class Destination(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), index = True, unique = True, nullable = False)
    description = db.Column(db.String(255))
    image = db.Column(db.String(400))
    currency = db.Column(db.String(5))
    # Comment Relation
    comments = db.relationship('Comment', backref = 'destination')
    
    def __repr__(self):
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(400), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now())
    # Adding FOREIGN KEYS
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))
    
    def __repr__(self):
        return f"Comment: {self.text}"