import click
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from scripts.dateUtils import get_sunday, get_base_sunday

# lookup table for fields in spreadsheet
note_rng_dict = {"Mon": 'B20:B21', "Tue": 'B22:G23', "Wed": 'B24:G25', "Thu": 'B26:G27', "Fri": 'B28:G29',
                 "Sat": 'B30:G31', "Sun": 'B32:G33'}
activity_rng_dict = {"steps": 'B54:B60', "miles": 'C54:C60', "combined": 'B54:C60'}
weight_nutrition_rng_dict = {"weight": 'B40:B46', "calories": 'E40:E46', "protein": 'F40:F46', "carbs": 'G40:G46',
                             "fat": 'H40:H46', "fiber": 'I40:I46'}

def clear_all():
    """
    Clears athlete notes, activity tracker, weight and nutrition tracker.
    Outputs progress bar to terminal.
    """
    with click.progressbar(length=3, label='Clearing other entries') as bar:
        clear_tracker()
        bar.update(1)
        clear_activity()
        bar.update(2)
        clear_notes()
        bar.update(3)


def clear_activity():
    """
    Clears activity tracker.
    """
    rng = activity_rng_dict['combined']
    populate_cells(sheet.range(rng), '')


def populate_activity(values):
    """
    Populates the activity tracker with FitBit data.
    Outputs progress bar to terminal.
    :param nested list values:  fitbit data to input to activity tracker.
    """
    with click.progressbar(length=2, label='Modifying activity tracker') as bar:
        rng = activity_rng_dict['steps']
        populate_cells(sheet.range(rng), values[0])
        bar.update(1)
        rng = activity_rng_dict['miles']
        populate_cells(sheet.range(rng), values[1])
        bar.update(2)


def clear_notes():
    """
    Clears the notes section.
    """
    rng = 'B20:G33'
    populate_cells(sheet.range(rng), '')


def add_note(msg, day):
    """
    Adds a note to specified day in the athlete notes section
    :param str msg: the message entry to add
    :param str day: the day of the week
    """
    rng = note_rng_dict[day]
    sheet.update(rng, msg, raw=True)


def clear_tracker():
    """
    Clears the activity tracker.
    """
    populate_tracker(None)


def populate_tracker(val_list, delta):
    """
    Populates the weight / nutrition tracker.
    Outputs progress bar to terminal.
    :param val_list:  potentially null list of values to populate weight / nutrition tracker. If val_list is null, clears tracker.
    Else, populates weight / nutrition tracker with MyFitnessPal data.
    :param delta: base date for api calls to MFP/fitbit
    """

    # update date col
    update_date(delta)
    # get list of ranges from dictionary
    range_list = list(weight_nutrition_rng_dict.values())

    if val_list is None:
        size = 6
        value = ''
        action = 'Clearing tracker'
    else:
        # get rid of date sublist in val_list
        val_list.pop(1)
        size = len(val_list)
        action = 'Updating tracker'

    with click.progressbar(length=size, label=action) as bar:
        for i in range(0, size):
            # get correct cell range and values
            rng = range_list[i]
            if val_list:
                value = val_list[i]
            populate_cells(sheet.range(rng), value)
            bar.update(i)


def update_date(delta):
    """
    Updates the Sunday date entry in the spreadsheet.
    :param delta: number of days to offset by
    """
    # sunday = get_sunday()
    sunday = get_base_sunday(delta)
    sunday = '{:%m/%d/%y}'.format(sunday)
    sheet.update_acell('C40', sunday)


def populate_cells(cell_range, val_sublist):
    """
    Populates individual cells in the given range with the given values.
    :param cell_range: the range of cells to update
    :param val_sublist: The values with which to populate the cells with. If empty, clears the cell.
    """

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
