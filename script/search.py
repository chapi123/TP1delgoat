import yt_dlp

BLOCKED_WORDS = ["mix", "live", "cover", "playlist", "full album", "extended"]
BLOCKED_CHANNELS = ["mix", "various artists"]

def is_valid_title(title):
    title = title.lower()
    return not any(word in title for word in BLOCKED_WORDS)

def is_valid_channel(channel):
    if not channel:
        return True
    channel = channel.lower()
    return not any(word in channel for word in BLOCKED_CHANNELS)

def score_title(title):
    title = title.lower()
    score = 0

    if "official" in title:
        score += 3
    if "audio" in title:
        score += 2
    if "video" in title:
        score += 1

    return score

def search_youtube(query, max_results=8):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'cookiefile': 'cookies.txt'
    }

    query = f"{query} official audio"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)

    songs = []

    for r in results['entries']:
        title = r.get('title', '')
        channel = r.get('uploader', '')

        if not is_valid_title(title):
            continue
        if not is_valid_channel(channel):
            continue

        songs.append({
            "title": title,
            "url": f"https://www.youtube.com/watch?v={r['id']}",
            "score": score_title(title)
        })

    songs.sort(key=lambda x: x["score"], reverse=True)

    return songs