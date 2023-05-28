import youtube_dl
import os
from config import configs


def download(link, title, filename, music_id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{configs.downloads_dir}/{filename}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print(f'[Youtube-DL] Downloading {title} ({link})')
            ydl.download([link])
        return True

    except youtube_dl.utils.DownloadError as e:
        error_message = f"[Youtube-DL] failed to download audio from {link}: {e}"
        raise Exception(error_message) from None

    except youtube_dl.utils.ExtractorError as e:
        error_message = f"[Youtube-DL] encountered an error while extracting audio from {link}: {str(e)}"
        raise Exception(error_message) from None

    except youtube_dl.utils.PostProcessingError as e:
        error_message = f"[Youtube-DL] encountered an error during post-processing of audio from {link}: {str(e)}"
        raise Exception(error_message) from None

    except youtube_dl.utils.RegexNotFoundError as e:
        error_message = f"[Youtube-DL] encountered a regex not found error: {str(e)}"
        raise Exception(error_message) from None

    except Exception as e:
        error_message = f"[Youtube-DL] error occurred during download: {str(e)}"
        raise Exception(error_message) from None
