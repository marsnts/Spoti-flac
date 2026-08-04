# Spoti-flac

A Python desktop application for loading Spotify playlists and downloading selected songs as FLAC files.

## Features

- Load Spotify playlists using a playlist URL
- Display playlist information and cover art
- Select or deselect individual songs
- Select all / deselect all songs
- Choose an output folder
- Download selected songs as FLAC
- Track download progress
- Cancel ongoing downloads
- Skip songs that have already been downloaded
- View download activity through the application log
- Choose between download providers

## Technologies

- Python
- CustomTkinter
- Spotipy
- Spotify Web API
- yt-dlp
- Git

## Installation

###### Install Python

Install python from the official Python website.

###### Install FFmpeg

FFmpeg must be installed and available in system PATH.

Download it from:

https://www.gyan.dev/ffmpeg/builds/

###### Clone the repository:

```bash
git clone https://github.com/marsnts/Spoti-flac.git
cd Spoti-flac
```

###### Create a virtual environment:
```bash
python -m venv .venv
```

###### Activate it on Windows:
```bash
.venv\Scripts\activate
```
###### Install require packages:
```bash
pip install -r requirements.txt
```

## Configuration

######Create a `env` file in the project root:
```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

## Usage
Run the Application

```bash
python main.py
```

1. Log in to Spotify when prompted.
2. Paste a Spotify playlist URL.
3. Click Load Playlist.
4. Select the songs you want to download.
5. Choose an output folder.
6. Select a download provider.
7. Click Download Selected.

## Project Status

🚧 **Work in Progress**

- ⚠️ Public Spotify playlists not owned by the logged-in account are currently **not supported** due to Spotify Web API restrictions.
- Some download providers are still a **work in progress**.
- Features and UI are still being improved.

## License

This project is for educational purposes.