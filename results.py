from utils import *
import math
import datetime

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

    def print_description(self, cprint, show_name, episode_name):
        show = self.shows[show_name]
        ep = show['episodes'][episode_name]
        cprint(show_name, text_color="dark red")
        cprint(f"Show Description: {show['show_description']} \n", background_color='mint cream')
        cprint(episode_name, text_color="dark red")
        cprint(f"Episode Description: {ep['episode_description']} \n", background_color='mint cream')

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
            episode_name = hit["metadata"]["_source"]["episode_name"]
            episode_description = hit["metadata"]["_source"]["episode_description"]
            show_description = hit["metadata"]["_source"]["show_description"]
            if not show_name in shows:
                shows[show_name] = {'show_name': show_name, 'show_description': show_description, 'episodes': {}}

            if not episode_name in shows[show_name]['episodes']:
                shows[show_name]['episodes'][episode_name] = {'episode_name': episode_name, 'episode_description': episode_description, 'clips': []}

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