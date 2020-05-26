import fitbit as bit
import gather_keys_oauth2 as Oauth2
import datetime
import pandas
import json


def init_bit_client():
    with open('json/creds.json') as src:
        data = json.load(src)
    CLIENT_ID = data['fitbit-clientID']
    CLIENT_SECRET = data['fitbit-secret']
    #use client id and secret to get access and refresh tokens that authorize access to the data
    server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
    server.browser_authorize()

    ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
    REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
    auth2_client = bit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

    print('auth success!!!!')