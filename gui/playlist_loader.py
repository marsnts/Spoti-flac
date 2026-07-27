import requests
import customtkinter as ctk

from tkinter import messagebox
from PIL import Image
from io import BytesIO


class PlaylistLoaderMixin:

    def load_playlist(self):

        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror(
                "Error",
                "Please enter a playlist URL."
            )
            return

        try:

            playlist = self.spotify.get_playlist(url)

            self.playlist_name.configure(
                text=playlist["name"]
            )

            if playlist["cover"]:

                response = requests.get(playlist["cover"])

                image = Image.open(
                    BytesIO(response.content)
                )

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

        except Exception as e:

            messagebox.showerror(
                "Spotify Error",
                str(e)
            )