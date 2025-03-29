import os
import sys
import json

sys.argv = sys.argv[1:]

if len(sys.argv) >= 1:
    os.makedirs(".peri\\projects\\"+sys.argv[0], exist_ok=True)

    data = {
        "display": sys.argv[0],
        "main": "main.dot",
        "hidden": False
    }

    with open(os.path.join(".peri", "projects", sys.argv[0], "project.json"), 'w') as f:
        json.dump(data, f, indent=4)
    with open(os.path.join(".peri", "projects", sys.argv[0], "main.dot"), 'w') as f:
        f.write("display \"this would be your project!\"")
