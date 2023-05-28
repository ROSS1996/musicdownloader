import yt_dlp
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
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return True

    except yt_dlp.DownloadError as e:
        error_message = f"[yt-dlp] failed to download audio from {link}: {str(e)}"
        raise Exception(error_message) from None

    except yt_dlp.utils.DownloadError as e:
        error_message = f"[yt-dlp] encountered an error during download from {link}: {str(e)}"
        raise Exception(error_message) from None

    except yt_dlp.utils.ExtractorError as e:
        error_message = f"[yt-dlp] encountered an error while extracting audio from {link}: {str(e)}"
        raise Exception(error_message) from None

    except Exception as e:
        error_message = f"[YT-DLP] Error occurred during download: {str(e)}"
        raise Exception(error_message) from None
