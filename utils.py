import json
from pprint import pprint

def find_time(search_word, item):
    pprint(search_word)
    print(item["transcript"])
    for word_item in item["words"]:
        if word_item["word"] == search_word:
            print("Start time: {}s\tEnd Time: {}s".format(parse_time(word_item["startTime"]), parse_time(word_item["endTime"])))
    print("\n")

def parse_time(time_str):
    return float(time_str[:-1])

def parse_filename2uri(filename):
    """
    Parser utility
    filename: "../podcasts-no-audio-13GB/spotify-podcasts-2020-summarization-testset/podcasts-transcripts-summarization-testset/1/A/show_1aSZnvp5sO3y6XkSHSFhw0/2jvWqUD1asYvFsDAFsozkZ.json"
    output: "1aSZnvp5sO3y6XkSHSFhw0"
    """
    return filename.split("_")[1][:-5].split("/")[0]
