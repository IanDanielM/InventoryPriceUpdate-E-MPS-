
import requests
from dropbox import DropboxOAuth2FlowNoRedirect

# authorization_url = 'https://api.authorization-server.com/authorize'
# client_id = ''
# client = WebApplicationClient(client_id)

# url = client.prepare_request_uri(
#   authorization_url,
#   redirect_uri = 'https://your-web-app.com/redirect',
#   scope = ['read:user'],
#   state = 'D8VAo311AAl_49LAtM51HA'
# )

import dropbox
# class DropboxFolderCreation:
   
#     def __init__(self):
#         # # define your dropbox app key below
#         # self.app_key = 
#         # # define your dropbox app secret key below
#         # self.app_secret = 
#         # define your MS Excel file path below   
# def login_dropbox():
#     APP_KEY = ""
#     APP_SECRET = "rxaq73eji557qoe"
#     auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
#     authorize_url = auth_flow.start()
#     print ("1. Go to: " + authorize_url)
#     print ("2. Click \"Allow\" (you might have to log in first).")
#     print ("3. Copy the authorization code.")
#     auth_code = input("Enter the authorization code here: ").strip()
#     try:
#         oauth_result = auth_flow.finish(auth_code)
#     except Exception as e:
#         print('Error: %s' % (e,))
#     return oauth_result

# if __name__ == "__main__":
#     login_dropbox()

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

'''
Populate your app key in order to run this locally
'''
APP_KEY = "1wukf9abyictawm"

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, use_pkce=True, token_access_type='offline')

authorize_url = auth_flow.start()
print("1. Go to: " + authorize_url)
print("2. Click \"Allow\" (you might have to log in first).")
print("3. Copy the authorization code.")
auth_code = input("Enter the authorization code here: ").strip()

try:
    oauth_result = auth_flow.finish(auth_code)
except Exception as e:
    print('Error: %s' % (e,))
    exit(1)

with dropbox.Dropbox(oauth2_refresh_token=oauth_result.refresh_token, app_key=APP_KEY) as dbx:
    dbx.users_get_current_account()
    print("Successfully set up client!")



# app_key = 
# app_secret = 

# # build the authorization URL:
# authorization_url = "?client_id=%s&response_type=code" % app_key

# # send the user to the authorization URL:
# print("Go to the following URL and allow access:")
# print(authorization_url)

# # get the authorization code from the user:
# authorization_code = raw_input('Enter the code:\n')

# # exchange the authorization code for an access token:
# token_url = "https://api.dropboxapi.com/oauth2/token"
# params = {
#     "code": authorization_code,
#     "grant_type": "authorization_code",
#     "client_id": app_key,
#     "client_secret": app_secret
# }
# r = requests.post(token_url, data=params)
# print(r.text)


# import json

# url = "https://api.dropboxapi.com/2/auth/token/from_oauth1"

# headers = {
#     "Authorization": "1wukf9abyictawm:f0pbc7n35zkv05a",
#     "Content-Type": "application/json"
# }

# data = {
#     "oauth1_token": "<DROPBOX_USERNAME>",
#     "oauth1_token_secret": "<DROPBOX_PASSWORD>"
# }

# r = requests.post(url, headers=headers, data=json.dumps(data))


