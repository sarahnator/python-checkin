import myfitnesspal as pal
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from dateUtils import *

# def update_row(dict):
#     # break dictionary into list of values
#     val_list = [*[list(idx.values()) for idx in dict]]
#     #                       [day 1]                                               [day 2]                                [day 3]
#     #func: [['123.3', '05-18', 2347, 153, 301, 65, 62], ['123.2', '05-19', 2324, 154, 298, 63, 63], ['123.4', '05-20', 2316, 152, 295, 63, 67]]
#     print("func: " + str(val_list))

def update_col(dict):
    #format:
    #[['122.5', '123.3', '123.2', '123.4'], --> weight    ['05-17', '05-18', '05-19', '05-20'],  --> date   [2321, 2347, 2324, 2316], --> cals
    #[298, 301, 298, 295], --> pro   [63, 65, 63, 63], --> fat   [154, 153, 154, 152], --> pro   [62, 62, 63, 67]] --> fiber
    val_list = [list(col) for col in zip(*[d.values() for d in dict])]
    update_date()
    update_all(val_list)

def update_all(val_list):
    update_weights(val_list)
    update_cals(val_list)
    update_pro(val_list)
    update_carb(val_list)
    update_fat(val_list)
    update_fiber(val_list)

def update_weights(val_list):
    # weight cells: B40:B46
    # data_offset = day of week data starts (sunday = 0, mo = 1...)
    rng = str('B40:B' + str(40 + len(val_list[0]) - 1))
    populate_cells(sheet.range(rng), val_list[0])

def update_date():
    sunday = get_sunday()
    sheet.update_acell('C40', sunday)

def update_cals(val_list):
    # date cells: E40:E46
    # data_offset = day of week data starts (sunday = 0, mo = 1...)
    rng = str('E40:E' + str(40 + len(val_list[0]) - 1))
    populate_cells(sheet.range(rng), val_list[2])

def update_pro(val_list):
    # date cells: E40:E46
    # data_offset = day of week data starts (sunday = 0, mo = 1...)
    rng = str('F40:F' + str(40 + len(val_list[0]) - 1))
    populate_cells(sheet.range(rng), val_list[3])


def update_carb(val_list):
    # date cells: E40:E46
    # data_offset = day of week data starts (sunday = 0, mo = 1...)
    rng = str('G40:G' + str(40 + len(val_list[0]) - 1))
    populate_cells(sheet.range(rng), val_list[4])

def update_fat(val_list):
    # date cells: E40:E46
    # data_offset = day of week data starts (sunday = 0, mo = 1...)
    rng = str('H40:H' + str(40 + len(val_list[0]) - 1))
    populate_cells(sheet.range(rng), val_list[5])

def update_fiber(val_list):
    # date cells: E40:E46
    # data_offset = day of week data starts (sunday = 0, mo = 1...)
    rng = str('I40:I' + str(40 + len(val_list[0]) - 1))
    populate_cells(sheet.range(rng), val_list[6])

def populate_cells(cell_range, val_sublist):
    for i, cell in enumerate(cell_range):
        cell.value = val_sublist[i]
    sheet.update_cells(cell_range)

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


