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
        'image': 'https://image.freepik.com/free-photo/close-up-man-playing-guitar_1139-363.jpg',
        'description': '''in its strictest sense, is a professionalized art-form based 
        on the various folkloric music traditions of southern Spain in the autonomous 
        community of Andalusia. In a wider sense, the term refers to a variety of 
        Spanish musical styles developed as early as the 19th century.'''
    },
    {
        'name': 'Jazz',
        'image': 'https://image.freepik.com/free-photo/man-plays-saxophone_1304-5306.jpg',
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
    },
    {
        'name': 'New age',
        'image': 'https://cdns-images.dzcdn.net/images/cover/e88a28b6bfad2cbfea3c3e41ecc5ace3/500x500.jpg',
        'description': '''is a genre of music intended to create artistic inspiration, 
        relaxation, and optimism. It is used by listeners for yoga, massage, meditation, 
        reading as a method of stress management to bring about a state of ecstasy 
        rather than trance, or to create a peaceful atmosphere in their home or other 
        environments, and is associated with environmentalism and New Age spirituality.'''
    }
]

music_items = [
    {
        'title': 'Pharaon',
        'artist': 'Gipsy Kings',
        'image': 'https://upload.wikimedia.org/wikipedia/en/3/36/Album_allegria.jpg',
        'video': '2nA11JEV3vA',
        'description': '''The Gipsy Kings are a group of flamenco, salsa and pop musicians 
        from Arles and Montpellier in the south of France, who perform in Andalusian Spanish. 
        Although group members were born in France, their parents were mostly gitanos, 
        Spanish gypsies who fled Catalonia during the 1930s Spanish Civil War.''',
        'genre_id': 1
    },
    {
        'title': 'Olvidado',
        'artist': 'Gipsy Kings',
        'image': 'https://covers4.hosting-media.net/jpgr295/u3610152499057.jpg',
        'video': 'n0231oVGqj8',
        'description': '''The Gipsy Kings are a group of flamenco, salsa and pop musicians 
        from Arles and Montpellier in the south of France, who perform in Andalusian Spanish. 
        Although group members were born in France, their parents were mostly gitanos, 
        Spanish gypsies who fled Catalonia during the 1930s Spanish Civil War.''',
        'genre_id': 1
    },
    {
        'title': 'Take Five',
        'artist': 'Dave Brubeck',
        'image': 'https://images-na.ssl-images-amazon.com/images/I/41D44VNMA2L.jpg',
        'video': 'vmDDOFXSgAs',
        'description': '''"Take Five" is a jazz standard composed by Paul Desmond and 
        originally recorded by the Dave Brubeck Quartet for their 1959 album Time Out. 
        Made at Columbia Records' 30th Street Studio in New York City on July 1, 1959, 
        fully two years later it became an unlikely hit[a] and the biggest-selling jazz 
        single ever. Revived since in numerous movie and television soundtracks, 
        the piece still receives significant radio airplay.''',
        'genre_id': 2
    },
    {
        'title': 'Prelude and Nostalgia',
        'artist': 'Yanni',
        'image': 'https://i1.sndcdn.com/artworks-000054711527-k9rjt6-t300x300.jpg',
        'video': 'tKVzm0SBYtQ',
        'description': '''The Concert Event is the fourth live album by Yanni. 
        It was recorded live at the Mandalay Bay Events Center, Las Vegas on 
        November 6, 2004, and released in August 2006 as a CD and concert film on DVD. 
        The album peaked at No. 1 on Billboard's "Top New Age Albums" chart; No. 6 on the 
        "Top Independent Albums" chart; No. 84 on the "Billboard 200" chart; and at No. 
        84 on the "Top Internet Albums" chart, during the same year.''',
        'genre_id': 3
    }
]


for i in genres:
    genre = Genre(
        name=i['name'],
        description=i['description'],
        image=i['image']
    )
    try:
        session.add(genre)
        session.commit()
        print('Genre:' + genre.name + ' added to the database')
    except exceptions.SQLAlchemyError:
        sys.exit('Encountered general SQLAlchemyError!')
        
        
for i in music_items:
    music = Music(
        title=i['title'],
        artist=i['artist'],
        image=i['image'],
        video=i['video'],
        description=i['description'],
        genre_id=i['genre_id'],
    )
    try:
        session.add(music)
        session.commit()
        print('Music:' + music.title + ' added to the database')
    except exceptions.SQLAlchemyError:
        sys.exit('Encountered general SQLAlchemyError!')
