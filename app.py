#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'All instrumental music must be shown here!'


@app.route('/genre/<int:id>')
def genre(id):
    return 'All instrumental music with genre: <b>'+ str(id) +'</b> must be shown here!'


@app.route('/genre/<int:id>/music/<int:mid>')
def music(id, mid):
    return 'music: <b>'+ str(mid) +'</b> with genre: <b>'+ str(id) +'</b> must be shown here!'


@app.route('/genre/add')
def add_genre():
    return 'New genre will be added here!'


@app.route('/genre/<int:id>/update')
def update_genre(id):
    return 'This genre: <b>'+ str(id) +'</b> will be updated here!'


@app.route('/music/add')
def add_music():
    return 'New music will be added here!'

@app.route('/music/<int:id>/update')
def update_music(id):
    return 'This music: <b>'+ str(id) +'</b> will be updated here!'



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)