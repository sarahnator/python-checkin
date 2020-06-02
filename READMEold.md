# PY-Checkin
Python program that automates data retrieval from MyFitnessPal and updates a google spreadsheet with daily nutrition stats and weights. 

## Set Up
1. See prereqs
2. Use system keyring to store MyFitnessPal credentials

### Prereqs
Tools needed:
* python
* pip
* keyring - enables safe storage of credentials using python's system keyring service
* gspread - enables interaction with google spreadsheets
* oauth2client - uses OAuth 2.0 to authorize with google drive API
* Since MyFitnessPal's api is private-access only, you'll need @coddingtonbear's
[myfitnesspal api workaround](https://github.com/coddingtonbear/python-myfitnesspal.git).

Check your python3 version with the following command. You may need >=3.7 on your system.
```angular2
$ python3 -V
```
```md
# installing pip:
>$ curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
>$ sudo pip install requests

# test install success
>$ python
>>> import requests
>>> response = requests.get("http://automatingosint.com")
>>> response.status_code
# if response code is 200, indicates success
>>> exit()

# install gspread, oauth2client, keyring:
>$ pip install gspread oauth2client keyring
```

To create the google drive api key:
follow these [directions](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)

### Using system keyring
To avoid hard-coding MFP credentials and its security implications, use python's keyring service to store credentials:
```md
# toggle python shell
>$ python
>>> import keyring
>>> keyring.set_password('myfitnesspal', 'YOUR_USERNAME_HERE', 'YOUR_PASSWORD_HERE')
# verify that you've stored your password correctly
>>> keyring.get_password('myfitnesspal', 'YOUR_USERNAME_HERE')
>>> exit()
```

## Acknowledgments
* @coddingtonbear [myfitnesspal api](https://github.com/coddingtonbear/python-myfitnesspal.git)
* On using [keyring](https://alexwlchan.net/2016/11/you-should-use-keyring/)
* On interacting with [gspreadsheets in python](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)

## fun notes

# def update_row(dict):
#     # break dictionary into list of values
#     val_list = [*[list(idx.values()) for idx in dict]]
#     #                       [day 1]                                               [day 2]                                [day 3]
#     #func: [['123.3', '05-18', 2347, 153, 301, 65, 62], ['123.2', '05-19', 2324, 154, 298, 63, 63], ['123.4', '05-20', 2316, 152, 295, 63, 67]]
#     print("func: " + str(val_list))

# sheet.batch_update([{
#     #update weight, date
#     'range': 'B40:C40',
#     'values': [['800', '0/2']],
# }, {
#     #update mfp cals, protein, carbs, fat
#     'range': 'E40:I40',
#     'values': [['a', 'b', 'c', 'd', 'e']],
# }])
 # day = parse(last_sunday, dayfirst=False)
# from dateutil.parser import parse

#script testing:
$ virtualenv venv
$ . venv/bin/activate
$ pip install --editable .
[src](https://click.palletsprojects.com/en/7.x/setuptools/#testing-the-script)



## TODO
 * update this readme
 * DRY code
 * Sample Dummy Credentials storage file
 * Unchecked stuff in features
 * Video walkthrough of commands/animation
 * [ ] Garmin API
 * [ ] Create a speadsheet class to contain lookup dictionaries of all editable regions and include functions to add or set a region of the spreadsheet to access.
 * [ ] Create setup function to prompt user for credentials and accordingly store them.
 * [ ] Add pypy python interpreter to speed up execution
 * [ ] Create PyPi package for GP clients to use this program