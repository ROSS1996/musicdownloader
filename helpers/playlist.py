import yt_dlp


def decouple(url):
    # Set the options to extract video URLs from the playlist
    ydl_opts = {
        'extract_flat': 'in_playlist',
        'dump_single_json': True,
        'playlist_items': '1-',
    }
    # Create a yt-dlp instance and fetch the playlist information
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(url, download=False)

    # Extract the video URLs from the playlist
    video_urls = [entry['url']
                  for entry in playlist_info['entries'] if entry.get('_type') == 'url']
    return video_urls
