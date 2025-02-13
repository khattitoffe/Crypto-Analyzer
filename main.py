import os 
import crypto_dataDownloader
import threading
import time 

def clearConsole():
    os.system('cls')

def update():
    crypto_dataDownloader.updateCoinList()


def start():
    crypto_dataDownloader.getCoinList()
    print("CSV will update after 1 minute")
    thread=threading.Thread(target=update)
    
    while(True):
        time.sleep(60)
        clearConsole() 
        thread.start()
        thread.join()
        print("CSV will update after 5min") 
        
        

def main():
    print("Welcome to Crypto Analyzer")
    start()

if __name__ =="__main__":
    main()