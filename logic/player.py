import random
from state import state

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02}"

def get_duration(media_player):
    length = media_player.get_length()
    if length <= 0:
        return 0
    return length / 1000

def get_current_time(media_player):
    ms = media_player.get_time()
    if ms < 0:
        return 0
    return ms / 1000

def get_songs_duration(instance, media_player, path):
    try:
        media = instance.media_new(path)
        media.parse()
        duration = media.get_duration() / 1000
        if duration > 0:
            return format_time(duration)
    except:
        pass
    return "0:00"

def generate_shuffle_queue():
    state["shuffle_queue"] = list(range(len(state["playlist"])))
    random.shuffle(state["shuffle_queue"])
    if state["current_song"] in state["shuffle_queue"]:
        state["shuffle_queue"].remove(state["current_song"])
    state["shuffle_index"] = 0

def next_song(media_player, instance, play_selected, play_from_url):
    if state["loop"]:
        if state["is_stream"]:
            play_from_url(state["current_url"], "")
        else:
            play_selected(state["playlist"][state["current_song"]])
        return

    if state["is_stream"] or not state["playlist"]:
        return

    state["history"].append(state["current_song"])

    if state["shuffle"]:
        if not state["shuffle_queue"] or state["shuffle_index"] >= len(state["shuffle_queue"]):
            generate_shuffle_queue()
        new_index = state["shuffle_queue"][state["shuffle_index"]]
        state["shuffle_index"] += 1
    else:
        new_index = (state["current_song"] + 1) % len(state["playlist"])

    play_selected(state["playlist"][new_index])

def prev_song(media_player, instance, play_selected, play_from_url):
    if state["loop"]:
        if state["is_stream"]:
            play_from_url(state["current_url"], "")
        else:
            play_selected(state["playlist"][state["current_song"]])
        return

    if not state["playlist"]:
        return

    if state["history"]:
        state["current_song"] = state["history"].pop()
    else:
        state["current_song"] = (state["current_song"] - 1) % len(state["playlist"])

    play_selected(state["playlist"][state["current_song"]])