import os
import sys
import json
import shutil

sys.argv = sys.argv[1:]

_json = {
    "name": "packname",
    "desc": "This is my Peridot package!",
    "version": "v1.0.0"
}

if len(sys.argv) >= 1:
    dir_path = sys.argv[0]
    
    if os.path.exists(dir_path):
        if not os.path.exists(os.path.join(dir_path, '.git')):
            os.system(f"git init {dir_path}")
        
        json_path = os.path.join(dir_path, ".json")
        if not os.path.exists(json_path):
            with open(json_path, 'w') as f:
                f.write(json.dumps(_json, indent=4))
                if shutil.which("code"):
                    os.system("code " + sys.argv[0])
                else:
                    print("you can open this in any editor manually since you don't have vscode installed.")
