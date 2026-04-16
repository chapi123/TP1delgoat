import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "c0e508362f62467680c103d7e91464c3"
CLIENT_SECRET = "c7bbd17298c74d72a592ad89a81ed568"

auth_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

sp = spotipy.Spotify(auth_manager=auth_manager)


def get_spotify_metadata(query):
    results = sp.search(q=query, limit=1, type='track')

    if not results['tracks']['items']:
        return None

    track = results['tracks']['items'][0]

    return {
        "title": track['name'],
        "artist": track['artists'][0]['name'],
        "album": track['album']['name'],
        "thumbnail": track['album']['images'][0]['url']
    }