import yt_dlp
import os


def download(link, title, filename, music_id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'downloads/{filename}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        # Check if the 'downloads' directory exists and create it if needed
        output_directory = 'downloads'
        os.makedirs(output_directory, exist_ok=True)

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
