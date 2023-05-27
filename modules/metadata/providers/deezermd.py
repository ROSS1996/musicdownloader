import requests
from datetime import datetime
from helpers import removechars, compare


def extract_metadata(track_data, album_data):
    # Album Info
    album_genre = ", ".join(genre["name"]
                            for genre in album_data["genres"]["data"])
    album_artists = [contributor["name"]
                     for contributor in album_data["contributors"] if contributor["role"] == "Main" and contributor["id"] != 5080]
    various = True if len(album_artists) == 0 else False
    # Track Info
    track_title = removechars.title(track_data["title"])
    contributors = track_data["contributors"]
    track_main_artist = ", ".join(
        contributor["name"] for contributor in contributors if contributor["name"] in album_artists or various == True)
    track_featured_artists = ", ".join(
        contributor["name"] for contributor in contributors if contributor["name"] not in track_main_artist)
    track_album = track_data["album"]["title"]
    track_position = track_data["track_position"]
    track_disc = track_data["disk_number"] if 'disk_number' in track_data else None
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
        'position': track_position,
        'disc': track_disc
    }

    return song_metadata


def getData(artist, features, title):
    print(
        f'Retrieving information for {removechars.title(title)} - {artist} {features} from Deezer API...')
    base_url = "https://api.deezer.com/search"
    params = {"q": removechars.title(title)}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if "data" in data and data["data"]:
            tracks = data["data"]

            filtered_tracks = [
                track for track in tracks
                if compare.strings(removechars.title(track['title']), removechars.title(title))
                and compare.strings(track["artist"]["name"], f"{artist}, {features}")
            ]

            track_metadata = None
            album_metadata = None
            for track in filtered_tracks:
                track_data = get_track_metadata(track["id"])
                album_data = get_album_metadata(track["album"]["id"])
                if "error" not in track_data and "error" not in album_data:
                    if track_metadata is None and album_metadata is None:
                        track_metadata = track_data
                        album_metadata = album_data
                        continue
                    album_type = albumType(album_data, track["artist"]["name"])
                    if album_type == "Album":
                        track_metadata = track_data
                        album_metadata = album_data
                        break
                    elif album_type == "Single" and albumType(album_metadata, track["artist"]["name"]) != "Album":
                        track_metadata = track_data
                        album_metadata = album_data
                    elif album_type == "Compilation" and albumType(album_metadata, track["artist"]["name"]) != "Album" and albumType(album_metadata, track["artist"]["name"]) != "Single":
                        track_metadata = track_data
                        album_metadata = album_data
            song_metadata = extract_metadata(track_metadata, album_metadata)
            return song_metadata

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {str(e)}")
    except (KeyError, IndexError) as e:
        print(f"No song metadata found for '{artist} - {title}'. {str(e)}")
    except ValueError as e:
        print(f"An error occurred while processing the response: {str(e)}")

    return None


def albumType(album_data, artist):
    if album_data["nb_tracks"] > 1 and any(compare.strings(contributor["name"], artist) for contributor in album_data["contributors"]):
        return "Album"
    elif album_data["nb_tracks"] == 1 and any(compare.strings(contributor["name"], artist) for contributor in album_data["contributors"]):
        return "Single"
    else:
        return "Compilation"


def get_track_metadata(track_id):
    track_response = requests.get(f'https://api.deezer.com/track/{track_id}')
    track_data = track_response.json()
    track_response.raise_for_status()
    return track_data


def get_album_metadata(album_id):
    album_response = requests.get(f'https://api.deezer.com/album/{album_id}')
    album_data = album_response.json()
    album_response.raise_for_status()
    return album_data
