import customtkinter as ctk
import tkinter as tk
import os
import shutil
from tkinter import filedialog
from state import state
from logic.player import get_songs_duration

def load_playlist(left_panel, title_playlists, btn_add_playlist, icons, open_playlist_cb, overlay, modal, modals):
    playlist_path = "playlists"

    if not os.path.exists(playlist_path):
        return

    for widget in left_panel.winfo_children():
        if widget not in (title_playlists, btn_add_playlist):
            widget.destroy()

    for folder in os.listdir(playlist_path):
        full_path = os.path.join(playlist_path, folder)

        if not os.path.isdir(full_path):
            continue

        row = ctk.CTkFrame(left_panel, fg_color="#121212")
        row.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            row,
            text=folder,
            fg_color="#1a1a1a",
            hover_color="#2a2a2a",
            anchor="w",
            command=lambda p=full_path: open_playlist_cb(p)
        ).pack(side="left", fill="x", expand=True)

        edit_btn = ctk.CTkButton(
            row,
            text="",
            image=icons["edit1"],
            width=30,
            fg_color="#1a1a1a",
            hover_color="#2a2a2a",
            command=lambda p=full_path, f=folder: modals["rename"](overlay, modal, p, f,
                lambda: load_playlist(left_panel, title_playlists, btn_add_playlist, icons, open_playlist_cb, overlay, modal, modals))
        )
        edit_btn.pack(side="left", padx=(4, 2))
        edit_btn.bind("<Enter>", lambda e, b=edit_btn: b.configure(image=icons["edit2"]))
        edit_btn.bind("<Leave>", lambda e, b=edit_btn: b.configure(image=icons["edit1"]))

        delete_btn = ctk.CTkButton(
            row,
            text="",
            image=icons["trash1"],
            width=30,
            fg_color="#1a1a1a",
            hover_color="#ff4444",
            command=lambda p=full_path: modals["delete_playlist"](overlay, modal, p,
                lambda: load_playlist(left_panel, title_playlists, btn_add_playlist, icons, open_playlist_cb, overlay, modal, modals))
        )
        delete_btn.pack(side="left", padx=2)
        delete_btn.bind("<Enter>", lambda e, b=delete_btn: b.configure(image=icons["trash2"]))
        delete_btn.bind("<Leave>", lambda e, b=delete_btn: b.configure(image=icons["trash1"]))


def open_playlist(path, right_container, scroll, content_frame, state_ref, instance, media_player, icons, play_selected_cb, overlay, modal, modals):
    if state_ref["lyrics_frame_active"] is not None:
        try:
            state_ref["lyrics_frame_active"].destroy()
        except:
            pass
        state_ref["lyrics_frame_active"] = None
        scroll.pack(side="left", fill="both", expand=True)

    for widget in right_container.winfo_children():
        widget.destroy()

    header_row = ctk.CTkFrame(right_container, fg_color="#121212")
    header_row.pack(fill="x", padx=10, pady=(10, 5))

    ctk.CTkLabel(
        header_row,
        text=os.path.basename(path),
        font=("Montserrat", 18),
        text_color="#FFFFFF"
    ).pack(side="left")

    search_local_frame = ctk.CTkFrame(header_row, fg_color="#1e1e1e", corner_radius=12, width=300, height=30)
    search_local_frame.pack(side="right")
    search_local_frame.pack_propagate(False)

    search_local_var = tk.StringVar()

    ctk.CTkEntry(
        search_local_frame,
        placeholder_text="filter songs...",
        textvariable=search_local_var,
        border_width=0,
        fg_color="#1e1e1e",
        text_color="#FFFFFF",
        font=("Montserrat", 12)
    ).pack(fill="x", expand=True, padx=10)

    def import_songs():
        files = filedialog.askopenfilenames(
            title="Select songs",
            filetypes=[("Audio files", "*.mp3 *.webm *.m4a *.wav *.flac *.ogg")]
        )
        for file in files:
            dest = os.path.join(path, os.path.basename(file))
            if not os.path.exists(dest):
                shutil.copy2(file, dest)
        open_playlist(path, right_container, scroll, content_frame, state_ref,
                      instance, media_player, icons, play_selected_cb, overlay, modal, modals)

    ctk.CTkButton(
        right_container,
        text="+ Import songs",
        fg_color="#1a1a1a",
        hover_color="#2a2a2a",
        anchor="w",
        font=("Montserrat", 12),
        command=import_songs
    ).pack(fill="x", padx=10, pady=(0, 8))

    songs_frame = ctk.CTkFrame(right_container, fg_color="#121212")
    songs_frame.pack(fill="both", expand=True)

    state_ref["playlist"] = []
    state_ref["current_song"] = 0

    all_songs = []
    for file in os.listdir(path):
        if file.endswith((".mp3", ".webm", ".m4a", ".wav", ".flac", ".ogg")):
            full_path = os.path.join(path, file)
            state_ref["playlist"].append(full_path)
            name = os.path.splitext(file)[0]
            duration = get_songs_duration(instance, media_player, full_path)
            all_songs.append((full_path, name, duration))

    def render_songs(filter_text=""):
        for widget in songs_frame.winfo_children():
            widget.destroy()

        for full_path, name, duration in all_songs:
            if filter_text.lower() not in name.lower():
                continue

            row = ctk.CTkFrame(songs_frame, fg_color="#121212")
            row.pack(fill="x", padx=10, pady=3)

            ctk.CTkButton(
                row,
                text=name,
                fg_color="#1a1a1a",
                hover_color="#2a2a2a",
                anchor="w",
                font=("Montserrat", 12),
                command=lambda p=full_path: play_selected_cb(p)
            ).pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(
                row,
                text=duration,
                text_color="#aaaaaa",
                font=("Montserrat", 11)
            ).pack(side="left", padx=10)

            delete_btn = ctk.CTkButton(
                row,
                text="",
                image=icons["trash1"],
                width=30,
                fg_color="#1a1a1a",
                hover_color="#ff4444",
                command=lambda p=full_path, pl=path: modals["delete_song"](overlay, modal, p, pl,
                    lambda pp=path: open_playlist(pp, right_container, scroll, content_frame, state_ref,
                                                  instance, media_player, icons, play_selected_cb, overlay, modal, modals))
            )
            delete_btn.pack(side="left", padx=2)
            delete_btn.bind("<Enter>", lambda e, b=delete_btn: b.configure(image=icons["trash2"]))
            delete_btn.bind("<Leave>", lambda e, b=delete_btn: b.configure(image=icons["trash1"]))

    render_songs()
    search_local_var.trace_add("write", lambda *a: render_songs(search_local_var.get()))