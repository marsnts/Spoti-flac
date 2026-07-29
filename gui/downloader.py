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

        enabled = "normal"
        disabled = "disabled"

        normal_state = disabled if downloading else enabled
        cancel_state = enabled if downloading else disabled
        
        self.download_button.configure(state=normal_state)
        self.load_button.configure(state=normal_state)
        self.url_entry.configure(state=normal_state)
        self.output_entry.configure(state=normal_state)
        self.browse_button.configure(state=normal_state)
        self.provider_menu.configure(state=normal_state)
        self.cancel_button.configure(state=cancel_state)
        self.select_all_button.configure(state=normal_state)
        self.deselect_all_button.configure(state=normal_state)

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
        
        stats = {
            "downloaded": 0,
            "skipped": 0,
            "failed": 0,
        }
        
        
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
                self.show_cancelled()
                break
            
            result = self.download_song(
                manager,
                output_folder,
                song,
                i,
                total
            )
            
            stats[result] += 1
                
        # After all downloads are complete,update the statuand        re-enable buttons
        self.finish_download(
                stats["downloaded"],
                stats["skipped"],
                stats["failed"],
            )
        
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
            
            self.show_skipped(song, i, total)
            return "skipped"
                   
        
        self.log(
            f"[{i}/{total}] Downloading: {song['title']}"
        )
        
        self.show_downloading(song, i, total)
        
        result = manager.download(song)
        
        self.set_progress(i / total)
        
        # Update the log and progress bar based on the download result
        self.log_download_result(
            result,
            song,
            i,
            total
        )
        
        if result.success:
            return "downloaded"
        else:
            return "failed"         

    def finish_download(self, downloaded, skipped, failed):

        if self.cancel_download:
            self.show_cancelled()
        else:
            self.show_finished(downloaded, skipped, failed)
        self.set_progress(1)
        self.set_download_state(False)

    def show_skipped(self, song, current, total):

        self.set_status(
            f"Skipped ({current}/{total})\n"
            f"{song['artists']} - {song['title']}"
        )
    
        self.log(
            f"[{current}/{total}] ⏭ Skipped: {song['title']}"
        )

        self.set_progress(current / total)
        
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
    

    def show_downloading(self, song, current, total):
        self.set_status(
            f"Downloading ({current}/{total})\n"
            f"{song['artists']} - {song['title']}"
        )
        
    def show_finished(self,downloaded,skipped,failed):
        self.set_status(
            "Finished!\n"
            f"✓ {downloaded} downloaded\n"
            f"⏭ {skipped} skipped\n"
            f"✗ {failed} failed"
        )
    
    def show_cancelled(self):
        self.set_status("Download cancelled.")
        