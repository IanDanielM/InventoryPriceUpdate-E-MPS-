import pathlib
import pandas as pd
import dropbox
from dropbox.exceptions import AuthError
from schedule import every, repeat, run_pending
import time
def dropbox_connect():
    try:
        dbx = dropbox.Dropbox('sl.BN-UwiEysxZyy_sSGYCu117ISTQIUpELCW1VjtjNWUmOYrS64tIiP2DfFpC71_3iwb1U4-Q9L7GrMEAs7K0sAf-xr2FafCOa2sShC4xFMv8Rt33e0FfJr-_M-h6cOoidQjJCpkE')
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx

#downloadd the files from drobox to be parsed
def dropbox_download_file():
    try:
        dbx = dropbox_connect()
        with open(r'files\Linnwork_Prices.csv', 'wb') as f:
            metadata, result = dbx.files_download(path="/E-MPS Work/e-mps Dev/Linnwork_Prices.csv")
            f.write(result.content)
        with open(r'files\Vendor_Price_Update.csv', 'wb') as f:
            metadata, result = dbx.files_download(path="/E-MPS Work/e-mps Dev/Vendor_Price_Update.csv")
            f.write(result.content)
    except Exception as e:
        print('Error downloading file from Dropbox: ' + str(e))

#parse the cvs based on new prices
def parsecvs():
#read the csvs
    df1 = pd.read_csv(r'files\Linnwork_Prices.csv')
    df2 = pd.read_csv(r'files\Vendor_Price_Update.csv')
#check for null columns in the mother file
    df3=df1[df1['Ebay UK'].notnull()]
#merge via inner join based  on sku
    checkprice=df3[["SKU"]].merge(df2[["SKU","Ebay UK"]], on ="SKU", how = "inner")
    checkprice.drop_duplicates(inplace = True)
#output file
    checkprice.to_csv(r'files\finalprices.csv',index = False)

def dropbox_upload_file():
    dbx = dropbox_connect()
    with open(r'files\inventoryupdate.csv', 'rb') as f:
        dbx.files_upload(f.read(), '/E-MPS Work/e-mps Dev/main.csv')


#start script run schedule
@repeat(every(10).seconds)   
def main():
    # dropbox_download_file()
    parsecvs()
    # dropbox_upload_file()
while True:
    run_pending()
    time.sleep(1)

    

# if __name__ == "__main__":
    
#     schedule()
    