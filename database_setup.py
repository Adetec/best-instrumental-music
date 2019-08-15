from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    image = Column(String(100))
    description = Column(String(2000))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'description': self.description,
            'user_id': self.user_id
        }


class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    artist = Column(String(100), nullable=False)
    image = Column(String(100))
    video = Column(String(100))
    description = Column(String(2000))

    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'image': self.image,
            'genre_id': self.genre_id,
            'user_id': self.user_id
        }

        

engine = create_engine('sqlite:///music.db')
Base.metadata.create_all(engine)
