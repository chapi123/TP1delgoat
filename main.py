import customtkinter as ctk
import tkinter as tk  
from PIL import ImageTk, Image
from tkinter import font
import os
import random
from mutagen.mp3 import MP3
import yt_dlp
import vlc
import requests
import re
from io import BytesIO
from script.search import search_youtube
from script.downloader import get_audio_url, download_audio
from script.spotiapi import get_spotify_metadata
from script.utils import clean_title, parse_artist_title

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
overlay.bind("<Button-1>", lambda e: hide_modal())
modal.bind("<Button-1>", lambda e: "break")

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

playing = False
shuffle = False
loop = False
playlist = []
current_song = 0
history = []
last_value = 30
dragging = False
ended_handled = False
shuffle_queue = []
shuffle_index = 0
seeking = False
is_stream = False
current_url = None

def show_metadata(query):
    clear_metadata_frame()

    data = get_spotify_metadata(query)

    if not data:
        label = ctk.CTkLabel(metadata_frame, text="No metadata found", text_color="#FFFFFF", font=("Montserrat", 16))
        label.pack(pady=20)
        return

    title = ctk.CTkLabel(
        metadata_frame,
        text=data["title"],
        font=("Montserrat", 16, "bold"),
        text_color="#FFFFFF",
        wraplength=250
    )
    title.pack(pady=(20, 5))

    artist = ctk.CTkLabel(
        metadata_frame,
        text=data["artist"],
        font=("Montserrat", 12),
        text_color="#aaaaaa"
    )
    artist.pack()

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

    btn_volume = ctk.CTkButton( 
    metadata_frame,
    text="",
    image=download_icon,
    width=5,
    height=5,
    fg_color="#121212",      
    hover_color="#121212",   
    border_width=0,     
    command=lambda: show_download_modal(current_url, query)
    )
    btn_volume.pack(pady=10)

def show_download_modal(song_url, song_title):
    overlay.lift()  

    for widget in modal.winfo_children():
        widget.destroy()

    search_var = tk.StringVar()

    entry = ctk.CTkEntry(modal, placeholder_text="Search playlist...", textvariable=search_var)
    entry.pack(fill="x", padx=10, pady=10)

    frame_list = ctk.CTkScrollableFrame(modal, fg_color="#181818")
    frame_list.pack(fill="both", expand=True, padx=10, pady=10)

def select_playlist(url, path):
        download_audio(url, output_path=path)
        hide_modal()

def hide_modal():
    overlay.lower()

def show_download_modal(song_url, song_title):
    overlay.lift()

    for widget in modal.winfo_children():
        widget.destroy()

    search_var = tk.StringVar()

    entry = ctk.CTkEntry(modal, placeholder_text="Search playlist...", textvariable=search_var)
    entry.pack(fill="x", padx=10, pady=10)

    frame_list = ctk.CTkScrollableFrame(modal, fg_color="#181818")
    frame_list.pack(fill="both", expand=True, padx=10, pady=10)

    def load_playlists(filter_text=""):
        for widget in frame_list.winfo_children():
            widget.destroy()

        for folder in os.listdir("playlists"):
            full_path = os.path.join("playlists", folder)

            if os.path.isdir(full_path) and filter_text.lower() in folder.lower():
                btn = ctk.CTkButton(
                    frame_list,
                    text=folder,
                    fg_color="#1a1a1a",
                    hover_color="#2a2a2a",
                    command=lambda p=full_path: select_playlist(song_url, p)
                )
                btn.pack(fill="x", pady=5)

    def on_search(*args):
        load_playlists(search_var.get())

    search_var.trace_add("write", on_search)

    load_playlists()

def get_audio_from_youtube(query):

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'format': 'bestaudio[ext=m4a]'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
        video = info['entries'][0]

    url = f"https://www.youtube.com/watch?v={video['id']}"

    ydl_opts = {
        'format': 'bestaudio[ext=webm]/bestaudio',
        'quiet': True,
        'outtmpl': 'temp.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    return file_path

def play_from_url(url, title):
    global playing, current_song, playlist, is_stream

    playlist = []
    current_song = 0
    is_stream = True

    stream_url = get_audio_url(url)
    if stream_url is None:
        print("Unable to get audio URL. The video may be unavailable or requires different access.")
        return
    
    media = instance.media_new(stream_url)
    media_player.set_media(media)
    media_player.play()

    playing = True
    btn_play.configure(image=pause_icon)
    progress.set(0)

    show_metadata(title)

def play_from_search(query):
    if not query.strip():
        return

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

def load_playlist () :
    global folder
    playlist_path = "playlists"
    
    if not os.path.exists(playlist_path):
        return
    
    for folder in os.listdir(playlist_path) :
        full_path = os.path.join(playlist_path,folder)
        
        if os.path.isdir(full_path) :
            btn = ctk.CTkButton(
                left_panel,
                text=folder,
                fg_color="#1a1a1a",
                hover_color="#2a2a2a",
                text_color="#FFFFFF",
                font=("Montserrat", 12),
                command=lambda path=full_path: open_playlist(path)
            )
            btn.pack(fill="x", padx="10", pady="5")

def open_playlist(path):
    global playlist, current_song, folder
    
    clear_right_panel()
    
    title_songs = ctk.CTkLabel(
        right_container,
        text=os.path.basename(path),
        font=("Montserrat", 18),
        text_color="#FFFFFF"
    )
    title_songs.pack(pady=10)

    playlist = []
    current_song = 0
    
    for file in os.listdir(path):
        if file.endswith(".mp3"):
            full_path = os.path.join(path, file)
            playlist.append(full_path)
            
            btn = ctk.CTkButton(
                right_container,
                text=file,
                fg_color="#1a1a1a",
                hover_color="#2a2a2a",
                anchor="w",
                command=lambda p=full_path: play_selected(p),
                font=("Montserrat", 12)
            )
            btn.pack(fill="x", padx=10, pady=3)

def play_selected(path):
    global current_song, playing, is_stream

    is_stream = False

    new_index = playlist.index(path)

    if playing and current_song != new_index:
        history.append(current_song)

    current_song = playlist.index(path)

    media = instance.media_new(path)
    media_player.set_media(media)
    media_player.play()

    progress.set(0)
    btn_play.configure(image=pause_icon)
    playing = True

    filename = os.path.splitext(os.path.basename(path))[0]
    cleaned = clean_title(filename)
    show_metadata(cleaned)

def get_duration():
    length = media_player.get_length()  
    if length <= 0:
        return 0
    return length / 1000

def get_current_time():
    ms = media_player.get_time()  
    if ms < 0:
        return 0
    return (ms / 1000) 

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02}"

def update_progress():
    global ended_handled

    state = media_player.get_state()

    if state in (vlc.State.Playing, vlc.State.Paused):

        current_time = get_current_time()
        duration = get_duration()

        if duration > 0:

            if not dragging:
                value = (current_time * 100) / duration
                progress.set(value)

            current_text = format_time(current_time)
            duration_text = format_time(duration)
            time_label.configure(text=f"{current_text} / {duration_text}")

    if state == vlc.State.Ended:

        if not ended_handled:
            ended_handled = True

            if loop:
                if is_stream:
                    media_player.stop()
                    media_player.play()
                else:
                    play_selected(playlist[current_song])
            else:
                if is_stream:
                    stop()
                else:
                    next_song()

    else:
        ended_handled = False

    root.after(200, update_progress)


def seek_song(value):
    global playing

    if not playing:
        return
    
    seeking = True

    duration = get_duration()
    new_time = (float(value) / 100) * duration
    media_player.set_time(int(new_time * 1000)) 

    if not playing:
        media_player.pause()

def reset_seeking():
    global seeking
    seeking = False

def set_dragging(state):
    global dragging
    dragging = state

def on_seek_release(event):
    global dragging
    dragging = False
    seek_song(progress.get())

def show_preview(value):
    if not playing:
        return

    duration = get_duration()
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
    global playing

    state = media_player.get_state()

    if state == vlc.State.Playing:
        media_player.pause()
        btn_play.configure(image=play_icon)
        playing = False
    else:
        media_player.play()
        btn_play.configure(image=pause_icon)
        playing = True

def generate_shuffle_queue():
    global shuffle_queue, shuffle_index

    shuffle_queue = list(range(len(playlist)))
    random.shuffle(shuffle_queue)

    if current_song in shuffle_queue:
        shuffle_queue.remove(current_song)

    shuffle_index = 0

def toggle_shuffle():
    global shuffle

    shuffle = not shuffle

    if shuffle:
        btn_shuffle.configure(image=shuffle2_icon)
        generate_shuffle_queue()
    else:
        btn_shuffle.configure(image=shuffle1_icon)

def toggle_loop():
    global loop
    
    loop = not loop
    
    if loop:
        btn_loop.configure(image=loop2_icon)
    else:
        btn_loop.configure(image=loop1_icon)

def stop():
    global playing

    media_player.stop()
    progress.set(0)

    time_label.configure(text="0:00 / 0:00")
    btn_play.configure(image=play_icon)
    playing = False

def toggle_mute():
    global last_value

    current_volume = media_player.audio_get_volume()

    if current_volume == 0:
        media_player.audio_set_volume(int(last_value))
        vol_level.set(last_value)
        update_volume(last_value)

    else:
        last_value = current_volume
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

def next_song():
    global current_song, shuffle_index

    if is_stream:
        return 

    if not playlist:
        return

    history.append(current_song)

    if shuffle:
        if not shuffle_queue or shuffle_index >= len(shuffle_queue):
            generate_shuffle_queue()

        new_index = shuffle_queue[shuffle_index]
        shuffle_index += 1

    else:
        new_index = (current_song + 1) % len(playlist)

    play_selected(playlist[new_index])

def prev_song():
    global current_song, playing
    
    if not playlist:
        return
    
    if history:
        current_song = history.pop()
    
    else:
        current_song = (current_song - 1) % len(playlist)

    media = instance.media_new(playlist[current_song])
    media_player.set_media(media)
    media_player.play()

    btn_play.configure(image=pause_icon)
    playing = True

def on_enter(e):
    btn_stop.configure(image=stop2_icon)

def on_leave(e):
    btn_stop.configure(image=stop1_icon)

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
    command=prev_song            
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

btn_foward = ctk.CTkButton(
    center_controls,
    text="",
    image=foward_icon,
    width=40,
    height=40,
    fg_color="#181818",      
    hover_color="#181818",   
    border_width=0,  
    command=next_song            
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
btn_stop.bind("<Enter>", on_enter)
btn_stop.bind("<Leave>", on_leave)

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
load_playlist()
root.mainloop()