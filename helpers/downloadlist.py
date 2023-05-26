import json
import os


def check(info):
    link = info["link"]
    downloadDir = info["downloadDir"]
    downloadedDir = info["downloadedDir"]
    try:
        with open(downloadedDir, 'r') as f:
            downloaded_data = json.load(f)
    except:
        return False

    for entry in downloaded_data:
        if entry['link'] == link:
            filename = entry['filename']
            mp3_path = os.path.join(downloadDir, f"{filename}.mp3")
            if os.path.exists(mp3_path):
                return True
            else:
                return False
    return False


def save(info):
    filename = info["filename"]
    link = info["link"]
    downloadedDir = info["downloadedDir"]

    downloaded_info = {'filename': filename, 'link': link}

    try:
        with open(downloadedDir, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(downloaded_info)

    with open(downloadedDir, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')
