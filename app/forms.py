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

class BiSectionForm(FlaskForm):
	equation    = StringField  (u'Function f(x)'  , validators=[DataRequired()])
	xValue    	= IntegerField  (u'X Value'  , validators=[DataRequired()])
	stepValue   = IntegerField  (u'Step Value'  , validators=[DataRequired()])
	terminationValue    = StringField  (u'Termination Value'  , validators=[DataRequired()])

class SecantForm(FlaskForm):
	equation    = StringField  (u'Function f(x)'  , validators=[DataRequired()])
	x0Value    	= IntegerField  (u'X0 Value'  , validators=[DataRequired()])
	x1Value    	= IntegerField  (u'X1 Value'  , validators=[DataRequired()])
	iteratorValue   = IntegerField  (u'Iterator Value'  , validators=[DataRequired()])
	errorValue   = StringField  (u'Error Value'  , validators=[DataRequired()])

class FixedPointForm(FlaskForm):
	equation    = StringField  (u'Function f(x)'  , validators=[DataRequired()])
	x0Value    	= IntegerField  (u'X0 Value'  , validators=[DataRequired()])
	tolerance   = StringField  (u'Tolerance Value'  , validators=[])
	maxiter   = IntegerField  (u'Maxiter Value'  , validators=[])