# Python-Checkin
A data retrieval automation program that migrates data from the MyFitnessPal and FitBit/Garmin APIs into google spreadsheets for data analysis.
 
 ## Current/Future Features
 * [X] Enables data retrieval from MyFitnessPal 
 * [X] Enables data retrieval from FitBit
 * [X] Enables user to remotely edit a spreadsheet (see Notes section)
 * [X] Editing allows a user to add notes to the Athlete Notes table, populate the Activity Tracker and Nutrition and Weight Tracker fields with the latest MFP/FItbit data, or clear any of all the editable regions mentioned.
 * [X] A [command-line interface](https://click.palletsprojects.com/en/7.x/) that allows the user to conveniently chain multiple commands for ease of use and access help page for any commands.
 * [X] User can see progress of requests through progress bars and outputs to the terminal.
 * [X] Secure MFP credential storage in system keyring.
 * [ ] Enable data retrieval from Garmin API
 * [ ] python interpreter for faster execution
 * [ ] ...

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

## Notes
The spreadsheet described above is based on the features of spreadsheets accessible to clients of Gifted Performance LLC.

## License
Project licensed under the MIT License

## Acknowledgments
* @coddingtonbear's [myfitnesspal API](https://github.com/coddingtonbear/python-myfitnesspal.git)
* ORCAS [fibit API](https://github.com/orcasgit/python-fitbit)

## TODO
 * update this readme
 * DRY code
 * Sample Dummy Credentials storage file
 * Unchecked stuff in features
 * Video walkthrough of commands/animation
 * Truncate distance values from fitbit data
 * [ ] Garmin API
 * [ ] Create a speadsheet class to contain lookup dictionaries of all editable regions and include functions to add or set a region of the spreadsheet to access.
 * [ ] Create setup function to prompt user for credentials and accordingly store them.
 * [ ] Add pypy python interpreter to speed up execution
 * [ ] Create PyPi package for GP clients to use this program