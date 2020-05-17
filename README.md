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
```

## Acknowledgments
* @coddingtonbear [program](https://github.com/coddingtonbear/python-myfitnesspal.git)
* On using [keyring](https://alexwlchan.net/2016/11/you-should-use-keyring/)
* On interacting with [gspreadsheets in python](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)

