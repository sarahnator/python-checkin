# Python-Checkin: Data analysis for the ~~lazy~~ energy-conscious athlete! (personal project)
A data retrieval automation program that migrates data from the MyFitnessPal and FitBit/Garmin APIs into google spreadsheets for data analysis.

![ ](demo/screenShot.png)

 ## Current/Future Features
 * [X] Enables data retrieval from MyFitnessPal 
 * [X] Enables data retrieval from FitBit
 * [X] Enables user to remotely edit a spreadsheet (see Notes section)
 * [X] Editing allows a user to add notes to the Athlete Notes table, populate the Activity Tracker and Nutrition and Weight Tracker fields with the latest MFP/FitBit data, retrieve other parameterized fitness data, or clear any of all the editable regions mentioned.
 * [X] A [command-line interface](https://click.palletsprojects.com/en/7.x/) that allows the user to conveniently chain multiple commands for ease of use and access help page for any commands.
 * [X] User can see progress of requests through progress bars and outputs to the terminal.
 * [X] Secure MFP credential storage in system keyring.
 * [X] Export data to CSV files
 * [ ] Prompting / storage of credentials for necessary APIs (populate an empty credentials file)
 * [ ] Enable data retrieval from Garmin API

## Note
This project is intended for use by members of Gifted Performance, as the program is designed to work specifically with spreadsheets of GP clients. Setup instructions below are in progress :)
 
## Demo
Well that sucks, apparently the demo video is too big to attach in markdown. See the demo folder.
![](demo/shortDemo.mp4)
[description](demo/shortDemo.md)

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
Install required python3 modules:
```angular2
$ sudo pip install -r requirements.txt
```

## License
Project licensed under the MIT License

## Acknowledgments
* Coddingtonbear [myfitnesspal API](https://github.com/coddingtonbear/python-myfitnesspal.git)
* ORCAS [fibit API](https://github.com/orcasgit/python-fitbit)
