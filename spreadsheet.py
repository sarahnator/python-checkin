import myfitnesspal as pal
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def update_row(dict):
    #TODO make update work with dictionary values
    #TODO test single entry --> mutltiple entries
    #TODO increment input range
    #TODO logic based on day of week? su = 40, mo = 41, tu = 42, etc?
    sheet.batch_update([{
            #update weight, date
            'range': 'B40:C40',
            'values': [[dict['weight'], dict['date']]],
        }, {
            #update mfp cals, protein, carbs, fat
            'range': 'E40:I40',
            'values': [[dict['cal'], dict['pro'], dict['car'], dict['fat'], dict['fiber']]],
        }])


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

# sheet.batch_update([{
#     #update weight, date
#     'range': 'B40:C40',
#     'values': [['800', '0/2']],
# }, {
#     #update mfp cals, protein, carbs, fat
#     'range': 'E40:I40',
#     'values': [['a', 'b', 'c', 'd', 'e']],
# }])


