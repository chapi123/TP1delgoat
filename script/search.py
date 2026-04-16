import yt_dlp

def search_youtube(query, max_results=5):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)

    songs = []
    for r in results['entries']:
        songs.append({
            "title": r['title'],
            "url": f"https://www.youtube.com/watch?v={r['id']}"
        })

    return songs