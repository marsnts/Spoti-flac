from dataclasses import dataclass


@dataclass
class DownloadResult:

    success: bool
    provider: str
    filename: str = ""
    error: str = ""