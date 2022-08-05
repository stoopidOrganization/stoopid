import tkinter as tk, os
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from urllib import request

root = tk.Tk()
root.title("Stoopid Installer")
root.resizable(False, False)
root.geometry(f'500x300+{int(root.winfo_screenwidth() / 2 - 275)}+{int(root.winfo_screenheight()/2 - 175)}')
foldername = ""
download = "https://github.com/kruemmelbande/stoopid/raw/main/stoopid.exe"

def start_install():
    global foldername
    try:
        os.system(f'cd {foldername} && rmdir stoopid /s /q')
    except:
        pass

    try:
        os.system(f'cd {foldername} && mkdir stoopid')
        local_file = f'{foldername}/stoopid/stoopid.exe'
        request.urlretrieve(download, local_file)
        path = os.getenv('path')
        paths = path.split(';')
        folder = '\\'.join(foldername.split('/')) + '\\stoopid'
        if not folder in paths:
            os.system(f'setx PATH "{folder}"')
            os.system(f'setx STOOPID {folder}')

        showinfo('Success', 'Installation finished!')

    except Exception:
        showinfo('Error', 'Installation failed!')

def select_file():
    global foldername
    foldername = fd.askdirectory(title='Open a file', initialdir=os.getenv('LocalAppData'))

    info = tk.Label(root, text=f'Selected folder: "{foldername}/Stoopid"')
    info.pack()

    start_button = ttk.Button(root, text='Start', command=start_install)
    start_button.pack()

message = tk.Label(root, text="Select install location...")
message.pack()

# open button
open_button = ttk.Button(root, text='Open...', command=select_file)
open_button.pack()

root.mainloop()