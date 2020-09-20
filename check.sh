echo "Hello there! Sit tight..."

cd /Users/cookiemonster/PycharmProjects/python-checkin > /dev/null || return

virtualenv venv > /dev/null
. venv/bin/activate > /dev/null
pip install --editable . > /dev/null

# for -d flag
if [ -z "$var" ]
then
  offset=0
else
  offset="$1"
fi

# add more robust error checking and options

checkin update -d "$offset" || checkin clear update -a -t -d "$offset"
echo "All updates made!"
