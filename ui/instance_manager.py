import os
import socket
import threading

from PyQt5.QtCore import QLockFile
from PyQt5.QtWidgets import QMessageBox

LOCK_FILE_DIR = os.path.join(os.getcwd(), 'temp')
LOCK_FILE_PATH = os.path.join(LOCK_FILE_DIR, 'app.lock')
PORT_PATH = os.path.join(LOCK_FILE_DIR, 'port.txt')
SERVER_HOST = '127.0.0.1'


class InstanceManager():
    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((SERVER_HOST, 0))
        self.create_directory()
        self.check_single_instance()

    def create_directory(self):
        if not os.path.exists(LOCK_FILE_DIR):
            os.makedirs(LOCK_FILE_DIR)

    def check_single_instance(self):
        self.lock_file = QLockFile(LOCK_FILE_PATH)
        port = self.socket.getsockname()[1]

        if self.lock_file.tryLock():
            with open(PORT_PATH, 'w') as f:
                f.write(str(port))
        else:
            self.send_signal_to_running_instance()
            exit(1)

    def listen_for_signal(self, toggle_main_window):
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            print("Received request from client")
            toggle_main_window()
            client_socket.close()

    def send_signal_to_running_instance(self):
        with open(PORT_PATH, 'r') as f:
            server_port = int(f.read())

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, server_port))
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")
        client_socket.close()

    def show_alert(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()
