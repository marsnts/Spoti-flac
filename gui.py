import customtkinter as ctk
from tkinter import messagebox
from spotify_client import SpotifyClient
from tkinter import filedialog
import requests
from PIL import Image
from io import BytesIO

class SpotiFlacGUI:

    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.spotify = SpotifyClient()

        # Store song checkboxes
        self.song_checkboxes = []

        self.app = ctk.CTk()
        self.app.title("Spoti-flac")
        self.app.geometry("900x650")

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self.app,
            text="🎵 Spoti-flac",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=(20, 10))

        subtitle = ctk.CTkLabel(
            self.app,
            text="Paste a Spotify Playlist URL",
            font=("Segoe UI", 14)
        )
        subtitle.pack()

        self.url_entry = ctk.CTkEntry(
            self.app,
            width=700,
            placeholder_text="https://open.spotify.com/playlist/..."
        )
        self.url_entry.pack(pady=20)

        self.load_button = ctk.CTkButton(
            self.app,
            text="Load Playlist",
            command=self.load_playlist
        )
        self.load_button.pack()

        self.song_frame = ctk.CTkScrollableFrame(
        self.app,
        width=820,
        height=300
        )

        self.song_frame.pack(padx=20, pady=10)

        self.cover_label = ctk.CTkLabel(
            self.app,
            text="No Cover",
            width=200,
            height=200
        )

        self.cover_label.pack(pady=10)

        self.playlist_name = ctk.CTkLabel(
            self.app,
            text="No playlist loaded",
            font=("Segoe UI",20,"bold")
        )

        self.playlist_name.pack()

        self.song_count = ctk.CTkLabel(
            self.app,
            text=""
        )

        self.song_count.pack()
        
        self.output_entry = ctk.CTkEntry(
        self.app,
        width=600
        )

        self.output_entry.pack()

        browse = ctk.CTkButton(
            self.app,
            text="Browse",
            command=self.select_folder
        )

        browse.pack()
        
        self.progress = ctk.CTkProgressBar(
            self.app,
            width=700
        )

        self.progress.pack(pady=20)

        self.progress.set(0)
        
        self.download_button = ctk.CTkButton(
            self.app,
            text="Download Selected",
            command=self.download_selected
            )

        self.download_button.pack(pady=15)
        
    def load_playlist(self):

        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a playlist URL.")
            return

        try:
            playlist = self.spotify.get_playlist(url)

            self.playlist_name.configure(text=playlist["name"])
            
            if playlist["cover"]:
                response = requests.get(playlist["cover"])

                image = Image.open(BytesIO(response.content))
                image = image.resize((180, 180))

                self.cover_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=(180, 180)
                )

                self.cover_label.configure(
                    image=self.cover_image,
                    text=""
                )
            
            self.song_count.configure(
                text=f"{len(playlist['songs'])} songs"
            )

            # Clear old songs
            self.song_checkboxes.clear()
            for widget in self.song_frame.winfo_children():
                widget.destroy()

            # Add new songs
            for i, song in enumerate(playlist["songs"], start=1):

                checkbox = ctk.CTkCheckBox(
                    self.song_frame,
                    text=f"{i}. {song['title']} - {song['artists']}"
)

                checkbox.select()      # Checked by default
                checkbox.pack(anchor="w", padx=10, pady=3)

                # Save both the checkbox and its song
                self.song_checkboxes.append((checkbox, song))

        except Exception as e:
            messagebox.showerror("Spotify Error", str(e))
            
    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, folder)
            
    def download_selected(self):

        selected = []

        for checkbox, song in self.song_checkboxes:

            if checkbox.get() == 1:
                selected.append(song)

        print(f"Selected {len(selected)} songs:\n")

        for song in selected:
            print(song["title"])

    def run(self):
        self.app.mainloop()