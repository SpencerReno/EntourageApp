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




def show_menu():
    main_background =tk.Label(blank_background, bg=main_color)
    main_background.place(relheight=1, relwidth=1)


    directors_ed = tk.Label(main_background, text="DIRECTORS EDITION", bg=main_color, fg='black', font=('Times', '36','bold'))
    directors_ed.place(relx=.12, rely=.05, relheight=.15, relwidth=.8)

    entourage_logo = tk.Label(main_background, width=w, height=h,image=EN_photo,bg=main_color)
    entourage_logo.place(relx=.19, rely=.23, relheight=.3, relwidth=.6)


    payment_totals = tk.Button(main_background, text='Daily Totals', bg='black', fg='white', command=lambda: reports_page(main_background))
    payment_totals.place(relheight=.1,relwidth=.25, relx=.23,rely=.6)

    hours_creator = tk.Button(main_background, text='Hours Creator', bg='black', fg='white', command=lambda: hours_menu(main_background))
    hours_creator.place(relheight=.1,relwidth=.25, relx=.52,rely=.6)

    account_cards = tk.Button(main_background, text='Account Cards', bg='black', fg='white', command=lambda: account_cards_page(main_background))
    account_cards.place(relheight=.1,relwidth=.25, relx=.38,rely=.8)






    root.mainloop()


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

def account_cards_page(main_background):
    main_background.destroy()
    account_background =tk.Label(blank_background, bg=main_color)
    account_background.place(relheight=1, relwidth=1)


    back_button = tk.Button(account_background, text='Back', bg='black', fg='white', activebackground='black',command= lambda: clear_main(account_background))
    back_button.place(relheight=.1,relwidth=.1, relx=.0,rely=.0)


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
            messagebox.showinfo("Student Removal", f'Failed to remove student {tv1.item(i)["values"][0]} please try again')
        

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



def get_path(event):
    pathLabel.configure(text = event.data)

def clear(background):
    hours_menu(background)

def clear_main(background):
    background.destroy()
    show_menu()

show_menu()
