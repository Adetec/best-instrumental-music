from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Music
import sys

engine = create_engine('sqlite:///music.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

genres = [

    {
        'name': 'Flamenco',
        'description': '''in its strictest sense, is a professionalized art-form based 
        on the various folkloric music traditions of southern Spain in the autonomous 
        community of Andalusia. In a wider sense, the term refers to a variety of 
        Spanish musical styles developed as early as the 19th century.'''
    },
    {
        'name': 'Jazz',
        'description': '''is a music genre that originated in the African-American communities 
        of New Orleans, United States. It originated in the late 19th and early 20th centuries, 
        and developed from roots in blues and ragtime. Jazz is seen by many as "America's classical music". 
        Since the 1920s Jazz Age, jazz has become recognized as a major form of musical expression. 
        It then emerged in the form of independent traditional and popular musical styles, 
        all linked by the common bonds of African-American and European-American musical parentage 
        with a performance orientation. Jazz is characterized by swing and blue notes, 
        call and response vocals, polyrhythms and improvisation. Jazz has roots in West African 
        cultural and musical expression, and in African-American music traditions including blues 
        and ragtime, as well as European military band music. Intellectuals around the world 
        have hailed jazz as "one of America's original art forms".'''
    }
]


for i in genres:
    genre = Genre(name=i['name'], description=i['description'])
    try:
        session.add(genre)
        session.commit()
        print(genre.name + ' added to the database')
    except exceptions.SQLAlchemyError:
        sys.exit('Encountered general SQLAlchemyError!')


