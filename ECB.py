# ----- IMPORTS ----- #
import requests
import io
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector as sql
from bs4 import BeautifulSoup
import datetime

# Main function that executes all the code
def main(request_url):
    response = requests.get(request_url, headers={'Accept': 'text/csv'})
    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text))
        ts = df.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)
        ts['TIME_PERIOD'] = pd.to_datetime(ts['TIME_PERIOD'])
        show_plot(ts)
        #df_to_mysql(ts)
            
        url = "https://www.ecb.europa.eu/press/calendars/mgcgc/html/index.en.html"
        meetings = get_data_frame_ECB_meeting(url)
        nextMeeting = get_next_meeting_rates(meetings)
        print(f"The next meeting of the ECB where the rates will be discussed: {nextMeeting}.")
                    
    else:
        print(f"Error: {response.status_code}")

# Function that recives a dataframe with two columns Time and Value and with that values makes a plot
def show_plot(ts):
    ts = ts.set_index('TIME_PERIOD')
    ts.tail(4).plot()
    plt.title('ECB - FIXED RATE')
    plt.xlabel('TIME PERIOD')
    plt.ylabel('OBSERVATION VALUES')
    plt.show()

# Function that enables the database connection 
def connect_db():
    db = sql.connect(
    host="localhost",
    user="root",
    password="1234",
    database = "ECB"
    )
    return db

# Function that selects one row in the dataframe and next intert it in the database, if that row exits the value is updated with the new
def insert_one(db,cursor,ts,i):
    date = ts.iloc[i]['TIME_PERIOD']
    formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
    value = float(ts.iloc[i]['OBS_VALUE'])
    parameters = (formatted_date,value,value)
    query = "INSERT INTO ecb_bank_rate VALUES (%s, %s) ON DUPLICATE KEY UPDATE obs_value = %s"
    cursor.execute(query,parameters)
    db.commit()


def df_to_mysql(ts):
    db = connect_db() 
    cursor = db.cursor()
    length = len(ts.index) #Lenght of the dataframe
    i=0
    while i != length:
        insert_one(db,cursor,ts,i)
        i+=1

# Function that does some web scrapping in the ECB press calendars and returns a dataframe with all the meeting of the year
def get_data_frame_ECB_meeting(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    dates = soup.find_all('dt')
    descriptions = soup.find_all('dd')

    dates_list = list()
    descrip_list = list()

    for i in dates:
        date = i.text.strip()
        date = datetime.datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
        dates_list.append(date)

    for i in descriptions:
        descrip = i.text.strip()
        descrip_list.append(descrip)

    return pd.DataFrame({'Date': dates_list,'Description': descrip_list})

# Function that search in the dataframe when the next rates are disscused
def get_next_meeting_rates(meetings):
    i=0
    loop = True
    next_monetary_meeting = "Governing Council of the ECB: monetary policy meeting"
    while loop==True:
        description = meetings.iloc[i]["Description"]
        if description[0:53] == next_monetary_meeting:
            loop = False
        else:
            i += 1
    return meetings.iloc[i]["Date"]




if __name__=="__main__":
    entrypoint = 'https://sdw-wsrest.ecb.europa.eu/service/' 
    resource = 'data'
    flowRef ='FM'  
    key = 'B.U2.EUR.4F.KR.MRR_FR.LEV' 
    request_url = entrypoint + resource + '/'+ flowRef + '/' + key
    main(request_url)
