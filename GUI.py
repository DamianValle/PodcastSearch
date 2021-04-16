import PySimpleGUI as sg
import search

sg.theme('DarkBlue13')  # Add a touch of color
left_column = [
    [
        sg.In(size=(30, 1), enable_events=True, key="query_input"),  # search box
        sg.Button('Search'),  # search button
        sg.Combo([i for i in range(1, 101)], size=(10, 10), key="k", default_value=10),
        sg.Combo(['sum', 'avg', 'max', 'min'], size=(10, 10), key="score_selector", default_value='avg')

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
layout = [
    [
        sg.Column(left_column),
        sg.VSeperator(),
        sg.Column(right_column)
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
        query_result = search.doSearch(values["query_input"], values["score_selector"], values["k"])

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
            query_result.print_description(cprint, show_name, episode_name)
            # cprint(query_result.string_description(show_name, episode_name), text_color="black", background_color="white")
            window["extra_info"].set_vscroll_position(0)

window.close()
