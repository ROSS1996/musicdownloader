import os
import traceback
import re
from modules.downloaders import pytubedownloader, youtubedldownloader, ytdlpdowloader
from modules.metadata import youtubemd, deezermd, editor
from helpers import songid, removechars

# Create a 'downloads' folder if it doesn't already exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Read in the list of YouTube Music links from a file
with open('links.txt', 'r') as f:
    links = f.readlines()

# Loop through each link and download the song and metadata
for link in links:
    try:
        music_id = songid.getter(link)
        info = youtubemd.pytubeFetcher(link)
        metadata = deezermd.getData(info['main_artist'], info['title'])
        if metadata:
            info.update(metadata)
        filename = removechars.remove(info['filename'])
        title = info['title']
        album = info['album']
        full_artist = info['full_artist']
        main_artist = info['main_artist']
        thumbnail_url = info['thumbnail_url']
        publish_date = info['publish_date']
        # Set genre, position, and disc variables
        genre = info['genre'] if 'genre' in info else None
        position = position = info['position'] if 'genre' in info else None
        disc = disc = info['disc'] if 'genre' in info else None

        ytdlpdowloader.download(link, title, filename, music_id)
        editor.edit_tags(filename, title, full_artist, main_artist,
                         album, thumbnail_url, publish_date, genre, position, disc)

    except Exception as e:
        print(f"An error occurred while processing link: {link}")
        print(f"Error details: {str(e)}")
        traceback.print_exc()
        continue
