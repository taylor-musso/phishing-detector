import PySimpleGUI as sg

def create_layout():
    '''
    Creates elements for GUI
    '''
    sg.theme("LightGrey1")

    # Top bar (header)
    top_bar = [
        [
            sg.Text("Mail", font=("Helvetica", 16, "bold"), pad=(10, 10)),
            sg.Push(),
        ]
    ]

    # Sidebar (folders)
    sidebar = [
        [sg.Text("Folders", font=("Helvetica", 12, "bold"), pad=(10, 5))],
        [sg.Button("Inbox", size=(18, 2), key="INBOX", button_color=("white", "#1a73e8"))],
        [sg.Button("Spam", size=(18, 2), key="SPAM", button_color=("white", "#d93025"))],
    ]

    # Message list (middle column)
    message_list = [
        [sg.Text("Inbox", font=("Helvetica", 12, "bold"))],
        [
            sg.Listbox(
                values=[],
                size=(40, 20),
                key="MSG_LIST",
                enable_events=True,
                no_scrollbar=False,
                font=("Helvetica", 10)
            )
        ]
    ]

    # Email content (right column)
    content_view = [
        [sg.Text("Message", font=("Helvetica", 12, "bold"))],
        [
            sg.Multiline(
                size=(60, 20),
                key="CONTENT",
                disabled=True,
                font=("Helvetica", 10),
                pad=(5, 5)
            )
        ]
    ]

    # Main layout
    layout = [
        [sg.Column(top_bar, expand_x=True, background_color="#f1f3f4")],
        [
            sg.Column(sidebar, background_color="#f8f9fa", pad=(5, 5)),
            sg.VSeparator(),
            sg.Column(message_list, pad=(5, 5)),
            sg.VSeparator(),
            sg.Column(content_view, pad=(5, 5)),
        ]
    ]

    return layout