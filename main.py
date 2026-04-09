import customtkinter as ctk
import tkinter as tk  
import pygame
from PIL import ImageTk, Image
from tkinter import font
import os
import random

#pygame.mixer.init()

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

title_current = ctk.CTkLabel(right_panel, text="Playlist actual", font=("Montserrat", 20), text_color="#FFFFFF")
title_current.pack(pady=10)


player = ctk.CTkFrame(root, height=80, fg_color="#181818")
player.pack(side="bottom", fill="x")
controls = ctk.CTkFrame(player, fg_color="#181818")
controls.pack(expand=True)

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

playing = False
shuffle = False
loop = False
playlist = []
current_song = 0
history = []

def load_playlist () :
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
    global playlist, current_song
    
    clear_right_panel()
    
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
                command=lambda p=full_path: play_selected(p)
            )
            btn.pack(fill="x", padx=10, pady=3)
    
    if playlist:
        pygame.mixer.music.load(playlist[0])

def play_selected(path):
    global current_song, playing

    new_index = playlist.index(path)

    if playing and current_song != new_index:
        history.append(current_song)
    
    pygame.mixer.music.stop()
    current_song = playlist.index(path)
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

    btn_play.configure(image=pause_icon)
    playing = True

def clear_right_panel():
    for widget in right_panel.winfo_children():
        widget.destroy()

def toggle_play():
    global playing
    
    if not playlist :
        return   

    playing = not playing

    if playing:
        pygame.mixer.music.pause()
        btn_play.configure(image=pause_icon)
        playing = False

    else:
        pygame.mixer.music.unpause()
        btn_play.configure(image=play_icon)
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

def next_song():
    global current_song
    
    if not playlist:
        return
    
    if shuffle:
        import random
        new_index = random.randint(0, len(playlist) - 1)
    else:
        new_index = (current_song + 1) % len(playlist)
    
    play_selected(playlist[new_index])  
 
    

def prev_song():
    global current_song, playing
    
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


btn_shuffle = ctk.CTkButton(
    controls,
    text="",
    image=shuffle1_icon,
    width=5,
    height=5,
    fg_color="#181818",      
    hover_color="#181818",   
    border_width=0,  
    command=toggle_shuffle             
)
btn_shuffle.pack(side="left", padx= 10, pady=15)

btn_backward = ctk.CTkButton(
    controls,
    text="",
    image=backward_icon,
    width=40,
    height=40,
    fg_color="#181818",      
    hover_color="#181818",   
    border_width=0,
    command=prev_song            
)
btn_backward.pack(side="left", padx= 10, pady=15)

btn_play = ctk.CTkButton(
    controls,
    text="", 
    image=play_icon,
    width=50,
    height=50,
    corner_radius=25,
    fg_color="#1DB954",
    hover_color="#1ed760",
    command=toggle_play
)
btn_play.pack(side="left", padx= 10,pady=15)

btn_foward = ctk.CTkButton(
    controls,
    text="",
    image=foward_icon,
    width=40,
    height=40,
    fg_color="#181818",      
    hover_color="#181818",   
    border_width=0               
)
btn_foward.pack(side="left", padx= 10, pady=15)

btn_stop = ctk.CTkButton(
    controls,
    text="",
    image=stop1_icon,
    width=40,
    height=40,
    fg_color="#181818",      
    hover_color="#181818",   
    border_width=0, 
    command=stop         
)
btn_stop.pack(side="left", padx= 10, pady=15)
btn_stop.bind("<Enter>", on_enter)
btn_stop.bind("<Leave>", on_leave)

btn_loop = ctk.CTkButton(
    controls,
    text="",
    image=loop1_icon,
    width=40,
    height=40,
    fg_color="#181818",      
    hover_color="#181818",   
    border_width=0,    
    command=toggle_loop           
)
btn_loop.pack(side="left", padx= 10, pady=15)

load_playlist()

root.mainloop()