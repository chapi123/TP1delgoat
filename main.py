import customtkinter as ctk
import tkinter as tk  
import pygame
from PIL import ImageTk, Image
from tkinter import font
import os
import random
from mutagen.mp3 import MP3

pygame.mixer.init()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("spotify prime")
root.configure(fg_color="#121212")

root.iconbitmap("assets/icon.ico")
root.geometry("1000x500")

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

title_current = ctk.CTkLabel(right_panel, text="Current Playlist", font=("Montserrat", 20), text_color="#FFFFFF")
title_current.pack(pady=10)

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

playing = False
shuffle = False
loop = False
playlist = []
current_song = 0
history = []
last_value = 30
dragging = False
start_offset = 0

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
    
    title_songs = ctk.CTkLabel(right_panel, text=folder, font=("Montserrat", 18), text_color="#FFFFFF")
    title_songs.pack(pady=10)

    playlist = []
    current_song = 0
    
    for file in os.listdir(path):
        if file.endswith(".mp3"):
            full_path = os.path.join(path, file)
            playlist.append(full_path)
            
            btn = ctk.CTkButton(
                right_panel,
                text=file,
                fg_color="#1a1a1a",
                hover_color="#2a2a2a",
                anchor="w",
                command=lambda p=full_path: play_selected(p),
                font=("Montserrat", 12)
            )
            btn.pack(fill="x", padx=10, pady=3)
    
    if playlist:
        pygame.mixer.music.load(playlist[0])

def play_selected(path):
    global current_song, playing, start_offset
    
    start_offset= 0

    new_index = playlist.index(path)

    if playing and current_song != new_index:
        history.append(current_song)
    
    pygame.mixer.music.stop()
    current_song = playlist.index(path)
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    progress.set(0)

    btn_play.configure(image=pause_icon)
    playing = True

def get_duration(path) :
    audio = MP3(path)
    return audio.info.length

def get_current_time ():
    return (pygame.mixer.music.get_pos() / 1000)+ start_offset

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02}"

def update_progress():
    if playlist and current_song < len(playlist) and playing:

        current_time = get_current_time()

        if current_time >= 0 and not dragging: 
            duration = get_duration(playlist[current_song])
            current_text = format_time(current_time)
            duration_text = format_time(duration)

            if duration > 0:
                value = (current_time * 100) / duration
                progress.set(value)
                time_label.configure(text=f"{current_text} / {duration_text}")

    root.after(500, update_progress)

def seek_song (value) :
    global playing

    if not playlist:
        return
    
    duration = get_duration(playlist[current_song])

    new_time = (float(value)/100) * duration

    start_offset = new_time

    pygame.mixer.music.stop()
    pygame.mixer.music.load(playlist[current_song])
    pygame.mixer.music.play(start=new_time)

    if not playing :
        pygame.mixer.music.pause()

def set_dragging(state):
    global dragging
    dragging = state

def clear_right_panel():
    for widget in right_panel.winfo_children():
        widget.destroy()

def toggle_play():
    global playing

    if not playlist:
        return   

    if playing:
        pygame.mixer.music.pause()
        btn_play.configure(image=play_icon)
        playing = False
    else:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.unpause()

        btn_play.configure(image=pause_icon)
        playing = True

def toggle_shuffle():
    global shuffle
    
    shuffle = not shuffle
    
    if shuffle:
        btn_shuffle.configure(image=shuffle2_icon)
    else:
        btn_shuffle.configure(image=shuffle1_icon)

def toggle_loop():
    global loop
    
    loop = not loop
    
    if loop:
        btn_loop.configure(image=loop2_icon)
    else:
        btn_loop.configure(image=loop1_icon)

def stop() :
    global playing

    pygame.mixer.music.stop()
    btn_play.configure(image=play_icon)
    playing = False

def toggle_mute():
    global last_value

    current_volume = pygame.mixer.music.get_volume() * 100

    if current_volume == 0:
        pygame.mixer.music.set_volume(last_value / 100)
        vol_level.set(last_value)
        update_volume(last_value)
    else:
        last_value = current_volume
        pygame.mixer.music.set_volume(0)
        vol_level.set(0)
        update_volume(0)

def update_volume(value):
    volume = float(value) / 100
    pygame.mixer.music.set_volume(volume)

    if value == 0:
        btn_volume.configure(image=volume1_icon)
    elif value <= 50:
        btn_volume.configure(image=volume2_icon)
    else:
        btn_volume.configure(image=volume3_icon)

def next_song():
    global current_song, start_offset
    start_offset = 0
    
    if not playlist:
        return
    
    if shuffle:
        import random
        new_index = random.randint(0, len(playlist) - 1)
    else:
        new_index = (current_song + 1) % len(playlist)
    
    play_selected(playlist[new_index])  

def prev_song():
    global current_song, playing, start_offset
    start_offset = 0
    
    if not history:
        pygame.mixer.music.stop()
        btn_play.configure(image=play_icon)
        playing = False
        return
    
    current_song = history.pop()
    
    pygame.mixer.music.stop()
    pygame.mixer.music.load(playlist[current_song])
    pygame.mixer.music.play()
    
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
    command=lambda value: seek_song(value),
)
progress.pack(side="left", fill="x", expand=True)
progress.set(0)
progress.bind("<Button-1>", lambda e: set_dragging(True))
progress.bind("<ButtonRelease-1>", lambda e: set_dragging(False))

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

update_progress()
load_playlist()
root.mainloop()