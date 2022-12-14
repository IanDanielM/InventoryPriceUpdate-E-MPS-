import pathlib as Path
import pandas as pd
import dropbox
from dropbox.exceptions import AuthError
from schedule import every, repeat, run_pending
from forex_python.converter import CurrencyRates
import time
import requests
from connect import dropbox_connect
import os
from dropbox.files import WriteMode
#downloadd the files from drobox to be parsed
def dropbox_download_file():
    try:
        dbx = dropbox_connect()
        with open(r'files/Linnwork_Prices.csv', 'wb') as f:
            metadata, result = dbx.files_download(path="/E-MPS Work/e-mps Dev/Linnwork_Prices.csv")
            f.write(result.content)
        with open(r'files/Vendor_Price_Update.csv', 'wb') as f:
            metadata, result = dbx.files_download(path="/E-MPS Work/e-mps Dev/Vendor_Price_Update.csv")
            f.write(result.content)
            
    except Exception as e:
        print('Error downloading file from Dropbox: ' + str(e))

#parse the cvs based on new prices
def parsecvs():
    #get currency rates
    c = CurrencyRates()
    Usd=c.get_rate('GBP','USD').__round__(2)
    Cad=c.get_rate('GBP','CAD').__round__(2)
    Aud=c.get_rate('GBP','AUD').__round__(2)
    df1 = pd.read_csv(r'files/Linnwork_Prices.csv')
    df2 = pd.read_csv(r'files/Vendor_Price_Update.csv')
    #check for null columns in the mother file
    df3=df1[df1['MarketPlacePriceUpdate'].notnull()]
    #merge via inner join based  on sku
    checkpricedf=df3[["SKU"]].merge(df2[["SKU","MarketPlacePriceUpdate"]], on ="SKU", how = "inner")
    #remove duplicates if any
    checkpricedf.drop_duplicates(inplace = True)
    #create columns based on currency update
    currencyfiledf = checkpricedf.assign(eBay_UK=lambda x: x.MarketPlacePriceUpdate,
    eBay_US=lambda x: x.MarketPlacePriceUpdate * Usd,
    eBay_CA=lambda x: x.MarketPlacePriceUpdate * Cad,
    eBay_AU=lambda x: x.MarketPlacePriceUpdate * Aud,
    OnBuy=lambda x: x.MarketPlacePriceUpdate)
    # output file
    currencyfiledf.to_csv(r'files/finalprice.csv',index = False)

#upload output file to Dropbox
def dropbox_upload_file():
    dbx = dropbox_connect()
    with open(r'files/finalprice.csv', 'rb') as f:
        dbx.files_upload(f.read(), path='/E-MPS Work/e-mps Dev/finalprice.csv',mode=dropbox.files.WriteMode.overwrite)

#start script run schedule
@repeat(every(1).hour)
def main():
    dropbox_download_file()
    parsecvs()
    dropbox_upload_file()   
    print("Updated")
while True:
    run_pending()
    time.sleep(1)




