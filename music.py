import os
import re
import traceback
import sys
import json
from modules.downloaders import ytdlpdowloader
from modules.metadata import youtubemd, deezermd, editor
from helpers import songid, removechars, playlist, downloadlist

# Get the current directory
current_dir = os.getcwd()
downloads_dir = os.path.join(current_dir, 'downloads')
links_file = os.path.join(current_dir, 'links.txt')
downloaded_file = os.path.join(current_dir, 'downloaded.json')

# Create the 'downloads' folder if it doesn't exist
os.makedirs(downloads_dir, exist_ok=True)

# Check if the downloaded JSON file exists, otherwise create it
if not os.path.exists(downloaded_file):
    with open(downloaded_file, 'w') as f:
        json.dump([], f)

# Read the YouTube Music links from the file
try:
    with open(links_file, 'r') as f:
        links = f.readlines()
except FileNotFoundError:
    print(f"The links file does not exist in the current directory. A new file was created. Consider adding some YouTube links to it before executing the script")
    sys.exit(1)

# Array to store all the decoupled video URLs
all_links = []

# Loop through each link and check if it is a playlist or single video link
for link in links:
    link = link.strip()
    if re.search(r"(playlist|list)", link, re.IGNORECASE):
        # Decouple the playlist link into video URLs
        playlist_video_urls = playlist.decouple(link)
        all_links.extend(playlist_video_urls)
    else:
        all_links.append(link)

print(f'{len(all_links)} links loaded.')

# Loop through each link and download the song and metadata
for link in all_links:
    if downloadlist.check({'link': link, 'downloadedDir': downloaded_file, 'downloadDir': downloads_dir}):
        print(
            f'Song {link} already exists in the downloads directory. Skipping...')
        continue

    try:
        music_id = songid.getter(link)
        info = youtubemd.pytubeFetcher(link)
        metadata = deezermd.getData(info['main_artist'], info['title'])
        if metadata:
            info.update(metadata)
        info['filename'] = removechars.remove(info['filename'])

        file_path = os.path.join(downloads_dir, f"{info['filename']}.mp3")
        if os.path.exists(file_path):
            print(
                f"Song '{info['filename']}' already exists in the downloads directory. Skipping...")
            downloadlist.save(
                {'filename': info['filename'], 'link': link, 'downloadedDir': downloaded_file})
            continue

        ytdlpdowloader.download(
            {'link': link, 'title': info['title'], 'filename': info['filename'], 'directory': downloads_dir, 'music_id': music_id})

        info['downloadDir'] = downloads_dir
        editor.edit_tags(info)
        downloadlist.save(
            {'filename': info['filename'], 'link': link, 'downloadedDir': downloaded_file})

    except Exception as e:
        print(f"An error occurred while processing link: {link}")
        print(f"Error details: {str(e)}")
        traceback.print_exc()
        continue
