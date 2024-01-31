# Definitions of application routes
from applicationfiles import app, custom_error
from applicationfiles.db_connect import connect_to_database, close_connection
from flask import render_template, request, url_for, redirect, session
import os
import secrets

error_message = None
#connection = None

try:
    import pymysql
except ImportError:
    pymysql = None
    error_message = 'Pymysql kirjastoa ei ole asennettu'
    custom_error.handle_error(error_message)
finally:
    error_message = None

class User:
    def __init__(self, id, username, password):
        self.user_id = id
        self.username = username
        self.password = password
    def __repr__(self):
        return f'<User: {self.username}>'

# Session management
app.config['SESSION_TYPE'] = 'memcached'
session_secret_key = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = session_secret_key

# Index and Home location routes
@app.route("/")
def index():
    return render_template("index.html")
    #print(__name__)
@app.route("/home")
def home():
    return render_template("index.html")
# About page route
@app.route('/about')
def about():
    return render_template("about.html")
# Contact page route
@app.route('/contact')
def contact():
    return render_template("contact.html")

# Registeration page route
@app.route('/register', methods=['GET','POST'])
def register():
    global connection
    if request.method == 'POST':
        userUsername = request.form['username']
        userPassword = request.form['password']
        userEmail = request.form['email']
        # Get database parameters from .env
        dbhost = os.getenv('MYSQL_HOST')
        dbuser = os.getenv('MYSQL_USER')
        dbpassword = os.getenv('MYSQL_PASSWORD')
        database = os.getenv('MYSQL_DB')
        # Connect to database
        connection = connect_to_database(dbhost, dbuser, dbpassword, database)
        if not connection:
            return render_template('error.html', error_message="Yhteyttä tietokantaan ei voitu luoda. Yritä myöhemmin uudelleen", redirect_url=url_for('login'))
        try:
            with connection.cursor() as cursor:
                # Check if the username and password match a record in the users table
                cursor.execute("SELECT id FROM kayttajat.users WHERE username = %s", (userUsername))
                existing_user = cursor.fetchone()
                if existing_user:
                    return render_template('registeration.html', error='Käyttäjänimeä ei voi valita. Valitse toinen.')
                else:
                    cursor.execute("INSERT INTO kayttajat.users (username, password, role, email, user_logged_in) VALUES (%s, %s, %s, %s, FALSE)", (userUsername, userPassword, 'user', userEmail))
                    connection.commit()
                    return redirect(url_for('login'))
        except pymysql.Error as error:
            error_message = "Tietokannan yhteydessä tapahtui virhe: " + error
            return render_template('error.html', error_message=error_message, redirect_url=url_for('login'))
        finally:
            if connection:
                close_connection()
            error_message = None
    return render_template("registeration.html")
# Login page route
@app.route('/login',methods=['GET','POST'])
def login():
    global connection
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Get database parameters from .env
        dbhost = os.getenv('MYSQL_HOST')
        dbuser = os.getenv('MYSQL_USER')
        dbpassword = os.getenv('MYSQL_PASSWORD')
        database = os.getenv('MYSQL_DB')
        
        connection = connect_to_database(dbhost, dbuser, dbpassword, database)
        if not connection:
            error_message = "Yhteyttä tietokantaan ei ole luotu." + dbhost + " " + dbuser + " " + dbpassword + " " + database
            return render_template('error.html', error_message, redirect_url=url_for('login'))
        try:
            with connection.cursor() as cursor:
                # Check if the username and password match a record in the users table
                cursor.execute("SELECT * FROM kayttajat.users WHERE username = %s AND password = %s", (username, password))
                user = cursor.fetchone()
                # If the login is successful, store the user's information in the session
                if user:
                    # Creates session key
                    os.environ['SECRET_KEY'] = secrets.token_urlsafe(32)
                    app.config['SESSION_TYPE'] = 'memcached'
                    session_secret_key = os.getenv("SECRET_KEY")
                    app.config['SECRET_KEY'] = session_secret_key
                    session['user_id'] = user[0]  # Assuming the user_id is the first column in the 'users' table
                    session['username'] = user[1]  # Assuming the username is the second column in the 'users' table
                    session['user_role'] = user[3] # Assuming the user role is the fourth column in the users table
                    if session['user_role'] == 'user':
                        return redirect(url_for('welcome'))
                    elif session['user_role'] == 'admin':
                        return redirect(url_for('welcome'))
                    elif session['user_role'] == 'softuser':
                        return redirect(url_for('home'))
                    else:
                        return redirect(url_for('home'))
                # If login fails, redirect to registeration page
                else:
                    error_message = 'Käyttäjää ei löytynyt. Sinun täytyy rekisteröityä ensin.'
                    return render_template('error.html',error_message=error_message,redirect_url=url_for('register'))
        except pymysql.Error as error:
                error_message = "Tietokannan yhteydessä tapahtui virhe: " + error
                return render_template('error.html', error_message=error_message, redirect_url=url_for('login'))
        finally:
            if connection:
                close_connection()
            error_message = None
    return render_template("login.html")
# Logout route
@app.route('/logout')
def logout():
    session.clear()
    #session.pop('user_role', default=None)
    #session.pop('username', default=None)
    #session.pop('user_id',default=None)
# Profile page route
@app.route('/profile')
def profile():
    username = session.get('username')
    userid = session.get('user_id')
    user_role = session.get('user_role')
    if userid is not None:
        if user_role == 'user':
            print("user as user")
        elif user_role == 'admin':
            print("user as admin")
        else:
            print("unknown user role")
    else:
        return redirect(url_for('register'))
    return redirect(url_for('home'))
# Welcome page redirected from succesfull login and registeration
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')
# Admin page route
@app.route('/admin')
def admin():
    return render_template("login.html")