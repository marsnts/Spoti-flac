from ast import main
from multiprocessing.util import info
from time import time
import customtkinter as ctk
from tkinter import messagebox
from spotify_client import SpotifyClient
from tkinter import filedialog
import requests
from PIL import Image
from io import BytesIO
import threading
from downloader import Downloader




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

        #main = ctk.CTkFrame(self.app)
        #main.pack(fill="both", expand=True, padx=20, pady=20)
        #
        #main.grid_columnconfigure(0, weight=1)
        #main.grid_columnconfigure(1, weight=3)
        #main.grid_rowconfigure(3, weight=1)
        #
        #info = ctk.CTkFrame(main)
        #info.grid(row=2, column=1, sticky="nsew")
        #
        #bottom = ctk.CTkFrame(main)
        #bottom.grid(
        #    row=4,
        #    column=0,
        #    columnspan=2,
        #    sticky="ew"
        #)
        #
        #self.status = ctk.CTkLabel(
        #    bottom,
        #    text="Ready"
        #    )
        #
        #self.status.configure(text="Downloading...")
        #self.status.configure(text="Finished!")
#
        #self.status.grid(row=0, column=0, padx=10)
        #
        #
        #title = ctk.CTkLabel(
        #    main,
        #    text="🎵 Spoti-flac",
        #    font=("Segoe UI", 28, "bold")
        #)
        #title.grid(pady=(20, 10))
#
        #subtitle = ctk.CTkLabel(
        #    main,
        #    text="Paste a Spotify Playlist URL",
        #    font=("Segoe UI", 14)
        #)
        #subtitle.grid()
#
        #self.url_entry = ctk.CTkEntry(
        #    main,
        #    width=700,
        #    placeholder_text="https://open.spotify.com/#playlist/..."
        #)
        #self.url_entry.grid(pady=20)
#
        #self.load_button = ctk.CTkButton(
        #    main,
        #    text="Load Playlist",
        #    command=self.load_playlist
        #)
        #self.load_button.grid()
#
        #self.song_frame = ctk.CTkScrollableFrame(
        #main
        #)
#
        #self.song_frame.grid(row=3, column=0, columnspan=2, #sticky="nsew", pady=20)
#
        #self.cover_label = ctk.CTkLabel(
        #    main,
        #    text="No Cover",
        #    width=220,
        #    height=220
        #)
#
        #self.cover_label.grid(row=2, column=0, padx=20, #pady=20, sticky="n")
#
        #self.playlist_name = ctk.CTkLabel(
        #    main,
        #    text="No playlist loaded",
        #    font=("Segoe UI",20,"bold")
        #)
#
        #self.playlist_name.grid()
#
        #self.song_count = ctk.CTkLabel(
        #    main,
        #    text=""
        #)
#
        #self.song_count.grid()
        #
        #self.output_entry = ctk.CTkEntry(
        #main,
        #width=600
        #)
#
        #self.output_entry.grid()
#
        #browse = ctk.CTkButton(
        #    main,
        #    text="Browse",
        #    command=self.select_folder
        #)
#
        #browse.grid()
        #
        #self.progress = ctk.CTkProgressBar(
        #    main,
        #    width=700
        #)
#
        #self.progress.grid(pady=20)
#
        #self.progress.set(0)
        #
        #self.download_button = ctk.CTkButton(
        #    main,
        #    text="Download Selected",
        #    command=self.download_selected
        #    )
#
        #self.download_button.grid(pady=15)

######## REBUILDING UI ########
        
        main = ctk.CTkFrame(self.app)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        top = ctk.CTkFrame(main)
        top.pack(fill="x", pady=(0, 15))
        
        title = ctk.CTkLabel(
            top,
            text="🎵 Spoti-flac",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=(10,5))
        
        subtitle = ctk.CTkLabel(
            top,
            text="Paste a Spotify Playlist URL"
        )
        subtitle.pack()
        
        url_frame = ctk.CTkFrame(top)
        url_frame.pack(fill="x", pady=15)
        
        self.url_entry = ctk.CTkEntry(
        url_frame
        )
        self.url_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0,10)
        )
        
        self.load_button = ctk.CTkButton(
        url_frame,
        text="Load Playlist",
        command=self.load_playlist
        )

        self.load_button.pack(side="right")
        
        info = ctk.CTkFrame(main)
        info.pack(fill="x", pady=10)
        
        left = ctk.CTkFrame(info)
        left.pack(side="left", padx=20) 
        
        self.cover_label = ctk.CTkLabel(
        left,
        text="No Cover",
        width=180,
        height=180
        )
        
        self.cover_label.pack()
        
        right = ctk.CTkFrame(info)
        right.pack(
            side="left",
            fill="both",
            expand=True,
            padx=20
        )   
        
        self.playlist_name = ctk.CTkLabel(
            right,
            text="No playlist loaded",
            font=("Segoe UI",20,"bold")
        )
        
        self.playlist_name.pack(anchor="w")
                    
        self.song_count = ctk.CTkLabel(
            right,
            text=""
        )
        
        self.song_count.pack(anchor="w", pady=(0,20))
        
        folder_frame = ctk.CTkFrame(right)
        folder_frame.pack(fill="x")    
        
        self.output_entry = ctk.CTkEntry(folder_frame)

        self.output_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0,10)
        )        

        browse = ctk.CTkButton(
            folder_frame,
            text="Browse",
            command=self.select_folder
        )

        browse.pack(side="right")   
        
        self.song_frame = ctk.CTkScrollableFrame(
        main,
        height=250
        )

        self.song_frame.pack(
        fill="both",
        expand=True,
        pady=20
        )
        
        bottom = ctk.CTkFrame(main)
        bottom.pack(fill="x")       
         
        self.progress = ctk.CTkProgressBar(bottom)

        self.progress.pack(
            fill="x",
            pady=(10,5)
        )

        self.progress.set(0)    
        
        self.status = ctk.CTkLabel(
        bottom,
        text="Ready"
        )

        self.status.pack(side="left")

        self.download_button = ctk.CTkButton(
            bottom,
            text="Download Selected",
            command=self.download_selected
        )

        self.download_button.pack(side="right")


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
                checkbox.grid(row=i-1, column=0, sticky="w", padx=10, pady=3)

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
            threading.Thread(
            target=self.download_worker,
            daemon=True
        ).start()
            
        

    def download_worker(self):

        selected = []

        # Collect checked songs
        for checkbox, song in self.song_checkboxes:
            if checkbox.get():
                selected.append(song)

        if not selected:
            messagebox.showwarning(
                "No Songs",
                "Please select at least one song."
            )
            return

        downloader = Downloader(
            self.output_entry.get()
        )

        total = len(selected)

        for i, song in enumerate(selected, start=1):

            self.status.configure(
                text=f"Downloading: {song['title']}"
            )

            downloader.download(song)

            self.progress.set(i / total)

        self.status.configure(text="Finished!")
        
    def download(self, song):

        print(f"Downloading {song['title']}...")
        time.sleep(1)
        print("Finished!")
    
    def run(self):
        self.app.mainloop()