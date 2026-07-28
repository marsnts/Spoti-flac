import customtkinter as ctk
from spotify_client import SpotifyClient

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
        
        self.app.update_idletasks()
        
        # Center the window on the screen
        
        width = 1200
        height = 900
        
        x = (self.app.winfo_screenwidth() - width) // 2
        y = (self.app.winfo_screenheight() - height) // 2
        
        self.app.geometry(f"{width}x{height}+{x}+{y}")

        self.build_ui()

    def build_ui(self):

        self.header_section()

        self.playlist_section()
        
        #self.song_section()
        
        self.bottom_section()
        
        self.log_section()

    # Run the GUI application
    def run(self):
        self.app.mainloop()
        
    def header_section(self):
    
        self.main = ctk.CTkFrame(self.app)
        self.main.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.top = ctk.CTkFrame(self.main)
        self.top.pack(fill="x", pady=(0, 15))
        
        title = ctk.CTkLabel(
            self.top,
            text="🎵 Spoti-flac",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=(10,5))
        
        subtitle = ctk.CTkLabel(
            self.top,
            text="Paste a Spotify Playlist URL"
        )
        subtitle.pack()
    
    def playlist_section(self):
        url_frame = ctk.CTkFrame(self.top)
        url_frame.pack(fill="x", pady=15)
        
        self.url_entry = ctk.CTkEntry(
        url_frame,
        placeholder_text="https://open.spotify.com/playlist/..."
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
        
        info = ctk.CTkFrame(self.main)
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
        
        self.output_entry = ctk.CTkEntry(
            folder_frame,
            placeholder_text="Choose output folder..."
            )
        
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
        self.main,
        height=250
        )
        
        self.song_frame.pack(
        fill="both",
        expand=True,
        pady=20
        )
        
#   def song_section():
    
    def bottom_section(self):
        
        bottom = ctk.CTkFrame(self.main)
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
            command=self.cancel_downloads,
            state="disabled"
        )
        
        self.cancel_button.pack(side="right", padx=(0, 10))
        
        self.provider_menu = ctk.CTkOptionMenu(
        bottom,
        values=["yt-dlp", "spotDL", "Qobuz"]
        )
        
        self.provider_menu.set("yt-dlp")  # Default provider
        self.provider_menu.pack(side="right", padx=(0,10))
    
    def log_section(self):
        
        self.log_box = ctk.CTkTextbox(
        self.app,
        width=700,
        height=120
        )
        
        self.log_box.pack(
            fill="both",
            padx=20,
            pady=10
        )