from flask import Flask
from flask_socketio import SocketIO
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables to hold the last lines of the files
last_lines = {
    'logs': '',
    'motors': '',
    'status': ''
}

file_paths = {
    'logs': 'C:\\xampp\\htdocs\\dashboard_ros\\storage\\app\\Logs.txt',
    'motors': 'C:\\xampp\\htdocs\\dashboard_ros\\storage\\app\\Motors.txt',
    'status': 'C:\\xampp\\htdocs\\dashboard_ros\\storage\\app\\Status.txt'
}

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path, socket_name):
        self._file_path = file_path
        self._socket_name = socket_name
        self.update_last_line()

    def on_modified(self, event):
        if event.src_path == self._file_path:
            self.update_last_line()

    def update_last_line(self):
        global last_lines
        with open(self._file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                new_last_line = lines[-1].strip()
                if new_last_line != last_lines[self._socket_name]:
                    last_lines[self._socket_name] = new_last_line
                    socketio.emit(f'file_changed_{self._socket_name}', {'data': new_last_line})

def monitor_file(file_path, socket_name):
    event_handler = FileChangeHandler(file_path, socket_name)
    observer = Observer()
    observer.schedule(event_handler, path='C:\\xampp\\htdocs\\dashboard_ros\\storage\\app', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

@app.route('/')
def index():
    return "File change notification server"

if __name__ == '__main__':
    threads = []
    for socket_name, path in file_paths.items():
        thread = threading.Thread(target=monitor_file, args=(path, socket_name))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    socketio.run(app, debug=True)
