import os
import requests
import eyed3


def edit_tags(info):
    if not isinstance(info, dict):
        raise TypeError("The 'info' argument must be a dictionary")

    filename = info['filename']
    title = info['title']
    main_artist = info['main_artist']
    full_artist = info['full_artist']
    album = info['album']
    publish_date = info['publish_date']
    thumbnail_url = info['thumbnail_url']
    genre = info['genre'] if 'genre' in info else None
    position = position = info['position'] if 'genre' in info else None
    disc = disc = info['disc'] if 'genre' in info else None
    album_artist = info['album_artist'] if 'album_artist' in info else None
    downloads_dir = info["downloadDir"]

    print(f"Setting tags for {filename}...")
    song_path = os.path.join(downloads_dir, f"{info['filename']}.mp3")

    audio_file = eyed3.load(song_path)

    if audio_file is None:
        audio_file = eyed3.core.AudioFile(song_path)
        audio_file.initTag()

    audio_file.tag.title = title
    audio_file.tag.artist = full_artist
    audio_file.tag.album = album

    try:
        year = int(publish_date)
    except ValueError:
        year = None

    if year is not None:
        audio_file.tag.recording_date = eyed3.core.Date(year)
    if album_artist is None:
        audio_file.tag.album_artist = main_artist
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
