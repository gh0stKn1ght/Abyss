from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from threading import Thread
import hashlib
import sqlite3
import socket

host = '0.0.0.0' # address to host(you can change it, but there is no need to)
port = int(input('Socket port: '))
server = socket.socket() # create socket
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # socket options
server.bind((host, port)) # bind socket
server.listen(5) # start socket listening


def register(user_key, login, password):
    registration_key = open('reg_key.txt', 'r').read().replace('\n', '')
    if user_key != registration_key:
        return 'Incorrect registration key', False
    hash = hashlib.shake_256()
    hash.update(password.encode())
    password = hash.hexdigest(512)
    database = sqlite3.connect('users.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Credentials (
    id INTEGER PRIMARY KEY,
    login TEXT NOT NULL,
    password TEXT NOT NULL
    )''')
    cursor.execute('SELECT id FROM Credentials WHERE login = ?', (login,))
    username_is_taken = cursor.fetchall()
    if username_is_taken:
        return 'This username is already taken. Please, choose another one.', False
    cursor.execute('INSERT INTO Credentials (login, password) VALUES (?, ?)', (login, password))
    database.commit()
    database.close()
    print(f'User {login} registered.')
    return 'Registration successful', True


def generate_keys():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048) # generate RSA private key
    public = private.public_key() # get public key from private key
    public = public.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo) # convert to PEM
    return private, public # return results


def rsa_encrypt(text, public_key):
    if type(text) is str: # encode text if not encoded already
        text = text.encode()
    return public_key.encrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)) # encrypt using RSA public key


def rsa_decrypt(text, private_key):
    return private_key.decrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)).decode() # decrypt using RSA private key


class Client(): # client class
    def __init__(self, connection, login, public_key, ip):
        self.connection, self.login, self.public_key, self.ip = connection, login, public_key, ip # client data

    def send(self, data):
        self.connection.send(rsa_encrypt(data, self.public_key)) # encrypt message with clients public key and send it

    def close(self):
        self.connection.close() # close connection with client

    def recv(self, package_size):
        return self.connection.recv(package_size) # receive message from client


def login_client(new_client, client_list, ip):
    new_client.send(public_key) # send RSA public key to client
    login_data = new_client.recv(61440) # receive login package from client
    try: # proccess and verify login data
        login_data = list(rsa_decrypt(login_data, private_key).split(' '))
        if login_data[0] == '$server-code-register$':
            login = login_data[1]
            password = login_data[2]
            registration_key = login_data[3]
            reg_answer, reg_success = register(registration_key, login, password)
            if not reg_success:
                new_client.send(reg_answer.encode())
                new_client.close()
                return
            login_data = [login, password]
        login = login_data[0]
        password = login_data[1].encode()
        database = sqlite3.connect('users.db')
        hash = hashlib.shake_256()
        hash.update(password)
        password = hash.hexdigest(512)
        cursor = database.cursor()
        cursor.execute('SELECT password FROM Credentials WHERE login = ?', (login,))
        stored_password = cursor.fetchone()[0]
        if not stored_password or stored_password != password:
            new_client.send(b'Password incorrect.')
            new_client.close()
            return
        new_client.send(b'login-code-success')
        client_public_key = serialization.load_pem_public_key(new_client.recv(2048))
    except Exception as error:
        print(f'{ip}: {error}. Socket closed.')
        new_client.send(b'Internal server error. Please, check your config.')
        new_client.close()
        return
    logged_client = Client(new_client, login, client_public_key, ip) # create new client
    client_list.append(logged_client) # append it to the list
    Thread(target=redirect_messages, args=(logged_client, client_list), daemon=True).start() # start new thread to receive messages from client


def wait_for_new_clients(client_list):
    while True: # wait for new clients and login them
        try:
            new_client, new_client_address = server.accept()
            print('New socket from', new_client_address)
            Thread(target=login_client, args=(new_client, client_list, new_client_address), daemon=True).start()
        except Exception as error:
            print('Error:', error)


def redirect_messages(client, client_list):
    message = client.login + ' connected.'
    for user in client_list: # announce everyone that new client connected
        try:
            user.send(message)
        except:
            user.close()
            client_list.remove(user)
    while True: # listen for messages from client and send them to everyone
        try:
            message = rsa_decrypt(client.recv(25600), private_key)
            message = f'{client.login}: ' + message
            message = message.encode()
        except Exception as error:
            print(f'{client.ip}: {error}. Socket closed.')
            message = 'FATAL_ERROR'
            client.close()
            client_list.remove(client)
        if message != 'FATAL_ERROR': # check if the client is still online
            for user in client_list:
                try:
                    user.send(message)
                except:
                    user.close()
                    client_list.remove(user)
        else: # if not, announce everyone that the client disconnected
            message = user.login + ' disconnected.'
            for user in client_list:
                try:
                    user.send(message)
                except:
                    user.close()
                    client_list.remove(user)
            break



private_key, public_key = generate_keys() # generate RSA keys

ls = []
wait_for_new_clients(ls) # start waiting for clients
