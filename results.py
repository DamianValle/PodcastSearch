from utils import *
import math
import datetime
import pprint
import requests

class Results:
    time = None
    shows = None

    def __init__(self, time=None, shows=None):
        self.time = time
        self.shows = shows

    def show_episode_names(self):
        return [(show['show_name'] +" : "+ episode['episode_name'])  for show in self.shows.values() for episode in show['episodes'].values()]

    def string_description(self, show_name, episode_name):
        show = self.shows[show_name]
        ep = show['episodes'][episode_name]
        return f'''
        Show: {show_name}
        Show Description: {show['show_description']}

        Episode: {episode_name}
        Episode Description: {ep["episode_description"]}

        Transcripts:
        {" : ".join(ep["clips"])}
        '''

    def update_preview(self, show_name, episode_name, spotify):
        show = self.shows[show_name]
        show_uri = show["show_uri"]
        ep = show['episodes'][episode_name]
        episode_uri = ep["episode_uri"]

        try:
            show_results = spotify.show(show_uri, market='US')
            ep_results = spotify.episode(episode_uri, market='US')
            print("show img: ", show_results['images'][0]['url'])
            print("ep img: ", ep_results['images'][0]['url'])

            img_data = requests.get(ep_results['images'][0]['url']).content
            with open('img/tmp.jpg', 'wb') as handler:
                handler.write(img_data)
        
        except Exception as e:
            print(e)

    def print_description(self, cprint, show_name, episode_name, spotify):
        show = self.shows[show_name]
        ep = show['episodes'][episode_name]

        cprint(show_name, text_color="dark red")
        cprint(f"Show Description: {deEmojify(show['show_description'])} \n", background_color='mint cream')
        cprint(episode_name, text_color="dark red")
        cprint(f"Episode Description: {deEmojify(ep['episode_description'])} \n", background_color='mint cream')

        cprint("CLIPS:  \n", text_color="dark blue")
        for clip in ep["clips"]:
            cprint(f"Start time: ", clip['start_time'], background_color='mint cream')
            cprint(f"End time: ", clip['end_time'], background_color='mint cream')
            cprint(clip['transcript'], background_color='mint cream')
            cprint("\n\n")


    @staticmethod
    def createFromSearch(res, time=None, search_word=None, interval_size=1):
        shows = {}
        for hit in res['hits']['hits']:
            show_name = hit["metadata"]["_source"]["show_name"]
            show_description = hit["metadata"]["_source"]["show_description"]
            show_uri = hit["metadata"]["_source"]["show_uri"]
            episode_name = hit["metadata"]["_source"]["episode_name"]
            episode_description = hit["metadata"]["_source"]["episode_description"]
            episode_uri = hit["metadata"]["_source"]["episode_uri"]
            
            if not show_name in shows:
                shows[show_name] = {'show_name': show_name, 'show_description': show_description, 'show_uri': show_uri, 'episodes': {}}

            if not episode_name in shows[show_name]['episodes']:
                shows[show_name]['episodes'][episode_name] = {'episode_name': episode_name, 'episode_description': episode_description, 'clips': [], 'episode_uri': episode_uri}

            clips = hit["_source"]["clips"]
            index = 0
            while(index < len(clips)):
                item = clips[index]
                if search_word in item['transcript']:

                    intervals_start = math.floor((interval_size - 1) / 2)
                    intervals_end = interval_size - intervals_start
                    start_index = max(index - intervals_start, 0)
                    end_index = min(index + intervals_end, len(hit["_source"]["clips"]))
                    transcripts = hit["_source"]["clips"][start_index:end_index]

                    full_transcript = "\n".join(map(lambda t: t["transcript"], transcripts))

                    start_time = seconds_to_time(transcripts[0]["words"][0]["startTime"])
                    end_time = seconds_to_time(transcripts[-1]["words"][-1]["endTime"])

                    shows[show_name]['episodes'][episode_name]['clips'].append({'transcript': full_transcript, 'start_time': start_time, 'end_time': end_time})
                    index = end_index - 1
                index += 1

        return Results(time, shows)