from flask import Blueprint, render_template, redirect, request, session
from util.pbkdf2 import pbkdf2_hex
from util.salts import get_random_salt
from app.models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

auth = Blueprint('auth', __name__,
                 template_folder='templates')


@auth.record
def getDB(state):
    """ Setup the database handle once I am attached to an app """
    db_uri = state.app.config['DB_URI']
    db_name = state.app.config['DB_NAME']
    engine = create_engine('%s/%s' % (db_uri, db_name))
    auth.db = sessionmaker(bind=engine)()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handler for anything related to login
    GET -- render the login page
        :return html

    POST -- Authenticate the user, return Invalid Credentials on error.
           Set session user.
        :return html
    """
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        # Get the user information
        name = request.form['username']
        passwd = request.form['userpass']

        # Find a user with that username an compare passwords
        user = auth.db.query(User).filter(User.name == name).one()
        if user:
            thehash = pbkdf2_hex(passwd.encode('utf-8'),
                                     user.salt.encode('utf-8'))
            # password matches
            if thehash == user.hash:
                session['user'] = user.id
                return redirect('/')
            else:
                error = 'Invalid Credentials'
                return render_template('login.html', error=error)
        else:
            error = 'Invalid Credentials'
            return render_template('login.html', error=error)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handler realted to anything signup
    GET -- render the signup page
        :return html
    POST -- If user passwords match, create a user.  Create session
        :return html

    @TODO - check username uniqueness
    """
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        name = request.form['username']
        pass1 = request.form['userpass']
        pass2 = request.form['userpass2']
        # do they match?
        if pass1 != pass2:
            error = 'Passwords do not match'
            return render_template('signup.html', error=error)
        # do we already have a user under that name?
        if auth.db.query(User).filter(User.name == name).one():
            error = 'User already taken'
            return render_template('signup.html', error=error)

        salt = get_random_salt(16)
        thehash = pbkdf2_hex(pass1.encode('utf-8'), salt.encode('utf-8'))

        # Make a new user out of the info
        new_user = User(name, unicode(thehash), salt)

        auth.db.add(new_user)
        auth.db.commit()
        # store user id in the session
        session['user'] = new_user.id

        return redirect('/')


@auth.route('/signout', methods=['GET'])
def signout():
    """ Sign out the user """
    if request.method == 'GET':
        del session['user']
        return redirect('/')
