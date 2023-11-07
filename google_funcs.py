import pandas as pd
import requests
from io import StringIO
from tkinter.filedialog import asksaveasfile
import re
from datetime import date
import datetime
import calendar

def adding(text):
    total = 0
    for line in text:
        res = re.findall(r'\d+', line)
        for x in res[:-1]:
            final =  ''.join(res)
            final = f'{final[:-2]}.{final[-2:]}'
        total = total + float(final)

    return total

def get_unpaid_students():
    url ='https://drive.google.com/file/d/1buS_BepyluxxeN1XS87vH6PC-RmBybmI/view?usp=sharing'
    file_id = url.split('/')[-2]
    dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
    url = requests.get(dwn_url).text
    csv_raw = StringIO(url)
    data = pd.read_csv(csv_raw)

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
    if course == 'Cos':
        url = 'https://drive.google.com/file/d/15ZJdQJdJzQnPLVf6cKBXs8UQgpUm9WXj/view?usp=sharing'
    if course == 'Esti':
        url = 'https://drive.google.com/file/d/1XUI-2h8oavIXlkY5SgLHlj0MCxw-IuZw/view?usp=sharing'
    if course == 'Nails':
        url = 'https://drive.google.com/file/d/1yIsDhgD1e2msO7nlIolVFFLzM8bxLbhz/view?usp=sharing'
    if course == 'Massage':
        url = 'https://drive.google.com/file/d/1JjoJggNgSMR3aMHG7YCogzHNMDQcJOfE/view?usp=sharing'
        
    file_id = url.split('/')[-2]
    dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
    url = requests.get(dwn_url).text
    csv_raw = StringIO(url)
    data = pd.read_csv(csv_raw)
    return data 



def esti_data_creation(course):  
    orig_url='https://drive.google.com/file/d/1T24pGSkjlXvIAUKXG3WOMK3CBM2o1jKw/view?usp=sharing'

    file_id = orig_url.split('/')[-2]
    dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
    url = requests.get(dwn_url).text
    csv_raw = StringIO(url)
    esti_data = pd.read_csv(csv_raw)
    esti_data['Name']= esti_data['Name'].str.split(',').str[1]
    esti_data['Name'] = esti_data['Name'].str.split(' ').str[1]

    try:
        esti_data['Tot hrs']=esti_data['Tot hrs'].str.replace(',', '')
        esti_data['Tot hrs'] = esti_data['Tot hrs'].astype(float)


    except:
        print('No Errors')
    

    esti_data['Tot hrs'] = esti_data['Tot hrs'] + esti_data['Tran hrs']


    esti_data.drop(columns=['Attend stat', 'Program', 'Tran hrs','Tran hrs/other school'],inplace=True)

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
            data['hours'] =  '9:00 - 2:00'
        if data['Tot hrs'].iloc[0] > 290 and data['Tot hrs'].iloc[0] < 690:
            data['Hours'] = '9:00 - 4:00'

        if data['Tot hrs'].iloc[0] >=690:
            data['Hours'] = '9:00 - 4:00'

        
        data['Date'] = ' '
        data['Aissigned Work'] = ' '
        data.reset_index(inplace=True)
        data.drop(columns=['Tot hrs', 'index', 'Groups'], inplace=True)




    def add_cols_pm(data):
        if data['Tot hrs'].iloc[0] < 290:
            data['hours'] =  '4:30 - 9:30'
        if data['Tot hrs'].iloc[0] > 290 and data['Tot hrs'].iloc[0] < 690:
            data['Hours'] = '4:30 - 9:30'
        
        if data['Tot hrs'].iloc[0] >= 690:
            data['Hours'] = '4:30 - 9:30'
            

        
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

    if course == 'fresh_am':
        download_fresh_am(fresh_am)
    if course == 'fresh_pm':
        download_fresh_pm(fresh_pm)
    if course == 'jr_am':
        download_jr_am(jr_am)
    if course == 'jr_pm':
        download_jr_pm(jr_pm)
    if course == 'sr_am':
        download_sr_am(sr_am)
    if course == 'sr_pm':
        download_sr_pm(sr_pm)
            

def download_fresh_am(data):
    data.reset_index(inplace=True)
    data.drop(columns='index', inplace=True)
    data = data.to_csv(index=False,line_terminator='\n')

    f = asksaveasfile(mode='w', initialfile = 'Esti_Fresh_AM.csv',
        defaultextension=".csv",filetypes=[("Microsoft Excel Comma Separated Values File","*.csv")])
    f.write(data)


def download_fresh_pm(data):
    data.reset_index(inplace=True)
    data.drop(columns='index', inplace=True)
    data = data.to_csv(index=False,line_terminator='\n')

    f = asksaveasfile(mode='w', initialfile = 'Esti_Fresh_PM.csv',
        defaultextension=".csv",filetypes=[("Microsoft Excel Comma Separated Values File","*.csv")])
    f.write(data)

def download_jr_am(data):
    data.reset_index(inplace=True)
    data.drop(columns='index', inplace=True)
    data = data.to_csv(index=False,line_terminator='\n')

    f = asksaveasfile(mode='w', initialfile = 'Esti_JR_AM.csv',
        defaultextension=".csv",filetypes=[("Microsoft Excel Comma Separated Values File","*.csv")])
    f.write(data)

def download_jr_pm(data):
    data.reset_index(inplace=True)
    data.drop(columns='index', inplace=True)
    data = data.to_csv(index=False,line_terminator='\n')

    f = asksaveasfile(mode='w', initialfile = 'Esti_JR_PM.csv',
        defaultextension=".csv",filetypes=[("Microsoft Excel Comma Separated Values File","*.csv")])
    f.write(data)

def download_sr_am(data):
    data.reset_index(inplace=True)
    data.drop(columns='index', inplace=True)
    data = data.to_csv(index=False,line_terminator='\n')

    f = asksaveasfile(mode='w', initialfile = 'Esti_SR_AM.csv',
        defaultextension=".csv",filetypes=[("Microsoft Excel Comma Separated Values File","*.csv")])
    f.write(data)

def download_sr_pm(data):
    data.reset_index(inplace=True)
    data.drop(columns='index', inplace=True)
    data = data.to_csv(index=False,line_terminator='\n')

    f = asksaveasfile(mode='w', initialfile = 'Esti_SR_PM.csv',
        defaultextension=".csv",filetypes=[("Microsoft Excel Comma Separated Values File","*.csv")])
    f.write(data)



    








def cos_data_creation(course):
    orig_url='https://drive.google.com/file/d/1vm5CfMQOuGucKm4Zn0YA_XXPktmUaop4/view?usp=sharing'

    file_id = orig_url.split('/')[-2]
    dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
    url = requests.get(dwn_url).text
    csv_raw = StringIO(url)
    cos_data = pd.read_csv(csv_raw)

    cos_data['Name']=cos_data['Name'].str.split(',').str[1]
    cos_data['Name'] = cos_data['Name'].str.split(' ').str[1]
    try:
        cos_data['Tot hrs']=cos_data['Tot hrs'].str.replace(',', '')
        cos_data['Tot hrs'] = cos_data['Tot hrs'].astype(float)


    except:
        print('No Errors')

    cos_data.drop(columns=['Attend stat','Program','Course Version', 'Tot hrs'],inplace=True)
    cos_data.sort_values(by='Name', inplace=True)

    cos_full = cos_data[cos_data['Groups'] == 'Cosmetology Full Time']
    cos_full.drop(columns=['Groups'], inplace=True)
    cos_full['Hours'] = "9:00 - 4:00"
    cos_full['Date'] = ' '
    cos_full['Aissigned Work'] = ' '


    
    cos_part = cos_data[cos_data['Groups'] != 'Cosmetology Full Time']
    cos_part.drop(columns=['Groups'], inplace=True)
    cos_part['Hours'] = "5:30 - 9:30"
    cos_part['Date'] = ' ' 
    cos_part['Aissigned Work'] = ' '


    cos_full.drop(columns=['Tran hrs', 'Tran hrs/other school'], inplace=True)
    cos_part.drop(columns=['Tran hrs', 'Tran hrs/other school'], inplace=True)
    cos_full.reset_index(inplace=True)
    cos_full.drop(columns='index', inplace=True)
    cos_full = cos_full.to_csv(index=False,line_terminator='\n')

    cos_part.reset_index(inplace=True)
    cos_part.drop(columns='index', inplace=True)
    cos_part = cos_part.to_csv(index=False,line_terminator='\n')

    if course == 'AM':
        f = asksaveasfile(mode='w', initialfile = 'COS_AM.csv',
        defaultextension=".csv",filetypes=[("Microsoft Excel Comma Separated Values File","*.csv")])
        f.write(cos_full)
    else:
        f = asksaveasfile(mode='w', initialfile = 'COS_PM.csv',
        defaultextension=".csv",filetypes=[("Microsoft Excel Comma Separated Values File","*.csv")])
        f.write(cos_part)



def nails_data_creation(course): 
    orig_url='https://drive.google.com/file/d/1HPjhVRWNGUsuXoYAJ0eVGavinpcHZOAa/view?usp=sharing'
    file_id = orig_url.split('/')[-2]
    dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
    url = requests.get(dwn_url).text
    csv_raw = StringIO(url)
    nails_data = pd.read_csv(csv_raw) 
    nails_data['Name']=nails_data['Name'].str.split(',').str[1]
    nails_data['Name'] = nails_data['Name'].str.split(' ').str[1]
    nails_data.drop(columns=['Attend stat','Program', 'Tot hrs'],inplace=True)
    nails_am = nails_data[nails_data['Groups'] == 'Nails Full Time']
    nails_pm = nails_data[nails_data['Groups'] == 'Nails Part Time']


    nails_am.sort_values('Last name', inplace=True)
    nails_pm.sort_values('Last name', inplace=True)

    def pm_data(data):
        data.drop(columns=['Groups'], inplace=True)
        data['Hours'] = '5:30 - 9:30'
        data['Date'] = ' '
        data['Aissigned Work'] = ' '

    def am_data(data):
        data.drop(columns=['Groups'], inplace=True)
        data['Hours'] = '9:00 - 4:00'
        data['Date'] = ' '
        data['Aissigned Work'] = ' '

    pm_data(nails_pm)
    am_data(nails_am)
    nails_am.reset_index(inplace=True)
    nails_am.drop(columns='index', inplace=True)
    nails_am = nails_am.to_csv(index=False,line_terminator='\n')

    nails_pm.reset_index(inplace=True)
    nails_pm.drop(columns='index', inplace=True)
    nails_pm = nails_pm.to_csv(index=False,line_terminator='\n')

    if course == 'AM':
        f = asksaveasfile(mode='w', initialfile = 'Nails_AM.csv',
        defaultextension=".csv",filetypes=[("Microsoft Excel Comma Separated Values File","*.csv")])
        f.write(nails_am)
    else:
        f = asksaveasfile(mode='w', initialfile = 'Nails_PM.csv',
        defaultextension=".csv",filetypes=[("Microsoft Excel Comma Separated Values File","*.csv")])
        f.write(nails_pm)

def massage_data_creation():
    orig_url='https://drive.google.com/file/d/1Mk_nIhyHHWIbfMSK92WU7mV3jpocfVZ-/view?usp=sharing'
    file_id = orig_url.split('/')[-2]
    dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
    url = requests.get(dwn_url).text
    csv_raw = StringIO(url)
    massage_data = pd.read_csv(csv_raw) 
    massage_data.drop(columns=['Tot hrs', 'LDA hrs', 'Remain hrs','Atnd %'], inplace=True)
    massage_data['Last'] = massage_data['Name'].str.split(',').str[0]
    massage_data['Name'] = massage_data['Name'].str.split(',').str[1]
    massage_data['Name'] = massage_data['Name'].str.split(' ').str[1]
    massage_data['Hours'] = '9:00 - 4:00'
    massage_data['Date'] = ' '
    massage_data['Assigned Work'] = ' '
    massage_data = massage_data.to_csv(index=False,line_terminator='\n')
    f = asksaveasfile(mode='w', initialfile = 'Massage_Hours.csv',
    defaultextension=".csv",filetypes=[("Microsoft Excel Comma Separated Values File","*.csv")])
    f.write(massage_data)





def held_back_students():
    url = 'https://api.apispreadsheets.com/data/aAZcLsK62BpKyvIJ/'
    res = requests.get(url).json()

    df = pd.DataFrame.from_dict(res['data'])

    return df

    




