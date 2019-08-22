# Import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import models
from database_setup import Base, User, Genre, Music
import sys

# Connect to the database and create a session
# engine = create_engine('sqlite:///music.db')
engine = create_engine('postgresql://music:password@localhost/music')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create default user
admin = User(name='Adel Lassag',
             email='adetech.aadl@gmail.com',
             picture='https://avatars0.githubusercontent.com/u/'
                     '24706903?s=400&u=82e40d41ecef3f64738a2c37'
                     'bb6de6c4dfa03efe&v=4')
# save user to the database
try:
    session.add(admin)
    session.commit()
    print('The admin ' + admin.name + ' added to the database')
except exceptions.SQLAlchemyError:
    sys.exit('Encountered general SQLAlchemyError!')

# Create some dummy data objcets
genres = [

    {
        'name': 'Flamenco',
        'image': 'https://image.freepik.com/free-photo/'
                 'close-up-man-playing-guitar_1139-363.jpg',
        'description': 'in its strictest sense, is a professionalized '
        ' art-form based on the various folkloric music traditions of '
        'southern Spain in the autonomous community of Andalusia',
        'user_id': 1
    },
    {
        'name': 'Jazz',
        'image': 'https://image.freepik.com/free-photo/'
                 'man-plays-saxophone_1304-5306.jpg',
        'description': 'is a music genre that originated in the '
        'African-American communities of New Orleans, United States. '
        'It originated in the late 19th and early 20th centuries, '
        'and developed from roots in blues and ragtime. Jazz is seen '
        'by many as "America\'s classical music".',
        'user_id': 1
    },
    {
        'name': 'New age',
        'image': '',
        'description': 'is a genre of music intended to create '
        'artistic inspiration, relaxation, and optimism. '
        'It is used by listeners for yoga, massage, meditation, '
        'reading as a method of stress management to bring '
        'about a state of ecstasyrather than trance, or to '
        'create a peaceful atmosphere in their home or other environments, '
        'and is associated with environmentalism and New Age spirituality.',
        'user_id': 1
    },
    {
        'name': 'Blues',
        'image': '',
        'description': 'is a music genre and musical '
        'form which was originated in the Deep South of '
        'the United States around the 1870s by African '
        'Americans from roots in African musical traditions, '
        'African-American work songs, and spirituals. Blues '
        'incorporated spirituals, work songs, field hollers, '
        'shouts, chants, and rhymed simple narrative ballads.',
        'user_id': 1
    },
    {
        'name': 'Rock',
        'image': 'https://image.freepik.com/free-photo/'
                 'musicians-stage-during-concert_1321-453.jpg',
        'description': 'is a broad genre of popular music '
        'that originated as "rock and roll" in the United '
        'States in the early 1950s, and developed into a '
        'range of different styles in the 1960s and later, '
        'particularly in the United States and the United '
        'Kingdom. It has its roots in 1940s and 1950s rock '
        'and roll, a style which drew heavily from the '
        'genres of blues, rhythm and blues, and from '
        'country music.',
        'user_id': 1
    }
]

music_items = [
    {
        'title': 'Pharaon',
        'artist': 'Gipsy Kings',
        'image': 'https://upload.wikimedia.org/'
                 'wikipedia/en/3/36/Album_allegria.jpg',
        'video': '2nA11JEV3vA',
        'description': 'The Gipsy Kings are a group of flamenco, '
        'salsa and pop musicians from Arles and Montpellier in the '
        'south of France, who perform in Andalusian Spanish. Although group '
        'members were born in France, their parents were mostly gitanos, '
        'who fled Catalonia during the 1930s Spanish Civil War.',
        'genre_id': 1,
        'user_id': 1
    },
    {
        'title': 'Olvidado',
        'artist': 'Gipsy Kings',
        'image': 'https://covers4.hosting-media.net/'
                 'jpgr295/u3610152499057.jpg',
        'video': 'n0231oVGqj8',
        'description': 'The Gipsy Kings are a group of flamenco, '
        'salsa and pop musicians from Arles and Montpellier in the '
        'south of France, who perform in Andalusian Spanish. Although group '
        'members were born in France, their parents were mostly gitanos, '
        'who fled Catalonia during the 1930s Spanish Civil War.',
        'genre_id': 1,
        'user_id': 1
    },
    {
        'title': 'Take Five',
        'artist': 'Dave Brubeck',
        'image': 'https://images-na.ssl-images-amazon.com/'
                 'images/I/41D44VNMA2L.jpg',
        'video': 'vmDDOFXSgAs',
        'description': '"Take Five" is a jazz standard composed by '
        'Paul Desmond and originally recorded by the Dave Brubeck '
        'Quartet for their 1959 album Time Out. Made at Columbia '
        'Records 30th Street Studio in New York City on July 1, 1959, '
        'fully two years later it became an unlikely hit[a] and the '
        'biggest-selling jazz single ever. Revived since in numerous '
        'movie and television soundtracks, the piece still receives '
        'significant radio airplay.',
        'genre_id': 2,
        'user_id': 1
    },
    {
        'title': 'Prelude and Nostalgia',
        'artist': 'Yanni',
        'image': 'https://i1.sndcdn.com/'
                 'artworks-000054711527-k9rjt6-t300x300.jpg',
        'video': 'tKVzm0SBYtQ',
        'description': 'The Concert Event is the fourth live album by Yanni. '
        'It was recorded live at the Mandalay Bay Events Center, Las Vegas '
        'on November 6, 2004, and released in August 2006 as a CD and '
        'concert film on DVD. The album peaked at No. 1 on Billboard\'s '
        '"Top New Age Albums" chart; No. 6 on the "Top Independent Albums" '
        'chart; No. 84 on the "Billboard 200" chart; and at No. 84 on the '
        '"Top Internet Albums" chart, during the same year.',
        'genre_id': 3,
        'user_id': 1
    },
    {
        'title': 'Tender surrender',
        'artist': 'Steve Vai',
        'image': 'https://is1-ssl.mzstatic.com/image/thumb/Video128/v4'
                 '/e9/c2/bf/e9c2bf8c-50d3-42fb-a5b3-36a8a25510b9/dj.'
                 'zaqliojr.jpg/735x414mv.jpg',
        'video': 'Yw74sDWPH7U',
        'description': 'Steve Vai performs "Tender Surrender" from '
        'the DVD "Alien Love Secrets" featuring full-length performance '
        'videos of every song from the "Alien Love Secrets" EP.',
        'genre_id': 5,
        'user_id': 1
    },
    {
        'title': 'Always With Me, Always With You',
        'artist': 'Joe Satriani',
        'image': 'https://media2.fdncms.com/clevescene/imager/'
                 'joe-satriani-playing-at-the-lakewood-civic-auditorium/'
                 'u/inlineslideshow/3660629/a-1.jpg',
        'video': 'VI57QHL6ge0',
        'description': 'Surfing with the Alien is the second '
        'studio album by American rock guitarist Joe Satriani. '
        'It was released on October 15, 1987, by Relativity Records. '
        'The album is one of Satriani\'s most successful to date and '
        'helped establish his reputation as a respected rock guitarist.',
        'genre_id': 5,
        'user_id': 1
    }
]

# Save created genres into database
for i in genres:
    genre = Genre(
        name=i['name'],
        description=i['description'],
        image=i['image'],
        user_id=i['user_id']
    )
    try:
        session.add(genre)
        session.commit()
        print('Genre:' + genre.name + ' added to the database')
    except exceptions.SQLAlchemyError:
        sys.exit('Encountered general SQLAlchemyError!')

# Save created music items into database
for i in music_items:
    music = Music(
        title=i['title'],
        artist=i['artist'],
        image=i['image'],
        video=i['video'],
        description=i['description'],
        genre_id=i['genre_id'],
        user_id=i['user_id']
    )
    
    session.add(music)
    session.commit()
    print('Music:' + music.title + ' added to the database')
