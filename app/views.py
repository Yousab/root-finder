# -*- encoding: utf-8 -*-
"""
Now UI Dashboard - coded in Flask
Author: AppSeed.us - App Generator 
"""

# all the imports necessary
from flask import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException, NotFound, abort

import os
import sys

from app  import app

from flask       import url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app         import app, lm, db, bc
from . models    import User
from . common    import COMMON, STATUS
from . assets    import *
from . forms     import LoginForm, RegisterForm, BiSectionForm, SecantForm, FixedPointForm

import os, shutil, re, cgi

from . algos import BiSection, Secant, FixedPoint
        
# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# authenticate user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

# register user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # define login form here
    form = RegisterForm(request.form)

    msg = None

    # custommize your pate title / description here
    page_title       = 'Register - Flask Now UI Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Now UI Dashboard, registration page.'

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        name     = request.form.get('name'    , '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:                    
            pw_hash = bc.generate_password_hash(password)

            user = User(username, pw_hash, name, email)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    # try to match the pages defined in -> themes/light-bootstrap/pages/
    return render_template( 'layouts/default.html',
                            title=page_title,
                            content=render_template( 'pages/register.html', 
                                                     form=form,
                                                     msg=msg) )

# authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # define login form here
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # custommize your page title / description here
    page_title = 'Login - Flask Now UI Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Now UI Dashboard, login page.'

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            if bc.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unkkown user"

    # try to match the pages defined in -> themes/light-bootstrap/pages/
    return render_template( 'layouts/default.html',
                            title=page_title,
                            content=render_template( 'pages/login.html', 
                                                     form=form,
                                                     msg=msg) )

# Used only for static export
@app.route('/user.html')
def user():

    # custommize your page title / description here
    page_title = 'Icons - Flask Now UI Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Now UI Dashboard, the icons page.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/user.html') )

# Used only for static export
@app.route('/icons.html')
def icons():

    # custommize your page title / description here
    page_title = 'Icons - Flask Now UI Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Now UI Dashboard, the icons page.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/icons.html') )

# Used only for static export
@app.route('/tables.html')
def tables():

    # custommize your page title / description here
    page_title = 'Tables - Flask Now UI Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Now UI Dashboard, the tables page.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/tables.html') )

# Used only for static export
@app.route('/notifications.html')
def notifications():

    # custommize your page title / description here
    page_title = 'Tables - Flask Now UI Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Now UI Dashboard, the tables page.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/notifications.html') )

# Used only for static export
@app.route('/typography.html')
def typography():

    # custommize your page title / description here
    page_title = 'Typography - Flask Now UI Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Now UI Dashboard, the tables page.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/typography.html') )

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    content = None

    try:

        # try to match the pages defined in -> themes/light-bootstrap/pages/
        return render_template('layouts/default.html',
                                content=render_template( 'pages/'+path) )
    except:
        abort(404)

##################################################################################
## Custom Algo Routes
##################################################################################
@app.route('/bisection', methods=['GET', 'POST'])
def bisectionPage():
    #define the general algo form
    form = BiSectionForm(request.form)

    if form.validate_on_submit():

        # assign form data to variables
        equation = request.form.get('equation', '', type=str)
        xValue = request.form.get('xValue', '', type=int)
        stepValue = request.form.get('stepValue', '', type=int)
        terminationCriteria = request.form.get('termination_criteria')
        terminationValue = request.form.get('terminationValue', '', type=str)

        bisectionObj = BiSection(equation)

        genertedTable = bisectionObj.generate_table(xValue, stepValue)

        if terminationCriteria == 'it':
            terminationValue=int(terminationValue)
            xRoot = bisectionObj.bisect_iter(genertedTable['xl'],genertedTable['xu'], terminationValue)
        else:
            terminationValue=float(terminationValue)
            xRoot = bisectionObj.bisect_error(genertedTable['xl'],genertedTable['xu'], terminationValue)

        return render_template('layouts/default.html',
                                content=render_template( 'pages/bisection.html',
                                form=form,
                                return_value="true",
                                xLower=genertedTable['xl'],
                                xUpper=genertedTable['xu'],
                                xRoot=xRoot,
                                xyTable=genertedTable['table'],))
    else:
        return render_template('layouts/default.html',
                                content=render_template( 'pages/bisection.html',
                                form=form) )

@app.route('/false-position', methods=['GET', 'POST'])
def falsePositionPage():
    #define the general algo form
    form = BiSectionForm(request.form)

    if form.validate_on_submit():
        return render_template('layouts/default.html',
                                content=render_template( 'pages/false-position.html',
                                form=form,
                                return_value="return_values") )
    else:
        return render_template('layouts/default.html',
                                content=render_template( 'pages/false-position.html',
                                form=form) )

@app.route('/secant', methods=['GET', 'POST'])
def secantPage():
    #define the general algo form
    form = SecantForm(request.form)
    if form.validate_on_submit():
        # assign form data to variables
        equation = request.form.get('equation', '', type=str)
        x0Value = request.form.get('x0Value', '', type=int)
        x1Value = request.form.get('x1Value', '', type=int)
        iteratorValue = request.form.get('iteratorValue', '', type=int)
        errorValue = request.form.get('errorValue', '', type=str)

        secantObj = Secant(equation)

        xRoot, iterationNumber, returnedValues = secantObj.secant(x0=x0Value, x1=x1Value, iterr=iteratorValue, err=float(errorValue))

        return render_template('layouts/default.html',
                                content=render_template( 'pages/secant.html',
                                form=form,
                                return_value = "true",
                                x0 = x0Value,
                                x1 = x1Value,
                                xRoot = xRoot,
                                noOfIterations = iterationNumber,
                                xyTable = returnedValues['table']) )
    else:
        return render_template('layouts/default.html',
                                content=render_template( 'pages/secant.html',
                                form=form) )

@app.route('/fixed-point', methods=['GET', 'POST'])
def fixedPointPage():
    #define the general algo form
    form = FixedPointForm(request.form)
    if form.validate_on_submit():
        # assign form data to variables
        equation = request.form.get('equation', '', type=str)
        g_equation = request.form.get('gequation', '', type=str)
        x0Value = float(request.form.get('x0Value', '', type=str))
        toleranceValue = float(request.form.get('tolerance', '', type=str)) if (request.form.get('tolerance')) else ''
        maxiterValue = float(request.form.get('maxiter', '', type=str)) if (request.form.get('maxiter')) else ''

        fixedPointObj = FixedPoint(equation, g_equation)

        returnedValues = fixedPointObj.solve_fixed_point(x0=x0Value, tolerance=toleranceValue, maxiter=maxiterValue)

        return render_template('layouts/default.html',
                                content=render_template( 'pages/fixed-point.html',
                                form=form,
                                return_value = "true",
                                execution_time=returnedValues['time'],
                                returnedValues = returnedValues) )
    else:
        return render_template('layouts/default.html',
                                content=render_template( 'pages/fixed-point.html',
                                form=form) )

#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'),
#                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#@app.route('/sitemap.xml')
#def sitemap():
#    return send_from_directory(os.path.join(app.root_path, 'static'),
#                               'sitemap.xml')

# ------------------------------------------------------

# error handling
# most common error codes have been added for now
# TO DO:
# they could use some styling so they don't look so ugly

def http_err(err_code):
	
    err_msg = 'Oups !! Some internal error ocurred. Thanks to contact support.'
	
    if 400 == err_code:
        err_msg = "It seems like you are not allowed to access this link."

    elif 404 == err_code:    
        err_msg  = "The URL you were looking for does not seem to exist."
        err_msg += "<br /> Define the new page in /pages"
    
    elif 500 == err_code:    
        err_msg = "Internal error. Contact the manager about this."

    else:
        err_msg = "Forbidden access."

    return err_msg
    
@app.errorhandler(401)
def e401(e):
    return http_err( 401) # "It seems like you are not allowed to access this link."

@app.errorhandler(404)
def e404(e):
    return http_err( 404) # "The URL you were looking for does not seem to exist.<br><br>
	                      # If you have typed the link manually, make sure you've spelled the link right."

@app.errorhandler(500)
def e500(e):
    return http_err( 500) # "Internal error. Contact the manager about this."

@app.errorhandler(403)
def e403(e):
    return http_err( 403 ) # "Forbidden access."

@app.errorhandler(410)
def e410(e):
    return http_err( 410) # "The content you were looking for has been deleted."

	