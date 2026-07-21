import os
import time
from providers.youtube_provider import YouTubeProvider


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
        
        
    