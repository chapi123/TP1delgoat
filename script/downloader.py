import yt_dlp
import os
from yt_dlp.utils import DownloadError

COOKIES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cookies.txt")

def get_audio_url(url):
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'cookiefile' : COOKIES_PATH
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url']
    except DownloadError as e:
        print(f"Error extracting audio URL: {e}")
        return None  

def download_audio(url, output_path="assets/canciones"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
