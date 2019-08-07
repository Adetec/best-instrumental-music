from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    description = Column(String(250))


class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    artist = Column(String(100), nullable=False)
    image = Column(String(100))
    description = Column(String(250))

    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)

    @property
    def serialize(self)
        return {
            'id' : self.id,
            'title' : self.title,
            'artist' : self.artist,
            'image' : self.image,
            'genre_id' : self.genre_id
        }
        

engine = create_engine('sqlite:///music.db')
Base.metadata.create_all(engine)
