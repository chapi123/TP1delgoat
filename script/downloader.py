import yt_dlp

def get_audio_url(url):
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url']  


def download_audio(url, output_path="assets/canciones"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
