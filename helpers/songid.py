import re


def getter(link):
    pattern = r"(?:youtu\.be\/|youtube(?:music)?\.com\/(?:embed\/|v\/|watch\?.*v=|shorts\/|music\/|attribution_link\?.*v=))([\w-]{11})"
    match = re.search(pattern, link)
    return match.group(1) if match else None
