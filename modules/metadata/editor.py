import os
import requests
from mutagen.id3 import ID3, TIT2, TPE1, TYER, TOPE, TPE2, APIC, TALB
from mutagen.id3._util import ID3NoHeaderError


def edit_tags(filename, title, full_artist, main_artist, album, thumbnail_url, publish_date):
    print(f"Setting tags for {filename}...")
    song_path = os.path.join('downloads', f"{filename}.mp3")

    try:
        audio_tags = ID3(song_path)
    except ID3NoHeaderError:
        audio_tags = ID3()

    audio_tags.delete()
    audio_tags["TIT2"] = TIT2(encoding=3, text=title)
    audio_tags["TPE1"] = TPE1(encoding=3, text=full_artist)
    audio_tags["TPE2"] = TPE2(encoding=3, text=main_artist)
    audio_tags["TALB"] = TALB(encoding=3, text=album)
    audio_tags["TYER"] = TYER(encoding=3, text=str(publish_date))

    try:
        thumbnail_data = requests.get(thumbnail_url).content
        audio_tags["APIC"] = APIC(
            encoding=3, mime='image/jpeg', type=3, desc='Cover', data=thumbnail_data)
    except requests.RequestException as e:
        print(f"Error retrieving thumbnail: {str(e)}")

    audio_tags.save(song_path, v1=2, v2_version=3)

    print(f"Tags set for {filename}!")
