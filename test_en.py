from download_manager import DownloadManager

manager = DownloadManager("./downloads")

manager.download({
    "title": "IT'S YOU",
    "artists": "MAX, keshi"
})

import providers.base_provider as bp

print(dir(bp))