from utils import *
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

    def print_description(self, cprint, show_name, episode_name, spotify):
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
            with open('tmp/ep.jpg', 'wb') as handler:
                handler.write(img_data)
        
        except:
            print("URI removed from Spotify.")

        cprint(show_name, text_color="dark red")
        cprint(f"Show Description: {show['show_description']} \n", background_color='mint cream')
        cprint(episode_name, text_color="dark red")
        cprint(f"Episode Description: {ep['episode_description']} \n", background_color='mint cream')

        cprint("CLIPS:  \n", text_color="dark blue")
        for clip_transcript, clip_time in zip(ep["clips"], ep["clip_times"]):
            cprint(f"Start time: ", clip_time, background_color='mint cream')
            cprint(clip_transcript, background_color='mint cream')
            cprint("\n\n")


    @staticmethod
    def createFromSearch(res, time=None, search_word=None):
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
                shows[show_name]['episodes'][episode_name] = {'episode_name': episode_name, 'episode_description': episode_description, 'episode_uri': episode_uri, 'clips': [], 'clip_times': []}
                  
            for item in hit["_source"]["clips"]:
                if search_word in item['transcript']:
                    shows[show_name]['episodes'][episode_name]['clips'].append(item["transcript"])
                    startTime = str(datetime.timedelta(seconds=round(parse_time(item["words"][0]["startTime"]))))
                    shows[show_name]['episodes'][episode_name]['clip_times'].append(startTime)

        return Results(time, shows)