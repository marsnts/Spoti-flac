from spotify_client import SpotifyClient

spotify = SpotifyClient()

user = spotify.current_user()
print(f"Logged in as: {user['display_name']}")

#playlist_url = input("Enter Spotify Playlist URL:\n> ").strip()
#
#playlist = spotify.get_playlist(playlist_url)
#
#print(f"\nPlaylist: {playlist['name']}")
#print("-" * 60)
#
#for i, song in enumerate(playlist["songs"], start=1):
#    print(f"{i}. {song['title']} - {song['artists']}")
#
#print(f"\nTotal songs: {len(playlist['songs'])}")

from app_gui import SpotiFlacGUI

if __name__ == "__main__":
    app = SpotiFlacGUI()
    app.run()