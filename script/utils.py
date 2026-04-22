import re

def clean_title(title):
    if not title:
        return ""

    title = re.sub(r"\(.*?\)", "", title)
    title = re.sub(r"\[.*?\]", "", title)

    garbage_patterns = [
        r"\bofficial\b",
        r"\bvideo\b",
        r"\baudio\b",
        r"\blyrics?\b",
        r"\blyric video\b",
        r"\bhd\b",
        r"\bhq\b",
        r"\b4k\b",
        r"\bvisualizer\b",
        r"\bprod\.?\b",
        r"\bexplicit\b"
    ]

    for pattern in garbage_patterns:
        title = re.sub(pattern, "", title, flags=re.IGNORECASE)

    title = re.sub(r"\b(feat|ft)\.?\s+[^-–|]+", "", title, flags=re.IGNORECASE)

    title = title.replace("_", " ")
    title = " ".join(title.split())

    return title.strip()


def parse_artist_title(title):
    title = clean_title(title)

    separators = [" - ", " – ", " | ", " • "]

    for sep in separators:
        if sep in title:
            artist, song = title.split(sep, 1)
            return artist.strip(), song.strip()

    return None, title