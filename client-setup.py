import sys
import os
try:
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    from cryptography.fernet import Fernet
except:
    print('Error: cryptography not found. Run "pip install cryptography".')
    sys.exit()
from threading import Thread
try:
    import hashlib
except:
    print('Error: hashlib not found. Run "pip install hashlib".')
    sys.exit()
try:
    import PySide6
except:
    print('Error: PySide6 not found. Run "pip install PySide6".')

directory = input('Path to install: ')


def ask_system():
    print('Choose your system(1/2):')
    print('  [1] - Linux/MacOS')
    print('  [2] - Windows')
    system = input('> ')
    if system == '1':
        slash = '/'
    elif system == '2':
        slash == '\\'
    else:
        print('Incorrect input! Please, enter 1 or 2.\n')
        slash = ask_system()
    return slash


slash = ask_system()
os.system(f'curl https://raw.githubusercontent.com/gh0stKn1ght/Abyss/main/client/client.py > {directory}{slash}client.py')
os.system(f'curl https://raw.githubusercontent.com/gh0stKn1ght/Abyss/main/client/client.py > {directory}{slash}config.py')
master-key = Fernet.generate_key()
config = b'username: changeme\npassword: changeme\nip: 127.0.0.1\nport: 1234'
fernet = Fernet(master-key)
config = fernet.encrypt(config)
open(f'{directory}{slash}config', 'wb').write(config)
input(f'Your local master-key. Save it somewhere. Press Enter when you are ready...')
print('Successfully installed Abyss client!')
