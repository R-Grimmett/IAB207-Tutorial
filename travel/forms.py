from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')

class DestinationForm(FlaskForm):
  name = StringField('Country', validators=[InputRequired()])
  # adding two validators, one to ensure input is entered and other to check if the 
  # description meets the length requirements
  description = TextAreaField('Description', validators = [InputRequired()])
  image = StringField('Cover Image', validators=[InputRequired()])
  currency = StringField('Currency', validators=[InputRequired()])
  submit = SubmitField("Create")
    
class LoginForm(FlaskForm):
  username = StringField('Username', validators=[InputRequired()])
  password = StringField('Password', validators=[InputRequired()])
  submit = SubmitField("Login")

class RegisterForm(FlaskForm):
  username = StringField('Username', validators=[InputRequired()])
  email = StringField('Email', validators=[InputRequired(), Email("Please Enter a Valid Email Address")])
  password = StringField('Password', validators=[InputRequired()])
  password_confirm = StringField('Confirm Your Password', validators=[InputRequired(), EqualTo('password', 'Passwords do not match!')])
  submit = SubmitField('Register')