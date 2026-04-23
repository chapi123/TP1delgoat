import customtkinter as ctk
import tkinter as tk  
from PIL import ImageTk, Image
import os
import vlc
import requests
import yt_dlp
from io import BytesIO
from state import state
from script.search import search_youtube
from logic.player import (
    format_time, get_duration, get_current_time,
    generate_shuffle_queue, next_song, prev_song
)
from ui.modals_ui import (
    hide_modal, create_playlist,
    delete_playlist, rename_playlist,
    show_download_modal, delete_song
)
from ui.lyrics_ui import open_lyrics_view
from script.downloader import get_audio_url, download_audio
from script.spotiapi import get_spotify_metadata
from script.utils import clean_title
from ui.playlist_ui import open_playlist as _open_playlist
from ui.playlist_ui import load_playlist as _load_playlist

instance = vlc.Instance()
media_player = instance.media_player_new()
media_player.audio_set_volume(30)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("chapify")
root.configure(fg_color="#121212")

root.iconbitmap("assets/icon.ico")
root.geometry("1200x600")

main = ctk.CTkFrame(root, fg_color="#121212")
main.pack(fill="both", expand=True)

left_panel = ctk.CTkFrame(main, width=250, fg_color="#121212")
left_panel.pack(side="left", fill="y")
left_panel.pack_propagate(False)

title_playlists = ctk.CTkLabel(left_panel, text="Playlists", font=("Montserrat", 18), text_color="#FFFFFF")
title_playlists.pack(pady=10)

separator = ctk.CTkFrame(main, width=2, fg_color="#2a2a2a")
separator.pack(side="left", fill="y")

right_panel = ctk.CTkFrame(main, fg_color="#121212")
right_panel.pack(side="left", fill="both", expand=True)


player = ctk.CTkFrame(root, height=100, fg_color="#181818")
player.pack(side="bottom", fill="x")
player.pack_propagate(False)
controls = ctk.CTkFrame(player, fg_color="#181818", height=60)
controls.pack(fill="x", pady=(5, 0))
controls.pack_propagate(False)
left_controls = ctk.CTkFrame(controls, fg_color="#181818")
left_controls.pack(side="left", padx=10)
center_controls = ctk.CTkFrame(controls, fg_color="#181818")
center_controls.pack(side="left", expand=True)
right_controls = ctk.CTkFrame(controls, fg_color="#181818")
right_controls.pack(side="right", padx=10)
progress_frame = ctk.CTkFrame(player, fg_color="#181818",height=20)
progress_frame.pack(side="bottom", fill="x", padx=80, pady=(0, 8))
header = ctk.CTkFrame(right_panel, height=45, fg_color="#121212")
header.pack(fill="x")
header.pack_propagate(False)
search_frame = ctk.CTkFrame(header, fg_color="#1e1e1e", corner_radius=20)
search_frame.pack(pady=(10,0))
search_frame.configure(width=600)
search_frame.pack_propagate(False)
content_frame = ctk.CTkFrame(right_panel, fg_color="#121212")
content_frame.pack(fill="both", expand=True)
scroll = ctk.CTkScrollableFrame(content_frame, fg_color="#121212")
scroll.pack(side="left", fill="both", expand=True)
right_container = scroll
separator = ctk.CTkFrame(content_frame, width=2, fg_color="#2a2a2a")
separator.pack(side="left", fill="y")
metadata_frame = ctk.CTkFrame(content_frame, width=300, fg_color="#121212")
metadata_frame.pack(side="right", fill="y")
metadata_frame.pack_propagate(False)
title_current = ctk.CTkLabel(metadata_frame, text="Play something", font=("Montserrat", 18), text_color="#FFFFFF")
title_current.pack(pady=(170, 0))
title_current = ctk.CTkLabel(right_container, text="Current Playlist", font=("Montserrat", 18), text_color="#FFFFFF")
title_current.pack()
overlay = ctk.CTkFrame(root, fg_color="#000000")
overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
overlay.lower() 
modal = ctk.CTkFrame(overlay, width=400, height=500, fg_color="#181818", corner_radius=15)
modal.place(relx=0.5, rely=0.5, anchor="center")
modal.pack_propagate(False)
overlay.bind("<Button-1>", lambda e: hide_modal(overlay))
modal.bind("<Button-1>", lambda e: "break")
root.bind("<Escape>", lambda e: hide_modal(overlay))


play_img = Image.open("assets/play.png").resize((25, 25))
pause_img = Image.open("assets/pause.png").resize((25, 25))
backward_img = Image.open("assets/backward.png").resize((38, 38))
foward_img = Image.open("assets/foward.png").resize((38, 38))
shuffle1_img = Image.open("assets/shuffle1.png").resize((30, 30))
shuffle2_img = Image.open("assets/shuffle2.png").resize((30, 30))
stop1_img = Image.open("assets/stop1.png").resize((22, 22))
stop2_img = Image.open("assets/stop2.png").resize((22, 22))
loop1_img = Image.open("assets/loop1.png").resize((25, 32))
loop2_img = Image.open("assets/loop2.png").resize((25, 32))
volume1_img = Image.open("assets/volume1.png").resize((25, 25))
volume2_img = Image.open("assets/volume2.png").resize((25, 25))
volume3_img = Image.open("assets/volume3.png").resize((25, 25))
search_img = Image.open("assets/search.png").resize((20, 20))
download_img = Image.open("assets/download.png").resize((30, 30))
trash1_img = Image.open("assets/trash1.png").resize((12,12))
trash2_img = Image.open("assets/trash2.png").resize((12,12))
edit1_img = Image.open("assets/edit1.png").resize((12,12))
edit2_img = Image.open("assets/edit2.png").resize((12,12))
lyrics1_img = Image.open("assets/lyrics1.png").resize((25,25))
lyrics2_img = Image.open("assets/lyrics2.png").resize((25,25))
                                                        
play_icon = ImageTk.PhotoImage(play_img)
pause_icon = ImageTk.PhotoImage(pause_img)
backward_icon = ImageTk.PhotoImage(backward_img)
foward_icon = ImageTk.PhotoImage(foward_img)
shuffle1_icon = ImageTk.PhotoImage(shuffle1_img)
shuffle2_icon = ImageTk.PhotoImage(shuffle2_img)
stop1_icon = ImageTk.PhotoImage(stop1_img)
stop2_icon = ImageTk.PhotoImage(stop2_img)
loop1_icon = ImageTk.PhotoImage(loop1_img)
loop2_icon = ImageTk.PhotoImage(loop2_img)
volume1_icon = ImageTk.PhotoImage(volume1_img)
volume2_icon = ImageTk.PhotoImage(volume2_img)
volume3_icon = ImageTk.PhotoImage(volume3_img)
search_icon = ImageTk.PhotoImage(search_img)
download_icon = ImageTk.PhotoImage(download_img)
trash1_icon = ImageTk.PhotoImage(trash1_img)
trash2_icon = ImageTk.PhotoImage(trash2_img)
edit1_icon = ImageTk.PhotoImage(edit1_img)
edit2_icon = ImageTk.PhotoImage(edit2_img)
lyrics1_icon = ImageTk.PhotoImage(lyrics1_img)
lyrics2_icon = ImageTk.PhotoImage(lyrics2_img)


icons = {
    "trash1": trash1_icon, "trash2": trash2_icon,
    "edit1":  edit1_icon,  "edit2":  edit2_icon,
}

modals = {
    "rename":          rename_playlist,
    "delete_playlist": delete_playlist,
    "delete_song":     delete_song,
}

def open_playlist(path):
    _open_playlist(path, right_container, scroll, content_frame,
                   state, instance, media_player, icons,
                   play_selected, overlay, modal, modals)

def load_playlist_ui():
    _load_playlist(left_panel, title_playlists, btn_add_playlist,
                   icons, open_playlist, overlay, modal, modals)

btn_add_playlist = ctk.CTkButton(
    left_panel,
    text="+ New Playlist",
    fg_color="#1DB954",
    hover_color="#1ed760",
    command=lambda: create_playlist(overlay, modal, load_playlist_ui)
)
btn_add_playlist.pack(pady=10, padx=10, fill="x")

def handle_space(event):
    if isinstance(event.widget, (tk.Entry, ctk.CTkEntry)):
        return

    toggle_play()

def show_metadata(query):
    clear_metadata_frame()

    data = get_spotify_metadata(query)

    if not data:
        label = ctk.CTkLabel(metadata_frame, text="No metadata found", text_color="#FFFFFF", font=("Montserrat", 16))
        label.pack(pady=20)
        return

    title_label = ctk.CTkLabel(
        metadata_frame,
        text=data["title"],
        font=("Montserrat", 16, "bold"),
        text_color="#FFFFFF",
        wraplength=250
    )
    title_label.pack(pady=(20, 5))

    artist_label = ctk.CTkLabel(
        metadata_frame,
        text=data["artist"],
        font=("Montserrat", 12),
        text_color="#aaaaaa"
    )
    artist_label.pack()

    album = ctk.CTkLabel(
        metadata_frame,
        text=data["album"],
        font=("Montserrat", 10),
        text_color="#777777"
    )
    album.pack(pady=(0, 10))

    try:
        response = requests.get(data["thumbnail"])
        img_data = Image.open(BytesIO(response.content)).resize((200, 200))
        img = ImageTk.PhotoImage(img_data)

        img_label = ctk.CTkLabel(metadata_frame, image=img, text="")
        img_label.image = img
        img_label.pack(pady=10)

    except:
        pass
    
    if state["is_stream"]:
        btn_download = ctk.CTkButton( 
        metadata_frame,
        text="",
        image=download_icon,
        width=5,
        height=5,
        fg_color="#121212",      
        hover_color="#121212",   
        border_width=0,     
        command=lambda: show_download_modal(overlay, modal, state["current_url"], open_playlist)
        )
        btn_download.pack(pady=10)
    
    btn_lyrics = ctk.CTkButton(
    metadata_frame,
    text="",
    image=lyrics2_icon,
    fg_color="#121212",      
    hover_color="#121212",  
    command=lambda: open_lyrics_view(data['artist'], data['title'], content_frame, scroll, clear_right_panel)
    )
    btn_lyrics.pack(pady=10)
    btn_lyrics.bind("<Enter>", lambda e, b=btn_lyrics: b.configure(image=lyrics1_icon))
    btn_lyrics.bind("<Leave>", lambda e, b=btn_lyrics: b.configure(image=lyrics2_icon))

    if state["lyrics_frame_active"] is not None and data:
        open_lyrics_view(data['artist'], data['title'], content_frame, scroll, clear_right_panel)

def play_from_url(url, title):
    state["current_url"] = url

    state["playlist"] = []
    state["current_song"] = 0
    state["is_stream"] = True

    stream_url = get_audio_url(url)
    if stream_url is None:
        print("Unable to get audio URL. The video may be unavailable or requires different access.")
        return
    
    media = instance.media_new(stream_url)
    media_player.set_media(media)
    media_player.play()

    state["playing"] = True
    btn_play.configure(image=pause_icon)
    progress.set(0)

    show_metadata(title)

def play_from_search(query):
    if not query.strip():
        return

    root.focus()

    results = search_youtube(query)  

    clear_right_panel()

    title_results = ctk.CTkLabel(
        right_container,
        text=f'Results: "{query}"',
        font=("Montserrat", 18),
        text_color="#FFFFFF"
    )
    title_results.pack(pady=10)

    for song in results:
        btn = ctk.CTkButton(
            right_container,
            text=song["title"],
            fg_color="#1a1a1a",
            hover_color="#2a2a2a",
            anchor="w",
            font=("Montserrat", 12),
            command=lambda s=song: play_from_url(s["url"], s["title"])
        )
        btn.pack(fill="x", padx=10, pady=3)

def play_selected(path):
    state["is_stream"] = False

    new_index = state["playlist"].index(path)

    if state["playing"] and state["current_song"] != new_index:
        state["history"].append(state["current_song"])

    state["current_song"] = state["playlist"].index(path)

    media = instance.media_new(path)
    media_player.set_media(media)
    media_player.play()

    progress.set(0)
    btn_play.configure(image=pause_icon)
    state["playing"] = True

    filename = os.path.splitext(os.path.basename(path))[0]
    cleaned = clean_title(filename)
    show_metadata(cleaned)

def update_progress():
    vlc_state = media_player.get_state()

    if vlc_state in (vlc.State.Playing, vlc.State.Paused):

        current_time = get_current_time(media_player)
        duration = get_duration(media_player)

        if duration > 0:

            if not state["dragging"]:
                value = (current_time * 100) / duration
                progress.set(value)

            current_text = format_time(current_time)
            duration_text = format_time(duration)
            time_label.configure(text=f"{current_text} / {duration_text}")

    if vlc_state == vlc.State.Ended:

        if not state["ended_handled"]:
            state["ended_handled"] = True

            if state["loop"]:
                if state["is_stream"]:
                    stream_url = get_audio_url(state["current_url"])
                    media = instance.media_new(stream_url)
                    media_player.set_media(media)
                    media_player.play()
                else:
                    play_selected(state["playlist"][state["current_song"]])
            else:
                if state["is_stream"]:
                    stop()
                else:
                    next_song(media_player, instance, play_selected, play_from_url)

    else:
        state["ended_handled"] = False

    root.after(200, update_progress)


def seek_song(value):
    if not state["playing"]:
        return
    
    state["seeking"] = True

    duration = get_duration(media_player)
    new_time = (float(value) / 100) * duration
    media_player.set_time(int(new_time * 1000)) 

    if not state["playing"]:
        media_player.pause()

def set_dragging(is_dragging):
    state["dragging"] = is_dragging

def on_seek_release(event):
    state["dragging"] = False
    seek_song(progress.get())

def show_preview(value):
    if not state["playing"]:
        return

    duration = get_duration(media_player)
    if duration <= 0:
        return

    new_time = (float(value) / 100) * duration

    current_text = format_time(new_time)
    duration_text = format_time(duration)

    time_label.configure(text=f"{current_text} / {duration_text}")

def clear_right_panel():
    for widget in right_container.winfo_children():
        widget.destroy()

def clear_metadata_frame():
    for widget in metadata_frame.winfo_children():
        widget.destroy()

def toggle_play():
    vlc_state = media_player.get_state()

    if vlc_state == vlc.State.Playing:
        media_player.pause()
        btn_play.configure(image=play_icon)
        state["playing"] = False
    else:
        media_player.play()
        btn_play.configure(image=pause_icon)
        state["playing"] = True

def toggle_shuffle():
    state["shuffle"] = not state["shuffle"]

    if state["shuffle"]:
        btn_shuffle.configure(image=shuffle2_icon)
        generate_shuffle_queue()
    else:
        btn_shuffle.configure(image=shuffle1_icon)

def toggle_loop():
    state["loop"] = not state["loop"]
    
    if state["loop"]:
        btn_loop.configure(image=loop2_icon)
    else:
        btn_loop.configure(image=loop1_icon)

def stop():
    media_player.stop()
    progress.set(0)

    time_label.configure(text="0:00 / 0:00")
    btn_play.configure(image=play_icon)
    state["playing"] = False

def toggle_mute():
    current_volume = media_player.audio_get_volume()

    if current_volume == 0:
        media_player.audio_set_volume(int(state["last_volume"]))
        vol_level.set(state["last_volume"])
        update_volume(state["last_volume"])

    else:
        state["last_volume"] = current_volume
        media_player.audio_set_volume(0)
        vol_level.set(0)
        update_volume(0)

def update_volume(value):
    media_player.audio_set_volume(int(float(value)))

    if float(value) == 0:
        btn_volume.configure(image=volume1_icon)
    elif float(value) <= 50:
        btn_volume.configure(image=volume2_icon)
    else:
        btn_volume.configure(image=volume3_icon)

progress = ctk.CTkSlider(
    progress_frame,
    from_=0,
    to=100,
    progress_color="#1DB954",
    button_color="#FFFFFF",
    button_hover_color="#cccccc",
    command=show_preview
)
progress.pack(side="left", fill="x", expand=True)
progress.set(0)
progress.bind("<Button-1>", lambda e: set_dragging(True))
progress.bind("<ButtonRelease-1>", on_seek_release)

time_label = ctk.CTkLabel(
    progress_frame,
    text="0:00 / 0:00",
    text_color="#FFFFFF",
    font=("Montserrat", 12),
)
time_label.pack(side="right", padx=10)

btn_volume = ctk.CTkButton( 
    left_controls,
    text="",
    image=volume2_icon,
    width=5,
    height=5,
    fg_color="#181818",      
    hover_color="#181818",   
    border_width=0,  
    command=toggle_mute             
)
btn_volume.pack(side="left", padx= (10, 0), pady=5)

vol_level = ctk.CTkSlider(
    left_controls,
    from_=0,
    to=100,
    progress_color="#1DB954",
    button_color="#FFFFFF",
    button_hover_color="#cccccc",
    command=lambda value: update_volume(value)
)
vol_level.pack(side="left", padx=(0, 10), pady=5)
vol_level.set(30)

btn_shuffle = ctk.CTkButton( 
    center_controls,
    text="",
    image=shuffle1_icon,
    width=5,
    height=5,
    fg_color="#181818",      
    hover_color="#181818",   
    border_width=0,  
    command=toggle_shuffle             
)
btn_shuffle.pack(side="left", padx= 10, pady=5)

btn_backward = ctk.CTkButton(
    center_controls,
    text="",
    image=backward_icon,
    width=40,
    height=40,
    fg_color="#181818",      
    hover_color="#181818",   
    border_width=0,
    command=lambda: prev_song(media_player, instance, play_selected, play_from_url)          
)
btn_backward.pack(side="left", padx= 10, pady=5)

btn_play = ctk.CTkButton(
    center_controls,
    text="", 
    image=play_icon,
    width=50,
    height=50,
    corner_radius=25,
    fg_color="#1DB954",
    hover_color="#1ed760",
    command=toggle_play
)
btn_play.pack(side="left", padx= 10,pady=5)
root.bind("<space>", handle_space)

btn_foward = ctk.CTkButton(
    center_controls,
    text="",
    image=foward_icon,
    width=40,
    height=40,
    fg_color="#181818",      
    hover_color="#181818",   
    border_width=0,  
    command=lambda: next_song(media_player, instance, play_selected, play_from_url)          
)
btn_foward.pack(side="left", padx= 10, pady=5)

btn_stop = ctk.CTkButton(
    center_controls,
    text="",
    image=stop1_icon,
    width=40,
    height=40,
    fg_color="#181818",      
    hover_color="#181818",   
    border_width=0, 
    command=stop         
)
btn_stop.pack(side="left", padx= 10, pady=5)
btn_stop.bind("<Enter>", lambda e, b=btn_stop: b.configure(image=stop2_icon))
btn_stop.bind("<Leave>", lambda e, b=btn_stop: b.configure(image=stop1_icon))

btn_loop = ctk.CTkButton(
    center_controls,
    text="",
    image=loop1_icon,
    width=40,
    height=40,
    fg_color="#181818",      
    hover_color="#181818",   
    border_width=0,    
    command=toggle_loop           
)
btn_loop.pack(side="left", padx= 10, pady=5)

search_entry = ctk.CTkEntry(
    search_frame,
    placeholder_text="looking for...?",
    border_width=0,
    fg_color="#1e1e1e",
    text_color="#FFFFFF"
)
search_entry.pack(side="left", fill="x", expand=True, padx=10)

search_btn = ctk.CTkButton(
    search_frame,
    text="",
    image=search_icon,
    width=30,
    fg_color="#1e1e1e",
    hover_color="#2a2a2a",
    command=lambda: play_from_search(search_entry.get())
)
search_btn.pack(side="right", padx=10)
search_entry.bind("<Return>", lambda e: play_from_search(search_entry.get()))

update_progress()
load_playlist_ui()
root.mainloop()