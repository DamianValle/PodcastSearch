import json
from pprint import pprint

def find_time(search_word, item):
    pprint(search_word)
    for word_item in item["words"]:
        if word_item["word"] == search_word:
            print(item["transcript"])
            print("Start time:\t{}s\nEnd Time:\t{}s\n\n\n".format(parse_time(word_item["startTime"]), parse_time(word_item["endTime"])))

def parse_time(time_str):
    return float(time_str[:-1])