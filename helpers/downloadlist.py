import json
import os


def check(link, historyFile, downloadDir):
    try:
        with open(historyFile, 'r') as f:
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


def save(filename, link, historyFile):
    try:
        with open(historyFile, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    downloaded_info = {'filename': filename, 'link': link}
    data.append(downloaded_info)

    with open(historyFile, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')
