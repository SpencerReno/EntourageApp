import tkinter as tk 
from tkinter.filedialog import asksaveasfile,asksaveasfilename
from tkinter import ttk, messagebox
import requests
import os
import sys
import pandas as pd
import requests
from datetime import date
from urllib.request import urlretrieve
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from google_funcs import * 

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


VERSION = '1.3'
main_color = '#313942'

root = tk.Tk()
root.config(bg=main_color)
root.title("Entourage App")
root.iconbitmap(resource_path('assets\\EIB_black_pink.ico'))
blank_background = tk.Label(root, bg=main_color)
blank_background.place(relheight=1, relwidth=1)

global EN_photo, w, h
EN_photo = tk.PhotoImage(file='assets\\EIB Pink_Black Logo.png')
w, h = EN_photo.width(), EN_photo.height()

global settings_photo
settings_photo = tk.PhotoImage(file='assets\\settingsWheel.png')


# def update_check():
#     root.geometry("700x500")
#     main_background =tk.Label(blank_background, bg=main_color)
#     main_background.place(relheight=1, relwidth=1)

#     update_label = tk.Label(main_background, text='Checking for updates...', bg=main_color, fg='gray',font=('Times', '15','bold'))
#     update_label.place(relx=.11, rely=.3, relheight=.15, relwidth=.8)

#     url = 'https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/app_info.json'
#     info = requests.get(url).json()
#     server_app_version = info['info']['APP_VERSION']

#     print(server_app_version)
#     if str(server_app_version) != str(VERSION):
#         update_label.config(text='Getting Updates...')
#         filename = os.path.basename(sys.argv[0])
#         for file in os.listdir():
#                     if file == filename: #Does not delete itself
#                         pass

#                     else:
#                         os.remove(file)

#         exename = 'EntourageApp.exe'
#         code= requests.get()    

#     elif str(server_app_version) == str(VERSION):
#         show_menu()



def show_menu():
    root.geometry("700x500")
    main_background =tk.Label(blank_background, bg=main_color)
    main_background.place(relheight=1, relwidth=1)

    directors_ed = tk.Label(main_background, text="INSTRUCTORS EDITION", bg=main_color, fg='gray', font=('Times', '36','bold'))
    directors_ed.place(relx=.07, rely=.05, relheight=.15, relwidth=.9)

    entourage_logo = tk.Label(main_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.19, rely=.23, relheight=.3, relwidth=.6)


    status_button = tk.Button(main_background, text='Student Status', bg='black', fg='white', command=lambda: status_page(main_background))
    status_button.place(relheight=.1,relwidth=.25, relx=.23,rely=.6)

    final_100 = tk.Button(main_background, text='Final 100', bg='black', fg='white', command=lambda: final_100_page(main_background))
    final_100.place(relheight=.1,relwidth=.25, relx=.38,rely=.75)

    hours_creator = tk.Button(main_background, text='Hours Creator', bg='black', fg='white', command=lambda: hours_menu(main_background))
    hours_creator.place(relheight=.1,relwidth=.25, relx=.52,rely=.6)
    root.mainloop()



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


def hours_menu(main_background):
    main_background.destroy()
    global menu_background


    menu_background =tk.Label(blank_background, bg=main_color)
    menu_background.place(relheight=1, relwidth=1)


    hours_title= tk.Label(menu_background, text="HOURS CREATION", bg=main_color, fg='gray', font=('Times', '36','bold'))
    hours_title.place(relx=.12, rely=.05, relheight=.15, relwidth=.8)

    menu_cos = tk.Button(menu_background, text='Cosmetology', bg='black', fg='white', command=lambda: cos(menu_background))
    menu_cos.place(relheight=.1,relwidth=.25, relx=.23,rely=.6)

    menu_esti = tk.Button(menu_background, text='Esthetics', bg='maroon', fg='white', command=lambda: esti(menu_background))
    menu_esti.place(relheight=.1,relwidth=.25, relx=.52,rely=.6)

    menu_nails = tk.Button(menu_background, text='Nails', bg='DarkBlue', fg='white', command=lambda: nails(menu_background))
    menu_nails.place(relheight=.1,relwidth=.25, relx=.23,rely=.8)

    menu_massage = tk.Button(menu_background, text='Massage', bg='dim Grey', fg='white', command=lambda: massage(menu_background))
    menu_massage.place(relheight=.1,relwidth=.25, relx=.52,rely=.8)

    back_button = tk.Button(menu_background, text='Back', bg='black', fg='white', activebackground='black',command= lambda: clear_main(menu_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)
    
    entourage_logo = tk.Label(menu_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.19, rely=.23, relheight=.3, relwidth=.6) 


    settings_button = tk.Button(menu_background,width=w, height=h, image=settings_photo, bg=main_color, activebackground=main_color, borderwidth=0, command= lambda: password())
    settings_button.place(relheight=.09,relwidth=.09, relx=.9, rely=.04)

    date = get_update_date('hours')
    update_date_label = tk.Label(menu_background, text=f'Last updated: {str(date)}', bg=main_color, fg='lightgreen', font=('Times', '13','bold'))
    update_date_label.place(relx=.39, rely= .02)

 
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

    title_label = tk.Label(settings_background, text = 'Students Held Back', bg=main_color, fg='gray', font=('Times', '36','bold'))
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

def cos(background):
    background.destroy()
    cos_full, cos_part = cos_online_hours()
    cos_hours_background =tk.Label(blank_background, bg=main_color)
    cos_hours_background.place(relheight=1, relwidth=1)

    title_label = tk.Label(cos_hours_background, text = 'Cosmetology Online Hours', bg=main_color, fg='gray', font=('Times', '30','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)

   
    cos_am_view = tk.Button(cos_hours_background, text='Day Cosmetology', bg='black', fg='white', command= lambda: new_hours_treeview(cos_full, cos_hours_background, tv1))
    cos_am_view.place(relheight=.1,relwidth=.25, relx=.05,rely=.75)

   
    cos_pm_view = tk.Button(cos_hours_background, text='Night Cosmetology', bg='black', fg='white', command= lambda: new_hours_treeview(cos_part, cos_hours_background, tv1))
    cos_pm_view.place(relheight=.1,relwidth=.25, relx=.05,rely=.88)

    download_button = tk.Button(cos_hours_background, text='Export', bg='Black', fg='white', activebackground='black',command= lambda: export_tree(tv1, 'cosmetology'))
    download_button.place(relheight=.1,relwidth=.1, relx=.9,rely=0)

    submit_button = tk.Button(cos_hours_background, text='Submit Hours', bg='Black', fg='white', activebackground='black',command= lambda: send_hours(tv1, 'Cosmetology'))
    submit_button.place(relheight=.1,relwidth=.25, relx=.75,rely=.88)
    


    tv1 = get_treeview(cos_full, cos_hours_background)

    tv1.place(relheight=1, relwidth=1)


    back_button = tk.Button(cos_hours_background, text='Back', bg='black', fg='white', activebackground='black',command= lambda: clear(cos_hours_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

def massage(background):
    background.destroy()
    massage_hrs = massage_online_hours()
    massage_hours_background =tk.Label(blank_background, bg=main_color)
    massage_hours_background.place(relheight=1, relwidth=1)

    title_label = tk.Label(massage_hours_background, text = 'Massage Online Hours', bg=main_color, fg='gray', font=('Times', '30','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)

    download_button = tk.Button(massage_hours_background, text='Export', bg='Black', fg='white', activebackground='black',command= lambda: export_tree(tv1, 'Massage'))
    download_button.place(relheight=.1,relwidth=.1, relx=.9,rely=0)

    submit_button = tk.Button(massage_hours_background, text='Submit Hours', bg='Black', fg='white', activebackground='black',command= lambda: send_hours(tv1, 'Massage'))
    submit_button.place(relheight=.1,relwidth=.25, relx=.75,rely=.88)
    


    tv1 = get_treeview(massage_hrs, massage_hours_background)
    
    tv1.place(relheight=1, relwidth=1)

    title_label.after(1000, new_hours_treeview(massage_hrs, massage_hours_background, tv1))

    


    back_button = tk.Button(massage_hours_background, text='Back', bg='black', fg='white', activebackground='black',command= lambda: clear(massage_hours_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)
def nails(background):
    background.destroy()
    nails_full, nails_part = nails_online_hours()

    nails_background=tk.Label(blank_background, bg=main_color)
    nails_background.place(relheight=1, relwidth=1)

    entourage_logo = tk.Label(nails_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.19, rely=.23, relheight=.3, relwidth=.6)

    nails_title = tk.Label(nails_background, text='NAILS ONLINE HOURS', bg = main_color, fg='gray', font=('Times', '36','bold'))
    nails_title.place(relx=.1, rely=0,relheight=.1, relwidth=.8)

    nail_am_view = tk.Button(nails_background, text='Day Nails', bg='black', fg='white', command= lambda: new_hours_treeview(nails_full, nails_background, tv1))
    nail_am_view.place(relheight=.1,relwidth=.25, relx=.05,rely=.75)

   
    nail_pm_view = tk.Button(nails_background, text='Night Nails', bg='black', fg='white', command= lambda: new_hours_treeview(nails_part, nails_background, tv1))
    nail_pm_view.place(relheight=.1,relwidth=.25, relx=.05,rely=.88)
    
    download_button = tk.Button(nails_background, text='Export', bg='Black', fg='white', activebackground='black',command= lambda: export_tree(tv1, 'Nails'))
    download_button.place(relheight=.1,relwidth=.1, relx=.9,rely=0)

    submit_button = tk.Button(nails_background, text='Submit Hours', bg='Black', fg='white', activebackground='black',command= lambda: send_hours(tv1, 'Nails'))
    submit_button.place(relheight=.1,relwidth=.25, relx=.75,rely=.88)
    

    tv1 = get_treeview(nails_part, nails_background)
    
    tv1.place(relheight=1, relwidth=1)



    back_button = tk.Button(nails_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear(nails_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

def esti(background):
    background.destroy()
    fresh_am, fresh_pm, jr_am, jr_pm, sr_am, sr_pm = esti_online_hours()
    print(fresh_am)

    esti_background=tk.Label(blank_background, bg=main_color)
    esti_background.place(relheight=1, relwidth=1)

    esti_title = tk.Label(esti_background, text='ESTHETICS ONLINE HOURS', bg = main_color, fg='gray', font=('Times', '25','bold'))
    esti_title.place(relx=.1, rely=0,relheight=.1, relwidth=.8)

    esti_hours_FRam = tk.Button(esti_background, text='Freshman AM', bg='maroon', fg='white', command= lambda: new_hours_treeview(fresh_am, esti_background, tv1))
    esti_hours_FRam.place(relheight=.1,relwidth=.2, relx=.01,rely=.77)

    esti_hours_FRpm = tk.Button(esti_background, text='Freshman PM', bg='Maroon', fg='white', command= lambda: new_hours_treeview(fresh_pm, esti_background, tv1))
    esti_hours_FRpm.place(relheight=.1,relwidth=.2, relx=.01,rely=.88)

    esti_hours_JRam = tk.Button(esti_background, text='Junior AM', bg='maroon', fg='white', command= lambda: new_hours_treeview(jr_am, esti_background, tv1))
    esti_hours_JRam.place(relheight=.1,relwidth=.2, relx=.23,rely=.77)

    esti_hours_JRpm = tk.Button(esti_background, text='Junior PM', bg='Maroon', fg='white', command= lambda: new_hours_treeview(jr_pm, esti_background, tv1))
    esti_hours_JRpm.place(relheight=.1,relwidth=.2, relx=.23,rely=.88)

    esti_hours_SRam = tk.Button(esti_background, text='Senior AM', bg='maroon', fg='white', command= lambda: new_hours_treeview(sr_am, esti_background, tv1))
    esti_hours_SRam.place(relheight=.1,relwidth=.2, relx=.45,rely=.77)

    esti_hours_SRpm = tk.Button(esti_background, text='Senior PM', bg='Maroon', fg='white', command= lambda: new_hours_treeview(sr_pm, esti_background, tv1))
    esti_hours_SRpm.place(relheight=.1,relwidth=.2, relx=.45,rely=.88)

    inservice_button = tk.Button(esti_background, text='Inservice Hours', bg='Black', fg='white', activebackground='black',command= lambda: inservice_day(esti_background, tv1))
    inservice_button.place(relheight=.1,relwidth=.25, relx=.75,rely=.77)

    download_button = tk.Button(esti_background, text='Export', bg='Black', fg='white', activebackground='black',command= lambda: export_tree(tv1, 'Esthetics'))
    download_button.place(relheight=.1,relwidth=.1, relx=.9,rely=0)

 
    submit_button = tk.Button(esti_background, text='Submit Hours', bg='Black', fg='white', activebackground='black',command= lambda: send_hours(tv1, 'Esthetics'))
    submit_button.place(relheight=.1,relwidth=.25, relx=.75,rely=.88)
    

    tv1 = get_treeview(fresh_am, esti_background)
    
    tv1.place(relheight=1, relwidth=1)


    back_button = tk.Button(esti_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear(esti_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)



def new_hours_treeview(data, background, tree):
    for item in tree.get_children():
      tree.delete(item)

    df_rows = data.to_numpy().tolist()
    for row in df_rows:
        tree.insert('', 'end', values=row)

    for x in range(len(tree['column'])):
        tree.heading(f'{x}', text=data.columns[x])

def inservice_day(background, tree):
    student_id = []
    first_name = []
    last_name = []
    clock_in = []
    clock_out = []


    for child in tree.get_children():
        student_id.append(tree.item(child)['values'][0])
        first_name.append(tree.item(child)['values'][1])
        last_name.append(tree.item(child)['values'][2])
        clock_in.append(tree.item(child)['values'][3])
        clock_out.append(tree.item(child)['values'][4])

    if '9:00' in clock_in[0] and '3:00' in clock_out[0]:
        df = pd.DataFrame(columns=['Acct', 'Name', 'Last name', 'clock in', 'clock out','Date', 'Aissigned Work'])
        df['Acct'] = student_id
        df['Name'] = first_name
        df['Last name'] = last_name
        df['clock in'] = '9:00 am'
        df['clock out'] = '4:00 pm'
        df['Date'] = ' '
        df['Aissigned Work'] = ' '

    if '4:30' in clock_in[0] and  '9:30' in clock_out[0]:
        df = pd.DataFrame(columns=['Acct', 'Name', 'Last name', 'clock in', 'clock out','Date', 'Aissigned Work'])
        df['Acct'] = student_id
        df['Name'] = first_name
        df['Last name'] = last_name
        df['clock in'] = '5:30 pm'
        df['clock out'] = '9:30 pm'
        df['Date'] = ' '
        df['Aissigned Work'] = ' '

    new_hours_treeview(df, background, tree)


def get_treeview(data, background):
    data_frame = tk.LabelFrame(background)
    data_frame.place(rely=0.1, relx=0, relheight=.65, relwidth=1)

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

    tv1.bind("<1>", lambda event: edit_tree(tv1, event))

    return tv1


##### ADD CLAUS FOR CHECKING DATE FORMAT AND POST ERROR IF INCORRECT 
def edit_tree(tree, event):

    if tree.identify_region(event.x, event.y) == 'cell':
        column = tree.identify_column(event.x)  # identify column
        item = tree.identify_row(event.y) 
        x, y, width, height = tree.bbox(item, column) 
        value = tree.set(item, column)
        place_entry(tree, x, y, width, height,value, item, column, event)


def place_entry(tree, x, y, width, height,value, item, column, event):

    entry = ttk.Entry(tree)  # create edition entry
    entry.place(x=x, y=y, width=width, height=height,
                anchor='nw')  # display entry on top of cell
    entry.insert(0, value)  # put former value in entry
    entry.bind('<FocusOut>', lambda e: entry.destroy())  
    entry.bind('<Return>', lambda x: ok_down(tree, item, column, entry, event))
    entry.bind('<Tab>', lambda x: ok_down(tree, item, column, entry, event))
    entry.bind('<Down>', lambda x: ok_down(tree, item, column, entry, event)) 
    entry.bind('<Up>', lambda x: ok_up(tree, item, column, entry, event)) 
    entry.focus_set()

def ok_up(tree, item, column, entry, event):
    tree.set(item, column, entry.get())
    entry.destroy()
    tab_up(tree,column, event) 

def tab_up(tree,column, event):
    current_item = tree.focus()
    next_item = tree.prev(current_item)
    current_item = tree.focus(next_item)
    tree.selection_set(next_item)
    x, y, width, height = tree.bbox(next_item, column) 
    value = tree.set(next_item, column)
    place_entry(tree, x, y, width, height,value, next_item, column, event)

def ok_down(tree, item, column, entry, event):
    tree.set(item, column, entry.get())
    entry.destroy()
    tab_down(tree,column, event) 
            
def tab_down(tree,column, event):
    current_item = tree.focus()
    next_item = tree.next(current_item)
    current_item = tree.focus(next_item)
    tree.selection_set(next_item)
    x, y, width, height = tree.bbox(next_item, column) 
    value = tree.set(next_item, column)
    place_entry(tree, x, y, width, height,value, next_item, column, event)
    
def export_tree(tree, course):
    row_list = []
    cols = tree['columns']
    for row in tree.get_children():
        row_list.append(tree.item(row)['values'])
    df = pd.DataFrame(row_list, columns=cols)
    file_save = asksaveasfilename(filetypes = [("csv file(*.csv)","*.csv"),('All tyes(*.*)', '*.*')], defaultextension = [("csv file(*.csv)","*.csv"),('All tyes(*.*)', '*.*')])
    df.to_csv(file_save, index=False)

    
def send_hours(tree, course):
    row_list = []
    cols = tree['columns']
    for row in tree.get_children():
        row_list.append(tree.item(row)['values'])
    df = pd.DataFrame(row_list, columns=cols)
    download_clock , send_clause= get_download_clock_file(df)
    print(download_clock, send_clause)
    if send_clause == True:
        hour_sheet =df 
        download_clock.to_csv(f'C:\\Windows\\Temp\\TimeClockReport.data', sep=' ', header=False, index=False)
        hour_sheet.to_csv(f'C:\\Windows\\Temp\\HoursSheet.csv',index=False)
        url = 'https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/app_info.json'
        info = requests.get(url).json()

        from_addr = 'eibehours@gmail.com'
        to_addr = []
        for email in info['info']['HOURS_EMAIL']:
            to_addr.append(str(email))
        print(to_addr)
        subject = 'Hours'

        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = ", ".join(to_addr)
        msg['Subject'] = subject
        body = MIMEText(f'New {course} hours!', 'plain')

        msg.attach(body)

        time_clock_report = 'C:\\Windows\\Temp\\TimeClockReport.data'

        with open(time_clock_report, 'rb') as f:
            attachment = MIMEApplication(f.read(), name=basename(time_clock_report))
            attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(time_clock_report))


        hours_sheet_report = 'C:\\Windows\\Temp\\HoursSheet.csv'

        with open(hours_sheet_report, 'r') as f:
            attachment2 = MIMEApplication(f.read(), name=basename(hours_sheet_report))
            attachment2['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(hours_sheet_report))

        url = 'https://drive.google.com/file/d/1m0qSNWx7e4DN5UxMXXfOSz2sruIYvcqA/view?usp=sharing'
        path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
        res = requests.get(path)
        code = res.text
        print(hour_sheet)
        msg.attach(attachment)
        msg.attach(attachment2)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(from_addr, code)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        success_window()

    elif send_clause == ValueError: 
        fail_date_window()
    elif send_clause == SyntaxError:
        fail_hours_window()
    elif send_clause == SyntaxWarning:
        fail_hours_mixup()

def final_100_page(main_background):
    main_background.destroy()
    final_100_background =tk.Label(blank_background, bg=main_color)
    final_100_background.place(relheight=1, relwidth=1)


    
    hours_title= tk.Label(final_100_background , text="Final 100s", bg=main_color, fg='grey', font=('Times', '36','bold'))
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

    data = data[['Acct', 'Name', 'Last name', 'Groups', 'Remain hrs', 'Rev grad']]
    data=data.sort_values(by='Remain hrs')
    menu_background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_100(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Esti Final 100', bg=main_color, fg='grey', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)

    info_label = tk.Label(settings_background, text = 'Double click any student to open \n student status page', bg=main_color, fg='green', font=('Times', '25','bold'))
    info_label.place(relx=.1, rely=.75,relheight=.3, relwidth=.8)
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
    tv1.bind('<Double-Button-1>',  lambda x: select_student(tv1, 'esti_100', settings_background, x))

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

    data = data[['Acct', 'Name', 'Last name', 'Groups', 'Remain hrs', 'Rev grad']]
    data=data.sort_values(by='Remain hrs')

    menu_background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_100(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'COS Final 100', bg=main_color, fg='grey', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)
    info_label = tk.Label(settings_background, text = 'Double click any student to open \n student status page', bg=main_color, fg='green', font=('Times', '25','bold'))
    info_label.place(relx=.1, rely=.75,relheight=.3, relwidth=.8)



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
    tv1.bind('<Double-Button-1>',  lambda x: select_student(tv1, 'cos_100', settings_background, x))
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


    data = data[['Acct', 'Name', 'Last name', 'Groups', 'Remain hrs', 'Rev grad']]
    data=data.sort_values(by='Remain hrs')

    menu_background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_100(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Nails Final 100', bg=main_color, fg='grey', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)
    info_label = tk.Label(settings_background, text = 'Double click any student to open \n student status page', bg=main_color, fg='green', font=('Times', '25','bold'))
    info_label.place(relx=.1, rely=.75,relheight=.3, relwidth=.8)

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
    tv1.bind('<Double-Button-1>',  lambda x: select_student(tv1, 'nails_100', settings_background, x))
    

def massage_100(menu_background):
    data = course_100_file('Massage')
    data['Remain hrs']=data['Remain hrs'].astype(float)
    data = data[data['Remain hrs']<=100]
    Last_name = data['Name'].str.split(',').str[0]
    data['Last Name'] =  data['Name'].str.split(' ').str[0]

    First_name = data['Name'].str.split(',').str[1]
    data['Name'] =  data['Name'].str.split(' ').str[1]
    data.drop(columns=[ 'Tot hrs', 'LDA hrs', 'Last Name'], inplace=True)


    data = data[['Acct', 'Name', 'Last name', 'Remain hrs', 'Rev grad']]
    data=data.sort_values(by='Remain hrs')
    menu_background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_100(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Massage Final 100', bg=main_color, fg='grey', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)
    info_label = tk.Label(settings_background, text = 'Double click any student to open \n student status page', bg=main_color, fg='green', font=('Times', '25','bold'))
    info_label.place(relx=.1, rely=.75,relheight=.3, relwidth=.8)


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
    tv1.bind('<Double-Button-1>',  lambda x: select_student(tv1, 'massage_100', settings_background, x))


def student_explode_view(data, practicaltotals,practical_data, test_data, date, course, background):
    background.destroy()
    student_background=tk.Label(blank_background, bg=main_color)
    student_background.place(relheight=1, relwidth=1)
    
    back_button = tk.Button(student_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_student_explode(student_background, course))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    name_data = data.reset_index()
    

    student_title= tk.Label(student_background, text=name_data.loc[0, 'Name'], bg=main_color, fg='grey', font=('Times', '20','bold'))
    student_title.place(relx=.12, rely=0, relheight=.1, relwidth=.8)


    test_data = test_data.fillna(0)
    test_data = test_data.loc[:, ~(test_data > 84).any()].transpose()
    test_data = test_data.reset_index()
    test_data.rename(columns = {'index':"test", test_data.columns[1]: 'score'}, inplace=True)

    practical_data.rename(columns = {'index':"practical", practical_data.columns[1]: 'completed'}, inplace=True)
    practical_data['required'] = practicaltotals
    practical_data['remaining'] = practical_data['required'] - practical_data['completed']
    
    for row in range(len(practical_data)):
        if practical_data.loc[row,'completed'] >= practical_data.loc[row,'required']:
            practical_data.drop(labels = row, axis=0, inplace=True)



    data=data.reset_index()
    

    studentTotHrs_label = tk.Label(student_background, text=f"Hours: \n{data.loc[0, 'Tot hrs']}", bg=main_color, fg='whitesmoke', font=('Times', '12','bold'))
    studentTotHrs_label.place(rely=0.16, relx=0,relheight=.07,relwidth=.17, anchor='w')


    studentTranHrs_label = tk.Label(student_background, text=f"Transfer: \n{data.loc[0, 'Tran hrs']}", bg=main_color, fg='whitesmoke', font=('Times', '12','bold'))
    studentTranHrs_label.place(rely=0.26, relx=0,relheight=.07,relwidth=.17, anchor='w')


    studentAbsHrs_label = tk.Label(student_background, text=f"Absent: \n{data.loc[0, 'Abs hrs']}", bg=main_color, fg='whitesmoke', font=('Times', '12','bold'))
    studentAbsHrs_label.place(rely=0.36, relx=0,relheight=.07,relwidth=.17, anchor='w')


    studentMkuHrs_label = tk.Label(student_background, text=f'Make-Up: \n{data.loc[0, "MU hrs"]}', bg=main_color, fg='whitesmoke', font=('Times', '12','bold'))
    studentMkuHrs_label.place(rely=0.46, relx=0,relheight=.07,relwidth=.17, anchor='w')


    studentStart_label = tk.Label(student_background, text=f"Start Date: \n{data.loc[0, 'Start']}", bg=main_color, fg='whitesmoke', font=('Times', '12','bold'))
    studentStart_label.place(rely=0.16, relx=.25,relheight=.07,relwidth=.18, anchor='w')


    studentGrad_label = tk.Label(student_background, text=f"Grad Date: \n{data.loc[0, 'Rev grad']}", bg=main_color, fg='whitesmoke',font=('Times', '12','bold'))
    studentGrad_label.place(rely=0.26, relx=.25,relheight=.07,relwidth=.18, anchor='w')


    studentLDA_label = tk.Label(student_background, text=f"Last Day Attended: \n{data.loc[0, 'LDA']}", bg=main_color, fg='whitesmoke', font=('Times', '12','bold'))
    studentLDA_label.place(rely=0.36, relx=.25,relheight=.07,relwidth=.19, anchor='w')

    studentPercent_label = tk.Label(student_background, text=f"Atnd Percentage: \n{data.loc[0, 'Atnd %']}", bg=main_color, fg='whitesmoke',font=('Times', '12','bold'))
    studentPercent_label.place(rely=.46, relx=0.25,relheight=.07,relwidth=.18, anchor='w')



    update_date_label = tk.Label(student_background, text=f'Last updated: \n{str(date)}', bg=main_color, fg='lightgreen', font=('Times', '13','bold'))
    update_date_label.place(relx=.85, rely= .02)




    practical_tv = student_academics_view(practical_data,student_background ,rely=0.15, relx=0.45, relheight=.85,relwidth=.55)
    practical_tv.place(relheight=1, relwidth=1)


    test_tv = student_academics_view(test_data,student_background, rely=0.5, relx=0, relheight=.55,relwidth=.4)
    test_tv.place(relheight=1, relwidth=1)




def student_academics_view(data,background, rely, relx, relheight, relwidth): 

    data_frame = tk.LabelFrame(background)
    data_frame.place(rely=rely, relx=relx, relheight=relheight, relwidth=relwidth)

    tv1 = ttk.Treeview(data_frame)

    treescrolly = tk.Scrollbar(data_frame, orient='vertical', command=tv1.yview)
    tv1.configure(yscrollcommand=treescrolly.set)
    treescrolly.pack(side='right', fill='y')

    tv1['column'] = list(data.columns)
    tv1.column(data.columns[0], anchor='w')
    

    for value in data.columns[1:]:
        tv1.column(value, anchor='c')
    tv1['show'] = 'headings'

    tv1.heading(tv1['columns'][0], text=tv1['columns'][0])
    tv1.column(tv1['columns'][0], width=100)
    for column in tv1['columns'][1:]:
        tv1.heading(column, text=column)
        tv1.column(column, width=50)

    df_rows = data.to_numpy().tolist()

    for row in df_rows:
        tv1.insert('', 'end', values=row)

    return tv1

    




def select_student(tree,course, background,  x):
    for y in tree.selection():
        selected_student_id=tree.item(y, 'values')[0]

    if course == 'cos' or course == 'cos_100'  :
        date =  get_update_date('cos_status')
        data, practicaltotals,practical_data, test_data = student_status_selected_cos(int(selected_student_id))
    if course == 'esti'or course == 'esti_100' :
        date =  get_update_date('esti_status')
        data, practicaltotals,practical_data, test_data = student_status_selected_esti(int(selected_student_id))
    if course == 'nails'or course == 'nails_100' :
        date =  get_update_date('nails_status')
        data, practicaltotals,practical_data, test_data = student_status_selected_nails(int(selected_student_id))

    if course == 'massage'or course == 'massage_100' :
        date =  get_update_date('massage_status')
        data, practicaltotals,practical_data, test_data = student_status_selected_massage(int(selected_student_id))

    
    
    student_explode_view(data, practicaltotals,practical_data, test_data, date, course, background)
  



def status_page(background):
    background.destroy()
    status_background=tk.Label(blank_background, bg=main_color)
    status_background.place(relheight=1, relwidth=1)

    hours_title= tk.Label(status_background, text="Student Status", bg=main_color, fg='gray', font=('Times', '36','bold'))
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


def status_show(data, course, background):
    data_frame = tk.LabelFrame(background)
    data_frame.place(rely=0.1, relx=.55, relheight=.9,relwidth=.45)

    tv1 = ttk.Treeview(data_frame)
    if 'Groups' in data.columns:
        data.drop(columns=['Groups'],inplace=True)
    data.drop(columns=['Tot hrs'], inplace=True)
    treescrolly = tk.Scrollbar(data_frame, orient='vertical', command=tv1.yview)
    tv1.configure(yscrollcommand=treescrolly.set)
    treescrolly.pack(side='right', fill='y')

    tv1['column'] = list(data.columns)
    for value in data.columns:
        tv1.column(value, anchor='w')
    tv1['show'] = 'headings'

    for column in tv1['columns']:
        tv1.heading(column, text=column)
    tv1.column(tv1['columns'][0], width=50)
    tv1.column(tv1['columns'][1], width=250)


    df_rows = data.to_numpy().tolist()

    for row in df_rows:
        tv1.insert('', 'end', values=row)

    tv1.bind("<Control-Key-c>", lambda x: your_copy(tv1, x))
    tv1.bind('<Double-Button-1>',  lambda x: select_student(tv1, course, background, x))


    return tv1 

def status_massage(background):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp.csv'
    data = pd.read_csv(url)
    data['Tot hrs']=data['Tot hrs'].str.replace(',', '')
    data['Tot hrs'] = data['Tot hrs'].astype(float)
    data['Tot hrs'] = data['Tot hrs'] + data['Tran hrs']
    data = data[['Acct', 'Name', 'Groups', 'Tot hrs']]
    data = data[data['Groups'] == 'Massage Therapy']
    data = data.sort_values('Name')
    background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_status(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Massage Student Status', bg=main_color, fg='gray', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)

    
    entourage_logo = tk.Label(settings_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.01, rely=.2, relheight=.25, relwidth=.5)


    tv1 = status_show(data, 'massage',settings_background)

    tv1.place(relheight=1, relwidth=1)

def status_cos(background):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp.csv'
    data = pd.read_csv(url)
    data['Tot hrs']=data['Tot hrs'].str.replace(',', '')
    data['Tot hrs'] = data['Tot hrs'].astype(float)
    data['Tot hrs'] = data['Tot hrs'] + data['Tran hrs']
    data = data[['Acct', 'Name', 'Groups', 'Tot hrs']]
    data = data[(data['Groups'] == 'Cosmetology Full Time') | (data['Groups'] == 'Cosmetology Part Time')]
    data = data.sort_values(by='Name')
    data['Groups'] = data['Groups'].str.replace('Cosmetology Full Time', 'FT')
    data['Groups'] = data['Groups'].str.replace('Cosmetology Part Time', 'PT')
    background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_status(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Cosmetology Student Status', bg=main_color, fg='gray', font=('Times', '30','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)


    
    entourage_logo = tk.Label(settings_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.01, rely=.2, relheight=.25, relwidth=.5)


#Change View to Freshman COS AM 
    cos_am_fresh = data[(data['Groups'] == 'FT') & (data['Tot hrs'] <= 350)].sort_values(by=['Name'])
    cos_am_fresh_view = tk.Button(settings_background, text='Day Freshman', bg='black', fg='white', command= lambda: get_small_treeview(cos_am_fresh, settings_background, tv1))
    cos_am_fresh_view.place(relheight=.1,relwidth=.25, relx=.01,rely=.5)

#Change View to JR Cos AM 
    cos_am_JR = data[(data['Groups'] == 'FT') & (data['Tot hrs'] <= 1000) & (data['Tot hrs'] >= 350)].sort_values(by=['Name'])
    cos_am_JR_view = tk.Button(settings_background, text='Day Juniors', bg='black', fg='white', command= lambda: get_small_treeview(cos_am_JR, settings_background, tv1))
    cos_am_JR_view.place(relheight=.1,relwidth=.25, relx=.01,rely=.64)

#Change View to SR Cos AM 
    cos_am_SR = data[(data['Groups'] == 'FT') & (data['Tot hrs'] >= 1000)].sort_values(by=['Name'])
    cos_am_SR_view = tk.Button(settings_background, text='Day Seniors', bg='black', fg='white', command= lambda: get_small_treeview(cos_am_SR, settings_background, tv1))
    cos_am_SR_view.place(relheight=.1,relwidth=.25, relx=.01,rely=.78)

#Change View to Freshman COS PM 
    cos_pm_fresh = data[(data['Groups'] == 'PT') & (data['Tot hrs'] <= 350)].sort_values(by=['Name'])
    cos_pm_fresh_view = tk.Button(settings_background, text='Night Freshman', bg='black', fg='white', command= lambda: get_small_treeview(cos_pm_fresh, settings_background, tv1))
    cos_pm_fresh_view.place(relheight=.1,relwidth=.25, relx=.28,rely=.5)

#Change View to JR Cos PM
    cos_pm_JR = data[(data['Groups'] == 'PT') & (data['Tot hrs'] <= 1000) & (data['Tot hrs'] >= 350)].sort_values(by=['Name'])
    cos_pm_JR_view = tk.Button(settings_background, text='Night Juniors', bg='black', fg='white', command= lambda: get_small_treeview(cos_pm_JR, settings_background, tv1))
    cos_pm_JR_view.place(relheight=.1,relwidth=.25, relx=.28,rely=.64)

#Change View to SR Cos PM
    cos_pm_SR = data[(data['Groups'] == 'PT') & (data['Tot hrs'] >= 1000)].sort_values(by=['Name'])
    cos_pm_SR_view = tk.Button(settings_background, text='Night Seniors', bg='black', fg='white', command= lambda: get_small_treeview(cos_pm_SR, settings_background, tv1))
    cos_pm_SR_view.place(relheight=.1,relwidth=.25, relx=.28,rely=.78)

    tv1 = status_show(data, 'cos', settings_background)

    tv1.place(relheight=1, relwidth=1)


def status_esti(background):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp.csv'
    data = pd.read_csv(url)
    data['Tot hrs']=data['Tot hrs'].str.replace(',', '')
    data['Tot hrs'] = data['Tot hrs'].astype(float)
    data['Tot hrs'] = data['Tot hrs'] + data['Tran hrs']
    data = data[['Acct', 'Name', 'Groups', 'Tot hrs']]
    data = data[(data['Groups'] == 'Esthetics Full Time') | (data['Groups'] == 'Esthetics Part Time')]
    data['Groups'] = data['Groups'].str.replace('Esthetics Full Time', 'FT')
    data['Groups'] = data['Groups'].str.replace('Esthetics Part Time', 'PT')
    data = data.sort_values('Tot hrs', ascending=False)
    background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_status(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Esthetics Student Status', bg=main_color, fg='gray', font=('Times', '30','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)


    esti_pm = data[data['Groups'] == 'PT'].sort_values('Tot hrs', ascending=False)
    esti_am = data[data['Groups'] == 'FT'].sort_values('Tot hrs', ascending=False)




    jr_pm = esti_pm[(esti_pm['Tot hrs'] > 290) & (esti_pm['Tot hrs'] < 690)].sort_values(by=['Name'])

    entourage_logo = tk.Label(settings_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.01, rely=.2, relheight=.25, relwidth=.5)


    fresh_am = esti_am[esti_am['Tot hrs'] < 290].sort_values(by=['Name'])
    esti_hours_FRam = tk.Button(settings_background, text='Freshman AM', bg='maroon', fg='white', command= lambda: get_small_treeview(fresh_am, settings_background, tv1))
    esti_hours_FRam.place(relheight=.1,relwidth=.25, relx=.01,rely=.5)


    jr_am = esti_am[(esti_am['Tot hrs'] > 290) & (esti_am['Tot hrs'] < 690)].sort_values(by=['Name'])
    esti_hours_JRam = tk.Button(settings_background, text='Junior AM', bg='maroon', fg='white', command= lambda: get_small_treeview(jr_am, settings_background, tv1))
    esti_hours_JRam.place(relheight=.1,relwidth=.25, relx=.01,rely=.64)

    sr_am = esti_am[esti_am['Tot hrs'] >= 690 ].sort_values(by=['Name'])
    esti_hours_SRam = tk.Button(settings_background, text='Senior AM', bg='maroon', fg='white', command= lambda: get_small_treeview(sr_am, settings_background, tv1))
    esti_hours_SRam.place(relheight=.1,relwidth=.25, relx=.01,rely=.78)



    fresh_pm = esti_pm[esti_pm['Tot hrs'] < 290].sort_values(by=['Name'])
    esti_hours_FRpm = tk.Button(settings_background, text='Freshman PM', bg='Maroon', fg='white', command= lambda: get_small_treeview(fresh_pm, settings_background, tv1))
    esti_hours_FRpm.place(relheight=.1,relwidth=.25, relx=.28,rely=.5)

    jr_pm = esti_pm[(esti_pm['Tot hrs'] > 290) & (esti_pm['Tot hrs'] < 690)].sort_values(by=['Name'])
    esti_hours_JRpm = tk.Button(settings_background, text='Junior PM', bg='Maroon', fg='white', command= lambda: get_small_treeview(jr_pm, settings_background, tv1))
    esti_hours_JRpm.place(relheight=.1,relwidth=.25, relx=.28,rely=.64)


    sr_pm = esti_pm[esti_pm['Tot hrs'] >= 690 ].sort_values(by=['Name'])
    esti_hours_SRpm = tk.Button(settings_background, text='Senior PM', bg='Maroon', fg='white', command= lambda: get_small_treeview(sr_pm, settings_background, tv1))
    esti_hours_SRpm.place(relheight=.1,relwidth=.25, relx=.28,rely=.78)

    tv1 = status_show(data, 'esti',settings_background)

    tv1.place(relheight=1, relwidth=1)


def status_nails(background):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp.csv'
    data = pd.read_csv(url)
    data['Tot hrs']=data['Tot hrs'].str.replace(',', '')
    data['Tot hrs'] = data['Tot hrs'].astype(float)
    data['Tot hrs'] = data['Tot hrs'] + data['Tran hrs']
    data = data[['Acct', 'Name', 'Groups', 'Tot hrs']]
    data = data[(data['Groups'] == 'Nails Full Time') | (data['Groups'] == 'Nails Part Time')]
    data['Groups'] = data['Groups'].str.replace('Nails Full Time', 'FT')
    data['Groups'] = data['Groups'].str.replace('Nails Part Time', 'PT')
    data = data.sort_values('Name')
    background.destroy()
    settings_background =tk.Label(blank_background, bg=main_color)
    settings_background.place(relheight=1, relwidth=1)

    back_button = tk.Button(settings_background, text='Back', bg='black', fg='white',activebackground='black', command= lambda: clear_status(settings_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)

    title_label = tk.Label(settings_background, text = 'Nail Student Status', bg=main_color, fg='gray', font=('Times', '36','bold'))
    title_label.place(relx=.1, rely=0,relheight=.1, relwidth=.8)

    entourage_logo = tk.Label(settings_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.01, rely=.2, relheight=.25, relwidth=.5)

    nail_am = data[data['Groups'] == 'FT'].sort_values('Name')
    nail_am_view = tk.Button(settings_background, text='Day Nails', bg='black', fg='white', command= lambda: get_small_treeview(nail_am, settings_background, tv1))
    nail_am_view.place(relheight=.1,relwidth=.25, relx=.01,rely=.5)

    nail_pm = data[data['Groups'] == 'PT'].sort_values('Name')
    nail_pm_view = tk.Button(settings_background, text='Night Nails', bg='black', fg='white', command= lambda: get_small_treeview(nail_pm, settings_background, tv1))
    nail_pm_view.place(relheight=.1,relwidth=.25, relx=.28,rely=.5)

    tv1 = status_show(data, 'nails',settings_background)

    tv1.place(relheight=1, relwidth=1)


def get_small_treeview(data, background, tree):

    for item in tree.get_children():
      tree.delete(item)
    if 'Groups' in data.columns:
        data.drop(columns= ['Groups'], inplace=True)
    df_rows = data.to_numpy().tolist()
    for row in df_rows:
        tree.insert('', 'end', values=row)



def success_window():
    messagebox.showinfo("Sucess", "Hours Have Been Submitted!") 

def fail_date_window():
    messagebox.showerror("Correct Dates Format", "Error Check Date Format is\nMM/DD/YY \nor\nMM/DD/YY - MM/DD/YY for two days") 
def fail_hours_window():
    messagebox.showerror("Correct hours Format", "Error Check hour Format is\nH:MM am \nor\nH:MM pm ") 
def fail_hours_mixup():
    messagebox.showerror("Correct hours Format", "Error one or more of your clock in times is later than then clock out time")
def clear(background):
    hours_menu(background)

def clear_status(background):
    status_page(background)

def clear_student_explode(background, course):
    if course == 'esti':
        status_esti(background)
    if course == 'cos':
        status_cos(background)
    if course == 'nails':
        status_nails(background)
    if course == 'massage':
        status_massage(background)
    if course == 'massage_100':
        massage_100(background)
    if course == 'cos_100':
        cos_100(background)
    if course == 'esti_100':
        esti_100(background)
    if course == 'nails_100':
        nails_100(background)




def clear_100(background):
    final_100_page(background)

def clear_main(background):
    background.destroy()
    show_menu()

show_menu()