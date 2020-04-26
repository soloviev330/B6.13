import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Error(Exception):
    pass


class AlreadyExists(Error):
    pass


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

# engine = sa.create_engine(DB_PATH)
# Sessions = sessionmaker(engine)
# session = Sessions()

def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums



def save_album(year, artist, genre, album):
    session = connect_db()

    album_list = session.query(Album).filter(Album.album == album).first()

    if album_list is None:
        print("Дубликатов не обнаружено")
        new_album = Album(
            year = year,
            artist = artist,
            genre = genre,
            album = album
        )
        # добавляем нового пользователя в сессию
        session.add(new_album)
        # сохраняем все изменения, накопленные в сессии
        session.commit()
    else:

        raise AlreadyExists(Error)
    return new_album

# print(find(Beatles))

# albums = session.query(Album).all()

# for album in albums:
#         print(album.year, album.artist, album.genre, album.album)

