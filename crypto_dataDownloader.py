import numpy as np
import requests
import requests.exceptions
import os
from dotenv import load_dotenv
import pandas as pd
import cv2
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import csv_analyzer

load_dotenv()  

API_KEY=os.environ["API_KEY"]
API_URL=os.environ["API_URL"]


def flatten_data(df):
    for col in df.columns:
        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)
    return df

def getCoinList():
    url=API_URL+"/coins/markets"+"?vs_currency=usd"+"&x-cg-demo-api-key="+API_KEY
    print("Downloading Data")
    try:
        coinList=(requests.get(url)).json()
    
    except requests.RequestException as e:
        print(str(e))

    cryptoData=pd.DataFrame(coinList)
    cryptoData=cryptoData.sort_values(by="market_cap",ascending=False)
    cryptoData = cryptoData.head(len(cryptoData) - 50)
    cryptoData=cryptoData.drop(columns=["image"])

    cryptoData.replace([np.inf, -np.inf], np.nan, inplace=True) 
    #cryptoData = cryptoData.map(lambda x: 0 if isinstance(x, float) and (np.isnan(x) or np.isinf(x)) else x)
    cryptoData=flatten_data(cryptoData)
    cryptoData.fillna("", inplace=True)
    
    savetoExcel(cryptoData)

def ping():
    url=API_URL+"/ping"
    ping=requests.get(url)
    ping=ping.json()
    print(ping)

"""
def savetoCSV(cryptoData):
    print("Saving to CSV file")
    try:
        filename="cryptoData.csv"
        cryptoData.to_csv(filename,mode='w')
    except Exception as e:
        print(str(e))
    print("Data saved to"+ filename)

"""

def savetoExcel(cryptoData):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("cryptoanalyzer-450719-fe88f5c365aa.json", scope)
    client = gspread.authorize(creds)
    sheet=client.open(os.environ["SHEET_NAME"])

    try:
        worksheet = sheet.sheet1
        #sheet.clear()
        data = [cryptoData.columns.tolist()] + cryptoData.values.tolist()
        worksheet.update(data)
        print("Data saved to Excel Sheet")
        
    except gspread.exceptions as e:
        print(str(e))

    csv_analyzer.analyzer(cryptoData)
    


def updateCoinList():
    print("Updateing Coin List")
    getCoinList()
