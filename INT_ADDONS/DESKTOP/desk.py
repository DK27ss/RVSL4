import socket
import pyautogui
import pickle
import struct
import cv2
import numpy as np

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '127.0.0.1' 
port = 8585
client_socket.connect((host_ip, port))

while True:
    try:
        # Capture screenshot
        screenshot = pyautogui.screenshot()
        # Convert the image into numpy array representation
        frame = np.array(screenshot)
        # Convert the BGR image into RGB image
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Serialize frame
        data = pickle.dumps(frame)
        # Send the length of the serialized data first
        message_size = struct.pack("Q", len(data))
        # Then data
        client_socket.sendall(message_size + data)
    except (BrokenPipeError, ConnectionResetError):
        print("Server connection was closed, exiting.")
        break

client_socket.close()
