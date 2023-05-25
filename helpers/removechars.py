import re


def removeAll(text):
    # Define the pattern to match special characters
    pattern = r"[^\w\s]"

    # Remove special characters using regex
    cleaned_text = re.sub(pattern, "", text)

    return cleaned_text


def remove(text):
    # Remove "#" symbol
    cleaned_text = text.replace("#", "")

    # Remove unauthorized Windows filename characters
    cleaned_text = re.sub(r'[<>:"/\\|?*]', "", cleaned_text)

    return cleaned_text
