# RVSL4 - Modular Windows Post Exploit Framework

# Description

RVSL4 is a modular framework designed for electronic surveillance actions on computers running the Windows OS. It enables flexible and customizable post-exploitation, offering a set of tools to monitor activities and collect information remotely. RVSL4 is intended for surveillance purposes only and must be used in compliance with applicable laws and regulations.

RVSL4 does not support multi-threading.

# ADDONS INTERNES

    - DESKTOP : Opens a server to receive the client's desktop stream in real-time.
    - WEBCAM : Opens a server to receive the client's webcam stream in real-time. (60 FPS)

# ADDONS EXTERNES

    - KLOG : Tracks keystrokes to analyze user interactions.
    - AUTOSCP : Automatically captures desktop screenshots at adjustable intervals and exfiltrates them to Discord with webhook.
    - DESKSCP : Captures desktop and webcam screenshots and exfiltrates them to Discord with webhook.
    - DWINDEF : Disables Windows Defender.
    - STLINFOS : Steals information and Discord tokens with Creal.

# USAGE

Start the C2 server with the following commands :

    python rvsl4.py <IP/DDNS> <PORT>
    Example : python rvsl4.py sha78221662145822.ddns.net 5555

![2](https://github.com/user-attachments/assets/f0179195-733e-4332-9c8b-04dfaa926c20)

Edit connection informations in the client file (cli.py) with the same IP or DDNS used to start the server to ensure your client connects correctly to your RVSL4 C2 server.

![3](https://github.com/user-attachments/assets/742a4f1a-07b4-41cb-82ac-382315cc6dc1)

# OBFUSCATION

It is recommended to obfuscate your client file before building it to bypass antivirus detection. 
There is no single best obfuscation technique as it depends on the antivirus software used by your targets and the strength and method of your obfuscation.
There are many ways to obfuscate code, but here is a basic approach.

- With python modules

      pip install pyarmor            https://pypi.org/project/pyarmor/
      pip install PyObfuscator       https://pypi.org/project/PyObfuscator/

- With web tools

      https://pyobfuscate.com/
      https://development-tools.net/python-obfuscator/
      https://freecodingtools.org/py-obfuscator
      https://pyob.oxyry.com/

- With Github ressources

      https://github.com/billythegoat356/Hyperion
      https://github.com/billythegoat356/Kramer
      https://github.com/spicesouls/onelinepy
      https://github.com/davidteather/python-obfuscator

# BUILD

Once obfuscated, build your client file into an executable (cli.exe). Command to build via pyinstaller : pyinstaller --onefile --windowed FILE_NAME.py

![6](https://github.com/user-attachments/assets/2de6aaf8-0a12-4131-96e3-83cfe54d9e00)
![9](https://github.com/user-attachments/assets/bd435dfa-870b-4aa3-8dcf-b73e701adfd6)

After building, go to the 'dist' directory where your cli.EXE executable will be located.
Follow the same building and obfuscation procedure if you want to use EXTERNAL ADDONS, so they can be uploaded and launched directly from the C2.

![10](https://github.com/user-attachments/assets/344342f0-5ca7-4c2c-b084-076bef03aa8d)
![11](https://github.com/user-attachments/assets/bad05ac7-a7c4-4ccb-8ea3-aadbae7fe334)

# COMMANDES

        //  exec            ->  Run external command or local file 
        //  start           ->  Start file from client machine (exe, txt, pdf, odt, etc..)
        //  check           ->  Check if client machine is connected to internet                                             
        //  browse          ->  Open an website on client machine browser
        //  download        ->  Download file from client machine 
        //  upload          ->  Upload file to client machine  
        //  kill            ->  Kill the connection with client machine 


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

        // webcam           ->  Remote webcam [DIRECT 60FPS] [NO GUI]
        // desktop          ->  Remote desktop [DIRECT 60FPS] [NO GUI]

        // dwd              ->  Disable Windows Defender AV [Real-Time Protect]
        // stlinfos         ->  Steal discord token | browser passwords | cookies | mail and others informations [Webhook ONLY]
        // deskscp          ->  Steal session name | desktop name | ip | camera and desktop screenshot [Webhook ONLY] [AUTO-MODE AVAILABLE]
        // autoscp          ->  Take a desktop screenshot every minute [Webhook ONLY] [AUTO-MODE]
        // klog             ->  Enable keylogger server


https://github.com/user-attachments/assets/b17b45fa-4e8d-47e0-a9e6-9901eab7d3b3

# ABOUT 📑

Buy me a Coffee ☕️ ETH ARBITRUM ONLY 0xCeB10eEC23826DdCb14397dB855B9302D36822bE
If you would like to contribute to the development of the project, please contact me on my Telegram @makaki22 

MIT License

Copyright (c) [2024] [SUPERPOSE INT]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:


