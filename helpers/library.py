import json
import os
import datetime
from helpers import linkchecker
from config import configs


def clean_inexistent():
    # Create the file if it is not created, create a new empty list
    try:
        with open(configs.library_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    # If there are items in the file, check if they exist in the directory.
    if data:
        data = [entry for entry in data if os.path.exists(
            os.path.join(configs.downloads_dir, f"{entry['filename']}.mp3"))]

    # Save the modified or new (empty) file
    with open(configs.library_file, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')

    return False


def check(link):
    try:
        with open(configs.library_file, 'r') as f:
            downloaded_data = json.load(f)
    except:
        return False

    for entry in downloaded_data:
        entry_id = linkchecker.songId(entry['link'])
        link_id = linkchecker.songId(link)
        if entry_id == link_id:
            filename = entry['filename']
            mp3_path = os.path.join(configs.downloadDir, f"{filename}.mp3")
            if os.path.exists(mp3_path):
                return True
            else:
                return False
    return False


def save(filename, link):
    try:
        with open(configs.library_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%d-%m-%Y %H:%M:%S')

    downloaded_info = {'filename': filename,
                       'link': link, 'datetime': formatted_datetime}
    data.append(downloaded_info)

    with open(configs.library_file, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')
