import os
import re
import json
import requests
from datetime import datetime
from pytube import YouTube
from mutagen.id3 import ID3, TIT2, TPE1, TYER, TOPE, TPE2, APIC, TALB
from mutagen.id3._util import ID3NoHeaderError
from mutagen import File
from pydub import AudioSegment
import youtube_dl
import yt_dlp


def link_id(link):
    pattern = r"(?:youtube(?:music)?.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|[^#]*[?&]v=|youtu\.be\/|embed\/|\/shorts\/|\/m\/|\/attribution_link\?.*v=))([\w-]{11})"
    match = re.search(pattern, link)
    return match.group(1) if match else None


# Create a 'downloads' folder if it doesn't already exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Read in the list of YouTube Music links from a file
with open('links.txt', 'r') as f:
    links = f.readlines()


def getSongMetadata(song_name):
    print(f'Retrieving metadata for {song_name}...')
    # Remove featured artists using regular expressions
    removed_features = re.sub(
        r"(?i)\s+(?:ft\.?|feat\.?|featuring)\s+.*?(?=\s+-)", "", song_name).strip()
    # Remove production information using regular expressions
    cleaned_name = re.sub(r"\(prod\..*?\)|\(prod\..*?\)$",
                          "", removed_features, flags=re.IGNORECASE).strip()

    # Search for song info
    base_url = "https://api.deezer.com/search"
    params = {"q": cleaned_name}
    response = requests.get(base_url, params=params)
    data = response.json()

    # Extract metadata from the response
    if "data" in data and data["data"]:
        track_info = data["data"][0]
        track_id = track_info["id"]
        track_response = requests.get(
            f'https://api.deezer.com/track/{track_id}')
        track_data = track_response.json()

        if "error" not in track_data:
            title = track_data["title"]
            main_artist = track_data["artist"]["name"]
            album = track_data["album"]["title"]
            thumbnail_url = track_data["album"]["cover_big"]
            release_date = track_data["release_date"]
            publish_date = datetime.strptime(release_date, "%Y-%m-%d").year
            featured_artists = [contributor["name"]
                                for contributor in track_data["contributors"] if contributor["name"] != main_artist]
            featured_artists = ", ".join(featured_artists)
            full_artist = f"{main_artist}, {featured_artists}" if featured_artists else main_artist

            # Construct the filename
            filename = f"{main_artist} - {title}" + \
                (f" (ft. {featured_artists})" if featured_artists else "")

            song_metadata = {
                'filename': filename,
                'title': title,
                'album': album,
                'main_artist': main_artist,
                'full_artist': full_artist,
                'thumbnail_url': thumbnail_url,
                'featured_artists': featured_artists,
                'publish_date': publish_date
            }

            return song_metadata

    return None


def getSongData(source, link):
    if not link:
        return False

    song_data = {
        'filename': None,
        'title': None,
        'album': None,
        'full_artist': None,
        'main_artist': None,
        'thumbnail_url': None,
        'featured_artists': None,
        'publish_date': None
    }

    print(f'Retrieving basic information for {link}...')

    if source == "pytube":
        # Create a YouTube object from the link
        yt = YouTube(link)
        # Retrieve song information and metadata
        artist = yt.author
        song_data['title'] = yt.title
        song_data['album'] = yt.title
        song_data['thumbnail_url'] = yt.thumbnail_url
        song_data['publish_date'] = yt.publish_date.year

    if source == "youtubedl":
        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(link, download=False)
            artist = info_dict.get("artist", "")
            song_data['title'] = info_dict.get("title", "")
            song_data['album'] = info_dict.get("title", "")
            song_data['thumbnail_url'] = info_dict.get("thumbnail", None)
            song_data['publish_date'] = info_dict.get("upload_date", "")[:4]

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


def downloadSong(link, title, filename, music_id, library):
    if library == "pytube":
        # Create a YouTube object from the link
        yt = YouTube(link)
        try:
            # Choose the best matching audio stream regardless of format
            audio_stream = yt.streams.filter(
                only_audio=True).order_by('abr').desc().first()
            if audio_stream is None:
                raise Exception(
                    f"Pytube wasn't able to find an audio stream for {title} (audio_stream is None)")
        except Exception as e:
            raise Exception(
                f"Pytube wasn't able to find an audio stream for {title}: {str(e)}")

        # Download the audio stream and save it as a webm file
        print(f"Downloading {filename}...")
        audio_path = audio_stream.download(
            output_path='downloads', filename=f'{filename}.webm')
        print(f"Done downloading {filename}!")

        # Convert webm to mp3
        print(f"Converting {filename} to mp3...")
        mp3_path = os.path.join('downloads', f"{filename}.mp3")
        audio = AudioSegment.from_file(audio_path, format='webm')
        audio.export(mp3_path, format='mp3')
        os.remove(audio_path)

    else:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'downloads/{music_id}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            if library == "youtubedl":
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])
            elif library == "ytdlp":
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])
            else:
                raise ValueError(f"Invalid library specified: {library}")

            # Rename the downloaded file with the desired filename
            old_filename = f"downloads/{music_id}.mp3"
            new_filename = f"downloads/{filename}.mp3"
            os.rename(old_filename, new_filename)

        except Exception as e:
            raise Exception(
                f"{library} failed to download audio from {link}: {str(e)}")

    return True


def editTags(filename, title, full_artist, main_artist, album, thumbnail_url, publish_date):
    print(f"Setting {filename} tags...")
    song = os.path.join('downloads', f"{filename}.mp3")

    try:
        audio_tags = ID3(song)
    except ID3NoHeaderError:
        audio_tags = ID3()

    audio_tags.delete()
    audio_tags["TIT2"] = TIT2(encoding=3, text=title)
    audio_tags["TPE1"] = TPE1(encoding=3, text=full_artist)
    audio_tags["TPE2"] = TPE2(encoding=3, text=main_artist)
    audio_tags["TALB"] = TALB(encoding=3, text=album)
    audio_tags["TYER"] = TYER(encoding=3, text=str(publish_date))

    thumbnail_data = requests.get(thumbnail_url).content
    audio_tags["APIC"] = APIC(
        encoding=3, mime='image/jpeg', type=3, desc='Cover', data=thumbnail_data)

    audio_tags.save(song, v1=2, v2_version=3)

    print(f"Tags set for {filename}!")


# Loop through each link and download the song and metadata
for link in links:
    music_id = link_id(link)
    if not music_id:
        print(
            f'ERROR: {link} is not a valid YouTube / YT Music link. skipping it...')
        continue

    info = getSongData("pytube", link)
    metadata = getSongMetadata(f"{info['main_artist']} - {info['title']}")
    if metadata:
        info.update(metadata)

    filename = info['filename']
    title = info['title']
    album = info['album']
    full_artist = info['full_artist']
    main_artist = info['main_artist']
    thumbnail_url = info['thumbnail_url']
    publish_date = info['publish_date']

    download_libraries = ["pytube", "ytdlp", "youtubedl"]
    download_successful = False

    for library in download_libraries:
        try:
            downloadSong(link, title, filename, music_id, library)
            download_successful = True
            break
        except Exception as download_exception:
            print(str(download_exception))
            print(f'Trying to download {filename} ({link}) with {library}...')

    if not download_successful:
        print(f'{filename} ({link}) could not be downloaded. Try again later.')
        continue

    editTags(filename, title, full_artist, main_artist,
             album, thumbnail_url, publish_date)
