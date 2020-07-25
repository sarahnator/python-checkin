import click
import myfitnesspal as pal
from scripts.spreadsheet import *
import fitbit as bit
import gather_keys_oauth2 as Oauth2
import datetime
import click
import json
from scripts.dateUtils import *
from fitbit import exceptions

def query_mfp():
    """
    Initiates mfp client and returns all MyFitnessPal macronutient and weight data relative to last calendar Sunday.
    Outputs progress bars to terminal.
    :return mfp_data: nested list [[weights], [dates], [calories], [carbohydrates], [fats], [protein], [fiber]]
    """

    print("Querying MyFitnessPal...")

    # init connection to mfp api
    with open('json/creds.json') as src:
        data = json.load(src)
    client = pal.Client(data['email'])

    with click.progressbar(length=4, label='Fetching weight trends') as bar:
        # query weights
        last_sunday = get_sunday()
        bar.update(1)
        y, m, d = last_sunday.year, last_sunday.month, last_sunday.day
        day = datetime.date(y, m, d)
        bar.update(2)
        weights = client.get_measurements('Weight', day)
        bar.update(3)
        weights = list(weights.items())  # convert ordered dictionary to list
        bar.update(4)

    data_list = []  # container for data row

    with click.progressbar(weights, label='Fetching nutrition data', length=len(weights)) as bar:
        for (a, b) in bar:
            # query nutrition data
            date = a
            y, m, d = date.year, date.month, date.day

            # get totals
            day = client.get_date(y, m, d)
            total = day.totals

            # int day totals
            cal, pro, car, fat, fiber = 0, 0, 0, 0, 0

            # check if data exists
            if total:
                total.pop("sodium")  # I am sodium queen DGAF - remove stat from dict
                desired_order = ["calories", "protein", "carbohydrates", "fat", "fiber"]
                total = {t: total[t] for t in desired_order}  # reorder list: {cal, pro, carb, fat, fiber}
            else:
                total = {"cal": cal, "pro": pro, "car": car, "fat": fat, "fiber": fiber}

            weight = float(b)

            # prints most recent --> least recent
            data_row = {"weight": weight, "date": date}
            data_row.update(total)  # append totals
            data_list.insert(0, data_row)  # prepend to front of list of all data

    # data list format:
    # [{'weight': 122.9, 'date': datetime.date(2020, 5, 24), 'calories': 2316, 'protein': 154, 'carbohydrates': 294,
    #   'fat': 65, 'fiber': 62},
    #  {'weight': 123.0, 'date': datetime.date(2020, 5, 28), 'calories': 2272, 'protein': 153, 'carbohydrates': 291,
    #   'fat': 63, 'fiber': 67}]

    mfp_data = [list(col) for col in zip(*[d.values() for d in data_list])]
    # reformat:   [[122.5, 123.3, 123.2, 123.4], --> weight    ['05-17', '05-18', '05-19', '05-20'],  --> date   [2321, 2347, 2324, 2316], --> cals
    #           [298, 301, 298, 295], --> carbs   [63, 65, 63, 63], --> fat   [154, 153, 154, 152], --> pro   [62, 62, 63, 67]] --> fiber

    return mfp_data


def query_fitbit():
    """
    Initiates fitbit client and server, returns  fitbit activity data relative to last calendar Sunday.
    If session token has expired, refreshes token and writes updated credentials to json file "json/creds.json".
    Outputs progress bars to terminal.
    :return fitbit_data: nested list [[steps], [distances]]
    """
    # TODO: put (re)authentication into separate function

    # get credentials from json file
    with open('json/creds.json') as src:
        data = json.load(src)
    CLIENT_ID = data['fitbit-clientID']
    CLIENT_SECRET = data['fitbit-secret']
    ACCESS_TOKEN = data['fitbit-token']
    REFRESH_TOKEN = data['fitbit-refresh-token']

    # create server and  client
    server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
    auth2_client = bit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
                              refresh_token=REFRESH_TOKEN)

    # get end and base date for api call
    today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    sunday = str(get_sunday().strftime("%Y-%m-%d"))

    # catch 401 error / refresh the token if token has expired (pops up browser window)
    try:
        auth2_client.time_series(resource="activities/steps", base_date=sunday, end_date=today)
    except bit.exceptions.HTTPUnauthorized:
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

    # reformat
    # steps: ['11519', '3428']  dist: ['4.93872658484712', '1.46974170786144']
    steps, dist, fitbit_data = [], [], []
    for i in range(0, len(steps_log)):
        steps_log[i].pop('dateTime')
        dist_log[i].pop('dateTime')
        steps.append(int(steps_log[i]['value']))
        # truncate to 3 decimal places
        d = float("%.3F" % float(dist_log[i]['value']))
        dist.append(d)

    # reformat
    #    --- steps ---                 ---  dist ---
    # [['11519', '3428'], ['4.93872658484712', '1.46974170786144']]
    fitbit_data.append(steps)
    fitbit_data.append(dist)

    return fitbit_data
