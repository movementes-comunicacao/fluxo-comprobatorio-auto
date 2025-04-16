
import re

def remove_emojis(text):
    emoji_pattern = re.compile("[\U0001F600-\U0001F64F"  # Emoticons
                               "\U0001F300-\U0001F5FF"  # Symbols & pictographs
                               "\U0001F680-\U0001F6FF"  # Transport & map symbols
                               "\U0001F700-\U0001F77F"  # Alchemical symbols
                               "\U0001F780-\U0001F7FF"  # Geometric shapes
                               "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               "\U0001F900-\U0001F9FF"  # Supplemental Symbols & Pictographs
                               "\U0001FA00-\U0001FA6F"  # Chess Symbols
                               "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               "\U00002702-\U000027B0"  # Dingbats
                               "\U000024C2-\U0001F251"  # Enclosed characters
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)

def merge_posts(*args):
        result_arr = []
        for obj in args:
                if obj == None:
                        continue
                result_arr.extend(obj)
        for value in result_arr:
                value["description"] = " ".join(remove_emojis(value["description"]).split())
        return result_arr