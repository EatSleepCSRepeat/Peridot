import os
import json
import tkinter as tk
import ctypes
import sys
import requests
from tkinter import simpledialog

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

ProgramFiles = "."
PeridotPath = os.path.join(ProgramFiles, ".peri")
DownloadDir = os.path.join(PeridotPath, "installations")

os.makedirs(DownloadDir, exist_ok=True)

def get():
    repo_url = "https://api.github.com/repos/EatSleepCSRepeat/peridot-installations/releases/latest"
    response = requests.get(repo_url)
    
    if response.status_code == 200:
        release_data = response.json()
        for asset in release_data['assets']:
            if asset['name'].endswith('.py'):
                return asset['browser_download_url']
    else:
        return None

def download():
    latest_release_url = get()
    
    if latest_release_url:
        python_file_path = os.path.join(DownloadDir, os.path.basename(latest_release_url))
        
        if not os.path.exists(python_file_path):
            response = requests.get(latest_release_url)
            
            if response.status_code == 200:
                with open(python_file_path, 'wb') as file:
                    file.write(response.content)
            else:
                pass
        else:
            pass
    else:
        pass

download()

import periApp
periApp.app()
