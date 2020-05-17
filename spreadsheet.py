#!/usr/bin/python3


import gspread
from oauth2client.service_account import ServiceAccountCredentials

import myfitnesspal
# # some_file.py
# import sys
# # insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, '/mfp/myfitnesspal')




# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('../client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Copy of Sarah Etter Macro & Cardio").sheet1

# Extract and print all of the values
#list_of_hashes = sheet.get_all_records()
#print(list_of_hashes)

#extract only values I care about
# dates = sheet.get('C40:C46')
# print(dates)
# weights = sheet.get('B40:B46')
# print(weights)

#arraylist of mfp data
# list_mfp = sheet.batch_get(['E40:E46','F40:F46', 'G40:G46', 'H40:H46'])
# print(list_mfp)

sheet.batch_update([{
    #update weight, date
    'range': 'B40:C40',
    'values': [['800', '0/2']],
}, {
    #update mfp cals, protein, carbs, fat
    'range': 'E40:H40',
    'values': [['a', 'b', 'c', 'd']],
}])

