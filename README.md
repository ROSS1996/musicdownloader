# Music Downloader

The Music Downloader is a Python script that allows you to download songs from YouTube Music and retrieve metadata from Deezer. It automates the process of downloading songs and editing their metadata tags.

## Prerequisites

Before using the Music Downloader, make sure you have the following installed:

- Python 3.x
- pip (Python package installer)

## Getting Started

1. Clone the repository or download the script files to your local machine.

2. Ensure you have a file named links.txt in the same directory as the script. This file should contain a list of YouTube Music or YouTube links (playlists supported) to be downloaded. Each link should be on a separate line or separated by spaces within a line.

3. Open the `pythonpip.bat` file if you are on Windows or the `pythonpip.sh` file if you are on Linux/MacOS to install Python 3 and pip in case they aren't. This step is recommended if you are unsure about having Python 3 and pip installed, as the script will not reinstall them if they are already installed.

4. Install the required packages by running the dependencies script. On Windows, open the `dependencies.bat` file. For Linux and MacOS, open the `dependencies.sh` file.

5. Open the ``run.bat`` file if you are on Windows or ``run.sh`` file if you are on Linux/MacOS to start the Music Downloader. The script will iterate over each link in ``links.txt``, download the corresponding song, and retrieve metadata from Deezer. Execute the following command in the terminal:

6. The downloaded songs will be stored in a downloads folder (created automatically if it doesn't exist) in the same directory as the script with all the available information.

## Limitations

- The script assumes that the provided YouTube Music or YouTube links are valid and point to the desired songs. Ensure that the links in `links.txt` are correct and accessible.

- The script retrieves song metadata from Deezer based on the main artist and title. Please note that the accuracy and availability of metadata may vary.

- For best results, it is recommended to use YouTube Music links for downloading songs.
