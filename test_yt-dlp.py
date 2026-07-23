from providers.ytdlp_provider import YtDlpProvider

provider = YtDlpProvider("./downloads")

song = {
    "title": "IT'S YOU",
    "artists": "MAX keshi",
    "album": "LOVE IN STEREO"
}

result = provider.download(song)

print(result)

