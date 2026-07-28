import requests
import customtkinter as ctk

from tkinter import messagebox
from PIL import Image
from io import BytesIO


class PlaylistLoaderMixin:

    def load_playlist(self):

        url = self.validate_playlist_url()

        if url is None:
            return

        try:

            playlist = self.fetch_playlist(url)

            self.display_playlist_info(playlist)
            
            self.display_cover(playlist)

            self.display_song_list(playlist)

        except Exception as e:

            messagebox.showerror(
                "Spotify Error",
                str(e)
            )
            
            
    def validate_playlist_url(self):

        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror(
                "Error",
                "Please enter a Spotify playlist URL."
            )
            return None

        return url
    
    def fetch_playlist(self, url):

        return self.spotify.get_playlist(url)
    
    def display_playlist_info(self, playlist):

        self.playlist_name.configure(
            text=playlist["name"]
        )

        self.song_count.configure(
            text=f"{len(playlist['songs'])} songs"
        )
        
    def display_cover(self, playlist):

        if not playlist["cover"]:
            self.cover_label.configure(image=None,  text="")
            return

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
        
    def display_song_list(self, playlist):
        
        self.song_checkboxes.clear()
        
        for widget in self.song_frame.winfo_children():
            widget.destroy()
        
        for i, song in enumerate(
            playlist["songs"],
            start=1
        ):
        
            checkbox = ctk.CTkCheckBox(
                self.song_frame,
                text=f"{i}. {song['title']} - {song['artists']}"
            )
        
            checkbox.select()
        
            checkbox.grid(
                row=i-1,
                column=0,
                sticky="w",
                padx=10,
                pady=3
            )
        
            self.song_checkboxes.append(
                (checkbox, song)
            )