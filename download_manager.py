import os
import time
from providers.youtube_provider import YouTubeProvider
from providers.spotdl_provider import SpotDLProvider
from providers.qobuz_provider import QobuzProvider
from providers.ytdlp_provider import YtDlpProvider


#class Downloader:
#
#    def __init__(self, output_folder):
#        self.output_folder = output_folder
#
#    def download(self, song):
#        print(f"Downloading: {song['title']}")
        
class Downloader:

    def __init__(self, output_folder):

        if not output_folder:
            output_folder = "./downloads"

        self.output_folder = output_folder
        
        # For now we only have one provider
        self.provider = YouTubeProvider(output_folder)
        

        os.makedirs(self.output_folder, exist_ok=True)       

    def download(self, song):
        print(f"Downloading {song['title']}...")
        time.sleep(1)
        print("Finished!")


class DownloadManager:

    def __init__(self, output_folder, provider="spotdl"):

        if provider == "yt-dlp":
            self.provider = YtDlpProvider(output_folder)

        elif provider == "qobuz":
            self.provider = QobuzProvider(output_folder)

        else:
            self.provider = SpotDLProvider(output_folder)

    def download(self, song):
        return self.provider.download(song)