import customtkinter as ctk
from state import state
from logic.lyrics import get_lyrics

def open_lyrics_view(artist, title, content_frame, scroll, clear_right_panel):
    if state["lyrics_frame_active"] is not None:
        try:
            state["lyrics_frame_active"].destroy()
        except:
            pass
        state["lyrics_frame_active"] = None
        scroll.pack(side="left", fill="both", expand=True)

    clear_right_panel()
    scroll.pack_forget()

    lyrics_frame = ctk.CTkFrame(content_frame, fg_color="#121212")
    lyrics_frame.pack(side="left", fill="both", expand=True)
    state["lyrics_frame_active"] = lyrics_frame

    def close_lyrics():
        lyrics_frame.destroy()
        state["lyrics_frame_active"] = None
        scroll.pack(side="left", fill="both", expand=True)

    separator = ctk.CTkFrame(lyrics_frame, width=2, fg_color="#2a2a2a")
    separator.pack(side="right", fill="y")

    ctk.CTkLabel(
        lyrics_frame,
        text=f"{artist} - {title}",
        font=("Montserrat", 20, "bold"),
        text_color="#FFFFFF"
    ).pack(pady=(10, 5))

    lyrics_box = ctk.CTkTextbox(
        lyrics_frame,
        fg_color="#121212",
        text_color="#FFFFFF",
        wrap="word",
        font=("Montserrat", 15)
    )
    lyrics_box.pack(fill="both", expand=True, padx=(20, 10), pady=(0, 10))

    lyrics_box.insert("1.0", "Loading lyrics...")
    lyrics_frame.update()

    lyrics = get_lyrics(artist, title)
    lyrics = lyrics.replace("\n", "\n\n")

    lyrics_box.delete("1.0", "end")
    lyrics_box.insert("1.0", lyrics)
    lyrics_box.configure(state="disabled")