from spotify_client import SpotifyClient

spotify = SpotifyClient()

user = spotify.current_user()
print(f"Logged in as: {user['display_name']}")

from app_gui import SpotiFlacGUI

if __name__ == "__main__":
    app = SpotiFlacGUI()
    app.run()