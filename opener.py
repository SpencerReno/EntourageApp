import tkinter as tk 
import requests 
import gdown
import os 
import sys 
from threading import *
import time



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



main_color = '#313942'

root = tk.Tk()
root.geometry("700x500")
root.config(bg=main_color)
root.title("Entourage Hours Sheets")
root.iconbitmap(resource_path('assets\\EIB_black_pink.ico'))



blank_background = tk.Label(root, bg=main_color)
blank_background.place(relheight=1, relwidth=1)

global EN_photo, w, h
EN_photo = tk.PhotoImage(file='assets\\EIB Pink_Black Logo.png')
w, h = EN_photo.width(), EN_photo.height()

global settings_photo
settings_photo = tk.PhotoImage(file='assets\\settingsWheel.png')


def update_google_func():
    url = 'https://drive.google.com/uc?id=1eODjDU5xX1xAtS83iY3CX08hmZLdgtRV'
    output = 'google_funcs.py'
    gdown.download(url, output, quiet=False)


def update_main_file():
    url = 'https://drive.google.com/uc?id=1N3hNmEw0hlXebtQVdAj8zddDaFsEriiT'
    output = 'main.py'
    gdown.download(url, output, quiet=False)


def update_app():
    # update_main_file()
    # update_google_func()
    print('hello')





def threading(): 
    # Call work function 
    t1=Thread(target=update_app) 
    t1.start() 
    t1.join()

def initiate_app(update_label):
    root.deiconify()
    from subprocess import call
    call(["python", "main.py"])
   # os.system('%s %s' % (sys.executable, './runprogram.py'))


def start_app():
    

    update_label = tk.Label(root, text='Checking for updates...', bg=main_color, fg='black',font=('Times', '15','bold'))
    update_label.place(relx=.11, rely=.3, relheight=.15, relwidth=.8)

    threading()
    initiate_app(update_label)
    root.mainloop()

start_app()

#https://stackoverflow.com/questions/6932389/how-to-remotely-update-python-applications

#make folder in documents to save the files 
#open a base screen to show downloading updates 
#close screen after saving the files to documents 
#call to open the main app off of documents location 
#