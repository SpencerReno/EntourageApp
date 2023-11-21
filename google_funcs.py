import pandas as pd
import requests
from io import StringIO
from tkinter.filedialog import asksaveasfile
import re
from datetime import date
import datetime
import calendar
import numpy as np 
import smtplib
from email import message
import getpass
import smtplib
from email import message
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def adding(text):
    total = 0
    for line in text:
        res = re.findall(r'\d+', line)
        for x in res[:-1]:
            final =  ''.join(res)
            final = f'{final[:-2]}.{final[-2:]}'
        total = total + float(final)

    return total



def get_student_status(course):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/Entourage%20Remaining%20Hours.csv'
    data = pd.read_csv(url)
    data = data[['Acct', 'Name','Groups', 'Tot hrs', 'Tran hrs', 'Remain hrs', 'Atnd %', 'Rev Grad']]

    if course == 'Cos PT':
        data = data[data['Groups'] =='Cosmetology Part Time']   
    elif course == 'Cos FT':
        data = data[data['Groups'] == 'Cosmetology Full Time']


    elif course == 'Nails PT':
        data = data[data['Groups'] == 'Nails Part Time']
    elif course == 'Nails FT':
        data = data[data['Groups'] == 'Nails Full Time']


    elif course == 'Esti FT':
        data = data[data['Groups'] == 'Esthetics Full Time']
    elif course == 'Esti PT':
        data = data[data['Groups'] == 'Esthetics Part Time']
    
    
    elif course == 'Massage':
        data = data[data['Groups'] == 'Massage Therapy']


    return data





def get_unpaid_students():
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/Entourage%20Remaining%20Hours.csv'
    data = pd.read_csv('./CSV Files/Ledger.csv')  
    student_column = data.columns[8]
    student_ids_column =data.columns[5]
    data.rename(columns={data.columns[4]: 'Dates'}, inplace=True)

    new_df = pd.DataFrame(columns=['Student Id', 'Name', 'Balance', 'Last Payed Date'] )


    data[data.columns[8]]=data[student_column].str.replace(r"\(.", "", regex=True)
    data[data[data.columns[8]].str.contains('\(')]

    data = data[[data.columns[4], data.columns[5], data.columns[8],
        data.columns[13]]]

    student_names = [student_column]
    student_ids = [student_ids_column]
    multiplyer = []
    data.rename(columns={student_column: 'Balance'}, inplace=True)
    for x in range(len(data)):
        try:
            data['Balance'][x] = int(data['Balance'][x])
        except:
            student_names.append(data['Balance'][x])
            student_ids.append(data[data.columns[1]][x])
            multiplyer.append(x)

    
    multiplyer.append(len(data))

    new_multi = [(multiplyer[i+1]-multiplyer[i]) -1 for i in range(len(multiplyer)-1)]
    new_multi.insert(0, multiplyer[0])
    balanceValues = []
    dateValues = []
    for x in range(len(data)):
        if type(data['Balance'][x]) == int:
            balanceValues.append(f"${data['Balance'][x]}")
        if data['Dates'][x] != 'Student ID:':
            dateValues.append(data['Dates'][x])


    fixed_student_ids = []
    for x in range(len(student_ids)):
        for num in range(new_multi[x]):
            fixed_student_ids.append(student_ids[x])

    student_names_col = []
    for x in range(len(student_names)):
        for num in range(new_multi[x]):
            student_names_col.append(student_names[x])


    
    new_df['Student Id'] = fixed_student_ids
    new_df['Name'] = student_names_col
    new_df['Balance'] = balanceValues
    new_df['Last Payed Date'] =dateValues 

    new_df['Last Payed Date'] = pd.to_datetime(new_df['Last Payed Date'])
    new_df['Last Payed Date'] = new_df['Last Payed Date'].dt.normalize()
    new_df['Last Payed Date'] = new_df['Last Payed Date'].dt.floor('D')

    new_df= new_df.drop_duplicates(['Name'], keep='last')
    res = calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)
    startdate = f'{datetime.datetime.now().year}-{datetime.datetime.now().month}-1'
    Final_df = new_df[(new_df['Last Payed Date'] < startdate)]
    Final_df['Last Payed Date'] = pd.to_datetime(Final_df['Last Payed Date']).dt.date
    return Final_df

def course_100_file(course):
    url  = 'https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/Entourage%20Remaining%20Hours.csv'
    data = pd.read_csv(url)
    if course == 'Cos':
        data = data[(data['Groups']=='Cosmetology Full Time') | (data['Groups'] == 'Cosmetology Part Time')]
    if course == 'Esti':
        data = data[(data['Groups']=='Esthetics Full Time') | (data['Groups'] == 'Esthetics Part Time')]
    if course == 'Nails':
        data = data[(data['Groups']=='Nails Full Time') | (data['Groups'] == 'Nails Part Time')]
    if course == 'Massage':
        data = data[data['Groups']=='Massage Therapy']
        
    try:
        data['Remain hrs'] = data['Remain hrs'].str.replace(',', '')
        return data
    except:
        return data
    



def esti_online_hours():  
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/Entourage%20Remaining%20Hours.csv'
    data = pd.read_csv(url)
    data = data[['Acct', 'Name', 'Last name', 'Groups', 'Tot hrs', 'Tran hrs']]
    esti_data = data[(data['Groups'] == 'Esthetics Full Time') | (data['Groups'] == 'Esthetics Part Time')]
    esti_data['Name']= esti_data['Name'].str.split(',').str[1]
    esti_data['Name'] = esti_data['Name'].str.split(' ').str[1]

    try:
        esti_data['Tot hrs']=esti_data['Tot hrs'].str.replace(',', '')
        esti_data['Tot hrs'] = esti_data['Tot hrs'].astype(float)


    except:
        print('No Errors')
    

    esti_data['Tot hrs'] = esti_data['Tot hrs'] + esti_data['Tran hrs']


    esti_data.drop(columns=['Tran hrs'],inplace=True)

    esti_data.sort_values(by='Last name',inplace=True)
    esti_data['Tot hrs']=esti_data['Tot hrs'].astype(float)
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Students Holding back
    try: 
        url = 'https://api.apispreadsheets.com/data/aAZcLsK62BpKyvIJ/'
        res = requests.get(url).json()

        


        for student_id in res['data']:
            try:    
                index_of_student = esti_data[esti_data['Acct'] == int(student_id['Acct'])].index
                
                esti_data.loc[index_of_student[0], 'Tot hrs'] -= 100
            except:
                print(f'Error with Student{student_id}')
    except:
        print('Out of request')

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    esti_pm = esti_data[esti_data['Groups'] != 'Esthetics Full Time']

    esti_am = esti_data[esti_data['Groups'] == 'Esthetics Full Time']

    fresh_am = esti_am[esti_am['Tot hrs'] < 290]
    jr_am = esti_am[(esti_am['Tot hrs'] > 290) & (esti_am['Tot hrs'] < 690)]
    sr_am = esti_am[esti_am['Tot hrs'] >= 690 ]
    sr_pm = esti_pm[esti_pm['Tot hrs'] >= 690 ]

    fresh_pm = esti_pm[esti_pm['Tot hrs'] < 290]
    jr_pm = esti_pm[(esti_pm['Tot hrs'] > 290) & (esti_pm['Tot hrs'] < 690)]


    def add_cols_am(data):
        if data['Tot hrs'].iloc[0] < 290:
            data['hours'] =  '9:00 - 3:00'
        if data['Tot hrs'].iloc[0] > 290 and data['Tot hrs'].iloc[0] < 690:
            data['hours'] = '9:00 - 3:00'

        if data['Tot hrs'].iloc[0] >=690:
            data['hours'] = '9:00 - 4:00'

        
        data['Date'] = ' '
        data['Aissigned Work'] = ' '
        data.reset_index(inplace=True)
        data.drop(columns=['Tot hrs', 'index', 'Groups'], inplace=True)




    def add_cols_pm(data):
        if data['Tot hrs'].iloc[0] < 290:
            data['hours'] =  '4:30 - 9:30'
        if data['Tot hrs'].iloc[0] > 290 and data['Tot hrs'].iloc[0] < 690:
            data['hours'] = '4:30 - 9:30'
        
        if data['Tot hrs'].iloc[0] >= 690:
            data['hours'] = '4:30 - 9:30'
            

        
        data['Date'] = ' '
        data['Aissigned Work'] = ' '
        data.reset_index(inplace=True)
        data.drop(columns=['Tot hrs', 'index', 'Groups'], inplace=True)


        
    add_cols_am(fresh_am)
    add_cols_am(jr_am)
    add_cols_pm(fresh_pm)
    add_cols_pm(jr_pm)
    add_cols_am(sr_am)
    add_cols_pm(sr_pm)

    return fresh_am, fresh_pm, jr_am, jr_pm, sr_am, sr_pm




def cos_online_hours():
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/Entourage%20Remaining%20Hours.csv'
    data = pd.read_csv(url)
    data = data[['Acct', 'Name', 'Last name', 'Groups']]
    cos_data = data[(data['Groups'] == 'Cosmetology Full Time') | (data['Groups'] == 'Cosmetology Part Time')]


    cos_data['Name']=cos_data['Name'].str.split(',').str[1]
    cos_data['Name'] = cos_data['Name'].str.split(' ').str[1]


    cos_data.sort_values(by='Name', inplace=True)

    cos_full = cos_data[cos_data['Groups'] == 'Cosmetology Full Time']
    cos_full.drop(columns=['Groups'], inplace=True)
    cos_full['hours'] = "9:00 - 4:00"
    cos_full['Date'] = ' '
    cos_full['Homework Given'] = ' '


    
    cos_part = cos_data[cos_data['Groups'] != 'Cosmetology Full Time']
    cos_part.drop(columns=['Groups'], inplace=True)
    cos_part['hours'] = "5:30 - 9:30"
    cos_part['Date'] = ' '
    cos_part['Homework Given'] =  ' '


    return cos_full, cos_part

def massage_online_hours():
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/Entourage%20Remaining%20Hours.csv'
    data = pd.read_csv(url)
    data = data[['Acct', 'Name', 'Last name', 'Groups']]
    massage_data = data[(data['Groups'] == 'Massage Therapy')].drop(columns=['Groups'])

    massage_data['hours'] = "9:00 - 4:00"
    massage_data['Date'] = ' '
    massage_data['Homework Given'] =  ' '


    return massage_data



def nails_online_hours():
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/Entourage%20Remaining%20Hours.csv'
    data = pd.read_csv(url)
    data = data[['Acct', 'Name', 'Last name', 'Groups']]
    nails_data = data[(data['Groups'] == 'Nails Full Time') | (data['Groups'] == 'Nails Part Time')]


    nails_data['Name']=nails_data['Name'].str.split(',').str[1]
    nails_data['Name'] = nails_data['Name'].str.split(' ').str[1]


    nails_data.sort_values(by='Name', inplace=True)

    nails_full = nails_data[nails_data['Groups'] == 'Nails Full Time']
    nails_full.drop(columns=['Groups'], inplace=True)
    nails_full['hours'] = "9:00 - 4:00"
    nails_full['Date'] = ' '
    nails_full['Homework Given'] = ' '


    
    nails_part= nails_data[nails_data['Groups'] != 'Nails Full Time']
    nails_part.drop(columns=['Groups'], inplace=True)
    nails_part['hours'] = "5:30 - 9:30"
    nails_part['Date'] = ' '
    nails_part['Homework Given'] =  ' '


    return nails_full, nails_part 
    



def get_download_clock_file(df):
    df['Date']=df['Date'].replace(' ', np.nan)
    df=df.dropna(axis=0)
    clocked_hours = pd.DataFrame(columns=[0,1,2])
    for x in range(0, len(df)):
        try:
            df['Date'] = df['Date'].iloc[x].replace(" ", '')
            if df['Date'].iloc[x].contains('&'): #find a way to handle & 
                dates = df['Date'].iloc[x].split('&')
                print('here', dates)
            else:
                dates = df['Date'].iloc[x].split('-')
            student_id = df['Acct'].iloc[x]
            for date in dates:
                month = date.split('/')[0]
                day = date.split('/')[1]
                year = date.split('/')[2][-2:]
                out_time = int(df['hours'].iloc[x].split('-')[1][1]) + 12
                clocked_in = {
                0 : 'PN00',
                1 : f'{year}{month}{day}090000',
                2: f'10000M00000{student_id}'
                }

                Clock_out = {
                    0 : 'PN00',
                    1 : f'{year}{month}{day}{str(out_time)}0000',
                    2: f'50000M00000{student_id}'
                }   
                
                clocked_hours = clocked_hours.append(clocked_in, ignore_index=True)
                clocked_hours=clocked_hours.append(Clock_out, ignore_index=True)
                
        except:
            
            student_id = df['Acct'].iloc[x]
            month = df['Date'].iloc[x].split('/')[0]
            day = df['Date'].iloc[x].split('/')[1]
            year = df['Date'].iloc[x].split('/')[2][-2:]
            print(df['hours'].iloc[x].split('-')[1][1])
            out_time = int(df['hours'].iloc[x].split('-')[1][1]) + 12
        
            clocked_in = {
                0 : 'PN00',
                1 : f'{year}{month}{day}090000',
                2: f'10000M00000{student_id}'
            }

            Clock_out = {
                0 : 'PN00',
                1 : f'{year}{month}{day}{str(out_time)}0000',
                2: f'50000M00000{student_id}'
            }

            clocked_hours = clocked_hours.append(clocked_in, ignore_index=True)
            clocked_hours=clocked_hours.append(Clock_out, ignore_index=True)


    return clocked_hours













def held_back_students():
    url = 'https://api.apispreadsheets.com/data/aAZcLsK62BpKyvIJ/'
    res = requests.get(url).json()

    df = pd.DataFrame.from_dict(res['data'])

    return df

    




