import os
import requests
import eyed3


def edit_tags(filename, title, full_artist, main_artist, album, album_artist, thumbnail_url, publish_date, genre, position, disc):
    print(f"Setting tags for {filename}...")
    song_path = os.path.join('downloads', f"{filename}.mp3")

    audio_file = eyed3.load(song_path)

    if audio_file is None:
        audio_file = eyed3.core.AudioFile(song_path)
        audio_file.initTag()

    audio_file.tag.title = title
    audio_file.tag.artist = full_artist
    audio_file.tag.album_artist = album_artist
    audio_file.tag.album = album
    audio_file.tag.recording_date = eyed3.core.Date(publish_date)

    if album_artist is None:
        audio_file.tag.genre = main_artist
    if genre is not None:
        audio_file.tag.genre = genre
    if position is not None:
        audio_file.tag.track_num = position
    if disc is not None:
        audio_file.tag.disc_num = disc

    try:
        thumbnail_data = requests.get(thumbnail_url).content
        audio_file.tag.images.set(3, thumbnail_data, 'image/jpeg', u"Cover")
    except requests.RequestException as e:
        print(f"Error retrieving thumbnail: {str(e)}")

    audio_file.tag.save()

    print(f"Tags set for {filename}!")
