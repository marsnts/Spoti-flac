import os
import threading
import re
from tkinter import messagebox

from download_manager import DownloadManager

class DownloaderMixin:
    
    # Downloading selected songs
    def download_selected(self):
    
            # Flag to indicate if the download process should be canceled
            self.cancel_download = False
    
            # Disable buttons to prevent multiple clicks
            self.set_download_state(True)
    
            #Start thread for downloading to keep GUI responsive
            threading.Thread(
            target=self.download_worker,
            daemon=True
        ).start()
    
    def get_selected_songs(self):

        return [
            song
            for checkbox, song
            in self.song_checkboxes
            if checkbox.get()
        ]


    # Function to cancel ongoing downloads    
    def cancel_downloads(self):

        self.cancel_download = True

        self.cancel_button.configure(state="disabled")

        self.set_status(
            text="Cancelling after current song..."
        )
        
    # Function to get the filename for a song based on its title and artists
    def sanitize_filename(self, text):
        return re.sub(
            r'[<>:"/\\|?*]',
            "_",
            text.strip()
        )

    def get_song_filename(
            self,
            output_folder,
            song,
            extension="flac"
        ):
        
        artist = self.sanitize_filename(song["artists"])
        title = self.sanitize_filename(song["title"])

        return os.path.join(
            output_folder,
            f"{artist} - {title}.{extension}"
        )

    def set_status(self, text):

        self.app.after(
            0,
            lambda:
                self.status.configure(text=text)
        )

    def set_progress(self, value):

        self.app.after(
            0,
            lambda:
                self.progress.set(value)
        )

    def set_download_state(self, downloading):

        self.app.after(
            0,
            lambda: (
                self.download_button.configure(
                    state="disabled" if downloading else    "normal"
                ),
                self.load_button.configure(
                    state="disabled" if downloading else    "normal"
                ),
                self.cancel_button.configure(
                    state="normal" if downloading else  "disabled"
                )
            )
        )

    def validate_download(self):
        # Get selected songs
        selected = self.get_selected_songs()
        
        # Check if any songs are selected
        if not selected:
            self.set_download_state(False)
    
            messagebox.showwarning(
                "No Songs",
                "Please select at least one song."
            )
            return None
        
        # Get output folder
        output_folder = self.output_entry.get().strip()

        # Check if output folder is selected
        if not output_folder:
            self.set_download_state(False)
            
            messagebox.showerror(
                "Output Folder",
                "Please select an output folder first."
            )
            return None

        return selected, output_folder

    def download_worker(self):

        validated = self.validate_download()

        if validated is None:
            return

        selected, output_folder = validated
        
        # disable buttons to prevent multiple clicks
        self.set_download_state(True)
        self.set_progress(0)
        
        # Initialize DownloadManager with the selected provider
        manager = DownloadManager(
            output_folder,
            provider=self.provider_menu.get().lower()
        )

        total = len(selected)
    
        
        # Update status to indicate the start of the download process
        self.set_status(
            f"Starting download of {total} songs..."
            )
        
        for i, song in enumerate(selected, start=1):

            if self.cancel_download:
                self.log("Download cancelled by user.")
                break
            
            self.download_song(
                manager,
                output_folder,
                song,
                i,
                total
            )
        
        # After all downloads are complete,update the statuand        re-enable buttons
        self.finish_download()
    
    def download_song(
        self,
        manager,
        output_folder,
        song,
        i,
        total
    ):
        filename = self.get_song_filename(
            output_folder,
            song
        )
        
        if os.path.exists(filename):
            
            self.skip_song(song, i, total)
            
            return
                   
        
        self.log(f"Downloading {song['title']}")
        
        self.set_status(
            f"Downloading ({i}/{total})\n{song['artists']} - {song['title']}"
            )
        
        result = manager.download(song)
        
        self.set_progress(i / total)
        
        # Update the log and progress bar based on the download result
        self.log_download_result(
            result,
            song,
            i,
            total
        )
        
        # Update the status label to show the number of songs downloaded
        self.set_status(
            f"{i}/{total} downloaded"
        )          

    def finish_download(self):

        if self.cancel_download:
            self.set_status("Download cancelled.")
        else:
            self.set_status("Finished!")

        self.set_progress(1)
        self.set_download_state(False)

    def skip_song(self, song, i, total):

        self.set_status(
            f"Skipped ({i}/{total})\n{song['title']}"
        )

        self.log(
            f"[{i}/{total}] ⏭ Skipped: {song['title']}"
        )

        self.set_progress(i / total)
        
    def log_download_result(
        self,
        result,
        song,
        i,
        total
    ):

        if result.success:

            self.log(
                f"[{i}/{total}] ✓ {song['title']}"
            )

        else:

            self.log(
                f"[{i}/{total}] ✗ {song['title']}"
            )
    

