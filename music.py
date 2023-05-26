import os
import re
import traceback
import sys
import json
from modules.downloaders import ytdlp
from modules.metadata import youtubemd, editor
from modules.metadata.providers import deezermd
from helpers import linkchecker, removechars, playlist, history


def createFiles(downloads_dir, history_file):
    os.makedirs(downloads_dir, exist_ok=True)
    if not os.path.exists(history_file):
        with open(file_path, 'w') as f:
            json.dump([], f)


def readLinks(links_file):
    try:
        with open(links_file, 'r') as f:
            lines = f.readlines()
            if not lines:
                raise Exception(
                    "The links file is empty. Consider adding some YouTube links to it before executing the script")
            split_lines = []
            for line in lines:
                split_items = line.strip().split()
                split_lines.extend(split_items)

            return split_lines

    except FileNotFoundError:
        print(f"The links file does not exist in the current directory. A new file was created. Consider adding some YouTube links to it before executing the script")
        sys.exit(1)


def processLinks(links):
    all_links = []
    for link in links:
        link = link.strip()
        if not linkchecker.validLink(link):
            print(f'{link} is not a valid Youtube/YT Music link. Skipping...')
            continue
        if linkchecker.isPlaylist(link):
            playlist_video_urls = playlist.decouple(link)
            all_links.extend(playlist_video_urls)
        else:
            all_links.append(link)
    return all_links


def downloadSong(link, history_file, downloads_dir):
    if history.check(link=link, historyFile=history_file, downloadDir=downloads_dir):
        print(
            f'Song {link} already exists in the downloads directory. Skipping...')
        return

    try:
        music_id = linkchecker.songId(link)
        info = youtubemd.pytubeFetcher(link)
        metadata = deezermd.getData(
            artist=info['main_artist'], title=info['title'])
        if metadata:
            info.update(metadata)
        info['filename'] = removechars.windows(info['filename'])

        file_path = os.path.join(downloads_dir, f"{info['filename']}.mp3")
        if os.path.exists(file_path):
            print(
                f"Song '{info['filename']}' already exists in the downloads directory. Skipping...")
            history.save(
                filename=info['filename'], link=link, historyFile=history_file)
            return

        ytdlp.download(
            link=link, title=info['title'], filename=info['filename'], directory=downloads_dir, music_id=music_id)

        info['downloadDir'] = downloads_dir
        editor.edit_tags(info)
        history.save(
            filename=info['filename'], link=link, historyFile=history_file)

    except Exception as e:
        print(f"An error occurred while processing link: {link}")
        print(f"Error details: {str(e)}")
        traceback.print_exc()
        return


# Get the current directory
current_dir = os.getcwd()
downloads_dir = os.path.join(current_dir, 'downloads')
history_file = os.path.join(current_dir, 'history.json')
links_file = os.path.join(current_dir, 'links.txt')

createFiles(downloads_dir=downloads_dir, history_file=history_file)
# Read the YouTube Music links from the file
links = readLinks(links_file)

# Array to store all the decoupled video URLs
all_links = processLinks(links)
print(f'{len(all_links)} links loaded.')

# Loop through each link and download the song and metadata
for link in all_links:
    downloadSong(link=link, history_file=history_file,
                 downloads_dir=downloads_dir)
