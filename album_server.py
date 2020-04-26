from bottle import route
from bottle import run
from bottle import request
from bottle import HTTPError

import album


@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список {} альбомов {}<br>".format(len(album_names), artist)
        result += "<br>".join(album_names)
    return result


@route("/albums", method="POST")
def new_albums():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")



    print("checked")

    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Указан некорректный год альбома")


    try:
        new_album = album.save_album(year, artist, genre, album_name)
    except AssertionError as err:
        result = HTTPError(400, str(err))
    except album.AlreadyExists as err:
        result = HTTPError(409, "Альбом с таким названием уже существует")
    else:    
        print("New #{} album successfully saved".format(new_album.id))
        result = "Альбом #{} успешно сохранен".format(new_album.id)

    # album.save_album(year, artist, genre, album_name)

    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)