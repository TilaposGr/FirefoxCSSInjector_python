import tkinter as tk
from tkinter import filedialog
import os
import shutil
from tkinter import messagebox

root = tk.Tk()

selected_css = ""
selected_ccss = ""
selected_folder = ""

css_label = tk.Label(root, text="No file selected")
css_label.pack()
ccss_label = tk.Label(root, text="No file selected")
ccss_label.pack()
folder_label = tk.Label(root, text="No folder selected")
folder_label.pack()


root.title("Firefox CSS Injector")
root.geometry("400x300")

def configure_chrome():
    path = os.path.join(selected_folder, "chrome")

    if not os.path.exists(path):
        os.makedirs(path)
        print("Chrome folder created!")
    else:
        print("Chrome folder already exists.")

def enable_config(folder_path):
    if not folder_path:
        print("No folder selected!")
        return

    target_file = os.path.join(folder_path, "user.js")
    pref_to_add = 'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);'

    already_enabled = False
    if os.path.exists(target_file):
        with open(target_file, "r") as f:
            if pref_to_add in f.read():
                already_enabled = True

    # If not found, add it
    if not already_enabled:
        with open(target_file, "a") as f:
            f.write(f"\n{pref_to_add}\n")
        print("Preference added to user.js!")
    else:
        print("Preference already exists.")

    if os.path.exists(target_file):
        with open(target_file, "r") as f:
            if pref_to_add in f.read():
                print("Setting already found! No change needed.")
                return

def import_css():
    global selected_css
    # This opens the "Open File" window
    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select your userChrome.css file",
        filetypes=(("userChrome.css", "userChrome.css"), ("all files", "*.*"))
    )
    if file_path:
        selected_css = file_path
        css_label.config(text=f"Selected: {file_path}")

    if file_path:
        print(f"User selected: {file_path}")

def import_ccss():
    global selected_ccss
    # This opens the "Open File" window
    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select your userContent.css file",
        filetypes=(("userContent.css files", "userContent.css"), ("all files", "*.*"))
    )
    if file_path:
        selected_ccss = file_path
        ccss_label.config(text=f"Selected: {file_path}")

    if file_path:
        print(f"User selected: {file_path}")

def select_profile():
    global selected_folder
    # This opens the "Open File" window
    file_path =  filedialog.askdirectory(initialdir=os.path.join(os.getenv('APPDATA'), "Mozilla/Firefox/Profiles"))
    if file_path:
        selected_folder = file_path
        folder_label.config(text=f"Selected: {file_path}")
    if file_path:
        print(f"User selected: {file_path}")

def css_injector():
    chrome_dir = os.path.join(selected_folder, "chrome")
    destination_path = os.path.join(chrome_dir, "userChrome.css")
    shutil.copy(selected_css, destination_path)

def ccss_injector():
    chrome_dir = os.path.join(selected_folder, "chrome")
    destination_path = os.path.join(chrome_dir, "userContent.css")
    shutil.copy(selected_ccss, destination_path)
    if css_injector:
        print("Injection complete!")
        messagebox.showinfo("Success", "Parfait injected successfully!\n\nPlease restart Firefox to apply changes.")

def on_click():
    print("Injection started!")
    enable_config(selected_folder)
    configure_chrome()
    css_injector()
    ccss_injector()

label = tk.Label(root, text="Firefox CSS Injector", font=("Arial", 12))
label.pack(pady=10)

import_button = tk.Button(root, text="Select userChrome.css", command=import_css)
import_button.pack(pady=10)
import_button = tk.Button(root, text="Select userContent.css", command=import_ccss)
import_button.pack(pady=10)
import_button = tk.Button(root, text="Select Firefox Profile", command=select_profile)
import_button.pack(pady=10)
import_button = tk.Button(root, text="Inject", command=on_click)
import_button.pack(pady=10)



#loop
root.mainloop()
