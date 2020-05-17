import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Desktop/client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Copy of Sarah Etter Macro & Cardio").sheet1

# Extract and print all of the values
#list_of_hashes = sheet.get_all_records()
#print(list_of_hashes)

#extract only values I care about
dates = sheet.get('C40:C46')
print(dates)
weights = sheet.get('B40:B46')
print(weights)

#arraylist of mfp data
list_mfp = sheet.batch_get(['E40:E46','F40:F46', 'G40:G46', 'H40:H46'])
print(list_mfp)

#update values
#row = first param
#col = second param
#update calories
#sheet.update_cell(40, 5, 0)

#update protein count
col = [[0],[5], [6],[3],[2],[1],[0]]
rng = 'F40:F46'
sheet.update('F40:F46', col)

# sheet.batch_update([{
#     'range': 'E40:E46',
#     'values': [['0', '1', '2', '4', '8', '16', '32']],
# }, {
#     'range': 'F40:F46',
#     'values': [['32', '16', '8', '4', '2', '1', '0']],
# },{
#     'range': 'G40:G46',
#     'values': [['0', '1', '2', '3', '4', '5', '6']],
# },{
#     'range': 'H40:H46',
#     'values': [['6', '5', '4', '3', '2', '1', '0']],
# }])
