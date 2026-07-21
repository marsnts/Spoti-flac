import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import config


class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=config["SPOTIPY_CLIENT_ID"],
                client_secret=config["SPOTIPY_CLIENT_SECRET"],
                redirect_uri=config["SPOTIPY_REDIRECT_URI"],
                scope="playlist-read-private playlist-read-collaborative",
            )
        )

    def current_user(self):
        """Return the logged-in user."""
        return self.sp.current_user()

    def get_playlist(self, playlist_url):
        """Return playlist name and all songs."""

        playlist = self.sp.playlist(playlist_url)

        songs = []

        results = self.sp.playlist_tracks(playlist["id"])

        while results:

            for item in results["items"]:

                # Compatible with both response formats
                track = item.get("track") or item.get("item")

                if track is None:
                    continue

                songs.append({
                    "title": track["name"],
                    "artists": ", ".join(
                        artist["name"] for artist in track["artists"]
                    ),
                    "album": track["album"]["name"],
                    "isrc": track["external_ids"].get("isrc"),
                    "duration_ms": track["duration_ms"],
                    "cover": (
                        track["album"]["images"][0]["url"]
                        if track["album"]["images"]
                        else None
                    ),
                })

            if results["next"]:
                results = self.sp.next(results)
            else:
                break

        return {
            "name": playlist["name"],
            "cover": (
                playlist["images"][0]["url"]
                if playlist["images"]
                else None
            ),
            "songs": songs,
        }