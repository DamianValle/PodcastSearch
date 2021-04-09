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
        cprint(f"Show: {show_name}", text_color="dark red")
        cprint(f"Show Description: {show['show_description']} \n", background_color='mint cream')
        cprint(f"Episode: {episode_name}", text_color="dark red")
        cprint(f"Episode Description: {ep['episode_description']} \n", background_color='mint cream')

        cprint("CLIPS:  \n", text_color="dark blue")
        for t in ep["clips"]:
            cprint(t, background_color='mint cream')
            cprint("\n\n")


    @staticmethod
    def createFromSearch(res, time=None, search_word=None):
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
                  
            for item in hit["_source"]["clips"]:
                if search_word in item['transcript']:
                    shows[show_name]['episodes'][episode_name]['clips'].append(item["transcript"])


        return Results(time, shows)
    
