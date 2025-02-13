import pandas as pd 

def analyzer(cryptoData):
    
    analyzeByPrice(cryptoData)
    priceChange(cryptoData)


def analyzeByPrice(cryptoData):
    
    print("Top Five Stocks By Current Price : \n")
    cryptoData=cryptoData.sort_values(by="current_price",ascending=False)
    for i in range(0,5):
        print(cryptoData.loc[i,'name']+ " "+ cryptoData.loc[i,'symbol'])

def priceChange(cryptoData):
    print("\n Crypto with Highest and Lowest 24 hour change : \n")
    cryptoData=cryptoData.sort_values(by="price_change_percentage_24h",ascending=False)
    
    print(cryptoData['name'].iloc[0]+" "+cryptoData.loc[0,"symbol"]+" "+str(cryptoData['price_change_percentage_24h'].iloc[0]))
    print("\n"+cryptoData['name'].iloc[49]+" "+cryptoData.loc[0,"symbol"]+" "+str(cryptoData['price_change_percentage_24h'].iloc[49])+"\n")
    