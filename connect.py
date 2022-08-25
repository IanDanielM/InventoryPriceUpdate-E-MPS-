import dropbox
import requests
from dropbox.exceptions import AuthError
def dropbox_connect():
    try:
        endpoint="https://api.dropboxapi.com/oauth2/token?grant_type=refresh_token&client_id=1wukf9abyictawm&client_secret=f0pbc7n35zkv05a&refresh_token=wEHJ421M1J4AAAAAAAAAAaX5BhwqPsj5L5pnL6XW1QHkvPvCPOjYK9uM-6ctAjGc"
# Replace DEMO_KEY below with your own key if you generated one.
        api_key = "1wukf9abyictawm"
        query_params = {"grant_type":"refresh_token",
        "client_id":"1wukf9abyictawm",
        "client_secret":"f0pbc7n35zkv05a",
        "refresh_token":"wEHJ421M1J4AAAAAAAAAAaX5BhwqPsj5L5pnL6XW1QHkvPvCPOjYK9uM-6ctAjGc"
        }
        response = requests.post(endpoint,params=query_params)
        r=response.json()
        dbx = dropbox.Dropbox(r['access_token'])
        print("success")
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx