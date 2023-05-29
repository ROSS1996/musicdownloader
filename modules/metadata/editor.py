import os
import requests
import eyed3
from config import configs
from config.configs import get_logger

logger = get_logger()


def edit_tags(info):
    if not isinstance(info, dict):
        raise TypeError(
            "[tag-editor] the 'info' argument must be a dictionary")

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
    link = info['url']

    logger.info(
        f"[tag-editor] adding tags to {filename} / Link: {link}")

    if configs.devmode:
        logger.info(
            f"[tag-editor] Tags: {info}")
    try:
        song_path = os.path.join(downloads_dir, f"{filename}.mp3")
        if configs.devmode:
            logger.info(f"[tag-editor] {song_path}")
        audio_file = eyed3.load(song_path)
        if configs.devmode:
            logger.info(
                f"[tag-editor] {song_path} was successfully opened")
    except:
        error_message = f"[tag-editor] the tag editor could not open {song_path}"
        raise Exception(error_message) from None

    if audio_file is None:
        audio_file = eyed3.core.AudioFile(song_path)
        audio_file.initTag()

    audio_file.tag.title = title
    audio_file.tag.artist = full_artist
    audio_file.tag.album = album
    audio_file.tag.album_artist = album_artist if album_artist is not None else main_artist

    try:
        year = int(publish_date)
    except ValueError:
        year = None

    if year is not None:
        audio_file.tag.recording_date = eyed3.core.Date(year)
        audio_file.tag.release_date = eyed3.core.Date(year)
    if genre is not None:
        audio_file.tag.genre = genre
    if position is not None:
        audio_file.tag.track_num = position
    if disc is not None:
        audio_file.tag.disc_num = disc

    try:
        thumbnail_data = requests.get(thumbnail_url).content
        audio_file.tag.images.set(3, thumbnail_data, 'image/jpeg', u"Cover")
        if configs.devmode:
            logger.info(
                f"[tag-editor] {song_path} was successfully opened")
    except requests.RequestException as e:
        logger.error(
            f"[tag-editor] the editor could not download the cover for {song_path} and the song file will be saved without it.")
        if configs.devmode:
            logger.error(
                f"[tag-editor] thumbnail url: {thumbnail_url}")
            logger.errror(f"[tag-editor] cause of the error: {str(e)}")

    audio_file.tag.save()

    logger.info(
        f"[tag-editor] the metadata tags for {filename} were successfully saved.")
