import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from scripts.dateUtils import get_sunday

# lookup table
note_rng_dict = {"Mon": 'B20:B21', "Tue": 'B22:G23', "Wed": 'B24:G25', "Thu": 'B26:G27', "Fri": 'B28:G29',
                 "Sat": 'B30:G31', "Sun": 'B32:G33'}
activity_rng_dict = {"steps": 'B54:B60', "miles": 'C54:C60', "combined": 'B54:C60'}


def update_cols(dict):
    # format:   [['122.5', '123.3', '123.2', '123.4'], --> weight    ['05-17', '05-18', '05-19', '05-20'],  --> date   [2321, 2347, 2324, 2316], --> cals
    #           [298, 301, 298, 295], --> pro   [63, 65, 63, 63], --> fat   [154, 153, 154, 152], --> pro   [62, 62, 63, 67]] --> fiber
    val_list = [list(col) for col in zip(*[d.values() for d in dict])]
    update_date()
    update_tracker(val_list)

def clear_activity():
    rng = activity_rng_dict['combined']
    populate_cells(sheet.range(rng), '')

def clear_notes():
    rng = 'B20:G33'
    populate_cells(sheet.range(rng), '')


def add_note(msg, day):
    rng = note_rng_dict[day]
    sheet.update(rng, msg, raw=True)


    # populate_cells(sheet.range(rng), msg)

def clear_tracker():
    update_tracker(None)


def update_tracker(val_list):
    # update weight first
    rng = 'B40:B46'
    value_idx = 0

    if val_list is None:
        length = 6
        value = ''
    else:
        length = len(val_list) - 1
    for i in range(0, length):
        # get correct cell range and values
        if i != 0:
            rng = rng.replace(rng[0], chr(68 + i), 2)  # D = 68 dec
            value_idx = 1 + i
        if val_list:
            value = val_list[value_idx]
        populate_cells(sheet.range(rng), value)


def update_date():
    sunday = get_sunday()
    sunday = '{:%m/%d/%y}'.format(sunday)
    sheet.update_acell('C40', sunday)


def populate_cells(cell_range, val_sublist):
    for i, cell in enumerate(cell_range):
        if (i > len(val_sublist) - 1) or val_sublist == '':
            cell.value = ''  # have no data for these cells
        else:
            cell.value = val_sublist[i]
    sheet.update_cells(cell_range)


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('json/client.json', scope)
client = gspread.authorize(creds)

# extract json information @sheetName
with open('json/creds.json') as src:
    data = json.load(src)

# Find workbook by name and open the first sheet
sheet = client.open(data['sheetName']).sheet1
