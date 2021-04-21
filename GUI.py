import PySimpleGUI as sg
import search
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from utils import *
from pygame import mixer

image_elem = sg.Image(size=(200, 200), data=get_img_data('img/logo.png', maxsize=(200, 200), first=True))



spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

sg.theme('Reddit')

left_column = [
    [
        sg.In(size=(30, 1), enable_events=True, key="query_input"),  # search box
        sg.Button('Search'),  # search button
        sg.Combo([i for i in range(1, 101)], size=(10, 10), key="k", default_value=10),
        sg.Combo(['sum', 'avg', 'max', 'min'], size=(10, 10), key="score_selector", default_value='avg'),
        sg.Combo([i for i in range(1, 10)], size=(10, 10), key="interval_selector", default_value='1')

    ],
    [
        sg.Listbox(
            values=['','','','','','','','','','','','','','Results will appear here'], enable_events=True, size=(70, 30), key="results"  # results
        ),
    ],
]

right_column = [
    [sg.MLine(key='extra_info', size=(70, 30), autoscroll=False)]
    # [sg.Text(size=(60, 30), key="extra_info", text="\n \n \n \n \n \n \n \n \n \n \n \n \n \n")]
]

img_column = [
    [image_elem],
    [sg.Button('Play'),
    sg.Button('Pause')],
    [sg.Button('Open on Spotify')]
]

layout = [
    [
        sg.Column(left_column),
        sg.VSeperator(),
        sg.Column(right_column),
        sg.VSeperator(),
        sg.Column(img_column, element_justification='center')
    ]
]

window = sg.Window("Podcast search", layout)
cprint = sg.cprint
sg.cprint_set_output_destination(window, 'extra_info')
results_available = False
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Search":
        """
        The variable query_result is a list of strings.
        These strings will be shown as a result in the GUI.
        """
        query_result = search.doSearch(values["query_input"], values["score_selector"], values["k"], interval_size = values["interval_selector"])

        if len(query_result.show_episode_names())==0:
            window["results"].update(['','','','','','','','','','','','','' ,'No results were found'])
            results_available=False
        else:
            window["results"].update(query_result.show_episode_names())
            results_available=True
        window["extra_info"].update("\n \n \n \n \n \n \n \n \n \n \n \n \n \n Click on a show episode for extra info")
    if event == 'results':
        if results_available:
            [show_name, episode_name] = values['results'][0].split(" : ")
            window["extra_info"].update("")

            query_result.print_description(cprint, show_name, episode_name, spotify)
            query_result.update_preview(show_name, episode_name, spotify)

            image_elem.update(data=get_img_data("img/tmp.jpg", maxsize=(200, 200), first=True))

            window["extra_info"].set_vscroll_position(0)

    if event == 'Play':
        mixer.init()
        mixer.music.load("img/tmp.mp3")
        mixer.music.play()
    
    if event == 'Pause':
        mixer.music.pause()

    if event == 'Open on Spotify':
        query_result.openurl()

window.close()