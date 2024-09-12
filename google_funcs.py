import pandas as pd
import requests
from io import StringIO
from tkinter.filedialog import asksaveasfile
import re
from datetime import date, datetime
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
from dateutil import parser
import os.path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


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
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp.csv'
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
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/ledger.csv'
    data = pd.read_csv(url, header=None)  
    data = data[[data.columns[4], data.columns[5], data.columns[6], data.columns[8], data.columns[13]]]

    data_test = data[data[data.columns[2]].str.contains('Student Status')].reset_index()
    balance =[]
    for x in data_test['index'][1:]:
        balance.append(data.iloc[x-1][data.columns[3]])

    balance.append(data.iloc[-1][data.columns[3]])
    last_date =[]
    for y in data_test['index'][1:]:
        last_date.append(data.iloc[y-1][data.columns[0]])

    last_date.append(data.iloc[-1][data.columns[0]])

    data_test['Balance'] = balance
    data_test['Last Payed Date'] = last_date
    data_test
    data = data_test[[5,8,'Balance','Last Payed Date', 6]]
    data.rename(columns={5:'Student Id', 8:'Name', 6: 'status'}, inplace=True)
    data['status'] =data['status'].str.split(':').str[1]
    print(data['status'].unique())
    return data

def course_100_file(course):
    url  = 'https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp.csv'
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
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp.csv'
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
            data['clock in'] =  '9:00 am'
            data['clock out'] =  '3:00 pm'
        if data['Tot hrs'].iloc[0] > 290 and data['Tot hrs'].iloc[0] < 690:
            data['clock in'] =  '9:00 am'
            data['clock out'] = '3:00 pm'

        if data['Tot hrs'].iloc[0] >=690:
            data['clock in'] =  '9:00 am'
            data['clock out'] = '4:00 pm'    
        
        data['Date'] = ' '
        data['Aissigned Work'] = ' '
        data.reset_index(inplace=True)
        data.drop(columns=['Tot hrs', 'index', 'Groups'], inplace=True)




    def add_cols_pm(data):
        if data['Tot hrs'].iloc[0] < 290:
            data['clock in'] =  '4:30 pm'
            data['clock out'] =  '9:30 pm'
        if data['Tot hrs'].iloc[0] > 290 and data['Tot hrs'].iloc[0] < 690:
            data['clock in'] =  '4:30 pm'
            data['clock out'] =  '9:30 pm'
        
        if data['Tot hrs'].iloc[0] >= 690:
            data['clock in'] =  '4:30 pm'
            data['clock out'] =  '9:30 pm'
            

        
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
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp.csv'
    data = pd.read_csv(url)
    data = data[['Acct', 'Name', 'Last name', 'Groups']]
    cos_data = data[(data['Groups'] == 'Cosmetology Full Time') | (data['Groups'] == 'Cosmetology Part Time')]


    cos_data['Name']=cos_data['Name'].str.split(',').str[1]
    cos_data['Name'] = cos_data['Name'].str.split(' ').str[1]


    cos_data.sort_values(by='Name', inplace=True)

    cos_full = cos_data[cos_data['Groups'] == 'Cosmetology Full Time']
    cos_full.drop(columns=['Groups'], inplace=True)
    cos_full['clock in'] =  '9:00 am'
    cos_full['clock out'] = '4:00 pm'
    cos_full['Date'] = ' '
    cos_full['Homework Given'] = ' '


    
    cos_part = cos_data[cos_data['Groups'] != 'Cosmetology Full Time']
    cos_part.drop(columns=['Groups'], inplace=True)
    cos_part['clock in'] =  '5:30 pm'
    cos_part['clock out'] = '9:30 pm'
    cos_part['Date'] = ' '
    cos_part['Homework Given'] =  ' '


    return cos_full, cos_part

def massage_online_hours():
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp.csv'
    data = pd.read_csv(url)
    data = data[['Acct', 'Name', 'Last name', 'Groups']]
    massage_data = data[(data['Groups'] == 'Massage Therapy')].drop(columns=['Groups'])
    massage_data['Name']=massage_data['Name'].str.split(',').str[1]
    massage_data['Name'] = massage_data['Name'].str.split(' ').str[1]

    massage_data['clock in'] =  '9:00 am'
    massage_data['clock out'] = '4:00 pm'   
    massage_data['Date'] = ' '
    massage_data['Homework Given'] =  ' '


    return massage_data



def nails_online_hours():
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp.csv'
    data = pd.read_csv(url)
    data = data[['Acct', 'Name', 'Last name', 'Groups']]
    nails_data = data[(data['Groups'] == 'Nails Full Time') | (data['Groups'] == 'Nails Part Time')]


    nails_data['Name']=nails_data['Name'].str.split(',').str[1]
    nails_data['Name'] = nails_data['Name'].str.split(' ').str[1]


    nails_data.sort_values(by='Name', inplace=True)

    nails_full = nails_data[nails_data['Groups'] == 'Nails Full Time']
    nails_full.drop(columns=['Groups'], inplace=True)

    nails_full['clock in'] =  '9:00 am'
    nails_full['clock out'] = '4:00 pm'
    nails_full['Date'] = ' '
    nails_full['Homework Given'] = ' '


    
    nails_part= nails_data[nails_data['Groups'] != 'Nails Full Time']
    nails_part.drop(columns=['Groups'], inplace=True)
    nails_part['clock in'] =  '5:30 pm'
    nails_part['clock out'] = '9:30 pm'   
    nails_part['Date'] = ' '
    nails_part['Homework Given'] =  ' '


    return nails_full, nails_part 



def get_download_clock_file(df):
    df['Date'] = df['Date'].apply(lambda x: x.strip())
    df['Date']= df['Date'].replace('', np.nan)
    df=df.dropna(axis=0)
    clocked_hours = pd.DataFrame(columns=[0,1,2])
    df['Date']=df['Date'].replace(' ', '')
    print(df)
    send_clause= False
    try:
        for x in range(len(df)):
            student_id = df['Acct'].iloc[x]
            date_list = []
            string = df['Date'].iloc[x].replace(' ', '')
            if len(string)> 9:
                if '-' in string:
                    if len(string.split('-')) <=2:
                        for y in range(len(string.split('-'))):
                            date_ = parser.parse(string.split('-')[y])
                            date_list.append(date_)
                        send_clause = True
            else:
                if '-' not in string:
                    if len(string) <= 8:
                        print(string)
                        if int(string.split('/')[0])>=1 and int(string.split('/')[0])<13:
                            if int(string.split('/')[1])>=1 and int(string.split('/')[1])<=31:
                                    date_list.append(parser.parse(string))
                                    send_clause = True

            for date_ in date_list:
                month = date_.month
                if len(str(month)) == 1:
                    month = f'0{str(month)}'

                day = date_.day
                if len(str(day)) == 1:
                    day = f'0{str(day)}'


                year_test = int(str(date_.year)[-2:])


                #Check if the year entered is == to last year   
                if year_test == int(str(date.today().year)[-2:]) - 1:
                    year= year_test
                #Check if the year entered is == to next year   
                elif year_test == int(str(date.today().year)[-2:]) +1:
                    year = year_test
                #Check if the year entered is == to current year    
                elif year_test == int(str(date.today().year)[-2:]):
                    year = year_test

                else:
                    year = int(str(date.today().year)[-2:])


           ## FIX ERROR HERE !!!!!!!
                intime = df['clock in'].iloc[x][:4].strip(' ')
                in_condition = df['clock in'].iloc[x][4:].strip(' ')
                outtime = df['clock out'].iloc[x][:4].strip(' ')
                out_condition = df['clock out'].iloc[x][4:].strip(' ')
                print(intime, in_condition, outtime, out_condition)
                if in_condition.lower()  != 'am' and in_condition.lower() != 'pm':
                    raise SyntaxError
            
                if  out_condition.lower()  !='am'   and out_condition.lower()  != 'pm':
                    raise SyntaxError
                print('here')
                in_time_hour = intime.split(':')[0]
                if len(in_time_hour) < 2 and 'am' in in_condition:
                    in_time_hour =f'0{in_time_hour}'

                out_time_hour = outtime.split(':')[0]    
                if len(out_time_hour) < 2 and 'am' in out_condition:
                    out_time_hour =f'0{out_time_hour}'

                if in_time_hour > out_time_hour:
                    raise SyntaxWarning

                if 'pm' in out_condition:
                    out_time_hour = str(int(out_time_hour )+ 12)
                
                if 'pm' in in_condition:
                    in_time_hour = str(int(in_time_hour )+ 12)


                clock_in = {
                    0 : 'PN00',
                    1 : f'{year}{month}{day}{in_time_hour}{str(intime.split(":")[1])}00'.replace(' ', ''),
                    2: f'10000M00000{student_id}'.replace(' ', '')
                    }

                clock_out = {
                        0 : 'PN00',
                        1 : f'{year}{month}{day}{out_time_hour}{str(outtime.split(":")[1])}00'.replace(' ', ''),
                        2: f'50000M00000{student_id}'.replace(' ', '')
                    }   
                print(clock_in)
                clocked_hours = clocked_hours.append(clock_in, ignore_index=True)
                clocked_hours=clocked_hours.append(clock_out, ignore_index=True)

        return clocked_hours, send_clause
    except ValueError:
        send_clause= ValueError
        return clocked_hours, send_clause
    except SyntaxError:
        send_clause = SyntaxError
        return clocked_hours, send_clause
    except SyntaxWarning:
        send_clause = SyntaxWarning
        return clocked_hours, send_clause
    except IndexError:
        send_clause = SyntaxError
        return clocked_hours, send_clause
    


def held_back_students():
    url = 'https://api.apispreadsheets.com/data/aAZcLsK62BpKyvIJ/'
    res = requests.get(url).json()

    df = pd.DataFrame.from_dict(res['data'])

    return df

    


def student_status_selected_cos(student_id):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp%20Cos.csv'
    data = pd.read_csv(url)

    data = data[data['Acct'] == student_id]
    column_renames = {
        'L01' : 'Hair Coloring',
        'L02': 'Hair Lightening',
        'L03': 'Chemical Waving',
        'L04':'Chemical Relaxing',
        'L05': 'Razor Cutting',
        'L06':  'Shear Cutting',
        'L07' : 'Pincurl Set',
        'L08': 'Pincurl & Wave',
        'L09' : 'Roller Set',
        'L10': 'Comb Out',
        'L11': 'Curling Iron Set',
        'L12' : 'Shampoo/Rinse/Treat',
        'L13': 'Blow Dry Styling',
        'L14': 'Sanitation',
        'L15': 'Manicure',
        'L16':'Pedicure',
        'L17': 'Business Practice',
        'L18' : 'Facials',
        'L19': 'Make-up',
        'L20': 'Client Consultation',
        'L21':   'Waxing',
        'L22' : 'Acrylic Nails', 

        'W01' : 'Ch 1 History & Career Opp',
        'W02' : 'Ch 2 Life Skills',
        'W03' : 'Ch 3 Professional Image',
        'W04' :'Ch 4 Commun. for Success',
        'W05' :'Ch 5 Infection Control',
        'W06' :'Ch 6 Anatomy & Physiology',
        'W07' :'Ch 7 Skin Struct & Growth',
        'W08' :'Ch 8 Skin Struct & Growth',
        'W09' :'Ch 9 Nail Structure',
        'W10':'Ch 10 Nails Disease & Dis',
        'W11':'Ch 11 Prop of Hair & Scal',
        'W12' :'Ch 12 Basics of Chemistry',
        'W13' : 'Ch 13 Electricity',
        'W14' : 'Ch 14 Hair Design',
        'W15' : 'Ch 15 Scalp, Shampoo & Co',
        'W16' : 'Ch 16 Haircutting',
        'W17' : 'Ch 17 Hairstyling',
        'W18' : 'Ch 18 Braiding',
        'W19' : 'Ch 19 Wigs & Hair Additio',
        'W20' : 'Ch 20 Chemical Texture',
        'W21' : 'Ch 21 Hair Coloring',
        'W22' : 'Ch 22 Hair Removal',
        'W23' : 'Ch 23 Facial',
        'W24' : 'Ch 24 Facial Makeup',
        'W25' : 'Ch 25 Manicuing',
        'W26' : 'Ch 26 Pedicuring',
        'W27': 'Ch 27-29 Nail Enhancemen',
        'W28':'Ch 30 Employment',
        'W29':'Ch 31-32 Salon Business',
        'W30':'Salon Project',
        'W31':'Kansas State Law',
        'W32':'Mid-Term Exam',
        'W33':'Final Exam',
        'W34':'Mock State Board Exam I',
        'W35':'Mock State Board Exam II',
        'W36':'Mock State Board Exam III',
        'W37':'Resume'

    }

    practicaltotals = [50,50,25,25,25,50,25,25,50,50,75,150,75,150,10,10,25,10,5,50,10,20]
    data = data.rename(columns= column_renames)
    
    test_data = data[data.columns[26:-9]]
    practical_data= data[data.columns[4:26]].transpose().reset_index()


    

    return data,practicaltotals, practical_data, test_data



def student_status_selected_esti(student_id):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp%20Esti.csv'
    data = pd.read_csv(url)

    data = data[data['Acct'] == student_id]
    column_renames= {
       'L01': 'Facial Treatments', 
       'L02': 'Body Treatments', 
       'L03' :'Adv Skin', 
       'L04': 'Skin Analysis & Consult',
       'L05' : 'Facial Wax', 
       'L06': 'Body Wax',
       'L07':'Make-Up', 
       'L08': 'Sanitation',
       'L09': 'Business Practice', 
       'L10':'Extractions', 
       'W01':'Chap 1 - Found Life Skill',
       'W02':'Chap 2 - Found Prof Image', 
       'W03' :'Chap 3 - Found Communicat',
       'W04' : 'Chap 4 - Found Healthy Pr',
       'W05' : 'Chap 5 - Found Infec Cont', 
       'W06':'Chap 6 - Found Chem & Saf', 
       'W07' : 'Chap 7- Found Electricity', 
       'W08':'Chap 8 - Found Career Pla', 
       'W09' :'Chap 9 - Foun On The Job', 
       'W10':'Chap 10 - Foun Beauty Bus', 
       'W11' : 'Mid Term Final', 
       'W12':'State Law', 
       'W13':'Esthetics Final',
       'W14':'Resume',
       'W15':'Chap 1- Fund His & Career',
        'W16': 'Chap 2- Fund A & P', 
        'W17':'Chap 3 - Fund Phys & Hst', 
        'W18':'Chap 4 - Fund Disor & Dis', 
        'W19':'Chap 5 - Fund Skin Analys', 
        'W20':'Chap 6 - Fund Skncare Pro', 
        'W21':'Chap 7 - Fund Trtment RM', 
        'W22':'Chap 8 - Fund Facial Trea', 
        'W23':'Chap 9 - Fund Facial Mass', 
        'W24':'Chap 10 - Fund Devices/Te',
        'W25':'Chap 11 - Fund Hair Remov', 
        'W26':"Chap 12 - Fund Make up Es", 
        'W27':'Chap 13 - Fund Adv Topics'
    }

    practicaltotals = [85,15,50,85,45,15,30,100,25,10]
    data = data.rename(columns= column_renames)
    test_data = data[data.columns[14:-9]]
    practical_data= data[data.columns[4:14]].transpose().reset_index()


    return data,practicaltotals, practical_data, test_data



def student_status_selected_nails(student_id):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp%20Nails.csv'
    data = pd.read_csv(url)

    data = data[data['Acct'] == student_id]
    column_renames= {
       'L01': 'Manicure', 
       'L02': 'Reconditioning Trmt', 
       'L03' :'Repair Technique', 
       'L04': 'Hand/Arm Massage',
       'L05' : 'Pedicure', 
       'L06': 'Foot/Leg Massage',
       'L07':'Sculpted Nail', 
       'L08': 'Tips',
       'L09': 'Wraps', 
       'L10':'Business Admin', 
       'L11':'Sanitation', 
       'W01':'Ch 1-3  Life Sk/Pro Im/Co',
       'W02':'Ch 4 Healthy Pro', 
       'W03' :'Ch 5  Infection Contr',
       'W04' : 'Ch 6 Chemistry/Chem Safe',
       'W05' : 'Ch 7 Electricity/Elec Saf', 
       'W06':'Ch 8,9,10 Career/Job/BeaB', 
       'W07' : 'Ch 2 Anatomy/Phys', 
       'W08':'Ch 3 Skin Str, Dis/Dis', 
       'W09' :'Ch 4 Nail Str,Dis/Dis', 
       'W10':'Ch 5 Nail Prod Chem', 
       'W11' : 'Ch 6 Manicuring', 
       'W12':'Ch 7 Pedicuring', 
       'W13':'Ch 8 Electric Filing',
       'W14':'Ch 9 Tips/Forms',
       'W15':'Ch 10 Nail Resin Systems',
        'W16': 'Ch 11 Mono Liq/Poly Powde', 
        'W17':'Ch 12 Gel Nail Enhance', 
        'W18':'Ch 13 Nail Art', 
        'W19':'Final', 
        'W20':'Mock #1', 
        'W21':'Mock #2', 
        'W22':'Mock #3', 
        'W23':'State Law', 
        'W24':'Resume',
        'W25':'Business Project'
    }

    practicaltotals = [30,12,12,30,20,20,120,120,120,10,100]
    data = data.rename(columns= column_renames)
    test_data = data[data.columns[15:-9]]
    practical_data= data[data.columns[4:15]].transpose().reset_index()

    return data, practicaltotals,practical_data, test_data


def student_status_selected_massage(student_id):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp%20Massage.csv'
    data = pd.read_csv(url)

    data = data[data['Acct'] == student_id]
    column_renames= {
       'L01': 'Sports Massage', 
       'L02': 'Trigger Point', 
       'L03' :'Reflexology', 
       'L04': 'Swedish Massage',
       'L05' : 'Deep Tissue', 
       'L06': '30 min',
       'L07':'60 min', 
       'L08': '90 min',
       'L09': '120 min', 
       'L10':'Chair Massage', 
       'L11':'Cupping Massage', 
       'L12':'Hot Stone', 
       'L13':'Foot Scrub', 
       'L14':'Dry Brushing', 
       'L15':'Facial Massage', 
       'L16':'Energy Work', 
       'L17':'Special Pops', 
       'W01':'Intro Massag',
       'W02':'Anat/Phy 1', 
       'W03' :'Path/Med Term',
       'W04' : 'TherMass/Body',
       'W05' : 'Anat/Phy 2', 
       'W06':'Sp Pop/Trmt', 
       'W07' : 'Kin/ Sp Trmt', 
       'W08':'Ener/Asian Ther', 
       'W09' :'Decomp Ther', 
       'W10':'Bus Develop', 
       'W11' : 'Clinic/Prac', 
       'W12':'Mass Ex Prep', 
    }

    practicaltotals = [3,3,3,3,3,4,20,15,6,3,3,2,2,1,2,1,4]
    data = data.rename(columns= column_renames)
    test_data = data[data.columns[21:-9]]
    practical_data= data[data.columns[4:21]].transpose().reset_index()
    print(data.columns)
    return data, practicaltotals,practical_data, test_data


def get_update_date(item):
    from github import Github
    g = Github()
    repo = g.get_repo("SpencerReno/EntourageApp")

    if item == 'hours':
        commits = repo.get_commits(path='CSV Files/EntourageApp.csv')
        if commits.totalCount:
            date = commits[0].commit.committer.date

    elif item == 'cos_status':
        commits = repo.get_commits(path='CSV Files/EntourageApp Cos.csv')
        if commits.totalCount:
            date = commits[0].commit.committer.date


    elif item == 'esti_status':
        commits = repo.get_commits(path='CSV Files/EntourageApp Esti.csv')
        if commits.totalCount:
            date = commits[0].commit.committer.date


    elif item == 'massage_status':
        commits = repo.get_commits(path='CSV Files/EntourageApp Massage.csv')
        if commits.totalCount:
            date = commits[0].commit.committer.date


    elif item == 'nails_status':
        commits = repo.get_commits(path='CSV Files/EntourageApp Nails.csv')
        if commits.totalCount:
            date = commits[0].commit.committer.date

    elif item =='ledger':
        commits = repo.get_commits(path='CSV Files/ledger.csv')
        if commits.totalCount:
            date = commits[0].commit.committer.date
            
    date = date.strftime("%m/%d/%Y")
    return date

def refresh_google():
    SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
    creds = None
    if os.path.exists("token.json"):
         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    return creds
        



def massage_last_subital():
    creds = refresh_google()
    try:
        folder_id='15-aqS6s0fyTxCI8qva9Y0p4oXeeaIeFe'
        service = build("drive", "v3", credentials=creds)

        # first call for recent year folder 
        results = (
            service.files().list(supportsAllDrives=True, includeItemsFromAllDrives=True, q=f"parents in '{folder_id}' and trashed = false", fields = "nextPageToken, files(id, name)").execute() )
        items = results.get("files", [])

        if not items:
            return 'No Files found'


    #gets most recent Year folder
        recent_year_folder_id = str(items[0]['id'])
        service = build("drive", "v3", credentials=creds)
        results = (
            service.files()
        
            .list(supportsAllDrives=True, includeItemsFromAllDrives=True, q=f"parents in '{recent_year_folder_id}' and trashed = false", fields = "nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])

        most_recent_file = items[0]['name']
        most_recent_file=most_recent_file.split('.')[0]
        datetime_object = datetime.strptime(most_recent_file,'%m/%d/%y')
        start, end = datetime_object, datetime.now()
        missing_dates = [str(d).split(' ')[0] for d in pd.date_range(start, end) if d.weekday() == 2]
        #dont include 1st date as that is the starting point from the last submition 
        missing_dates = missing_dates[1:]



    except HttpError as error:
        print(f"An error occurred: {error}")
    
    
    return missing_dates


def cos_last_subital(course):
    creds = refresh_google()
    course_type = course
    try:
        if course_type == 'am': 
            folder_id='1s80kHVRny8A4IpKQo8-9cS1-nmkP3ZkX'
        if course_type =='pm':
            folder_id='1alOony4AAbHpktMqpg1qhQOOZMmFGdhR'
        service = build("drive", "v3", credentials=creds)

        # first call for recent year folder 
        results = (
            service.files().list(supportsAllDrives=True, includeItemsFromAllDrives=True, q=f"parents in '{folder_id}' and trashed = false", fields = "nextPageToken, files(id, name)").execute() )
        items = results.get("files", [])

        if not items:
            return 'No Files found'


    #gets most recent Year folder
        recent_year_folder_id = str(items[0]['id'])
        service = build("drive", "v3", credentials=creds)
        results = (
            service.files()
        
            .list(supportsAllDrives=True, includeItemsFromAllDrives=True, q=f"parents in '{recent_year_folder_id}' and trashed = false", fields = "nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])

        most_recent_file = items[0]['name']
        most_recent_file=most_recent_file.split('.')[0]
        datetime_object = datetime.strptime(most_recent_file,'%m/%d/%y')
        start, end = datetime_object, datetime.now()
        missing_dates = [str(d).split(' ')[0] for d in pd.date_range(start, end) if d.weekday() == 2]
        #dont include 1st date as that is the starting point from the last submition 
        missing_dates = missing_dates[1:]



    except HttpError as error:
        print(f"An error occurred: {error}")
    
    
    return missing_dates

def nails_last_subital():
    return 'Test'

def esti_last_subital():
    return 'Test'


def unsubmit_page_info():
    creds = refresh_google()
    cos_am='1s80kHVRny8A4IpKQo8-9cS1-nmkP3ZkX'
    cos_pm='1alOony4AAbHpktMqpg1qhQOOZMmFGdhR'
    nails_am='1-l-Wb1sCyApJXkF1_-6Bha9xsc_L_8TC'
    nails_pm='1wgdHXkbk7vKjLypBFnKol2SH6jUG9oSl'
    massage_am='15-aqS6s0fyTxCI8qva9Y0p4oXeeaIeFe'
    massage_pm = None
    esti_fresh_am='1AVBJ9AjZyujkxWLQcpWKwNpm-2H6F_be'
    esti_fresh_pm='1eEnVN-hz39ykox1yPHdgCksZDc8XpQJW'
    esti_jr_am='1apiHkKHca809_zkGOwnS3Eb10cE8-27w'
    esti_jr_pm='1yTbLF4V7o5cpRSd7SIX9zHCcPVgrbkKb'
    esti_sr_am='1Eb5sCYy9TgFviititCzud9IvUntPEkMT'
    esti_sr_pm='1Gx9Z09iFrKMOi-EZPoqvndmKbExscYP-'

    return missing_dates(massage_am, creds, 2),missing_dates(cos_am, creds, 0),missing_dates(cos_pm, creds, 0), missing_dates(nails_pm, creds, 0), missing_dates(esti_fresh_am, creds, 3), missing_dates(esti_fresh_pm, creds, 3), missing_dates(esti_jr_am,creds, 0), missing_dates(esti_jr_pm, creds, 0), missing_dates(esti_sr_am, creds, 2), missing_dates(esti_sr_pm, creds, 2)



def missing_dates(folder_id, creds, weekdays):
    service = build("drive", "v3", credentials=creds)

    # first call for recent year folder 
    results = (
        service.files().list(supportsAllDrives=True, includeItemsFromAllDrives=True, q=f"parents in '{folder_id}' and trashed = false", fields = "nextPageToken, files(id, name)").execute() )
    items = results.get("files", [])
    for x in range(len(items)):
        if items[x]['name'] == str(datetime.now().year):
            recent_year_folder_id = str(items[x]['id'])
    if not items:
        return 'No Files found'


#gets most recent Year folder

    service = build("drive", "v3", credentials=creds)
    results = (
        service.files()
    
        .list(supportsAllDrives=True, includeItemsFromAllDrives=True, q=f"parents in '{recent_year_folder_id}' and trashed = false", fields = "nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])
    most_recent_file = items[0]['name']    
    most_recent_file=most_recent_file.split('.')[0]
    if '-' in most_recent_file:
        most_recent_file= most_recent_file.split('-')[0].strip(' ')
    datetime_object = datetime.strptime(most_recent_file,'%m/%d/%y')
    start, end = datetime_object, datetime.now()
    missing_dates = [str(d.strftime('%m/%d/%Y')).split(' ')[0] for d in pd.date_range(start, end) if (d.weekday() == weekdays) & (d != start)]
    #dont include 1st date as that is the starting point from the last submition 
    if len(missing_dates)<=0:
        return ["All Submitted"]
    else:
        return missing_dates
