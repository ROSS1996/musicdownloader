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
    all_artists = f"{artist} {features}"
    full_song_name = f"{removechars.title(title)} - {all_artists}"
    print(
        f'Retrieving information for {removechars.title(title)} - {all_artists} from Deezer API...')
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
                if compare.strings(removechars.title(track['title']), removechars.title(title)) and compare_track_artist(track_artist=track['artist']['name'], artist=full_song_name) or track["artist"]["id"] == 5080
            ]

            sorted_tracks = sorted(
                filtered_tracks, key=lambda track: track["rank"], reverse=True)

            track_metadata = None
            album_metadata = None

            for track in sorted_tracks:
                track_data = get_track_metadata(track["id"])
                track_contributors = [contributor["name"]
                                      for contributor in track_data["contributors"]]
                track_from_artist = compare_track_artist(
                    track_artist=track_data["artist"]["name"], track_contributors=track_contributors, artist=all_artists) or compare_track_artist(
                    track_artist=track_data["artist"]["name"], track_contributors=track_contributors, artist=full_song_name)
                track_from_various = True if track_data["artist"]["id"] == 5080 else False

                if not track_from_artist or track_from_various:
                    print(
                        f"The artists from track {track_data['title']} didn't match the specified artist and it was ignored")
                    print(
                        f"Track artists {track_contributors}. The artists you are looking for are {all_artists}")
                    print(
                        f"Track from artist? {track_from_artist}, album from various? {track_from_various}")
                    continue

                album_data = get_album_metadata(track["album"]["id"])

                if "error" in track_data or "error" in album_data:
                    continue

                album_contributors = [contributor["name"]
                                      for contributor in album_data["contributors"]]
                album_from_artist = compare_album_artist(
                    album_artist=album_data["artist"]["name"], album_contributors=album_contributors, artist=all_artists) or compare_album_artist(
                    album_artist=album_data["artist"]["name"], album_contributors=album_contributors, artist=full_song_name)
                album_from_various = True if album_data["artist"]["id"] == 5080 else False

                if not album_from_artist and not album_from_various:
                    print(
                        f"The artists from album {album_data['title']} didn't match the specified artist and it was ignored")
                    print(
                        f"Album artists: {album_contributors}. The artists you are looking for are {all_artists}")
                    print(
                        f"Album from artist? {album_from_artist}, album from various? {album_from_various}")
                    continue

                if track_metadata is None and album_metadata is None:
                    track_metadata = track_data
                    album_metadata = album_data
                    continue

                album_type_value = album_type(
                    number_tracks=album_data["nb_tracks"], record_type=album_data["record_type"], from_artist=album_from_artist, from_various=album_from_various)
                if album_type_value == "Album":
                    track_metadata = track_data
                    album_metadata = album_data
                    break
                elif album_type_value == "Single" and album_data["fans"] > album_metadata["fans"]:
                    track_metadata = track_data
                    album_metadata = album_data
                elif album_type_value == "Compilation" and album_data["fans"] > album_metadata["fans"]:
                    track_metadata = track_data
                    album_metadata = album_data
            if track_metadata is None and album_metadata is None:
                print(
                    f"No song metadata found for '{title} - {all_artists}' in Deezer API, using YT Information...")
                return None
            song_metadata = extract_metadata(track_metadata, album_metadata)
            return song_metadata

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {str(e)}")
    except (KeyError, IndexError) as e:
        print(f"No song metadata found for '{artist} - {title}'. {str(e)}")
    except ValueError as e:
        print(f"An error occurred while processing the response: {str(e)}")

    return None


def album_type(number_tracks, record_type, from_artist, from_various):
    if number_tracks > 1 and from_artist:
        return "Album"
    elif number_tracks == 1 or record_type.lower() == "single" and from_artist or from_various:
        return "Single"
    else:
        return "Compilation"


def compare_track_artist(artist=None, track_artist=None, track_contributors=None):
    if not isinstance(track_artist, (str, type(None))):
        return False

    if not isinstance(track_contributors, (list, type(None))):
        return False

    if track_artist is not None and track_contributors is None:
        return compare.strings(track_artist, artist)

    if track_contributors is not None and track_artist is None:
        return any(compare.strings(contributor, artist) for contributor in track_contributors)

    return compare.strings(track_artist, artist) or any(compare.strings(contributor, artist) for contributor in track_contributors)


def compare_album_artist(artist=None, album_artist=None, album_contributors=None):
    if not isinstance(album_artist, (str, type(None))):
        return False

    if not isinstance(album_contributors, (list, type(None))):
        return False

    if album_artist is not None and album_contributors is None:
        return compare.strings(album_artist, artist)

    if album_contributors is not None and album_artist is None:
        return any(compare.strings(contributor, artist) for contributor in album_contributors)

    return compare.strings(album_artist, artist) or any(compare.strings(contributor, artist) for contributor in album_contributors)


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
