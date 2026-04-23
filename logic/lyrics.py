import requests

def get_lyrics(artist, title):
    try:
        url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
        res = requests.get(url)
        data = res.json()
        return data.get("lyrics", "No lyrics found.")
    except:
        return "Error getting lyrics"