import _testclinic_limited
import customtkinter as ctk
from tkinter import messagebox
from spotify_client import SpotifyClient
from tkinter import filedialog
import requests
from PIL import Image
from io import BytesIO
import threading
from download_manager import DownloadManager
import os

from gui.logger import LoggerMixin
from gui.logger import LoggerMixin
from gui.dialogs import DialogMixin
from gui.playlist_loader import PlaylistLoaderMixin
from gui.downloader import DownloaderMixin

#  GUI Class
class SpotiFlacGUI(
    LoggerMixin,
    DialogMixin,
    PlaylistLoaderMixin,
    DownloaderMixin
):

    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.spotify = SpotifyClient()

        # Store song checkboxes
        self.song_checkboxes = []
        
        # Flag to indicate if the download process should be canceled
        self.cancel_download = False

        self.app = ctk.CTk()
        self.app.title("Spoti-flac")
        #self.app.geometry("900x650")
        
        # Center the window on the screen
        self.app.geometry(f"+{(self.app.winfo_screenwidth()-self.app.winfo_width())//2}"
              f"+{(self.app.winfo_screenheight()-self.app.winfo_height())//2}")

        self.build_ui()

    def build_ui(self):
        
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
        text="Ready",
        justify="left",
        anchor="w"
        )

        self.status.pack(side="left")
       

        self.download_button = ctk.CTkButton(
            bottom,
            text="Download Selected",
            command=self.download_selected
        )

        self.download_button.pack(side="right")
        
        self.cancel_button = ctk.CTkButton(
            bottom,
            text="Cancel",
            command=self.cancel_download,
            state="disabled"
        )

        self.cancel_button.pack(side="right", padx=(0, 10))
        
        self.provider_menu = ctk.CTkOptionMenu(
        bottom,
        values=["yt-dlp", "spotDL", "Qobuz"]
        )

        self.provider_menu.set("yt-dlp")  # Default provider
        self.provider_menu.pack(side="right", padx=(0,10))
        
        self.log_box = ctk.CTkTextbox(
        self.app,
        width=700,
        height=120
        )
        
        self.log_box.pack(pady=10)



#   def build_top():
#
#   def build_playlist_info():
#
#   def build_song_list():
#
#   def build_bottom():
#
#   def build_log():


    # Run the GUI application
    def run(self):
        self.app.mainloop()