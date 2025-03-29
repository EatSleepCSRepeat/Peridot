import tkinter as tk
import os
import json
import requests
from tkinter import simpledialog
from tkinter import messagebox
import shutil
import colorama
colorama.init(strip=False)

__tk_config = {
    "interpreter": "1.1"
}

isIde = 0
isIde_ = 0

def __run_peri_main__():
    global isIde 
    File = simpledialog.askstring("File", "Enter .dot to run.")
    
    if File:
        file_path = os.path.abspath(File)
        cmd = f'python "{os.path.join(".", ".peri", "installations", __tk_config.get("interpreter") + ".py")}" "{file_path}"'
        isIde += 1 
        print(colorama.Style.BRIGHT + colorama.Fore.MAGENTA + "Running Peridot with sesID " + str(isIde) + colorama.Style.RESET_ALL)
        os.system(cmd)

def __run_peri__(version):
    global isIde 
    File = simpledialog.askstring("File", "Enter .dot to run.")
    
    if File:
        file_path = os.path.abspath(File)
        cmd = f'python "{os.path.join(".", ".peri", "installations", version + ".py")}" "{file_path}"'
        isIde += 1 
        print(colorama.Style.BRIGHT + colorama.Fore.MAGENTA + "Running Peridot with sesID " + str(isIde) + colorama.Style.RESET_ALL)
        os.system(cmd)

def __new_project__():
    File = simpledialog.askstring("File", "Enter project name.")
    
    if File:
        cmd = f'python "{os.path.join(".", "init", "initProject.py")}" {File}'
        os.system(cmd)

def load_projects(npl):
    for widget in npl.winfo_children():
        if widget != npl.winfo_children()[0]: 
            widget.destroy()

    projects_dir = ".peri/projects"
    if not os.path.exists(projects_dir):
        return []

    project_folders = [f for f in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, f))]
    project_buttons = []
    
    def rc(event, project_folder):
        def hp():
            project_json_path = os.path.join(projects_dir, project_folder, "project.json")
            if os.path.exists(project_json_path):
                try:
                    with open(project_json_path, "r") as f:
                        project_data = json.load(f)
                    project_data["hidden"] = True
                    with open(project_json_path, "w") as f:
                        json.dump(project_data, f, indent=4)
                    load_projects(npl)
                except Exception as e:
                    print(f"Error hiding {project_json_path}: {e}")

        def delete_project():
            project_path = os.path.join(projects_dir, project_folder)
            dialog = messagebox.askquestion("Are you sure?","Are you sure you wanna delete this project?")
            if dialog == "yes":
                try:
                    shutil.rmtree(project_path)
                    load_projects(npl)
                except Exception as e:
                    print(f"Error deleting {project_path}: {e}")
            else:
                return

        menu = tk.Menu(__app__, tearoff=0)
        menu.add_command(label="Hide", command=hp)
        menu.add_command(label="Delete", command=delete_project)
        menu.post(event.x_root, event.y_root)

    if not os.path.exists(projects_dir):
        return []

    for folder in project_folders:
        project_json_path = os.path.join(projects_dir, folder, "project.json")
        if os.path.exists(project_json_path):
            try:
                with open(project_json_path, "r") as f:
                    project_data = json.load(f)
                    display_name = project_data.get("display", "Untitled")
                    hidden = project_data.get("hidden", False)
                    if not hidden:
                        button = tk.Button(npl, text=display_name, command=lambda p=folder: __run_project(p))
                        button.pack(fill=tk.X, padx=10, pady=5)
                        button.bind("<Button-3>", lambda event, p=folder: rc(event, p))
                        project_buttons.append(button)
            except Exception as e:
                print(f"Error reading {project_json_path}: {e}")

    return project_buttons

def __run_project(project):
    global isIde_
    base_path = os.path.abspath(os.path.join(".peri", "projects"))
    isIde_ += 1 
    print(colorama.Style.BRIGHT + colorama.Fore.MAGENTA + "Running " + str(project) + " with sesID " + str(isIde_) + colorama.Style.RESET_ALL)
    project_path = os.path.join(base_path, project)
    
    if not os.path.exists(project_path):
        raise FileNotFoundError(f"Project directory {project_path} does not exist.")
    
    project_json_path = os.path.join(project_path, "project.json")
    
    if not os.path.exists(project_json_path):
        raise FileNotFoundError(f"{project_json_path} does not exist.")
    
    with open(project_json_path, 'r') as f:
        cfg = json.load(f)
    
    main_script = cfg.get("main")
    if not main_script:
        raise ValueError("The project.json file does not contain a 'main' key.")
    with open(".\\.peri\\config.json", 'r') as fl:
        _cfg = json.load(fl)
    cmd = f"python {os.path.join('.peri', 'installations', _cfg.get('interpreter') + '.py')} {os.path.join(project_path, main_script)}"
    
    os.system(cmd)

def add_interpreter():
    release_version = simpledialog.askstring("Add Interpreter", "Enter the version of the interpreter you want to add:")
    
    if release_version:
        releases_url = f"https://api.github.com/repos/EatSleepCSRepeat/peridot-installations/releases"
        response = requests.get(releases_url)
        
        if response.status_code == 200:
            releases = response.json()
            found = False
            for release in releases:
                if release["tag_name"] == release_version:
                    download_url = release["assets"][0]["browser_download_url"]
                    download_file = os.path.join(".peri", "installations", f"peri.{release_version}.py")
                    with requests.get(download_url, stream=True) as rfile:
                        if rfile.status_code == 200:
                            with open(download_file, "wb") as f:
                                for chunk in rfile.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            print(f"Interpreter {release_version} added successfully.")
                            found = True
                            break
            if not found:
                print(f"No release found for {release_version}.")
        else:
            print(f"Failed to fetch releases. Status code: {response.status_code}")


def app():
    global __app__
    __app__ = tk.Tk()
    __app__.geometry("550x300")
    __app__.title("Peridot Launcher")
    __app__.config(bg='darkgrey')
    
    __app__.wm_iconbitmap(".\\src\\peridot.ico")

    _pady = 5
    isl = tk.Frame(__app__)
    isl.pack(side=tk.LEFT, fill=tk.Y)

    npl = tk.Frame(__app__, width=100)
    npl.pack(side=tk.RIGHT, fill=tk.Y)

    newprojbutton = tk.Button(npl, text="New Peridot project", command=__new_project__)
    newprojbutton.pack(fill=tk.X, padx=10, pady=5)

    installations_path = ".peri\\installations"
    files = [f for f in os.listdir(installations_path) if os.path.isfile(os.path.join(installations_path, f))]

    if __tk_config.get("interpreter"):
        button = tk.Button(isl, text=__tk_config.get("interpreter") + " (Main Interpreter)", command=__run_peri_main__)
        button.pack(fill=tk.X, padx=10, pady=_pady)
    else:
        button = tk.Button(isl, text="No main interpreter")
        button.pack(fill=tk.X, padx=10, pady=_pady)

    add_interpreter_button = tk.Button(isl, text="Add Interpreter", command=add_interpreter)
    add_interpreter_button.pack(fill=tk.X, padx=10, pady=_pady)

    for file in files:
        version = file[:-3]
        button = tk.Button(isl, text=version, command=lambda v=version: __run_peri__(v))
        button.pack(fill=tk.X, padx=10, pady=_pady)

    _pady += 5

    load_projects(npl)

    def refresh_projects():
        load_projects(npl)
        __app__.after(1000, refresh_projects)

    __app__.after(1000, refresh_projects)

    __app__.mainloop()
