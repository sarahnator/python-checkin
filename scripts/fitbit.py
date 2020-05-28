import fitbit as bit
import gather_keys_oauth2 as Oauth2
import datetime
import click
import json
from scripts.dateUtils import *
from fitbit import exceptions


def fitbit_query():

    # get credentials from json file
    with open('json/creds.json') as src:
        data = json.load(src)
    CLIENT_ID = data['fitbit-clientID']
    CLIENT_SECRET = data['fitbit-secret']
    ACCESS_TOKEN = data['fitbit-token']
    REFRESH_TOKEN = data['fitbit-refresh-token']
    server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
    auth2_client = bit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
                              refresh_token=REFRESH_TOKEN)

    # get end and base date for api call
    today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    sunday = str(get_sunday().strftime("%Y-%m-%d"))

    # catch 401 errors and refresh the token
    # if token has expired,
    try:
        auth2_client.time_series(resource="activities/steps", base_date=sunday, end_date=today)
    except bit.exceptions.HTTPUnauthorized:
        #refresh_token()
        server.browser_authorize()
        ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
        REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

        # rewrite new credentials into json file
        with open("json/creds.json", "r") as jsonFile:
            creds = json.load(jsonFile)
        tmp1 = creds['fitbit-token']
        creds['fitbit-token'] = ACCESS_TOKEN
        tmp2 = creds['fitbit-refresh-token']
        creds['fitbit-refresh-token'] = REFRESH_TOKEN
        with open("json/creds.json", "w") as jsonFile:
            json.dump(creds, jsonFile)
        auth2_client = bit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
                                  refresh_token=REFRESH_TOKEN)


    # steps and distance query
    print("Querying fitbit...")
    # format: {'activities-steps': [{'dateTime': '2020-05-25', 'value': '11519'}, {'dateTime': '2020-05-26', 'value': '3428'}]}
    # {'activities-distance': [{'dateTime': '2020-05-25', 'value': '4.93872658484712'}, {'dateTime': '2020-05-26', 'value': '1.46974170786144'}]}
    steps_log = auth2_client.time_series(resource="activities/steps", base_date=sunday, end_date=today)
    dist_log = auth2_client.time_series(resource="activities/distance", base_date=sunday, end_date=today)

    # convert to dict-array
    # f [{'dateTime': '2020-05-25', 'value': '4.93872658484712'}, {'dateTime': '2020-05-26', 'value': '1.46974170786144'}]
    steps_log = steps_log['activities-steps']
    dist_log = dist_log['activities-distance']

    # get in format
    # steps: ['11519', '3428']
    # dist: ['4.93872658484712', '1.46974170786144']
    steps, dist, fitbit_data = [], [], []
    for i in range(0, len(steps_log)):
        steps_log[i].pop('dateTime')
        dist_log[i].pop('dateTime')
        steps.append(int(steps_log[i]['value']))
        dist.append(float(dist_log[i]['value']))


    # combine into format
    #       steps                           dist
    # [['11519', '3428'], ['4.93872658484712', '1.46974170786144']]
    fitbit_data.append(steps)
    fitbit_data.append(dist)

    return fitbit_data
