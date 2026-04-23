import customtkinter as ctk
import tkinter as tk
import os
from state import state
from script.downloader import download_audio

def hide_modal(overlay):
    overlay.lower()

def create_playlist(overlay, modal, load_playlist_cb):
    overlay.lift()

    for widget in modal.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        modal,
        text="New Playlist",
        text_color="#FFFFFF",
        font=("Montserrat", 18)
    ).pack(pady=20)

    name_var = tk.StringVar()

    ctk.CTkEntry(
        modal,
        placeholder_text="Playlist's name",
        textvariable=name_var,
        corner_radius=12
    ).pack(fill="x", padx=20, pady=10)

    def create():
        name = name_var.get().strip()
        if not name:
            return
        path = os.path.join("playlists", name)
        if not os.path.exists(path):
            os.makedirs(path)
            load_playlist_cb()
        hide_modal(overlay)

    ctk.CTkButton(
        modal,
        text="Create",
        command=create,
        fg_color="#1DB954",
        hover_color="#1ed760"
    ).pack(pady=20)

def delete_playlist(overlay, modal, path, load_playlist_cb):
    overlay.lift()

    for widget in modal.winfo_children():
        widget.destroy()

    name = os.path.basename(path)

    ctk.CTkLabel(
        modal,
        text=f"Delete '{name}'?",
        text_color="#FFFFFF",
        font=("Montserrat", 18)
    ).pack(pady=30)

    ctk.CTkLabel(
        modal,
        text="This action cannot be undone",
        text_color="#aaaaaa",
        font=("Montserrat", 12)
    ).pack(pady=(0, 20))

    def confirm_delete():
        try:
            for file in os.listdir(path):
                os.remove(os.path.join(path, file))
            os.rmdir(path)
            load_playlist_cb()
        except Exception as e:
            print("Error deleting:", e)
        hide_modal(overlay)

    btn_frame = ctk.CTkFrame(modal, fg_color="#181818")
    btn_frame.pack(pady=20)

    ctk.CTkButton(
        btn_frame,
        text="Cancel",
        command=lambda: hide_modal(overlay),
        fg_color="#2a2a2a",
        hover_color="#3a3a3a"
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        btn_frame,
        text="Delete",
        command=confirm_delete,
        fg_color="#ff4444",
        hover_color="#ff6666"
    ).pack(side="left", padx=10)

def rename_playlist(overlay, modal, path, old_name, load_playlist_cb):
    overlay.lift()

    for widget in modal.winfo_children():
        widget.destroy()

    name_var = tk.StringVar(value=old_name)

    ctk.CTkLabel(
        modal,
        text="Edit Playlist",
        text_color="#FFFFFF",
        font=("Montserrat", 18)
    ).pack(pady=20)

    ctk.CTkEntry(
        modal,
        textvariable=name_var,
        font=("Montserrat", 12)
    ).pack(padx=20, pady=10)

    def save():
        new_name = name_var.get().strip()
        if not new_name:
            return
        new_path = os.path.join("playlists", new_name)
        try:
            os.rename(path, new_path)
            hide_modal(overlay)
            load_playlist_cb()
        except Exception as e:
            print("Rename error:", e)

    ctk.CTkButton(
        modal,
        text="Save",
        command=save,
        fg_color="#1DB954",
        hover_color="#1ed760",
        font=("Montserrat", 12)
    ).pack(pady=20)

def show_download_modal(overlay, modal, song_url, open_playlist_cb):
    overlay.lift()

    for widget in modal.winfo_children():
        widget.destroy()

    search_var = tk.StringVar()

    ctk.CTkEntry(
        modal,
        placeholder_text="search playlist...",
        textvariable=search_var,
        corner_radius=12,
        border_width=0,
        fg_color="#1e1e1e",
        text_color="#FFFFFF"
    ).pack(fill="x", padx=10, pady=10)

    frame_list = ctk.CTkScrollableFrame(modal, fg_color="#181818")
    frame_list.pack(fill="both", expand=True, padx=10, pady=10)

    def load_playlists(filter_text=""):
        for widget in frame_list.winfo_children():
            widget.destroy()
        for folder in os.listdir("playlists"):
            full_path = os.path.join("playlists", folder)
            if os.path.isdir(full_path) and filter_text.lower() in folder.lower():
                ctk.CTkButton(
                    frame_list,
                    text=folder,
                    fg_color="#1a1a1a",
                    hover_color="#2a2a2a",
                    command=lambda p=full_path: [
                        download_audio(song_url, output_path=p),
                        hide_modal(overlay)
                    ]
                ).pack(fill="x", pady=5)

    search_var.trace_add("write", lambda *a: load_playlists(search_var.get()))
    load_playlists()

def delete_song(overlay, modal, song_path, playlist_path, open_playlist_cb):
    overlay.lift()

    for widget in modal.winfo_children():
        widget.destroy()

    name = os.path.basename(song_path)

    ctk.CTkLabel(
        modal,
        text=f"Delete '{name}'?",
        text_color="#FFFFFF",
        font=("Montserrat", 18)
    ).pack(pady=30)

    ctk.CTkLabel(
        modal,
        text="This action cannot be undone",
        text_color="#aaaaaa",
        font=("Montserrat", 12)
    ).pack(pady=(0, 20))

    def confirm_delete():
        try:
            os.remove(song_path)
            if song_path in state["playlist"]:
                state["playlist"].remove(song_path)
            open_playlist_cb(playlist_path)
        except Exception as e:
            print("Error deleting song:", e)
        hide_modal(overlay)

    btn_frame = ctk.CTkFrame(modal, fg_color="#181818")
    btn_frame.pack(pady=20)

    ctk.CTkButton(
        btn_frame,
        text="Cancel",
        command=lambda: hide_modal(overlay),
        fg_color="#2a2a2a",
        hover_color="#3a3a3a"
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        btn_frame,
        text="Delete",
        command=confirm_delete,
        fg_color="#ff4444",
        hover_color="#ff6666"
    ).pack(side="left", padx=10)