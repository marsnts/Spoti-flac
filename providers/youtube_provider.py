import os
import time


class YouTubeProvider:

    def __init__(self, output_folder):
        self.output_folder = output_folder

        os.makedirs(output_folder, exist_ok=True)

    def download(self, song):

        print(f"Searching YouTube for:")
        print(f"{song['title']} - {song['artists']}")

        time.sleep(1)

        print("Download complete\n")