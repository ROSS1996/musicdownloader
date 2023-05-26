import re
import youtube_dl
from pytube import YouTube
from helpers import removechars


def extract_song_data(artist, info_dict):
    song_data = {
        'filename': None,
        'title': info_dict.get("title", ""),
        'album': info_dict.get("title", ""),
        'full_artist': None,
        'main_artist': None,
        'thumbnail_url': info_dict.get("thumbnail", None),
        'featured_artists': None,
        'publish_date': info_dict.get("upload_date", "")[:4]
    }

    song_data["title"] = removechars.title(song_data["title"])

    # Extract the main artist and featured artists
    artist_names = re.split(r", | & ", artist)
    song_data['main_artist'] = artist_names[0]
    song_data['featured_artists'] = ", ".join(artist_names[1:])
    if "&" in song_data['featured_artists']:
        song_data['featured_artists'] = song_data['featured_artists'].replace(
            " & ", " ")

    # Join main artist and featured artists into a single string
    if song_data['featured_artists']:
        song_data['full_artist'] = f"{song_data['main_artist']}, {song_data['featured_artists']}"
    else:
        song_data['full_artist'] = song_data['main_artist']

    # Construct the filename
    if song_data['featured_artists']:
        song_data['filename'] = f"{song_data['main_artist']} - {song_data['title']} (ft. {song_data['featured_artists']})"
    else:
        song_data['filename'] = f"{song_data['main_artist']} - {song_data['title']}"
    return song_data


def pytubeFetcher(link):
    print(f'Retrieving information for {link} from YouTube using Pytube...')

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
        song_data = extract_song_data(artist, info_dict)

        return song_data

    except KeyError as e:
        print(f"Error: Failed to retrieve song data. Key not found: {str(e)}")
    except Exception as e:
        print(
            f"Error occurred during song data retrieval using Pytube: {str(e)}")
    return None


def youtubedlFetcher(link):
    print(f'Retrieving basic information for {link} using Youtube-DL...')

    try:
        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(link, download=False)
            artist = info_dict.get("artist", "")

        song_data = extract_song_data(artist, info_dict)

        return song_data

    except youtube_dl.DownloadError as e:
        print("Error: Failed to retrieve the data:", str(e))
    except youtube_dl.utils.ExtractorError as e:
        print("Error: Failed to extract audio information:", str(e))
    except Exception as e:
        print(
            f"Error occurred during song data retrieval using Youtube-DL: {str(e)}")
    return None
