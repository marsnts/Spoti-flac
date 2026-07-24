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


#  GUI Class
class SpotiFlacGUI:

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





    # Functions

    #Selecting output folder
    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, folder)
            
    # Downloading selected songs
    def download_selected(self):
        
            # Flag to indicate if the download process should be canceled
            self.cancel_download = False

            self.download_button.configure(state="disabled")
            self.load_button.configure(state="disabled")

            self.cancel_button.configure(state="normal")
        
            # Get output folder
            output_folder = self.output_entry.get().strip()
        
            # Disable buttons to prevent multiple clicks
            self.download_button.configure(state="disabled")
            self.load_button.configure(state="disabled")
            
            # Check if output folder is selected
            if not output_folder:
                messagebox.showerror(
                "Output Folder",
                "Please select an output folder first."
                )
                return
            
            #Start thread for downloading to keep GUI responsive
            threading.Thread(
            target=self.download_worker,
            daemon=True
        ).start()
            
        
    def download_worker(self):

        # Get selected songs
        selected = []

        # Collect checked songs
        for checkbox, song in self.song_checkboxes:
            if checkbox.get():
                selected.append(song)

        # Check if any songs are selected
        if not selected:
            messagebox.showwarning(
                "No Songs",
                "Please select at least one song."
            )
            return
        
        # Get output folder
        output_folder = self.output_entry.get().strip()

        # Check if output folder is selected
        if not output_folder:
            messagebox.showerror(
                "Output Folder",
                "Please select an output folder first."
            )
            return

        # disable buttons to prevent multiple clicks
        self.download_button.configure(state="disabled")
        self.load_button.configure(state="disabled")
        self.progress.set(0)
        
        # Initialize DownloadManager with the selected provider
        manager = DownloadManager(
            self.output_entry.get(),
            provider=self.provider_menu.get().lower()
        )

        total = len(selected)
        
        self.app.after(
            0,
            lambda: self.progress.set(0)
        )
        
        # Update status to indicate the start of the download process
        self.app.after(
            0,
            lambda: self.status.configure(
                text=f"Starting download of {total} songs..."
            )
        )
        
        
        
        # Download each selected song
        for i, song in enumerate(selected, start=1):
            
            # Check if the user clicked the cancel button during the download process
            if self.cancel_download:
                    
                self.log("Download cancelled by user.")
            
                break
            
            # Check if the song already exists in the output folder
            filename = self.get_song_filename(song)

            if os.path.exists(filename):
                
                self.app.after(
                    0,
                    lambda i=i, total=total, song=song:
                        self.status.configure(
                            text=f"Skipped ({i}/{total})\n{song['title']}"
                        )
                )
                
                self.log(
                    f"[{i}/{total}] ⏭ Skipped: {song['title']}"
                )

                progress = i / total

                self.app.after(
                    0,
                    lambda p=progress: self.progress.set(p)
                )
                
                continue

            self.app.after(
            0,
                lambda i=i, total=total, song=song:
                self.status.configure(
                    text=f"Downloading ({i}/{total}): {song['title']}"
                )
            )

            self.log(f"Downloading {song['title']}")

            self.app.after(
                0,
                lambda i=i, total=total, song=song:
                    self.status.configure(
                        text=f"Downloading ({i}/{total})\n{song         ['artists']} - {song['title']}"
                    )
            )

            result = manager.download(song)
            
            progress = i / total

            self.app.after(
                0,
                lambda p=progress: self.progress.set(p)
            )

            # Update the log and progress bar based on the download result
            if result.success:

                self.log(
                    f"[{i}/{total}] ✓ {song['title']}"
                )

            else:
            
                self.log(
                    f"[{i}/{total}] ✗ {song['title']}"
                )
                
            # Update progress bar and status
            self.progress.set(i / total)
            
            # Update the status label to show the number of songs downloaded
            self.status.configure(
                text=f"{i}/{total} downloaded"
            )          
            
            # After all downloads are complete, update the status and re-enable buttons
            if self.cancel_download:
                self.app.after(
                    0,
                    lambda: self.status.configure(text="Download cancelled.")
                )
            else:
                self.app.after(
                    0,
                    lambda: self.status.configure(text="Finished!")
                )
            
            self.app.after(
                0,
                lambda: self.progress.set(1)
            )
            
            self.app.after(
                0,
                lambda: self.download_button.configure(state="normal")
                
            )

            self.app.after(
                0,
                lambda: self.load_button.configure(state="normal")
            )
            self.progress.set(1)
            
            self.app.after(
                0,
                lambda: self.cancel_button.configure(state="disabled")
            )    
    
    # Logging function to update the log box in the GUI
    def log(self, text):
        self.app.after(
            0,
            lambda: (
            self.log_box.insert("end", text + "\n"),
            self.log_box.see("end")
            )
        )

    # Function to get the filename for a song based on its title and artists
    def get_song_filename(self, song):
        return os.path.join(
            self.output_entry.get(),
            f"{song['artists']} - {song['title']}.flac"
        )
    
    # Function to cancel ongoing downloads    
    def cancel_downloads(self):

        self.cancel_download = True

        self.cancel_button.configure(state="disabled")

        self.status.configure(
            text="Cancelling after current song..."
        )
    
    # Run the GUI application
    def run(self):
        self.app.mainloop()