import PySimpleGUI as sg
import search

sg.theme('DarkGreen')  # Add a touch of color
left_column = [
    [
        sg.In(size=(50, 1), enable_events=True, key="query_input"),  # search box
        sg.Button('Search'),  # search button
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
# Run the Event Loop
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
        query_result = search.doSearch(query)
        window["results"].update(query_result[0])
        window["extra_info"].update("\n \n \n \n \n \n \n \n \n \n \n \n \n \n Click on a transcript for extra info")
    if event == 'results':
        print("ok")
        ind = (query_result[0].index(values['results'][0]))
        window["extra_info"].update(query_result[1][ind])

window.close()
