from providers.base_provider import BaseProvider


class QobuzProvider(BaseProvider):

    @property
    def name(self):
        return "Qobuz"

    def __init__(self, output_folder):
        self.output_folder = output_folder

    def download(self, song):
        print(f"Qobuz provider selected:")
        print(f"{song['title']} - {song['artists']}")

    