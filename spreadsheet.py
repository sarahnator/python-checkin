import myfitnesspal as pal
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('../json/client_secret.json', scope)
client = gspread.authorize(creds)

# extract json information @sheetName
with open('../json/creds.json') as src:
    data = json.load(src)

# Find workbook by name and open the first sheet
sheet = client.open(data['sheetName']).sheet1

sheet.batch_update([{
    #update weight, date
    'range': 'B40:C40',
    'values': [['800', '0/2']],
}, {
    #update mfp cals, protein, carbs, fat
    'range': 'E40:H40',
    'values': [['a', 'b', 'c', 'd']],
}])

