import socket
import sys
from threading import Thread
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QScrollArea,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QLabel)


def rsa_encrypt(text, public_key):
    return public_key.encrypt(text.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)) # encrypt using given RSA public key


def rsa_decrypt(text, private_key):
    return private_key.decrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)).decode() # decrypt using given RSA private key


def generate_keys():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048) # generate private key
    public = private.public_key() # get public key from private key
    public = public.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo) # convert to PEM
    return private, public # return results


class Ui_ChatWindow(object): # chat window
    def setupUi(self, ChatWindow):
        if not ChatWindow.objectName():
            ChatWindow.setObjectName(u"ChatWindow")
        ChatWindow.setFixedSize(800, 600)
        font = QFont() # font
        font.setFamilies([u"Quicksand Medium"])
        font.setPointSize(12)
        ChatWindow.setFont(font)
        ChatWindow.setStyleSheet(u"background: #000000;\n" # I am a terrible designer, I know
"color: #55BB55;\n"
"selection-background-color: #55BB55;\n"
"selection-color: #000000;"
"border: 1px solid #55BB55;") # sorry
        self.centralwidget = QWidget(ChatWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.msgedit = QTextEdit(self.centralwidget) # message input
        self.msgedit.setObjectName(u"msgedit")
        self.msgedit.setGeometry(QRect(0, 560, 700, 40))
        self.msgedit.setFont(font)
        self.msgedit.setPlaceholderText('Enter your message(180 characters max)')
        self.send_button = QPushButton(self.centralwidget) # button that sends messages
        self.send_button.setObjectName(u"send_button")
        self.send_button.setGeometry(QRect(700, 560, 100, 40))
        self.send_button.setFont(font)
        self.send_button.clicked.connect(self.send_message)
        self.chat = QScrollArea(self.centralwidget) # messages block
        self.chat.setObjectName(u"chat")
        self.chat.setGeometry(QRect(0, 0, 800, 560))
        self.chat.setFont(font)
        self.chat.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 800, 560))
        self.scrollAreaWidgetContents_2.setFont(font)
        self.chatWidget = QWidget(self.scrollAreaWidgetContents_2)
        self.chatLayout = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.label = QLabel(self.scrollAreaWidgetContents_2) # messages label
        self.label.setWordWrap(True)
        self.label.setGeometry(QRect(0, 0, 800, 560))
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.chatLayout.addWidget(self.label)
        self.chat.setWidget(self.scrollAreaWidgetContents_2)
        ChatWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ChatWindow)

        QMetaObject.connectSlotsByName(ChatWindow)
    # setupUi

    def retranslateUi(self, ChatWindow):
        ChatWindow.setWindowTitle(QCoreApplication.translate("ChatWindow", u"Chat", None))
        self.send_button.setText(QCoreApplication.translate("ChatWindow", u"Send", None))

    def connect_to_server(self, username, password, ip, port): # connect to server and login
        try:
            self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket
            self.chat_socket.connect((ip, port)) # connect to server
            self.public_key = serialization.load_pem_public_key(self.chat_socket.recv(2048)) # receive RSA public key from server
            self.local_private_key, self.local_public_key = generate_keys() # generate local keys
            if len(sys.argv) > 1:
                if sys.argv[1] == 'register': # check if user want to login or register
                    reg_key = sys.argv[2] # get registration key from terminal
                    login_signal = f'$server-code-register$ {username} {password} {reg_key}' # create package to register on server
                else:
                    print('Invalid run arguments!')
                    sys.exit()
            else:
                login_signal = f'{username} {password}' # create package to login on server
            self.chat_socket.send(rsa_encrypt(login_signal, self.public_key)) # encrypt and send login package to server
            login_answer = self.chat_socket.recv(1024).decode()
            if login_answer == 'login-code-success': # check if login was successful
                self.chat_socket.send(self.local_public_key)
            else:
                print('Login attempt failed. ' + login_answer)
        except Exception as e:
            print(e)
            print('Error while connecting to server. Please, check your config file and try again later.')

    def get_messages(self):
        while True:
            try:
                message = self.chat_socket.recv(25600) # receive message from server
                message = rsa_decrypt(message, self.local_private_key) # decrypt message
                self.label.setText(self.label.text() + '\n' + message) # add message to label
            except:
                pass

    def send_message(self):
        message = self.msgedit.toPlainText() # get text from message input
        if len(message) >= 180:
            message = message[0:180]
        if message != '': # check if message not empty
            message = rsa_encrypt(message, self.public_key) # encrypt message
            self.chat_socket.send(message) # send message
            self.msgedit.setText('') # clear message input


class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.setFixedSize(450, 145)
        font = QFont()
        font.setFamilies([u"Quicksand Medium"])
        font.setPointSize(12)
        Login.setFont(font)
        Login.setAutoFillBackground(False)
        Login.setStyleSheet(u"background: #000000;\n"
"color: #55BB55;\n"
"selection-background-color: #55BB55;\n"
"selection-color: #000000;") # sorry x2
        Login.setInputMethodHints(Qt.ImhNone)
        self.master_key_edit = QLineEdit(Login)
        self.master_key_edit.setObjectName(u"master_key_edit")
        self.master_key_edit.setGeometry(QRect(19, 50, 412, 30))
        self.master_key_edit.setFont(font)
        self.master_key_edit.setPlaceholderText('Your local master-key')
        self.decrypt_button = QPushButton(Login)
        self.decrypt_button.setObjectName(u"decrypt_button")
        self.decrypt_button.setGeometry(QRect(150, 100, 150, 31))
        self.decrypt_button.setFont(font)
        self.decrypt_button.clicked.connect(self.import_config)

        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Enter key", None))
        self.decrypt_button.setText(QCoreApplication.translate("Login", u"Decrypt", None))

    def import_config(self):
        key = self.master_key_edit.text() # get key from input
        fernet = Fernet(key) # create Fernet object
        config = list(fernet.decrypt(open('config', 'rb').read()).decode().split('\n')) # decrypt and read config file
        username = config[0][10:] # get username from config
        password = config[1][10:] # get password from config
        ip = config[2][4:] # get host ip from config
        port = int(config[3][6:]) # get host port from config
        main_window.show() # show chat window
        key_window.hide() # hide window with key input
        chat_window.connect_to_server(username, password, ip, port) # connect to server
        Thread(target=chat_window.get_messages, daemon=True).start() # start thread to receive messages


app = QApplication(sys.argv) # create application

main_window = QMainWindow() # create main window
chat_window = Ui_ChatWindow() # chat UI
chat_window.setupUi(main_window) # setup chat UI in main window
chat_window.retranslateUi(main_window)

key_window = QWidget() # create widget
login = Ui_Login() # decryption UI
login.setupUi(key_window) # setup decryption UI in widget
login.retranslateUi(key_window)
key_window.show() # show decryption UI

app.exec() # execute application
