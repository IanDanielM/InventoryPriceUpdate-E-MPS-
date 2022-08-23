import pathlib
import pandas as pd
import dropbox
from dropbox.exceptions import AuthError
from schedule import every, repeat, run_pending
import time
def dropbox_connect():
    try:
        dbx = dropbox.Dropbox('sl.BN4FSME8XYGILWyRLVSCCYu6BzqB8qs-GvEZsfS0DdAB5lUlL1dxu4Ug7UGTPOIndoqYUappCKEe-gFgwBylNjCEoD9_NOwVHM7V8g5jjSub-Mr8ne8Pg-VSgpbd3Z1DYBL9qxA')
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx
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
def dropbox_upload_file():
    dbx = dropbox_connect()
    with open(r'files\inventoryupdate.csv', 'rb') as f:
        dbx.files_upload(f.read(), '/E-MPS Work/e-mps Dev/inventoryupdatez.csv')
def parsecvs():
    df1 = pd.read_csv(r'files\Linnwork_Prices.csv')
    df2 = pd.read_csv(r'files\Vendor_Price_Update.csv')
    result1=df2[~df2.apply(tuple,1).isin(df1.apply(tuple,1))]
    resu2 = result1.merge(df1[['SKU']],how='inner',on='SKU')
    resu2.to_csv(r'files\inventoryupdate.csv', index = False)
@repeat(every(10).seconds)   
def main():
    dropbox_download_file()
    parsecvs()
    dropbox_upload_file()
while True:
    run_pending()
    time.sleep(1)

    

# if __name__ == "__main__":
    
#     schedule()
    