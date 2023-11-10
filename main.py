import tkinter as tk 
#from PIL import ImageTk, Image
from google_funcs import *
from tkinter.filedialog import asksaveasfile
from tkinter import ttk, filedialog, messagebox
import requests
import os
import sys
import pandas as pd
import requests
from io import StringIO
from tkinter.filedialog import asksaveasfile
from datetime import date
import datetime
import calendar
import pyperclip 
import json
import subprocess
from urllib.request import urlretrieve
import getpass
##https://stackoverflow.com/questions/6932389/how-to-remotely-update-python-applications


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


def update_check():
    print('checking for updates')
    root.geometry('300x300')
    main_background =tk.Label(blank_background, bg=main_color)
    main_background.place(relheight=1, relwidth=1)
    update_label = tk.Label(main_background, text='Checking for updates...', bg=main_color, fg='black',font=('Times', '15','bold'))
    update_label.place(relx=.11, rely=.3, relheight=.15, relwidth=.8)

    url = 'https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/app_info.json'
    info = requests.get(url).json()
    server_app_version = info['info']['APP_VERSION']


    local_info=open(os.path.join(os.path.dirname(sys.argv[0]), 'app_info.json'))
    local_info = json.load(local_info)
    local_app_version =local_info['info']['APP_VERSION']

    if server_app_version != local_app_version:
        update_label.config(text='UPDATE REQUIRED!!')
        update_button = tk.Button(main_background, text='Update', bg='black', fg='white', command= lambda: update_app())
        update_button.place(relheight=.1,relwidth=.25, relx=.35,rely=.6)


    else:
        update_label.after(2000, show_menu)
    root.mainloop()

def update_app():
    url = 'https://github.com/SpencerReno/EntourageApp/raw/main/EntourageDirectors.exe'

    print('File Downloading')

    usrname = getpass.getuser()
    destination = f'C:\\Users\\{usrname}\\Downloads\\EntourageApp.exe'

    download = urlretrieve(url, destination)

    print('File downloaded')
    #delete_old()
    install_new()

def delete_old():
    try:
        cmd = f'C:\\Program Files (x86)\\EntourageDirectors\\unins000.exe'

        returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
        print('returned value:', returned_value)

        install_new()
    except:
        install_new()
def install_new():
    usrname = getpass.getuser()

    cmd = f'C:\\Users\\{usrname}\\Downloads  EntourageApp.exe'

    returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
    print('returned value:', returned_value)



def show_menu():
    root.geometry("700x500")
    main_background =tk.Label(blank_background, bg=main_color)
    main_background.place(relheight=1, relwidth=1)


    directors_ed = tk.Label(main_background, text="DIRECTORS EDITION", bg=main_color, fg='black', font=('Times', '36','bold'))
    directors_ed.place(relx=.12, rely=.05, relheight=.15, relwidth=.8)

    entourage_logo = tk.Label(main_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.19, rely=.23, relheight=.3, relwidth=.6)


    payment_totals = tk.Button(main_background, text='Daily Totals', bg='black', fg='white', command=lambda: reports_page(main_background))
    payment_totals.place(relheight=.1,relwidth=.25, relx=.23,rely=.55)

    hours_creator = tk.Button(main_background, text='Hours Creator', bg='black', fg='white', command=lambda: hours_menu(main_background))
    hours_creator.place(relheight=.1,relwidth=.25, relx=.52,rely=.55)

    final_100 = tk.Button(main_background, text='Final 100', bg='black', fg='white', command=lambda: final_100_page(main_background))
    final_100.place(relheight=.1,relwidth=.25, relx=.23,rely=.68)

    unpaid = tk.Button(main_background, text='Unpaid Students', bg='black', fg='white', command=lambda: unpaid_students(main_background))
    unpaid.place(relheight=.1,relwidth=.25, relx=.52,rely=.68)

    status_button = tk.Button(main_background, text='Student Status', bg='black', fg='white', command=lambda: status_page(main_background))
    status_button.place(relheight=.1,relwidth=.25, relx=.23,rely=.8)

    update_button = tk.Button(main_background, text='Update App', bg='black', fg='white', command=lambda: update_app(main_background))
    update_button.place(relheight=.1,relwidth=.25, relx=.52,rely=.8)






def unpaid_students(menu_background): 
    data = get_unpaid_students()
    menu_background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_main(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Unpaid Students', bg=main_color, fg='black', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)


    data_frame = tk.LabelFrame(settings_background)
    data_frame.place(rely=0.1, relx=0, relheight=.9,relwidth=1)


    tv1 = ttk.Treeview(data_frame)
    tv1.place(relheight=1, relwidth=1)

    treescrolly = tk.Scrollbar(data_frame, orient='vertical', command=tv1.yview)
    tv1.configure(yscrollcommand=treescrolly.set)
    treescrolly.pack(side='right', fill='y')

    tv1['column'] = list(data.columns)
    for value in data.columns:
        tv1.column(value, anchor='w')
    tv1['show'] = 'headings'

    for column in tv1['columns']:
        tv1.heading(column, text=column)
        tv1.column(column, width=data_frame.winfo_width())

    df_rows = data.to_numpy().tolist()

    for row in df_rows:
        tv1.insert('', 'end', values=row)

    tv1.bind("<Control-Key-c>", lambda x: your_copy(tv1, x))


def reports_page(main_background):
    main_background.destroy()
    reports_background =tk.Label(blank_background, bg=main_color)
    reports_background.place(relheight=1, relwidth=1)


    daily_totals_title= tk.Label(reports_background, text="DAILY TOTALS", bg=main_color, fg='black', font=('Times', '36','bold'))
    daily_totals_title.place(relx=.15, rely=-.02, relheight=.15, relwidth=.8)

    totals_entry = tk.Text(reports_background,)
    totals_entry.place(rely=0.1, relx=0, relheight=1,relwidth=.55)


    total_label = tk.Label(reports_background, text="TOTAL", bg=main_color, fg='black', font=('Times', '36','bold'))
    total_label.place(relheight=.1,relwidth=.25, relx=.65,rely=.35)


    total_display= tk.Entry(reports_background,bg=main_color, fg='lightgreen', font=('Times', '28','bold'))
    total_display.place(relheight=.1,relwidth=.25, relx=.65,rely=.5)
    

    submit_button= tk.Button(reports_background, text='Submit', bg='black', fg='white', command=lambda: add_totals(totals_entry, total_display))
    submit_button.place(relheight=.1,relwidth=.25, relx=.65,rely=.7)




    back_button = tk.Button(reports_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_main(reports_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)


def add_totals(text, total_display):
    lst = text.get("1.0",'end-1c')
    lst = lst.split('\n')
    nums = []

    import re
    total = 0
    for line in lst:
        line= line.replace(',', '')
        res = re.findall(r'\d+', line)
        if len(res) >=1:
            final = '.'.join(res)
            nums.append(float(final))


    for num in nums:
        total = total + float(num)

    print(total)

    total= str(total)
    split_total = total.split('.')
    print(split_total)
    if len(split_total[1]) >2:
        total = f'{split_total[0]}.{split_total[1][:2]}'
    else:
        total = total


    print(total)
    total_display.delete(0, tk.END)
    total_display.insert(0,total)



def your_copy(tree, event):
    sel = tree.selection() # get selected items
    root.clipboard_clear()  # clear clipboard
    # copy headers
    headings = [tree.heading("#{}".format(i), "text") for i in range(len(tree.cget("columns")) + 1)]
    #root.clipboard_append("\t".join(headings) + "\n")
    for item in sel:
        # retrieve the values of the row
        values = [tree.item(item, 'text')]
        values.extend(tree.item(item, 'values'))
        # append the values separated by \t to the clipboard
        root.clipboard_append("\t".join(values) + "\n")

def final_100_page(main_background):
    main_background.destroy()
    final_100_background =tk.Label(blank_background, bg=main_color)
    final_100_background.place(relheight=1, relwidth=1)


    
    hours_title= tk.Label(final_100_background , text="Final 100s", bg=main_color, fg='black', font=('Times', '36','bold'))
    hours_title.place(relx=.12, rely=.05, relheight=.15, relwidth=.8)

    menu_cos = tk.Button(final_100_background , text='Cosmetology', bg='black', fg='white', command=lambda: cos_100(final_100_background))
    menu_cos.place(relheight=.1,relwidth=.25, relx=.23,rely=.6)

    menu_esti = tk.Button(final_100_background , text='Esthetics', bg='maroon', fg='white', command=lambda: esti_100(final_100_background))
    menu_esti.place(relheight=.1,relwidth=.25, relx=.52,rely=.6)

    menu_nails = tk.Button(final_100_background , text='Nails', bg='DarkBlue', fg='white', command=lambda: nails_100(final_100_background))
    menu_nails.place(relheight=.1,relwidth=.25, relx=.23,rely=.8)

    menu_massage = tk.Button(final_100_background , text='Massage', bg='dim Grey', fg='white', command=lambda: massage_100(final_100_background))
    menu_massage.place(relheight=.1,relwidth=.25, relx=.52,rely=.8)


    back_button = tk.Button(final_100_background, text='Back', bg='black', fg='white', activebackground='black',command= lambda: clear_main(final_100_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    entourage_logo = tk.Label(final_100_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.19, rely=.23, relheight=.3, relwidth=.6)


def esti_100(menu_background):
    data = course_100_file('Esti')
    data['Remain hrs']=data['Remain hrs'].astype(float)
    data = data[data['Remain hrs']<=100]
    Last_name = data['Name'].str.split(',').str[0]
    data['Last Name'] =  data['Name'].str.split(' ').str[0]

    First_name = data['Name'].str.split(',').str[1]
    data['Name'] =  data['Name'].str.split(' ').str[1]
    data.drop(columns=[ 'Tot hrs', 'LDA hrs', 'Last Name'], inplace=True)
    data['Groups']=data['Groups'].str.replace('Esthetics Full Time' , 'FT')
    data['Groups']=data['Groups'].str.replace('Esthetics Part Time' , 'PT')

    data = data[['Acct', 'Name', 'Last name', 'Groups', 'Remain hrs', 'Rev grad', 'Balance']]
    data=data.sort_values(by='Remain hrs')
    menu_background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_100(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Esti Final 100', bg=main_color, fg='black', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)



    data_frame = tk.LabelFrame(settings_background)
    data_frame.place(rely=0.1, relx=0, relheight=.65,relwidth=1)


    tv1 = ttk.Treeview(data_frame)
    tv1.place(relheight=1, relwidth=1)

    treescrolly = tk.Scrollbar(data_frame, orient='vertical', command=tv1.yview)
    tv1.configure(yscrollcommand=treescrolly.set)
    treescrolly.pack(side='right', fill='y')

    tv1['column'] = list(data.columns)
    tv1['show'] = 'headings'

    for column in tv1['columns']:
        tv1.heading(column, text=column)
        tv1.column(column, width=data_frame.winfo_width(), anchor='w')

    df_rows = data.to_numpy().tolist()

    for row in df_rows:
        tv1.insert('', 'end', values=row)


    tv1.bind("<Control-Key-c>", lambda x: your_copy(tv1, x))

def cos_100(menu_background):
    data = course_100_file('Cos')
    data['Remain hrs']= data['Remain hrs'].str.replace(',', '')
    data['Remain hrs']=data['Remain hrs'].astype(float)
    data = data[data['Remain hrs']<=100]
    Last_name = data['Name'].str.split(',').str[0]
    data['Last Name'] =  data['Name'].str.split(' ').str[0]

    First_name = data['Name'].str.split(',').str[1]
    data['Name'] =  data['Name'].str.split(' ').str[1]
    data.drop(columns=[ 'Tot hrs', 'LDA hrs', 'Last Name'], inplace=True)
    data['Groups']=data['Groups'].str.replace('Cosmetology Full Time' , 'FT')
    data['Groups']=data['Groups'].str.replace('Cosmetology Part Time' , 'PT')

    data = data[['Acct', 'Name', 'Last name', 'Groups', 'Remain hrs', 'Rev grad', 'Balance']]
    data=data.sort_values(by='Remain hrs')

    menu_background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_100(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'COS Final 100', bg=main_color, fg='black', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)


    data_frame = tk.LabelFrame(settings_background)
    data_frame.place(rely=0.1, relx=0, relheight=.65,relwidth=1)


    tv1 = ttk.Treeview(data_frame)
    tv1.place(relheight=1, relwidth=1)

    treescrolly = tk.Scrollbar(data_frame, orient='vertical', command=tv1.yview)
    tv1.configure(yscrollcommand=treescrolly.set)
    treescrolly.pack(side='right', fill='y')

    tv1['column'] = list(data.columns)
    tv1['show'] = 'headings'

    for column in tv1['columns']:
        tv1.heading(column, text=column)
        tv1.column(column, width=data_frame.winfo_width(), anchor='w')

    df_rows = data.to_numpy().tolist()

    for row in df_rows:
        tv1.insert('', 'end', values=row)

    tv1.bind("<Control-Key-c>", lambda x: your_copy(tv1, x))
    

def nails_100(menu_background):
    data = course_100_file('Nails')
    data['Remain hrs']=data['Remain hrs'].astype(float)
    data = data[data['Remain hrs']<=100]
    Last_name = data['Name'].str.split(',').str[0]
    data['Last Name'] =  data['Name'].str.split(' ').str[0]

    First_name = data['Name'].str.split(',').str[1]
    data['Name'] =  data['Name'].str.split(' ').str[1]
    data.drop(columns=[ 'Tot hrs', 'LDA hrs', 'Last Name'], inplace=True)
    data['Groups']=data['Groups'].str.replace('Nails Full Time' , 'FT')
    data['Groups']=data['Groups'].str.replace('Nails Part Time' , 'PT')

    data = data[['Acct', 'Name', 'Last name', 'Groups', 'Remain hrs', 'Rev grad', 'Balance']]
    data=data.sort_values(by='Remain hrs')

    menu_background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_100(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Nails Final 100', bg=main_color, fg='black', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)


    data_frame = tk.LabelFrame(settings_background)
    data_frame.place(rely=0.1, relx=0, relheight=.65,relwidth=1)


    tv1 = ttk.Treeview(data_frame)
    tv1.place(relheight=1, relwidth=1)

    treescrolly = tk.Scrollbar(data_frame, orient='vertical', command=tv1.yview)
    tv1.configure(yscrollcommand=treescrolly.set)
    treescrolly.pack(side='right', fill='y')

    tv1['column'] = list(data.columns)
    tv1['show'] = 'headings'

    for column in tv1['columns']:
        tv1.heading(column, text=column)
        tv1.column(column, width=data_frame.winfo_width(), anchor='w')

    df_rows = data.to_numpy().tolist()

    for row in df_rows:
        tv1.insert('', 'end', values=row)
    tv1.bind("<Control-Key-c>", lambda x: your_copy(tv1, x))
    

def massage_100(menu_background):
    data = course_100_file('Massage')
    data['Remain hrs']=data['Remain hrs'].astype(float)
    data = data[data['Remain hrs']<=100]
    Last_name = data['Name'].str.split(',').str[0]
    data['Last Name'] =  data['Name'].str.split(' ').str[0]

    First_name = data['Name'].str.split(',').str[1]
    data['Name'] =  data['Name'].str.split(' ').str[1]
    data.drop(columns=[ 'Tot hrs', 'LDA hrs', 'Last Name'], inplace=True)


    data = data[['Acct', 'Name', 'Last name', 'Remain hrs', 'Rev grad', 'Balance']]
    data=data.sort_values(by='Remain hrs')
    menu_background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_100(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Massage Final 100', bg=main_color, fg='black', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)


    data_frame = tk.LabelFrame(settings_background)
    data_frame.place(rely=0.1, relx=0, relheight=.65,relwidth=1)


    tv1 = ttk.Treeview(data_frame)
    tv1.place(relheight=1, relwidth=1)

    treescrolly = tk.Scrollbar(data_frame, orient='vertical', command=tv1.yview)
    tv1.configure(yscrollcommand=treescrolly.set)
    treescrolly.pack(side='right', fill='y')

    tv1['column'] = list(data.columns)
    tv1['show'] = 'headings'

    for column in tv1['columns']:
        tv1.heading(column, text=column)
        tv1.column(column, width=data_frame.winfo_width(), anchor='w')

    df_rows = data.to_numpy().tolist()

    for row in df_rows:
        tv1.insert('', 'end', values=row)

    tv1.bind("<Control-Key-c>", lambda x: your_copy(tv1, x))




def hours_menu(main_background):
    main_background.destroy()
    global menu_background


    menu_background =tk.Label(blank_background, bg=main_color)
    menu_background.place(relheight=1, relwidth=1)


    hours_title= tk.Label(menu_background, text="HOURS CREATION", bg=main_color, fg='black', font=('Times', '36','bold'))
    hours_title.place(relx=.12, rely=.05, relheight=.15, relwidth=.8)

    menu_cos = tk.Button(menu_background, text='Cosmetology', bg='black', fg='white', command=lambda: cos())
    menu_cos.place(relheight=.1,relwidth=.25, relx=.23,rely=.6)

    menu_esti = tk.Button(menu_background, text='Esthetics', bg='maroon', fg='white', command=lambda: esti())
    menu_esti.place(relheight=.1,relwidth=.25, relx=.52,rely=.6)

    menu_nails = tk.Button(menu_background, text='Nails', bg='DarkBlue', fg='white', command=lambda: nails())
    menu_nails.place(relheight=.1,relwidth=.25, relx=.23,rely=.8)

    menu_massage = tk.Button(menu_background, text='Massage', bg='dim Grey', fg='white', command=lambda: massage())
    menu_massage.place(relheight=.1,relwidth=.25, relx=.52,rely=.8)

    back_button = tk.Button(menu_background, text='Back', bg='black', fg='white', activebackground='black',command= lambda: clear_main(menu_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)
    

    w, h = settings_photo.width(), settings_photo.height()


    settings_button = tk.Button(menu_background,width=w, height=h, image=settings_photo, bg=main_color, activebackground=main_color, borderwidth=0, command= lambda: password())
    settings_button.place(relheight=.09,relwidth=.09, relx=.9, rely=.04)
    

    entourage_logo = tk.Label(menu_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.19, rely=.23, relheight=.3, relwidth=.6)

def password():
    menu_background.destroy()


    password_background=tk.Label(blank_background, bg=main_color)
    password_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(password_background, text='Back', bg='black', fg='white', activebackground='black', command= lambda: clear(password_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    


    entourage_logo = tk.Label(password_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.19, rely=.23, relheight=.3, relwidth=.6)
    

    password_entry = tk.Entry(password_background, font=([20]) )
    password_entry.bind("<Button-1>", lambda e: password_entry.delete(0, tk.END))
    password_entry.insert(0, 'Password')
    password_entry.place(relx=.15, rely=.75, relheight=.1,  relwidth=.7)
    password_entry.bind("<Return>", lambda x: password_successful(None, password_background, password_entry, ))


def password_successful(x, password_background, password_entry, ):
    print(password_entry.get())
    if password_entry.get() == '12004EIBE':
        settings_page()
        pass
    else:   
        password_entry.delete(0, tk.END)
        password_entry.insert(0, 'FAILED')

def settings_page():
    data = held_back_students()
    menu_background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Students Held Back', bg=main_color, fg='black', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)


    data_frame = tk.LabelFrame(settings_background)
    data_frame.place(rely=0.1, relx=0, relheight=.65,relwidth=1)


    tv1 = ttk.Treeview(data_frame)
    tv1.place(relheight=1, relwidth=1)

    treescrolly = tk.Scrollbar(data_frame, orient='vertical', command=tv1.yview)
    tv1.configure(yscrollcommand=treescrolly.set)
    treescrolly.pack(side='right', fill='y')

    tv1['column'] = list(data.columns)
    tv1['show'] = 'headings'

    for column in tv1['columns']:
        tv1.heading(column, text=column)
        tv1.column(column, width=data_frame.winfo_width())

    df_rows = data.to_numpy().tolist()

    for row in df_rows:
        tv1.insert('', 'end', values=row)


    
    student_id_entry = tk.Entry(settings_background, )
    student_id_entry.place(relx=.0, rely=.7,relheight=.05, relwidth=.17)

    student_first_entry = tk.Entry(settings_background)
    student_first_entry.place(relx=.17, rely=.7,relheight=.05, relwidth=.17)

    student_last_entry = tk.Entry(settings_background)
    student_last_entry.place(relx=.34, rely=.7,relheight=.05, relwidth=.17)

    student_group_entry = tk.Entry(settings_background)
    student_group_entry.insert(0,'Esthetics Full Time')
    student_group_entry.place(relx=.51, rely=.7,relheight=.05, relwidth=.17)

    student_hrs_entry = tk.Entry(settings_background)
    student_hrs_entry.place(relx=.68, rely=.7,relheight=.05, relwidth=.17)

    student_trans_entry = tk.Entry(settings_background)
    student_trans_entry.place(relx=.85, rely=.7,relheight=.05, relwidth=.12)


    submit_button= tk.Button(settings_background, text='Submit', bg='black', fg='white', command=lambda: add_student(submit_button, student_id_entry, student_first_entry,student_last_entry,student_group_entry,student_hrs_entry,student_trans_entry))
    submit_button.place(relheight=.1,relwidth=.25, relx=.4,rely=.8)

    tv1.bind('<Delete>', lambda d : selection_delete(None, tv1, data))
    tv1.bind("<Control-Key-c>", lambda x: your_copy(tv1, x))

def selection_delete(event, tv1, data):
    for i in tv1.selection():
        dropped_index = data[data['Acct'] == tv1.item(i)['values'][0]].index
        data.drop(index=dropped_index, inplace=True)
        json_data = data.to_json()
        url = 'https://api.apispreadsheets.com/data/aAZcLsK62BpKyvIJ/'
        r= requests.post(url,json=json_data)
        if r.status_code == 201:
            messagebox.showinfo("Student Removal", f'Student {tv1.item(i)["values"][0]} has been removed')
            tv1.delete(i)
        else:
            messagebox.showinfo("Student Removal", f'Failed to remove student {tv1.item(i)["values"][0]} please go to Google sheets and delete them')
        

def add_student(submit_button, student_id_entry, student_first_entry,student_last_entry,student_group_entry,student_hrs_entry,student_trans_entry):
    url = 'https://api.apispreadsheets.com/data/aAZcLsK62BpKyvIJ/'
    data = {"data": 
            {"Acct":student_id_entry.get(),
             "Name":student_first_entry.get(),
             "Last Name":student_last_entry.get(),
             "Groups":student_group_entry.get(),
             "Tot hrs":student_hrs_entry.get(),
             "tran hrs":student_trans_entry.get(),}}
    r= requests.post(url,json=data )
    if r.status_code == 201:
        submit_button.config(bg='Green') 
        student_id_entry.delete(0, tk.END)
        student_first_entry.delete(0, tk.END)
        student_last_entry.delete(0, tk.END)
        student_hrs_entry.delete(0, tk.END)
        student_trans_entry.delete(0, tk.END)
    else:
        submit_button.config(bg='Red') 

def cos():
    global pathLabel
    menu_background.destroy()

    cos_background=tk.Label(blank_background, bg=main_color)
    cos_background.place(relheight=1, relwidth=1)

    entourage_logo = tk.Label(cos_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.19, rely=.23, relheight=.3, relwidth=.6)

    cos_title = tk.Label(cos_background, text='COSMETOLOGY', bg = main_color, fg='black', font=('Times', '36','bold'))
    cos_title.place(relx=.15, rely=.05, relheight=.15, relwidth=.7)

    download_am = tk.Button(cos_background, text='Download AM', bg='black', fg='white', command= lambda: cos_data_creation('AM'))
    download_am.place(relheight=.1,relwidth=.25, relx=.23,rely=.6)

    download_pm = tk.Button(cos_background, text='Download PM', bg='black', fg='white', command= lambda: cos_data_creation('PM'))
    download_pm.place(relheight=.1,relwidth=.25, relx=.52,rely=.6)

    back_button = tk.Button(cos_background, text='Back', bg='black', fg='white', activebackground='black',command= lambda: clear(cos_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

def massage():
    menu_background.destroy()

    massage_background=tk.Label(blank_background, bg=main_color)
    massage_background.place(relheight=1, relwidth=1)

    entourage_logo = tk.Label(massage_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.19, rely=.23, relheight=.3, relwidth=.6)

    massage_title = tk.Label(massage_background, text='MASSAGE', bg = main_color, fg='black', font=('Times', '36','bold'))
    massage_title.place(relx=.15, rely=.05, relheight=.15, relwidth=.7)

    download_am = tk.Button(massage_background, text='Download AM', bg='black', fg='white', command= lambda: massage_data_creation())
    download_am.place(relheight=.1,relwidth=.25, relx=.37,rely=.6)

    back_button = tk.Button(massage_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear(massage_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

def nails():
    menu_background.destroy()

    nails_background=tk.Label(blank_background, bg=main_color)
    nails_background.place(relheight=1, relwidth=1)

    entourage_logo = tk.Label(nails_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.19, rely=.23, relheight=.3, relwidth=.6)

    nails_title = tk.Label(nails_background, text='NAILS', bg = main_color, fg='black', font=('Times', '36','bold'))
    nails_title.place(relx=.15, rely=.05, relheight=.15, relwidth=.7)

    download_am = tk.Button(nails_background, text='Download AM', bg='DarkBlue', fg='white',command= lambda: nails_data_creation('AM'))
    download_am.place(relheight=.1,relwidth=.25, relx=.23,rely=.6)

    download_pm = tk.Button(nails_background, text='Download PM', bg='DarkBlue', fg='white',command= lambda: nails_data_creation('PM'))
    download_pm.place(relheight=.1,relwidth=.25, relx=.52,rely=.6)

    back_button = tk.Button(nails_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear(nails_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

def esti():
    menu_background.destroy()

    esti_background=tk.Label(blank_background, bg=main_color)
    esti_background.place(relheight=1, relwidth=1)

    entourage_logo = tk.Label(esti_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.19, rely=.23, relheight=.3, relwidth=.6)

    esti_title = tk.Label(esti_background, text='ESTHETICS', bg = main_color, fg='black', font=('Times', '36','bold'))
    esti_title.place(relx=.15, rely=.05, relheight=.15, relwidth=.7)

    download_FRam = tk.Button(esti_background, text='Freshman AM', bg='maroon', fg='white', command= lambda: esti_data_creation('fresh_am'))
    download_FRam.place(relheight=.1,relwidth=.25, relx=.23,rely=.55)

    download_FRpm = tk.Button(esti_background, text='Freshman PM', bg='Maroon', fg='white', command= lambda: esti_data_creation('fresh_pm'))
    download_FRpm.place(relheight=.1,relwidth=.25, relx=.52,rely=.55)

    download_JRam = tk.Button(esti_background, text='Junior AM', bg='maroon', fg='white', command= lambda: esti_data_creation('jr_am'))
    download_JRam.place(relheight=.1,relwidth=.25, relx=.23,rely=.68)

    download_JRpm = tk.Button(esti_background, text='Junior PM', bg='Maroon', fg='white', command= lambda: esti_data_creation('jr_pm'))
    download_JRpm.place(relheight=.1,relwidth=.25, relx=.52,rely=.68)

    download_SRam = tk.Button(esti_background, text='Senior AM', bg='maroon', fg='white', command= lambda: esti_data_creation('sr_am'))
    download_SRam.place(relheight=.1,relwidth=.25, relx=.23,rely=.8)

    download_SRpm = tk.Button(esti_background, text='Senior PM', bg='Maroon', fg='white', command= lambda: esti_data_creation('sr_pm'))
    download_SRpm.place(relheight=.1,relwidth=.25, relx=.52,rely=.8)

    back_button = tk.Button(esti_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear(esti_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)


def status_page(background):
    background.destroy()
    status_background=tk.Label(blank_background, bg=main_color)
    status_background.place(relheight=1, relwidth=1)

    hours_title= tk.Label(status_background, text="Student Status", bg=main_color, fg='black', font=('Times', '36','bold'))
    hours_title.place(relx=.12, rely=.05, relheight=.15, relwidth=.8)

    menu_cos = tk.Button(status_background, text='Cosmetology', bg='black', fg='white', command=lambda: status_cos(status_background))
    menu_cos.place(relheight=.1,relwidth=.25, relx=.23,rely=.6)

    menu_esti = tk.Button(status_background, text='Esthetics', bg='black', fg='white', command=lambda: status_esti(status_background))
    menu_esti.place(relheight=.1,relwidth=.25, relx=.52,rely=.6)

    menu_nails = tk.Button(status_background, text='Nails', bg='black', fg='white', command=lambda: status_nails(status_background))
    menu_nails.place(relheight=.1,relwidth=.25, relx=.23,rely=.8)

    menu_massage = tk.Button(status_background, text='Massage', bg='black', fg='white', command=lambda: status_massage(status_background))
    menu_massage.place(relheight=.1,relwidth=.25, relx=.52,rely=.8)

    back_button = tk.Button(status_background, text='Back', bg='black', fg='white', activebackground='black',command= lambda: clear_main(status_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)


    entourage_logo = tk.Label(status_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.19, rely=.23, relheight=.3, relwidth=.6)


def status_show(course):
    data = get_student_status(course)
    menu_background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_main(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Unpaid Students', bg=main_color, fg='black', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)


    data_frame = tk.LabelFrame(settings_background)
    data_frame.place(rely=0.1, relx=0, relheight=.9,relwidth=1)


    tv1 = ttk.Treeview(data_frame)
    tv1.place(relheight=1, relwidth=1)

    treescrolly = tk.Scrollbar(data_frame, orient='vertical', command=tv1.yview)
    tv1.configure(yscrollcommand=treescrolly.set)
    treescrolly.pack(side='right', fill='y')

    tv1['column'] = list(data.columns)
    for value in data.columns:
        tv1.column(value, anchor='w',)
    tv1['show'] = 'headings'

    for column in tv1['columns']:
        tv1.heading(column, text=column)
        tv1.column(column, width=data_frame.winfo_width())

    df_rows = data.to_numpy().tolist()

    for row in df_rows:
        tv1.insert('', 'end', values=row)

    tv1.bind("<Control-Key-c>", lambda x: your_copy(tv1, x))

def status_massage(background):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/Entourage%20Remaining%20Hours.csv'
    data = pd.read_csv(url)
    data.drop(columns=['Last name', 'Balance', 'LDA hrs'], inplace=True)
    data = data[data['Groups'] == 'Massage Therapy']
    data['Tot hrs']=data['Tot hrs'].str.replace(',', '')
    data['Tot hrs'] = data['Tot hrs'].astype(float)
    data = data.sort_values('Tot hrs', ascending=False)
    background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_status(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Massage Student Status', bg=main_color, fg='black', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)




    tv1 = get_treeview(data, settings_background)

    tv1.place(relheight=1, relwidth=1)

def status_cos(background):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/Entourage%20Remaining%20Hours.csv'
    data = pd.read_csv(url)
    data.drop(columns=['Last name', 'Balance', 'LDA hrs'], inplace=True)
    data = data[(data['Groups'] == 'Cosmetology Full Time') | (data['Groups'] == 'Cosmetology Part Time')]
    data['Tot hrs']=data['Tot hrs'].str.replace(',', '')
    data['Tot hrs'] = data['Tot hrs'].astype(float)
    background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_status(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Cosmetology Student Status', bg=main_color, fg='black', font=('Times', '30','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)

    cos_am = data[data['Groups'] == 'Cosmetology Full Time'].sort_values('Tot hrs', ascending=False)
    cos_am_view = tk.Button(settings_background, text='Day Cosmetology', bg='black', fg='white', command= lambda: get_small_treeview(cos_am, settings_background, tv1))
    cos_am_view.place(relheight=.1,relwidth=.25, relx=.23,rely=.85)

    cos_pm = data[data['Groups'] == 'Cosmetology Part Time'].sort_values('Tot hrs', ascending=False)
    cos_pm_view = tk.Button(settings_background, text='Night Cosmetology', bg='black', fg='white', command= lambda: get_small_treeview(cos_pm, settings_background, tv1))
    cos_pm_view.place(relheight=.1,relwidth=.25, relx=.52,rely=.85)



    tv1 = get_treeview(data, settings_background)

    tv1.place(relheight=1, relwidth=1)


def status_esti(background):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/Entourage%20Remaining%20Hours.csv'
    data = pd.read_csv(url)
    data.drop(columns=['Last name', 'Balance', 'LDA hrs'], inplace=True)
    data = data[(data['Groups'] == 'Esthetics Full Time') | (data['Groups'] == 'Esthetics Part Time')]
    data['Tot hrs']=data['Tot hrs'].str.replace(',', '')
    data['Tot hrs'] = data['Tot hrs'].astype(float)
    background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_status(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Esthetics Student Status', bg=main_color, fg='black', font=('Times', '30','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)

    esti_am = data[data['Groups'] == 'Esthetics Full Time'].sort_values('Tot hrs', ascending=False)
    esti_am_view = tk.Button(settings_background, text='Day Esthetics', bg='black', fg='white', command= lambda: get_small_treeview(esti_am, settings_background, tv1))
    esti_am_view.place(relheight=.1,relwidth=.25, relx=.23,rely=.85)

    esti_pm = data[data['Groups'] == 'Esthetics Part Time'].sort_values('Tot hrs', ascending=False)
    esti_pm_view = tk.Button(settings_background, text='Night Esthetics', bg='black', fg='white', command= lambda: get_small_treeview(esti_pm, settings_background, tv1))
    esti_pm_view.place(relheight=.1,relwidth=.25, relx=.52,rely=.85)



    tv1 = get_treeview(data, settings_background)

    tv1.place(relheight=1, relwidth=1)

def status_nails(background):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/Entourage%20Remaining%20Hours.csv'
    data = pd.read_csv(url)
    data.drop(columns=['Last name', 'Balance', 'LDA hrs'], inplace=True)
    data = data[(data['Groups'] == 'Nails Full Time') | (data['Groups'] == 'Nails Part Time')]
    data['Tot hrs']=data['Tot hrs'].str.replace(',', '')
    data['Tot hrs'] = data['Tot hrs'].astype(float)
    background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_status(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Nail Student Status', bg=main_color, fg='black', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)

    nail_am = data[data['Groups'] == 'Nails Full Time'].sort_values('Tot hrs', ascending=False)
    nail_am_view = tk.Button(settings_background, text='Day Nails', bg='black', fg='white', command= lambda: get_small_treeview(nail_am, settings_background, tv1))
    nail_am_view.place(relheight=.1,relwidth=.25, relx=.23,rely=.85)

    nail_pm = data[data['Groups'] == 'Nails Part Time'].sort_values('Tot hrs', ascending=False)
    nail_pm_view = tk.Button(settings_background, text='Night Nails', bg='black', fg='white', command= lambda: get_small_treeview(nail_pm, settings_background, tv1))
    nail_pm_view.place(relheight=.1,relwidth=.25, relx=.52,rely=.85)



    tv1 = get_treeview(data, settings_background)

    tv1.place(relheight=1, relwidth=1)

def get_small_treeview(data, background, tree):

    for item in tree.get_children():
      tree.delete(item)

    df_rows = data.to_numpy().tolist()
    for row in df_rows:
        tree.insert('', 'end', values=row)





def get_treeview(data, background):
    data_frame = tk.LabelFrame(background)
    data_frame.place(rely=0.1, relx=0, relheight=.65,relwidth=1)

    tv1 = ttk.Treeview(data_frame)
    

    treescrolly = tk.Scrollbar(data_frame, orient='vertical', command=tv1.yview)
    tv1.configure(yscrollcommand=treescrolly.set)
    treescrolly.pack(side='right', fill='y')

    tv1['column'] = list(data.columns)
    for value in data.columns:
        tv1.column(value, anchor='w')
    tv1['show'] = 'headings'

    for column in tv1['columns']:
        tv1.heading(column, text=column)
        tv1.column(column, width=data_frame.winfo_width())

    df_rows = data.to_numpy().tolist()

    for row in df_rows:
        tv1.insert('', 'end', values=row)

    tv1.bind("<Control-Key-c>", lambda x: your_copy(tv1, x))

    return tv1 

def update_app(background):
    background.destroy()
    update_background =tk.Label(blank_background, bg=main_color)
    update_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(update_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_main(update_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(update_background, text = 'Application Update', bg=main_color, fg='black', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)


    data_entry_frame = tk.LabelFrame(update_background)
    data_entry_frame.place(rely=0.1, relx=0, relheight=.65,relwidth=1)


def get_path(event):
    pathLabel.configure(text = event.data)

def clear(background):
    #background.destroy()
    hours_menu(background)

def clear_status(background):
    status_page(background)


def clear_100(background):
    final_100_page(background)

def clear_main(background):
    background.destroy()
    show_menu()

update_check()