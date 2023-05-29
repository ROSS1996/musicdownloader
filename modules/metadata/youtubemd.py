import re
import youtube_dl
from pytube import YouTube
from helpers import removechars
from config import configs
from config.configs import get_logger

logger = get_logger()


def extract_song_data(artist, info_dict, link):
    if configs.verbose or configs.devmode:
        logger.info(f"[data-extractor] extracting data for {link}")
    song_data = {
        'filename': None,
        'title': info_dict.get("title", ""),
        'album': info_dict.get("title", ""),
        'full_artist': None,
        'main_artist': None,
        'thumbnail_url': info_dict.get("thumbnail", None),
        'featured_artists': None,
        'publish_date': info_dict.get("upload_date", "")[:4],
        'url': link
    }
    if configs.devmode:
        logger.info(f"[data-extractor] Original Data: {song_data}")

    song_data["title"] = removechars.title(song_data["title"])

    # Extract the main artist and featured artists
    artist_names = re.split(r", | & ", artist)
    song_data['main_artist'] = artist_names[0]
    if configs.devmode:
        logger.info(
            f"[data-extractor] extracted: {song_data['main_artist']} as main artist from {artist_names}")
    song_data['featured_artists'] = ", ".join(artist_names[1:])
    if configs.devmode:
        logger.info(
            f"[data-extractor] extracted: {song_data['featured_artists']} as featured artist from {artist_names}")
    if "&" in song_data['featured_artists']:
        song_data['featured_artists'] = song_data['featured_artists'].replace(
            " & ", " ")
    # Join main artist and featured artists into a single string
    if song_data['featured_artists']:
        song_data['full_artist'] = f"{song_data['main_artist']}, {song_data['featured_artists']}"
    else:
        song_data['full_artist'] = song_data['main_artist']
    if configs.devmode:
        logger.info(
            f"[data-extractor] all artists extracted from the data: {song_data['full_artist']}")
    # Construct the filename
    if song_data['featured_artists']:
        song_data['filename'] = f"{song_data['main_artist']} - {song_data['title']} (ft. {song_data['featured_artists']})"
    else:
        song_data['filename'] = f"{song_data['main_artist']} - {song_data['title']}"

    if configs.verbose or configs.devmode:
        logger.info(
            f"[data-extractor] data extracted for {link} - {song_data['filename']}")
    if configs.devmode:
        logger.info(f"[data-extractor] data after extraction: {song_data}")

    return song_data


def pytubeFetcher(link):
    logger.info(f'[youtubemd-pytube] retrieving information for {link}')

    try:
        # Create a YouTube object from the link
        yt = YouTube(link)
        # Retrieve song information and metadata
        artist = yt.author
        info_dict = {
            'title': yt.title,
            'thumbnail': yt.thumbnail_url,
            'upload_date': str(yt.publish_date.year)
        }

        logger.info(
            f'[youtubemd-pytube] sucesfully retrieved information for {link}')
        song_data = extract_song_data(
            artist=artist, info_dict=info_dict, link=link)
        return song_data

    except KeyError as e:
        logger.error(
            f"[youtubemd-pytube] failed to retrieve song data. Key not found: {str(e)}")
    except Exception as e:
        logger.error(
            f"[youtubemd-pytube] an error occurred during song data retrieval: {str(e)}")
    return None


def youtubedlFetcher(link):
    logger.info(f'[youtubemd-ytdl] retrieving information for {link}')

    try:
        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(link, download=False)
            artist = info_dict.get("artist", "")
        logger.info(
            f'[youtubemd-ytdl] sucesfully retrieved information for {link}')
        song_data = extract_song_data(
            artist=artist, info_dict=info_dict, link=link)

        return song_data

    except youtube_dl.DownloadError as e:
        logger.error("[youtubemd-ytdl] failed to retrieve the data:", str(e))
    except youtube_dl.utils.ExtractorError as e:
        logger.error(
            "[youtubemd-ytdl] failed to extract audio information:", str(e))
    except Exception as e:
        logger.errror(
            f"[youtubemd-ytdl] an error occurred during song data retrieval: {str(e)}")
    return None
