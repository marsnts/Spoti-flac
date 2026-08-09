import customtkinter as ctk
from spotify_client import SpotifyClient

from gui.logger import LoggerMixin
from gui.dialogs import DialogMixin
from gui.playlist_loader import PlaylistLoaderMixin
from gui.downloader import DownloaderMixin
from gui.config import ConfigMixin

#  GUI Class
class SpotiFlacGUI(
    LoggerMixin,
    DialogMixin,
    PlaylistLoaderMixin,
    DownloaderMixin,
    ConfigMixin
):
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 900
    COVER_SIZE = 180
    SONG_LIST_HEIGHT = 250
    LOG_HEIGHT = 120
    LOG_WIDTH = 700

    def __init__(self):
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.spotify = SpotifyClient()

        # Flag to indicate if the download process should be canceled
        self.cancel_download = False
        
        self.failed_songs = []
        
        self.app = ctk.CTk()
        
        self.app.update_idletasks()
        
        # Center the window on the screen
        self.configure_window()

        self.build_ui()

        self.load_saved_settings()
        
       
        

    def build_ui(self):

        self.build_header_section()

        self.build_playlist_section()
        
        #self.song_section()
        
        self.build_bottom_section()
        
        self.build_log_section()

    # Run the GUI application
    def run(self):
        self.app.mainloop()
        
    def build_header_section(self):
    
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
    
    def build_playlist_section(self):
        
        self.build_url_section()
        self.build_playlist_info()
        self.build_output_folder()
        self.build_song_list()
        self.build_controls()
            
    def build_bottom_section(self):
        
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
        
        self.retry_button = ctk.CTkButton(
            bottom,
            text="Retry Failed",
            command=self.retry_failed_downloads,
            state="disabled"
        )
        
        self.retry_button.pack(
            side="right",
            padx=(0, 10)
        )
        
        self.cancel_button = ctk.CTkButton(
            bottom,
            text="Cancel",
            command=self.cancel_downloads,
            state="disabled"
        )
        
        self.cancel_button.pack(side="right", padx=(0, 10))
        
        self.provider_menu = ctk.CTkOptionMenu(
        bottom,
        values=["yt-dlp", "spotDL (WIP)", "Qobuz (WIP)"]
        )
        
        self.provider_menu.set("yt-dlp")  # Default provider
        self.provider_menu.pack(side="right", padx=(0,10))
    
    def build_log_section(self):
        
        self.log_box = ctk.CTkTextbox(
        self.app,
        width=self.LOG_WIDTH,
        height=self.LOG_HEIGHT
        )
        
        self.log_box.pack(
            fill="both",
            padx=20,
            pady=10
        )
        
    def select_all_songs(self):

        for checkbox, _ in self.song_checkboxes:
            checkbox.select()
            
    def deselect_all_songs(self):

        for checkbox, _ in self.song_checkboxes:
            checkbox.deselect()
                
    def build_url_section(self):
        
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
        
    def build_playlist_info(self):
        info = ctk.CTkFrame(self.main)
        info.pack(fill="x", pady=10)
        
        left = ctk.CTkFrame(info)
        left.pack(side="left", padx=20) 
        
        self.cover_label = ctk.CTkLabel(
        left,
        text="No Cover",
        width=self.COVER_SIZE,
        height=self.COVER_SIZE
        )
        
        self.cover_label.pack()
        
        self.right = ctk.CTkFrame(info)
        self.right.pack(
            side="left",
            fill="both",
            expand=True,
            padx=20
        )   
        
        self.playlist_name = ctk.CTkLabel(
            self.right,
            text="No playlist loaded",
            font=("Segoe UI",20,"bold")
        )
        
        self.playlist_name.pack(anchor="w")
        
        self.song_count = ctk.CTkLabel(
            self.right,
            text=""
        )
        
        self.song_count.pack(anchor="w", pady=(0,20))
        
    def build_output_folder(self):
        
        folder_frame = ctk.CTkFrame(self.right)
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
        
        self.browse_button = ctk.CTkButton(
            folder_frame,
            text="Browse",
            command=self.select_folder
        )
        
        self.browse_button.pack(side="right")
        
    def build_song_list(self):
        # Store song checkboxes
        self.song_checkboxes = []
        
        self.song_frame = ctk.CTkScrollableFrame(
        self.main,
        height=self.SONG_LIST_HEIGHT
        )
        
        self.song_frame.pack(
        fill="both",
        expand=True,
        pady=20
        )
    
    def build_controls(self):
        
        controls = ctk.CTkFrame(self.main)
        controls.pack(fill="x", pady=(10, 5))
        
        self.select_all_button = ctk.CTkButton(
            controls,
            text="Select All",
            width=120,
            command=self.select_all_songs
        )
        self.select_all_button.pack(side="left", padx=(0, 10))
        
        self.deselect_all_button = ctk.CTkButton(
            controls,
            text="Deselect All",
            width=120,
            command=self.deselect_all_songs
        )
        self.deselect_all_button.pack(side="left")
        
    def configure_window(self):

        self.app.title("Spoti-flac")

        width = self.WINDOW_WIDTH
        height = self.WINDOW_HEIGHT

        x = (self.app.winfo_screenwidth() - width) // 2
        y = (self.app.winfo_screenheight() - height) // 2

        self.app.geometry(
            f"{width}x{height}+{x}+{y}"
        )
        
    def load_saved_settings(self):
        
        config = self.load_config()
        
        folder = config.get("output_folder", "")
        
        if folder:
            self.output_entry.insert(0, folder)