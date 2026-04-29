import PySimpleGUI as sg

def create_layout():
    sidebar = [
        [sg.Button("Inbox", size=(15, 2), key="INBOX")],
        [sg.Button("Spam", size=(15, 2), key="SPAM")],
    ]

    message_list = [
        [sg.Text("Messages")],
        [sg.Listbox(values=[], size=(50, 20), key="MSG_LIST", enable_events=True)]
    ]

    content_view = [
        [sg.Text("Content")],
        [sg.Multiline(size=(50, 10), key="CONTENT", disabled=True)]
    ]

    layout = [
        [
            sg.Column(sidebar),
            sg.VSeparator(),
            sg.Column(message_list),
            sg.VSeparator(),
            sg.Column(content_view),
        ]
    ]

    return layout