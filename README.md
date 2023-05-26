# Music Downloader

The Music Downloader is a Python script that allows you to download songs from YouTube Music and retrieve metadata from Deezer. It automates the process of downloading songs and editing their metadata tags.

## Prerequisites

Before using the Music Downloader, make sure you have the following installed:

- Python 3.x

## Getting Started

1. Clone the repository or download the script files to your local machine.

2. Ensure you have a file named `links.txt` in the same directory as the script. This file should contain a list of YouTube Music links, each on a separate line.

3. Run the script by executing the following command in the terminal:

```bash
    python music.py
```

4. The script will iterate over each link in links.txt, download the corresponding song, and retrieve metadata from Deezer.

5. The downloaded songs will be stored in a downloads folder (created automatically if it doesn't exist) in the same directory as the script.

6. The script will also edit the metadata tags (title, artist, album, etc.) of the downloaded songs using the retrieved metadata from Deezer.

## Dependencies

Make sure you have the script dependencies installed before running the script. You can install them using pip:

```bash
    pip install -r requirements.txt
```

## Limitations

- The script assumes that the provided YouTube Music links are valid and point to the desired songs. Ensure that the links in links.txt are correct and accessible.

- The script retrieves song metadata from Deezer based on the main artist and title. Please note that the accuracy and availability of metadata may vary.
