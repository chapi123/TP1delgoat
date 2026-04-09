import customtkinter as ctk
import tkinter as tk  
import pygame
from PIL import ImageTk, Image 

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

title_playlists = ctk.CTkLabel(left_panel, text="Playlists", font=("Montserrat", 18))
title_playlists.pack(pady=10)

separator = ctk.CTkFrame(main, width=2, fg_color="#2a2a2a")
separator.pack(side="left", fill="y")

right_panel = ctk.CTkFrame(main, fg_color="#121212")
right_panel.pack(side="left", fill="both", expand=True)

title_current = ctk.CTkLabel(right_panel, text="Playlist actual", font=("Montserrat", 20))
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

def toggle_play():
    global playing
    
    playing = not playing
    
    if playing:
        btn_play.configure(image=pause_icon)
    else:
        btn_play.configure(image=play_icon)

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
    border_width=0               
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

root.mainloop()