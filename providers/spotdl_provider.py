import subprocess

from providers.base_provider import BaseProvider






class SpotDLProvider(BaseProvider):

    @property
    def name(self):
            return "spotDL"
        
    def __init__(self, output_folder):

        self.output_folder = output_folder

    def download(self, song):

        query = f"{song['title']} {song['artists']}"

        command = [
            "spotdl",
            query,
            "--output",
            self.output_folder
        ]

        subprocess.run(command)