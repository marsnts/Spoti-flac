import requests

from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, APIC, TIT2, TALB, TPE1, TDRC, TRCK, TPE2
from mutagen.mp3 import MP3


class MetadataWriter:

    @staticmethod
    def write(file_path, song):
        try:
            
            if file_path.lower().endswith(".mp3"):
                MetadataWriter.write_mp3(file_path, song)

            elif file_path.lower().endswith(".flac"):
                MetadataWriter.write_flac(file_path, song)
            
        except Exception as e:
            print(f"Metadata error: {e}")


    @staticmethod
    def write_mp3(file_path, song):

        audio = MP3(file_path)

        if audio.tags is None:
            audio.add_tags()

        audio.tags.add(TIT2(encoding=3, text=song["title"]))
        audio.tags.add(TPE1(encoding=3, text=song["artists"]))
        audio.tags.add(TALB(encoding=3, text=song["album"]))

        if song.get("release_date"):
            audio.tags.add(
                TDRC(
                    encoding=3,
                    text=song["release_date"][:4]
                )
            )
            
        if song.get("release_date"):
            audio.tags.add(
                TDRC(
                    encoding=3,
                    text=song["release_date"][:4]
                )
            )
        
        if song.get("track_number"):
            audio.tags.add(
                TRCK(
                    encoding=3,
                    text=str(song["track_number"])
                )
            )
            
        if song.get("album_artist"):
            audio.tags.add(
                TPE2(
                    encoding=3,
                    text=song["album_artist"]
                )
            )

        if song["cover"]:

            response = requests.get(song["cover"], timeout=10)
            response.raise_for_status()
            image = response.content

            audio.tags.add(
                APIC(
                    encoding=3,
                    mime="image/jpeg",
                    type=3,
                    desc="Cover",
                    data=image
                )
            )

        audio.save()


    @staticmethod
    def write_flac(file_path, song):

        audio = FLAC(file_path)

        audio["TITLE"] = song["title"]
        audio["ARTIST"] = song["artists"]
        audio["ALBUM"] = song["album"]
        
        if song.get("album_artist"):
            audio["ALBUMARTIST"] = song["album_artist"]

        if song.get("track_number"):
            audio["TRACKNUMBER"] = str(song["track_number"])

        if song.get("disc_number"):
            audio["DISCNUMBER"] = str(song["disc_number"])

        if song.get("release_date"):
            audio["DATE"] = song["release_date"][:4]

        if song.get("isrc"):
            audio["ISRC"] = song["isrc"]

        if song["cover"]:

            response = requests.get(song["cover"], timeout=10)
            response.raise_for_status()

            image = response.content
            
            audio.clear_pictures()
            
            picture = Picture()

            picture.data = image
            picture.mime = "image/jpeg"
            picture.type = 3

            audio.add_picture(picture)

        audio.save()