import threading
import json
import PySimpleGUI as sg
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from bloom_filter import BloomFilter
from graphics import create_layout
from utils import bloom_filter_args


sc = SparkContext()
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 10)



hash_algo, bit_array_path = bloom_filter_args()
bf = BloomFilter(hash_algorithm=hash_algo)
bf.load_bit_array(bit_array_path)

false_pos = 0
false_neg = 0
true_neg = 0
true_pos = 0

inbox = []
spam = []

lock = threading.Lock() # Using threading in order to run GUI and Bloom Filter at the same time
window = None 

def process_rdd(rdd):
    '''
    Processes each line in JSON file used for streaming.
    It will check each URL against the Bloom Filter to determine
    if it is malicious or not, and update accurate FP, TP, FN, TN 
    counts to measure accuracy.

    Also populates "new_inbox" and "new_spam" lists according to 
    classifications to update the GUI.
    '''
    global false_pos, false_neg, true_neg, true_pos

    if rdd.isEmpty():
        return

    lines = list(set(rdd.collect()))

    new_inbox = []
    new_spam = []

    # Go through all links in batch to check against Bloom Filter
    for line in lines:
        obj = json.loads(line)
        url = obj.get("url", "").strip()
        if not url:
            continue

        is_malicious = bf.check(url)
        link_type = obj.get("label", "").strip()

        with lock:
            if is_malicious:
                new_spam.append(url)
                if link_type == "good":
                    false_pos += 1
                else:
                    true_pos += 1
            else:
                new_inbox.append(url)
                if link_type == "good":
                    true_neg += 1
                else:
                    false_neg += 1
    
    # Update Inbox and Spam after batch is proccessed.
    with lock: 
        inbox.extend(new_inbox)
        spam.extend(new_spam)
    
    if window is not None:
        window.write_event_value("NEW_DATA", {
            "inbox": new_inbox,
            "spam": new_spam
        })

    print(f"FP: {false_pos}, FN: {false_neg}, TN: {true_neg}, TP: {true_pos}")


def start_streaming():
    '''
    Starts SocketTextStream and calls process_rdd() on every line in JSON
    '''
    lines = ssc.socketTextStream("localhost", 9999)
    lines.foreachRDD(process_rdd)
    ssc.start()
    ssc.awaitTermination()

def display():
    '''
    Code for GUI, includes features for refreshing lists and 
    switching between folders
    '''
    sg.theme("LightBlue")

    window = sg.Window("Email Inbox", create_layout(), finalize=True)

    current_folder = "INBOX"

    displayed_inbox = []
    displayed_spam = []

    def refresh_list(folder):
        '''
        Updates the displayed Message List with new data processed 
        by the Bloom Filter
        '''
        with lock:
            if folder == "INBOX":
                window["MSG_LIST"].update(list(inbox))
            else:
                window["MSG_LIST"].update(list(spam))
        window["CONTENT"].update("")

    refresh_list(current_folder)

    while True:
        '''
        Loop to constantly display and update graphics.
        Keeps track of events like "INBOX", "SPAM", "MSG_LIST",
        "NEW_DATA" and "__TIMEOUT__" to handle updates properly.
        '''
        event, values = window.read(timeout=1000)

        if event == sg.WINDOW_CLOSED:
            break

        elif event == "INBOX": # Switches current folder to INBOX
            current_folder = "INBOX"
            refresh_list(current_folder)

        elif event == "SPAM": # Switches current folder to SPAM
            current_folder = "SPAM"
            refresh_list(current_folder)

        elif event == "MSG_LIST": # Selects message to view
            selected = values["MSG_LIST"]
            if selected:
                url = selected[0]
                content = f"From: unknown\nSubject: Link\n\nVisit:\n{url}"
                window["CONTENT"].update(content)
        
        elif event == "NEW_DATA": # Updates all lists when new data comes in
            data = values[event]
            if current_folder == "INBOX" and data["inbox"]:
                current_values = window["MSG_LIST"].get_list_values()
                window["MSG_LIST"].update(current_values + data["inbox"])
            elif current_folder == "SPAM" and data["spam"]:
                current_values = window["MSG_LIST"].get_list_values()
                window["MSG_LIST"].update(current_values + data["spam"])

        elif event == "__TIMEOUT__": # Refreshes list after a certain amount of time
            refresh_list(current_folder)

    window.close()

if __name__ == "__main__":
    '''
    Start streaming and display
    '''
    t = threading.Thread(target=start_streaming, daemon=True)
    t.start()

    display()