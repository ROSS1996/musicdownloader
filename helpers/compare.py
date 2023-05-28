from fuzzywuzzy import fuzz
from config.configs import devmode


def strings(str1, str2, threshold=90):
    # Convert strings to lowercase
    string1 = str1.lower()
    string2 = str2.lower()

    # Calculate the similarity ratio using fuzzywuzzy's token set ratio
    similarity_ratio = fuzz.token_set_ratio(string1, string2)

    # Check if the similarity ratio is above the threshold
    if similarity_ratio >= threshold:
        if devmode:
            print(
                f"[string-compare] {str1} is similar to {str2} / similarity ratio {similarity_ratio}")
        return True  # Strings are considered similar
    else:
        if devmode:
            print(
                f"[string-compare] {str1} is not similar to {str2} / similarity ratio {similarity_ratio}")
        return False  # Strings are not considered similar
