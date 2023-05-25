import os
import pytube

# Create a 'downloads' folder if it doesn't already exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Read in the list of YouTube links from a file
with open('links.txt', 'r') as f:
    links = f.readlines()

# Loop through each link and download the audio
for link in links:
    # Create a YouTube object from the link
    yt = pytube.YouTube(link)

    # Choose the best matching audio stream regardless of format
    audio_stream = yt.streams.filter(
        only_audio=True).order_by('abr').desc().first()

    # Check if audio stream is None, and if so, print an error message and skip to the next link
    if audio_stream is None:
        print(f"No audio stream found for {yt.title}, skipping...")
        continue

    # Download the audio stream and save it to the 'downloads' folder
    print(f"Downloading {yt.title}...")
    audio_stream.download(output_path='downloads')
    print(f"Done downloading {yt.title}!")
