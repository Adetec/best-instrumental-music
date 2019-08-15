#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Genre, Music
from flask import session as login_session
import random, string, httplib2, json, requests

from google.oauth2 import id_token
from oauth2client.client import FlowExchangeError, flow_from_clientsecrets

app = Flask(__name__)


engine = create_engine('sqlite:///music.db?check_same_thread=False')
DBsession = sessionmaker(bind=engine)
session = DBsession()

# google client secret
g_credentials = json.loads(open('client_secret.json', 'r').read())['web']
CLIENT_ID = g_credentials['client_id']
CLIENT_SECRET = g_credentials['client_secret']
APP_NAME = g_credentials['project_id']
AUTH_URI = g_credentials['auth_uri']
TOKEN_URI = g_credentials['token_uri']
CERTS = g_credentials['auth_provider_x509_cert_url']
CLIENT_REDIRECT = g_credentials['redirect_uris'][0]
CLIENT_REDIRECT = '/%s' % (CLIENT_REDIRECT.split('/')[-1])







@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase +
                    string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', state=state, CLIENT_ID=CLIENT_ID, login_session=login_session)


@app.route('/logout')
def logout():
    access_token = None
    if 'access_token' in login_session:
        access_token = login_session['access_token']
    if access_token is None:
        print('Access Token is None')
        response = make_response(
                json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['user_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        flash("Successfully loged out")
        return redirect(url_for('index'))
    else:
        flash("FAILED to revoke token for given user")
        return redirect(url_for('index'))



@app.route('/gconnect', methods=['GET', 'POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        print(login_session['state'], request.args.get('state'))
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output = '<div class="center-align">'
    output += '<h1 class="white-text">Welcome, <span class="">'
    output += login_session['username']
    output += '</span>!</h1>'
    output += '<img class="circle responsive-img" src="'
    output += login_session['picture']
    output += ' "></div> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user



def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response



@app.route('/')
def index():
    genres = session.query(Genre).all()
    music = session.query(Music).all()
    count = len(music)
    for item in login_session:
        print(login_session.get(item))
    return render_template('genres.html', genres=genres, music_items=music, login_session=login_session)


@app.route('/genre/<int:id>')
def genre(id):
    genre = session.query(Genre).filter_by(id=id).one()
    creator = getUserInfo(genre.user_id)
    music = session.query(Music).all()
    print(creator.name + 'is thecreator')
    return render_template('genre.html', genre=genre, music_items=music, creator=creator, login_session=login_session)


@app.route('/genre/<int:gid>/music/<int:mid>')
def music(gid, mid):
    genre = session.query(Genre).filter_by(id=gid).one()
    playlist = session.query(Music).filter_by(genre_id=gid).all()
    music = session.query(Music).filter_by(id=mid).one()
    num_of_music = len(playlist)

    return render_template('music.html', genre=genre, music=music, playlist=playlist, num_of_music=num_of_music, login_session=login_session)


@app.route('/genre/add', methods=['GET', 'POST'])
def add_genre():
    if 'username' not in login_session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        genre= Genre(
            name=request.form['name'],
            image=request.form['image'],
            description=request.form['description'],
            user_id=login_session['user_id']
        )
        try:
            session.add(genre)
            session.commit()
            print('Genre:' + genre.name + ' added to the database')
            flash(genre.name + ' Has been added')
            return redirect(url_for('index'))
        except exceptions.SQLAlchemyError:
            sys.exit('Encountered general SQLAlchemyError!')
    else:
        return render_template('add-genre.html', login_session=login_session)


@app.route('/genre/<int:id>/update', methods=['GET', 'POST'])
def update_genre(id):
    genre = session.query(Genre).filter_by(id=id).one()
    if request.method == 'POST':
        genre.name = request.form['name']
        genre.image = request.form['image']
        genre.description = request.form['description']
        genre.user_id=login_session['user_id']
        try:
            session.add(genre)
            session.commit()
            print('Genre:' + genre.name + ' updated to the database')
            flash(genre.name + ' Has been updated')
            return redirect(url_for('index'))
        except exceptions.SQLAlchemyError:
            sys.exit('Encountered general SQLAlchemyError!')
    else:
        return render_template('update-genre.html', genre=genre, login_session=login_session)


@app.route('/genre/<int:id>/delete')
def delete_genre(id):
    genre = session.query(Genre).filter_by(id=id).one()
    try:
        if genre:
            print(genre.name + ' exist')
            music = session.query(Music).filter_by(genre_id=id).all()
            for item in music:
                session.delete(item)
        session.delete(genre)
        session.commit()
        flash(genre.name + ' Has been deleted')
    except exceptions.SQLAlchemyError:
        sys.exit('Encountered general SQLAlchemyError!')
        
    return redirect(url_for('index'))



@app.route('/music/add', methods=['GET', 'POST'])
def add_music():
    if 'username' not in login_session:
        return redirect(url_for('login'))

    genres = session.query(Genre).all()
    if request.method == 'POST':
        music= Music(
            title=request.form['title'],
            artist=request.form['artist'],
            image=request.form['image'],
            video=request.form['video'],
            genre_id=request.form.get('genre'),
            description=request.form['description'],
            user_id=login_session['user_id']
        )
        try:
            session.add(music)
            session.commit()
            print('Music:' + music.title + ' added to the database')
            flash(music.title + ' Has been added')
            return redirect(url_for('index'))
        except exceptions.SQLAlchemyError:
            sys.exit('Encountered general SQLAlchemyError!')
    else:
        return render_template('add-music.html', genres=genres, login_session=login_session)

@app.route('/music/<int:id>/update', methods=['GET', 'POST'])
def update_music(id):
    music = session.query(Music).filter_by(id=id).one()
    genres = session.query(Genre).all()
    if request.method == 'POST':
        music.title = request.form['title']
        music.image = request.form['image']
        music.video = request.form['video']
        music.description = request.form['description']
        music.genre_id = request.form['genre']
        music.user_id=login_session['user_id']
        try:
            session.add(music)
            session.commit()
            print('Music:' + music.title + ' updated to the database')
            flash(music.title + ' Has been updated')
            return redirect(url_for('index'))
        except exceptions.SQLAlchemyError:
            sys.exit('Encountered general SQLAlchemyError!')
    else:
        return render_template('update-music.html', music=music, login_session=login_session, genres=genres)


@app.route('/music/<int:id>/delete')
def delete_music(id):
    music = session.query(Music).filter_by(id=id).one()
    try:
        session.delete(music)
        session.commit()
        flash(music.title + ' Has been deleted')
    except exceptions.SQLAlchemyError:
        sys.exit('Encountered general SQLAlchemyError!')
    finally:
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0', port=5000)