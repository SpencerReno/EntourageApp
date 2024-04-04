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
from dateutil import parser


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
    data = pd.read_csv(url)  
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
            data['clock in'] =  '5:30 pm'
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
                            date = parser.parse(string.split('-')[y])
                            date_list.append(date)
                        send_clause = True
            else:
                if '-' not in string:
                    if len(string) <= 8:
                        print(string)
                        if int(string.split('/')[0])>=1 and int(string.split('/')[0])<13:
                            if int(string.split('/')[1])>=1 and int(string.split('/')[1])<31:
                                    date_list.append(parser.parse(string))
                                    send_clause = True

            for date in date_list:
                month = date.month
                if len(str(month)) == 1:
                    month = f'0{str(month)}'

                day = date.day
                if len(str(day)) == 1:
                    day = f'0{str(day)}'


                year_test = int(str(date.year)[-2:])


                #Check if the year entered is == to last year   
                if year_test == int(str(datetime.date.today().year)[-2:]) - 1:
                    year= year_test
                #Check if the year entered is == to next year   
                elif year_test == int(str(datetime.date.today().year)[-2:]) +1:
                    year = year_test
                #Check if the year entered is == to current year    
                elif year_test == int(str(datetime.date.today().year)[-2:]):
                    year = year_test

                else:
                    year = int(str(datetime.date.today().year)[-2:])



                intime = df['clock in'].iloc[x][:4].strip(' ')
                in_condition = df['clock in'].iloc[x][4:].strip(' ')
                outtime = df['clock out'].iloc[x][:4].strip(' ')
                out_condition = df['clock out'].iloc[x][4:].strip(' ')
                if in_condition != 'am' or in_condition != 'pm':
                    raise SyntaxError
            
                if out_condition != 'am' or out_condition != 'pm':
                    raise SyntaxError

                in_time_hour = intime.split(':')[0]
                if len(in_time_hour) < 2 and 'am' in in_condition:
                    in_time_hour =f'0{in_time_hour}'

                out_time_hour = outtime.split(':')[0]    
                if len(out_time_hour) < 2 and 'am' in out_condition:
                    out_time_hour =f'0{out_time_hour}'

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
                clocked_hours = clocked_hours.append(clock_in, ignore_index=True)
                clocked_hours=clocked_hours.append(clock_out, ignore_index=True)

        return clocked_hours, send_clause
    except ValueError:
        send_clause= ValueError
        return clocked_hours, send_clause
    except SyntaxError:
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
        'L010': 'Comb Out',
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

    data = data.rename(columns= column_renames)

    return data



def student_status_selected_esti(student_id):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp%20Esti.csv'
    data = pd.read_csv(url)

    data = data[data['Acct'] == student_id]

    return data



def student_status_selected_nails(student_id):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp%20nails.csv'
    data = pd.read_csv(url)

    data = data[data['Acct'] == student_id]

    return data


def student_status_selected_massage(student_id):
    url ='https://raw.githubusercontent.com/SpencerReno/EntourageApp/main/CSV%20Files/EntourageApp%20massage.csv'
    data = pd.read_csv(url)

    data = data[data['Acct'] == student_id]

    return data
