import threading
import json
import PySimpleGUI as sg
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from bloom_filter import BloomFilter
from graphics import create_layout

sc = SparkContext()
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 10)

bf = BloomFilter()
bf.load_bit_array("bit_array.bin")

false_pos = 0
true_neg = 0
true_pos = 0

inbox = []
spam = []

lock = threading.Lock()  

def process_rdd(rdd):
    global false_pos, true_neg, true_pos

    if rdd.isEmpty():
        return

    lines = list(set(rdd.collect()))

    for line in lines:
        obj = json.loads(line)
        url = obj.get("url", "").strip()
        if not url:
            continue

        is_malicious = bf.check(url)
        link_type = obj.get("label", "").strip()

        with lock:
            if is_malicious:
                spam.append(url)
                if link_type == "good":
                    false_pos += 1
                else:
                    true_pos += 1
            else:
                inbox.append(url)
                if link_type == "good":
                    true_neg += 1

    print(f"FP: {false_pos}, TN: {true_neg}, TP: {true_pos}")


def start_streaming():
    lines = ssc.socketTextStream("localhost", 9999)
    lines.foreachRDD(process_rdd)
    ssc.start()
    ssc.awaitTermination()

def display():
    sg.theme("LightBlue")

    window = sg.Window("Email Inbox Simulator", create_layout(), finalize=True)

    current_folder = "INBOX"

    def refresh_list(folder):
        with lock:
            if folder == "INBOX":
                window["MSG_LIST"].update(list(inbox))
            else:
                window["MSG_LIST"].update(list(spam))
        window["CONTENT"].update("")

    refresh_list(current_folder)

    while True:
        event, values = window.read(timeout=1000)

        if event == sg.WINDOW_CLOSED:
            break

        elif event == "INBOX":
            current_folder = "INBOX"
            refresh_list(current_folder)

        elif event == "SPAM":
            current_folder = "SPAM"
            refresh_list(current_folder)

        elif event == "MSG_LIST":
            selected = values["MSG_LIST"]
            if selected:
                url = selected[0]
                content = f"From: unknown\nSubject: Link\n\nVisit:\n{url}"
                window["CONTENT"].update(content)

        elif event == "__TIMEOUT__":
            refresh_list(current_folder)

    window.close()

if __name__ == "__main__":
    t = threading.Thread(target=start_streaming, daemon=True)
    t.start()

    display()