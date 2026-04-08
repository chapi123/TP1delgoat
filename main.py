import customtkinter as ctk
import tkinter as tk  
from PIL import ImageTk, Image 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("spotify prime")
root.configure(fg_color="#121212")

root.iconbitmap("assets/icon.ico")
root.geometry("1000x500")


player = ctk.CTkFrame(root, height=80, fg_color="#181818")
player.pack(side="bottom", fill="x")
controls = ctk.CTkFrame(player, fg_color="#181818")
controls.pack(expand=True)

play_img = Image.open("assets/play.png").resize((25, 25))
pause_img = Image.open("assets/pause.png").resize((25, 25))
backward_img = Image.open("assets/backward.png").resize((38, 38))
foward_img = Image.open("assets/foward.png").resize((38, 38))

play_icon = ImageTk.PhotoImage(play_img)
pause_icon = ImageTk.PhotoImage(pause_img)
backward_icon = ImageTk.PhotoImage(backward_img)
foward_icon = ImageTk.PhotoImage(foward_img)

reproduciendo = False


def toggle_play():
    global reproduciendo
    
    reproduciendo = not reproduciendo
    
    if reproduciendo:
        btn_play.configure(image=pause_icon)
    else:
        btn_play.configure(image=play_icon)


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

root.mainloop()