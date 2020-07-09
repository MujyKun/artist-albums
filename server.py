from flask import Flask, jsonify, request
import Spotify

app = Flask(__name__)

"""
EXPECTED JSON FORMAT FOR EXISTING ALBUMS
Key names do not matter.
{
    "album1": value,
    "album2": value,
    ...
}

ARTIST ID is taken through /artist/{artist-id}
"""


@app.route('', methods=['GET'])
def github():
    return 'https://github.com/MujyKun/artist-albums'


@app.route('/artist/<id>', methods=['GET'])
def query_records(id):
    existing_albums = request.get_json()
    send_back = Spotify.get_albums_and_songs(artist_id=id, existing_albums=existing_albums)
    if send_back is None:
        send_back = {'error': "Could not retrieve albums."}
    return jsonify(send_back)


app.run(port=5454)


