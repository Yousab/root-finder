# -*- encoding: utf-8 -*-
"""
Flask Boilerplate
Author: AppSeed.us - App Generator 
"""

from flask_wtf          import FlaskForm, RecaptchaField
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, DataRequired

class LoginForm(FlaskForm):
	username    = StringField  (u'Username'        , validators=[DataRequired()])
	password    = PasswordField(u'Password'        , validators=[DataRequired()])

class RegisterForm(FlaskForm):
	username    = StringField  (u'Username'  , validators=[DataRequired()])
	password    = PasswordField(u'Password'  , validators=[DataRequired()])
	email       = StringField  (u'Email'     , validators=[DataRequired(), Email()])
	name        = StringField  (u'Name'      , validators=[DataRequired()])

class AlgoForm(FlaskForm):
	equation    = StringField  (u'Function f(x)'  , validators=[DataRequired()])
	xValue    	= IntegerField  (u'X Value'  , validators=[DataRequired()])
	stepValue   = IntegerField  (u'Step Value'  , validators=[DataRequired()])
	terminationValue    = StringField  (u'Termination Value'  , validators=[DataRequired()])
