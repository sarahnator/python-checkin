# Python-Checkin
A data retrieval automation program that migrates data from the MyFitnessPal and FitBit/Garmin APIs into google spreadsheets for data analysis.

## TODO
 * update this readme
 * DRY code
 * CLI
 * PyPi package

## Configuration
* Gspread: Create credentials [here](https://gspread.readthedocs.io/en/latest/oauth2.html), follow the setup instructions detailed in [this post](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
* Fitbit: Register personal application [here](https://dev.fitbit.com/apps/new), following these [instructions](https://towardsdatascience.com/collect-your-own-fitbit-data-with-python-ff145fa10873)
    * To configure the application to avoid webbrowser redirection for verification,  on the dev.fitbit page, go to MANAGE MY APPS > OAuth2.0 tutorial page. Under Flow Type, select Authorization Code Flow and fill in the form fields below. Store the Access Token and Refresh Token.
* MyFitnessPal: Use python's keyring service to store  your account credentials:
```md
Toggle python shell:
$ python 
>>> import keyring
>>> keyring.set_password('myfitnesspal', 'YOUR_USERNAME_HERE', 'YOUR_PASSWORD_HERE')
Verify that you've stored your password correctly:
>>> keyring.get_password('myfitnesspal', 'YOUR_USERNAME_HERE') 
>>> exit()
```
## Usage
Check your python3 version with the following command. You may need >=3.7 on your system.
```angular2
$ python3 -V
```
Install required python3 modules:
```angular2
sudo pip install -r requirements.txt
```
## License
Project licensed under the MIT License

## Acknowledgments
* @coddingtonbear's [myfitnesspal api](https://github.com/coddingtonbear/python-myfitnesspal.git)
* ORCAS [fibit API](https://github.com/orcasgit/python-fitbit)
* On using [keyring](https://alexwlchan.net/2016/11/you-should-use-keyring/)
* On interacting with [gspreadsheets](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)

