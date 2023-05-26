
from difflib import SequenceMatcher


def strings(str1, str2):
    # Create a SequenceMatcher object with the two strings
    matcher = SequenceMatcher(None, str1, str2)

    # Get the ratio of similarity between the strings (ranges from 0 to 1)
    similarity_ratio = matcher.ratio()

    # Define a threshold for equality (adjust as needed)
    equality_threshold = 0.9

    # Compare the similarity ratio with the equality threshold
    if similarity_ratio >= equality_threshold:
        return True  # Strings are considered equal
    else:
        return False  # Strings are not considered equal
