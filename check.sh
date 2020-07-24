echo "Hello there! Sit tight..."

cd /Users/cookiemonster/PycharmProjects/python-checkin > /dev/null

virtualenv venv > /dev/null
. venv/bin/activate > /dev/null
pip install --editable . > /dev/null

# add more robust error checking and options
checkin update || checkin clear update -a -t
echo "All updates made!"
