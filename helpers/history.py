import json
import os
import datetime
from helpers import linkchecker


def check(link, historyFile, downloadDir):
    try:
        with open(historyFile, 'r') as f:
            downloaded_data = json.load(f)
    except:
        return False

    for entry in downloaded_data:
        entry_id = linkchecker.songId(entry['link'])
        link_id = linkchecker.songId(link)
        if entry_id == link_id:
            filename = entry['filename']
            mp3_path = os.path.join(downloadDir, f"{filename}.mp3")
            if os.path.exists(mp3_path):
                return True
            else:
                return False
    return False


def save(filename, link, historyFile):
    try:
        with open(historyFile, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%d-%m-%Y %H:%M:%S')

    downloaded_info = {'filename': filename,
                       'link': link, 'datetime': formatted_datetime}
    data.append(downloaded_info)

    with open(historyFile, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')
