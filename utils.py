from pprint import pprint
import datetime
from PIL import Image, ImageTk
import io
import re

def get_img_data(f, maxsize=(1200, 850), first=False):
    """
    Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

def find_time(search_word, item):
    for word_item in item["words"]:
        if word_item["word"] == search_word:
            #print(item["transcript"])
            #print("Start time:\t{}s\nEnd Time:\t{}s\n\n\n".format(parse_time(word_item["startTime"]), parse_time(word_item["endTime"])))
            pass

def parse_time(time_str):
    return float(time_str[:-1])

def parse_filename2uri(filename):
    """
    Parser utility
    filename: "../podcasts-no-audio-13GB/spotify-podcasts-2020-summarization-testset/podcasts-transcripts-summarization-testset/1/A/show_1aSZnvp5sO3y6XkSHSFhw0/2jvWqUD1asYvFsDAFsozkZ.json"
    output: "1aSZnvp5sO3y6XkSHSFhw0, 2jvWqUD1asYvFsDAFsozkZ"
    output: show_uri, episode_uri
    """
    return filename.split("_")[1][:-5].split("/")[0], filename.split("_")[1][:-5].split("/")[1]

def seconds_to_time(seconds):
    return str(datetime.timedelta(seconds=round(parse_time(seconds))))

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "[^\x00-\x7F]+")
    return regrex_pattern.sub(r'',text)