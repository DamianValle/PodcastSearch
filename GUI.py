import PySimpleGUI as sg
import search

sg.theme('DarkBlue13')  # Add a touch of color
left_column = [
    [
        sg.In(size=(50, 1), enable_events=True, key="query_input"),  # search box
        sg.Button('Search'),  # search button
        sg.Combo([i for i in range(1, 101)], size=(10, 10), key="k", default_value=10),
        sg.Text(" results")
    ],
    [
        sg.Listbox(
            values=['','','','','','','','','','','','','',' Results will appear here'], enable_events=True, size=(60, 30), key="results"  # results
        ),
    ],
]

right_column = [
    [sg.Text(size=(60, 30), key="extra_info", text="\n \n \n \n \n \n \n \n \n \n \n \n \n \n")]
]
layout = [
    [
        sg.Column(left_column),
        sg.VSeperator(),
        sg.Column(right_column),
    ]
]

window = sg.Window("Podcast search", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Search":
        query = values["query_input"]
        """
        The variable query_result is a list of strings.
        These strings will be shown as a result in the GUI.
        """
        query_result = search.doSearch(query, values["k"])
        window["results"].update(query_result["results"])
        window["extra_info"].update("\n \n \n \n \n \n \n \n \n \n \n \n \n \n Click on a transcript for extra info")
    if event == 'results':
        print("ok")
        ind = (query_result["results"].index(values['results'][0]))
        window["extra_info"].update(query_result["extraInfo"][ind])

window.close()
