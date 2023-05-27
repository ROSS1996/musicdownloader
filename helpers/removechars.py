import re


def title(title):
    # Clean title
    title = re.sub(
        r"(?i)\s+(?:ft\.?|feat\.?|featuring|with)\s+.*?(?=\s+-)", "", title)
    title = re.sub(r"\(prod\..*?\)|\(prod\..*?\)$",
                   "", title, flags=re.IGNORECASE)
    title = re.sub(r'\([^)]*\)', '', title)
    title = re.sub(r'\[.*?\]', '', title)

    # Remove emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # Emoticons
                               u"\U0001F300-\U0001F5FF"  # Symbols & Pictographs
                               u"\U0001F680-\U0001F6FF"  # Transport & Map Symbols
                               u"\U0001F1E0-\U0001F1FF"  # Flags (iOS)
                               u"\U00002702-\U000027B0"  # Dingbats
                               u"\U000024C2-\U0001F251"  # Miscellaneous Symbols and Shapes
                               "]+", flags=re.UNICODE)
    title = emoji_pattern.sub(r'', title)

    cleaned_title = title.strip()

    # Escape special characters except '/'
    cleaned_title = re.sub(r'([{}])'.format(
        re.escape(r':*?"<>')), r'\\\1', cleaned_title)

    return cleaned_title


def all(text):
    # Define the pattern to match special characters
    pattern = r"[^\w\s]"

    # Remove special characters using regex
    cleaned_text = re.sub(pattern, "", text)

    return cleaned_text


def windows(text):
    # Remove "#" symbol
    cleaned_text = text.replace("#", "")

    # Remove unauthorized Windows filename characters
    cleaned_text = re.sub(r'[<>:"/\\|?*]', "", cleaned_text)

    return cleaned_text
