from pytube import YouTube
from pydub import AudioSegment
import os
from pytube.exceptions import RegexMatchError, ExtractError, VideoUnavailable
from config import configs


def download(link, title, filename):
    # Create a YouTube object from the link
    try:
        print(f'[Pytube] Accessing {title} ({link})')
        yt = YouTube(link)
    except (RegexMatchError, ExtractError, VideoUnavailable) as e:
        raise Exception(
            f"Unable to create YouTube object for {title} ({link}): {str(e)}")

    try:
        print(f'[Pytube] Looking for audio streams for {title} ({link})')
        try:
            audio_stream = yt.streams.filter(
                only_audio=True).order_by('abr').desc().first()
            if audio_stream is None:
                raise ValueError(
                    f"[Pytube] Couldn't find an audio stream for {title} ({link})")
        except (VideoUnavailable, ValueError) as e:
            raise Exception(
                f"[Pytube] Error finding audio stream for {title} ({link}): {str(e)}")
    except RegexMatchError as e:
        raise Exception(
            f"[Pytube] Error finding audio stream for {title} ({link}): {str(e)}") from None

    # Download the audio stream and save it as a webm file
    output_directory = configs.downloads_dir
    os.makedirs(output_directory, exist_ok=True)
    print(f"Downloading {filename}...")
    audio_path = audio_stream.download(
        output_path=output_directory, filename=f'{filename}.webm')
    print(f"Done downloading {filename}!")

    # Convert webm to mp3
    print(f"Converting {filename} to mp3...")
    mp3_filename = f"{filename}.mp3"
    mp3_path = os.path.join(output_directory, mp3_filename)
    try:
        audio = AudioSegment.from_file(audio_path, format='webm')
        audio.export(mp3_path, format='mp3')
        print(f"Conversion of {filename} to mp3 complete!")
    except Exception as e:
        raise Exception(f"Error converting {filename} to mp3: {str(e)}")
    finally:
        # Remove the webm file
        os.remove(audio_path)
        print(f"Removed {filename}.webm")
