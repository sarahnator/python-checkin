import requests
import json
import base64


# Insert your own info here as you defined when you created your APP
# Note that in a real app you would not want to hard-code these values
# Instead you would want to import them from the environment or even use
# a more secure solution like a keystore.
with open('../json/creds.json', 'r') as f:
    creds = json.load(f)
CLIENT_ID = creds['fitbit-clientID']
CLIENT_SECRET = creds['fitbit-secret']
CODE = creds['fitbit-code']
REDIRECT_URI = "http://127.0.0.1:8080/"
STATE = "NewJersey"  # note that in a true production app you would use state to protect against cross site attacks
DOMAIN = 'daas.api.hp.com' # use eu hostname if you are in EU


def refresh_token():
    '''refresh existing token for a new one'''

    with open('../json/creds.json', 'r') as f:
        creds = json.load(f)

    refresh_token = creds['fitbit-refresh-token']

    base64_encoded_clientid_clientsecret = base64.b64encode(str.encode(f'{CLIENT_ID}:{CLIENT_SECRET}'))  # concatenate with : and encode in base64
    base64_encoded_clientid_clientsecret = base64_encoded_clientid_clientsecret.decode('ascii')  # turn bytes object into ascii string

    base_url = f'https://{DOMAIN}'
    url = f"{base_url}/oauth/v1/token"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': f'Basic {base64_encoded_clientid_clientsecret}'
    }

    data = {'grant_type': 'refresh_token',
            'code': CODE,
            'redirect_uri': REDIRECT_URI,
            'refresh_token': refresh_token
            }
    print('code: ' + CODE)
    r = requests.post(url, headers=headers, data=data)
    response = r.json()

    if response.get('access_token'):
        # don't store creds in plaintext in a real app obviously
        with open('../json/creds.json', 'w') as f:
            json.dump(response, f, indent=4)
    else:
        print('There was an error refreshing your access token')
        print(r.text)


if __name__ == '__main__':
    refresh_token()  # refresh an existing token (we are assuming you have one stored in creds.json)