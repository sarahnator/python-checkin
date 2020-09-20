# note -- run in virtualenv w/ command: python scripts/export.py
import numpy as np
import pandas as pd
import myfitnesspal as pal
from scripts.spreadsheet import *
import fitbit as bit
import gather_keys_oauth2 as Oauth2
import datetime
import json
from scripts.dateUtils import *
from fitbit import exceptions


def mfp_data_from_date(date):
    """
    Non-verbose function to retrieve all myfitnesspal data from date to now.
    :param date:  datetime object of desired date, ex: datetime.date(2015, 5, 11)
    :return mfp_data: nested list [[weights], [dates], [calories], [carbohydrates], [fats], [protein], [fiber]]

    """
    # init connection to mfp api
    with open('json/creds.json') as src:
        data = json.load(src)
    client = pal.Client(data['email'])
    weights = client.get_measurements('Weight', date)
    weights = list(weights.items())  # convert ordered dictionary to list

    data_list = []  # container for data row

    for (a, b) in weights:
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
    # fmt:   [[122.5, 123.3, 123.2, 123.4], --> weight    ['05-17', '05-18', '05-19', '05-20'],  --> date   [2321, 2347, 2324, 2316], --> cals
    #           [298, 301, 298, 295], --> carbs   [63, 65, 63, 63], --> fat   [154, 153, 154, 152], --> pro   [62, 62, 63, 67]] --> fiber

    return mfp_data


def fitbit_data_from_date(date):
    """
    Non verbose version.
    Initiates fitbit client and server, returns  fitbit activity data relative to last calendar Sunday.
    If session token has expired, refreshes token and writes updated credentials to json file "json/creds.json".
    Outputs progress bars to terminal.
    :param date:  datetime object of desired date, ex: datetime.date(2015, 5, 11)
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
    sunday = str(date.strftime("%Y-%m-%d"))

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

    # print(fitbit_data)

    return fitbit_data


def export_subset(mfp_data, fitbit_data):
    """
    Exports weights as y array, calories and steps as multidimensional X matrix
    Saves y to y_data.csv, X to X_data.csv in exportedData directory.
    Inconveniently uses numpy arrays instead of panda dataframes because I was lazy.
    :param mfp_data: nested array of myfitnesspal data
    :param fitbit_data: nested array of fitbit data
    """
    # create numpy array for weights as ground truth
    y = mfp_data[0]
    y_data = np.array(y)

    # create X inputs
    c = np.array(mfp_data[2])
    s = np.array(fitbit_data[0])
    # transpose 1D matrices
    c = np.reshape(c, (len(mfp_data[2]), 1))
    s = np.reshape(s, (len(fitbit_data[0]), 1))
    # horizontally stack 1D matrices
    X_data = np.hstack((c, s))

    # print(y_data)
    print(X_data)  # for debug - if data is 0 anywhere, requery, error on fitbit/mfp

    # TODO: save to file function with parameter for appending or overwriting file
    fX = open("./exportedData/X_data.csv", "w")
    fy = open("./exportedData/y_data.csv", "w")
    np.savetxt(fX, X_data, fmt='%6d', delimiter=',')
    np.savetxt(fy, y_data, fmt='%3.1f', delimiter=',')


def export_all(mfp_data, fitbit_data):
    """
    Combines myfitnesspal and fitbit data into one dataframe, which is then written to a csv file
    :param mfp_data: nested array of myfitnesspal data
    :param fitbit_data: nested array of fitbit data
    """
    mfp_df = pd.DataFrame(mfp_data).transpose()
    fitbit_df = pd.DataFrame(fitbit_data).transpose()
    all = pd.concat([mfp_df, fitbit_df], axis=1)
    print(all)
    fAll = open("./exportedData/all.csv", "w")
    all.to_csv(fAll, index=False, index_label=False)


if __name__ == "__main__":
    d1 = datetime.date(2020, 1, 28)  # since working with coach
    d2 = datetime.date(2020, 5, 25)  # date started fitbit tracking

    mfp_data = mfp_data_from_date(d2)
    fitbit_data = fitbit_data_from_date(d2)
    export_all(mfp_data, fitbit_data)
