import os
import re
import traceback
import sys
import json
from pathlib import Path
from modules.downloaders import ytdlp
from modules.metadata import youtubemd, editor
from modules.metadata.providers import deezermd
from helpers import linkchecker, removechars, playlist, library
from config import configs


def createFiles():
    os.makedirs(configs.downloads_dir, exist_ok=True)
    if not os.path.exists(configs.library_file):
        with open(file_path, 'w') as f:
            json.dump([], f)


def readLinks():
    try:
        with open(configs.links_file, 'r') as f:
            lines = f.readlines()
            if not lines:
                raise Exception(
                    "[script] The links file is empty. Consider adding some YouTube links to it before executing the script")
            split_lines = []
            for line in lines:
                split_items = line.strip().split()
                split_lines.extend(split_items)

            return split_lines

    except FileNotFoundError:
        print(f"[script] the links file does not exist in the current directory. A new file was created. Consider adding some YouTube links to it before executing the script")
        sys.exit(1)


def processLinks(links):
    all_links = []
    for link in links:
        link = link.strip()
        if not linkchecker.validLink(link):
            print(
                f'[script] {link} is not a valid Youtube/YT Music link. Skipping...')
            continue
        if linkchecker.isPlaylist(link):
            playlist_video_urls = playlist.decouple(link)
            all_links.extend(playlist_video_urls)
        else:
            all_links.append(link)
    return all_links


def downloadSong(link):
    if library.check(link=link):
        print(
            f'[script] song {link} already exists in the downloads directory. Skipping...')
        return

    try:
        music_id = linkchecker.songId(link)
        info = youtubemd.pytubeFetcher(link)
        metadata = deezermd.getData(
            artist=info['main_artist'], features=info['featured_artists'], title=info['title'])
        if metadata:
            info.update(metadata)
        info['filename'] = removechars.windows(info['filename'])

        file_path = os.path.join(
            configs.downloads_dir, f"{info['filename']}.mp3")
        if os.path.exists(file_path):
            print(
                f"[script] song '{info['filename']}' already exists in the downloads directory. Skipping...")
            library.save(
                filename=info['filename'], link=link)
            return

        ytdlp.download(
            link=link, title=info['title'], filename=info['filename'], music_id=music_id)

        info['downloadDir'] = configs.downloads_dir
        editor.edit_tags(info)
        library.save(filename=info['filename'], link=link)

    except Exception as e:
        print(f"[script] an error occurred while processing link: {link}")
        print(f"Error details: {str(e)}")
        traceback.print_exc()
        return


createFiles()
links = readLinks()
library.clean_inexistent()
all_links = processLinks(links)
print(f'[script] {len(all_links)} links loaded.')
# Loop through each link and download the song and metadata
for link in all_links:
    downloadSong(link=link)
