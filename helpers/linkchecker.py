import re


def validLink(link):
    # Regular expression pattern for matching allowed YouTube/YouTube Music links
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?(?:.*&)?v=[\w-]+|music\.youtube\.com/watch\?(?:.*&)?v=[\w-]+|music\.youtube\.com/playlist\?list=[\w-]+|music\.youtube\.com/shorts/[\w-]+|www\.youtube\.com/embed/[\w-]+|www\.youtube\.com/playlist\?list=[\w-]+)'

    # Check if the link matches the pattern
    match = re.match(pattern, link)

    return match is not None


def isPlaylist(link):
    # Regular expression pattern for matching playlist links
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/playlist\?list=[\w-]+|music\.youtube\.com/playlist\?list=[\w-]+|music\.youtube\.com/watch\?v=[\w-]+&list=[\w-]+)'

    # Check if the link matches the pattern
    match = re.match(pattern, link)

    return match is not None


def removeList(link):
    # Remove 'list' parameter from YouTube link
    pattern = r'(\?|&)list=[^&]+'
    modified_link = re.sub(pattern, '', link)
    return modified_link


def songId(link):
    pattern = r"(?:youtu\.be\/|youtube(?:music)?\.com\/(?:embed\/|v\/|watch\?.*v=|shorts\/|music\/|attribution_link\?.*v=))([\w-]{11})"
    match = re.search(pattern, link)
    return match.group(1) if match else None
