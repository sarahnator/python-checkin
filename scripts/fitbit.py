import fitbit as bit
import gather_keys_oauth2 as Oauth2
import datetime
import pandas
import json
from scripts.dateUtils import *


# def init_bit_client():
#get credentials from json file
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

today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
sunday = str(get_sunday())


#steps and distance query
def query_fitbit():
    print(today)

    time = auth2_client.time_series(resource="activities/steps", period='max')
    print(time)
    # stepsActivites = auth2_client.time_series('activities/steps', base_date=sunday, end_date=today)
    # trackerSteps = auth2_client.time_series('activities/tracker/steps', userID='-', base_date=sunday, end_date=today)
    # print("activity steps: ", stepsActivites, " tracker steps: ", trackerSteps)

    # resource URL
    # GET / 1 / user / [user - id] / [resource - path] / date / [base - date] / [end - date].json
    #resource path opts:
        # activities / tracker / steps
        #activities/tracker/distance
        #example request:
    # GET https: // api.fitbit.com / 1 / user / - / activities / steps / date / today / 1m.json
    """https://dev.fitbit.com/build/reference/web-api/activity/"""


