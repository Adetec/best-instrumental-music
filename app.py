#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Music

app = Flask(__name__)

engine = create_engine('sqlite:///music.db?check_same_thread=False')
DBsession = sessionmaker(bind=engine)
session = DBsession()


@app.route('/')
def index():
    genres = session.query(Genre).all()
    music = session.query(Music).all()
    return render_template('genres.html', genres=genres, music_items=music)


@app.route('/genre/<int:id>')
def genre(id):
    genre = session.query(Genre).filter_by(id=id).one()
    music = session.query(Music).all()
    return render_template('genre.html', genre=genre, music_items=music)


@app.route('/genre/<int:gid>/music/<int:mid>')
def music(gid, mid):
    genre = session.query(Genre).filter_by(id=gid).one()
    similar_music = session.query(Music).filter_by(genre_id=gid).all()
    music = session.query(Music).filter_by(id=mid).one()
    return render_template('music.html', genre=genre, music=music, similar_music=similar_music)


@app.route('/genre/add', methods=['GET', 'POST'])
def add_genre():
    if request.method == 'POST':
        genre= Genre(
            name=request.form['name'],
            image=request.form['image'],
            description=request.form['description']
        )
        try:
            session.add(genre)
            session.commit()
            print('Genre:' + genre.name + ' added to the database')
            return redirect(url_for('index'))
        except exceptions.SQLAlchemyError:
            sys.exit('Encountered general SQLAlchemyError!')
    else:
        return render_template('add-genre.html')


@app.route('/genre/<int:id>/update', methods=['GET', 'POST'])
def update_genre(id):
    genre = session.query(Genre).filter_by(id=id).one()
    if request.method == 'POST':
        genre.name = request.form['name']
        genre.image = request.form['image']
        genre.description = request.form['description']
        try:
            session.add(genre)
            session.commit()
            print('Genre:' + genre.name + ' updated to the database')
            return redirect(url_for('index'))
        except exceptions.SQLAlchemyError:
            sys.exit('Encountered general SQLAlchemyError!')
    else:
        return render_template('update-genre.html', genre=genre)


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
    except exceptions.SQLAlchemyError:
        sys.exit('Encountered general SQLAlchemyError!')
            
    # session.add(genre)
    # session.commit()
    # print('Genre:' + genre.name + ' updated to the database')
    return redirect(url_for('index'))



@app.route('/music/add', methods=['GET', 'POST'])
def add_music():
    genres = session.query(Genre).all()
    if request.method == 'POST':
        music= Music(
            title=request.form['title'],
            artist=request.form['artist'],
            image=request.form['image'],
            video=request.form['video'],
            genre_id=request.form.get('genre'),
            description=request.form['description']
        )
        try:
            session.add(music)
            session.commit()
            print('Music:' + music.title + ' added to the database')
            return redirect(url_for('index'))
        except exceptions.SQLAlchemyError:
            sys.exit('Encountered general SQLAlchemyError!')
    else:
        return render_template('add-music.html', genres=genres)

@app.route('/music/<int:id>/update')
def update_music(id):
    return 'This music: <b>'+ str(id) +'</b> will be updated here!'


@app.route('/music/<int:id>/delete')
def delete_music(id):
    music = session.query(Music).filter_by(id=id).one()
    try:
        session.delete(music)
        session.commit()
    except exceptions.SQLAlchemyError:
        sys.exit('Encountered general SQLAlchemyError!')
    finally:
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)