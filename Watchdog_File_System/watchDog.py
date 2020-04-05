from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import time


def check_file_complete(path):
    file_complete = False

    try:
        while not file_complete:
            file_size = os.path.getsize(path)
            time.sleep(0.5)
            if file_size != os.path.getsize(path):
                file_complete = False
            else:
                time.sleep(0.5)
                file_complete = True
    except FileNotFoundError:
        time.sleep(1)

    return file_complete


class MyHandler(FileSystemEventHandler):
    last_file = ""

    def on_modified(self, event):
        if event.src_path != folder_to_track and event.src_path != self.last_file and os.path.exists(event.src_path):
            rename = check_file_complete(event.src_path)
            if rename:
                self.last_file = event.src_path
                filename = event.src_path.split(folder_to_track + "/")[1]
                dst_path = os.path.join(destination_folder, filename)
                os.rename(event.src_path, dst_path)
                print(f"Moved: {filename}")


folder_to_track = "/home/ich/Downloads"
destination_folder = "/home/ich/Desktop/New_Location"
event_handler = MyHandler()

observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
