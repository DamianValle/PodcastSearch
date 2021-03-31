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
            values=['/n /n Results will appear here'], enable_events=True, size=(60, 30), key="results"  # results button
        ),
    ],
]

right_column = [
    [sg.Text("Click on a transcript for more info")],
    [sg.Text(size=(40, 1), key="extra_info")],
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
        window["results"].update(query_result)

window.close()
