import yt_dlp
import os


def download(info):

    link = info["link"]
    title = info["title"]
    filename = info["filename"]
    music_id = info["music_id"]
    directory = info["directory"]

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{directory}/{filename}.%(ext)s',
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
        error_message = f"[YT-DLP] failed to download audio from {link}: {str(e)}"
        raise Exception(error_message) from None

    except yt_dlp.utils.DownloadError as e:
        error_message = f"[YT-DLP] encountered an error during download from {link}: {str(e)}"
        raise Exception(error_message) from None

    except yt_dlp.utils.ExtractorError as e:
        error_message = f"[YT-DLP] encountered an error while extracting audio from {link}: {str(e)}"
        raise Exception(error_message) from None

    except Exception as e:
        error_message = f"[YT-DLP] Error occurred during download: {str(e)}"
        raise Exception(error_message) from None
