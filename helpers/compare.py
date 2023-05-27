from fuzzywuzzy import fuzz


def strings(str1, str2, threshold=90):
    # Convert strings to lowercase
    string1 = str1.lower()
    string2 = str2.lower()

    # Calculate the similarity ratio using fuzzywuzzy's token set ratio
    similarity_ratio = fuzz.token_set_ratio(string1, string2)

    # Check if the similarity ratio is above the threshold
    if similarity_ratio >= threshold:
        return True  # Strings are considered similar
    else:
        return False  # Strings are not considered similar
