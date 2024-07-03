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
os.system(f'curl https://raw.githubusercontent.com/gh0stKn1ght/Abyss/main/server/server.py > {directory}{slash}server.py')
os.system(f'curl https://raw.githubusercontent.com/gh0stKn1ght/Abyss/main/server/reg_user.py > {directory}{slash}reg_user.py')
reg_key = input('Registration key for server: ')
open(f'{directory}{slash}reg_key.txt', 'w').write(reg_key)
print('Successfully installed Abyss server!')
