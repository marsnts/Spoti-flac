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
        
         
        self.provider_menu = ctk.CTkOptionMenu(
        bottom,
        values=["spotDL", "Qobuz", "yt-dlp"]
        )

        self.provider_menu.set("yt-dlp")  # Default provider
        self.provider_menu.pack(side="right", padx=(0,10))
        
        self.log_box = ctk.CTkTextbox(
        self.app,
        width=700,
        height=120
        )
        
        self.log_box.pack(pady=10)


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





    ## FUNCTIONS

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
        
        output_folder = self.output_entry.get().strip()

        if not output_folder:
            messagebox.showerror(
                "Output Folder",
                "Please select an output folder first."
            )
            return

        self.download_button.configure(state="disabled")
        self.load_button.configure(state="disabled")
        self.progress.set(0)
        
        manager = DownloadManager(
            self.output_entry.get(),
            provider=self.provider_menu.get().lower()
        )

        total = len(selected)
        
        

        for i, song in enumerate(selected, start=1):

            self.status.configure(
                text=f"Downloading: {song['title']}"
            )

            self.log(f"Downloading {song['title']}")

            result = manager.download(song)

            if result.success:
                self.log(f"✓ {song['title']} ({result.provider})")
            else:
                self.log(f"✗ {song['title']} ({result.error})")

            self.progress.set(i / total)

            self.status.configure(
                text=f"{i}/{total} downloaded"
            )           
            
        self.download_button.configure(state="normal")
        self.load_button.configure(state="normal")  
        self.progress.set(1)    
            
    def log(self, text):
        self.app.after(
            0,
            lambda: (
            self.log_box.insert("end", text + "\n"),
            self.log_box.see("end")
            )
        )
    
    def run(self):
        self.app.mainloop()