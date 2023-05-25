import requests
import json
import re
from datetime import datetime


def cleanTitle(title):
    title = re.sub(
        r"(?i)\s+(?:ft\.?|feat\.?|featuring)\s+.*?(?=\s+-)", "", title)
    title = re.sub(r"\(prod\..*?\)|\(prod\..*?\)$",
                   "", title, flags=re.IGNORECASE)
    title = re.sub(r'\([^)]*\)', '', title)
    title = title.strip()
    return title


def extract_metadata(track_data, album_data):
    # Album Info
    album_genre = ", ".join(genre["name"]
                            for genre in album_data["genres"]["data"])
    album_artists = [contributor["name"]
                     for contributor in album_data["contributors"] if contributor["role"] == "Main" and contributor["id"] != 5080]
    album_label = album_data["label"]
    various = False
    if len(album_artists) == 0:
        various = True

    # Track Info
    track_title = track_data["title"]
    contributors = track_data["contributors"]
    track_main_artist = ", ".join(
        contributor["name"] for contributor in contributors if contributor["name"] in album_artists or various == True)
    track_featured_artists = ", ".join(
        contributor["name"] for contributor in contributors if contributor["name"] not in track_main_artist)
    track_album = track_data["album"]["title"]
    track_position = track_data["track_position"]
    track_disk = track_data["disk_number"]
    thumbnail_url = track_data["album"]["cover_big"]
    track_release_date = track_data["release_date"]
    track_publish_date = datetime.strptime(track_release_date, "%Y-%m-%d").year

    # Construct the filename
    filename = f"{track_main_artist} - {track_title}"
    if track_featured_artists:
        filename += f" (ft. {track_featured_artists})"

    song_metadata = {
        'filename': filename,
        'title': track_title,
        'album': track_album,
        'main_artist': track_main_artist,
        'full_artist': f"{track_main_artist}, {track_featured_artists}" if track_featured_artists else track_main_artist,
        'thumbnail_url': thumbnail_url,
        'featured_artists': track_featured_artists,
        'publish_date': track_publish_date,
        'genre': album_genre,
        'album_artist': ", ".join(album_artists),
        'label': album_label,
        'position': track_position,
        'disk': track_disk
    }

    return song_metadata


def getData(artist, title):
    song_name = f"{artist} - {title}"
    print(f'Retrieving information for {song_name} from Deezer API...')
    cleaned_name = cleanTitle(song_name)

    base_url = "https://api.deezer.com/search"
    params = {"q": cleaned_name}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if "data" in data and data["data"]:
            tracks = data["data"]

            track_info = min(tracks, key=lambda track: (track["rank"], cleanTitle(
                track["title"]) == cleanTitle(title) or track["artist"]["name"] == artist))

            track_id = track_info["id"]
            album_id = track_info["album"]["id"]
            track_response = requests.get(
                f'https://api.deezer.com/track/{track_id}')
            track_data = track_response.json()
            album_response = requests.get(
                f'https://api.deezer.com/album/{album_id}')
            album_data = album_response.json()

            if "error" not in track_data:
                song_metadata = extract_metadata(track_data, album_data)
                return song_metadata

    except requests.RequestException as e:
        print(f"An error occurred during the API request: {str(e)}")
    except (KeyError, IndexError):
        print("No song metadata found for the provided artist and title.")
    except ValueError as e:
        print(f"An error occurred while processing the response: {str(e)}")

    return None
