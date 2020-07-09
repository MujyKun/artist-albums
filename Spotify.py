from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

load_dotenv()
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def get_albums_and_songs(artist_id, existing_albums):
    """Main Function - Returns all albums and songs from that artist_id excluding the existing albums."""
    try:
        full_albums = get_artist_albums(artist_id)  # list from api
        singles = get_artist_albums(artist_id, include_groups="single")  # list from api

        album_dict = reformat_albums(full_albums, singles)  # combined full_albums and singles
        if existing_albums is not None:
            album_dict = remove_already_existing(album_dict, existing_albums)  # removed any already existing
        return album_dict
    except Exception as e:
        print(e)
        return None


def get_artist_albums(artist_id, include_groups="album"):
    """Get the albums of an artist, include_groups should be 'album' or 'single'"""
    try:
        results = spotify.artist_albums(artist_id, album_type=include_groups, limit=20)
        return results['items']
    except Exception as e:
        print(e)
        return None


def get_album_songs(album_id):
    """Get the tracks in an album"""
    try:
        results = spotify.album_tracks(album_id, limit=50)
        return results['items']
    except Exception as e:
        print(e)
        return None


def reformat_albums(album_dict: list, single_dict: list):  # these are lists that have dicts inside them
    """Reformats the albums to combine the singles and albums as well as remove unnecessary information
    and add tracks to the albums."""

    def adjust_album(current_album_t):
        """Removes unnecessary fields and adds songs to album"""
        current_album_t.pop('available_markets')
        current_album_t.pop('album_group')
        current_album_id = current_album['id']
        current_album['songs'] = get_album_songs(current_album_id)
        for song in current_album['songs']:
            song.pop('available_markets')
            song.pop('artists')
        return current_album

    new_album_list = []
    for current_album in album_dict:
        new_album = adjust_album(current_album)
        new_album_list.append(new_album)
    for current_album in single_dict:
        new_album = adjust_album(current_album)
        new_album_list.append(new_album)
    return {"albums": new_album_list}


def remove_already_existing(albums, existing_albums):
    """Removes the already existing albums"""
    existing = []
    for existing_album in existing_albums:
        existing.append(str(existing_albums[existing_album]))
    all_albums = albums['albums']
    for album in all_albums:
        album_id = str(album['id'])
        if album_id in existing:
            all_albums.remove(album)
    return albums

