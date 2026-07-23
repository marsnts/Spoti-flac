import os
import yt_dlp
from providers.base_provider import BaseProvider
from models.download_result import DownloadResult
from metadata import MetadataWriter

class YtDlpProvider(BaseProvider):

    @property
    def name(self):
        return "yt-dlp"
    
    def __init__(self):
        pass

    def __init__(self, output_folder):
        self.output_folder = output_folder

    def download(self, song):

        query = f"{song['artists']} {song['title']}"
        
        print(f"Searching: {query}")

        ydl_opts = {
            "format": "bestaudio/best",

            "outtmpl": os.path.join(
                self.output_folder,
                f"{song['artists']} - {song['title']}.%(ext)s"
            ),

            "quiet": True,

            "noplaylist": True,

            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "flac",
                    "preferredquality": "320",
                }
            ],
        }

        try:

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:

                info = ydl.extract_info(
                    f"ytsearch1:{query}",
                    download=True
                )

                video = info["entries"][0]

                print(f"Found: {video['title']}")

                filename = os.path.join(
                    self.output_folder,
                    f"{song['artists']} - {song['title']}.flac"
                )

                MetadataWriter.write(
                    filename,
                    song
                )
                
                return DownloadResult(
                    success=True,
                    provider="yt-dlp",
                    filename=filename
                )       

        except Exception as e:

            return DownloadResult(
                success=False,
                provider=self.name,
                error=str(e)
            )