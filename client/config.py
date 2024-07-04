from cryptography.fernet import Fernet
import sys
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QSizePolicy,
    QTextEdit, QWidget, QLineEdit)

class Ui_Config(object):
    def setupUi(self, Config):
        if not Config.objectName():
            Config.setObjectName(u"Config")
        Config.setFixedSize(800, 600)
        Config.setStyleSheet(u"background: #000000;\n"
"color: #55BB55;\n"
"selection-background-color: #55BB55;\n"
"selection-color: #000000;")
        font = QFont()
        font.setFamilies([u"Quicksand Medium"])
        font.setPointSize(12)
        Config.setFont(font)
        self.centralwidget = QWidget(Config)
        self.centralwidget.setObjectName(u"centralwidget")
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(0, 25, 800, 575))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(0, 0, 80, 25))
        self.pushButton.clicked.connect(self.save_changes)
        Config.setCentralWidget(self.centralwidget)
        self.masterkey = False

        self.retranslateUi(Config)

        QMetaObject.connectSlotsByName(Config)
    # setupUi

    def retranslateUi(self, Config):
        Config.setWindowTitle(QCoreApplication.translate("Config", u"Config", None))
        self.pushButton.setText(QCoreApplication.translate("Config", u"Save", None))
    # retranslateUi

    def import_encryption(self, masterkey, configtext):
        self.masterkey = masterkey
        self.textEdit.setText(configtext)

    def save_changes(self):
        if self.masterkey:
            config = open(sys.argv[0].replace('config.py', 'config'), 'wb')
            fernet = Fernet(self.masterkey)
            data = self.textEdit.toPlainText()
            data = fernet.encrypt(data.encode())
            config.write(data)
            config.close()
        else:
            print('Error: Please, provide encryption key')


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
"selection-color: #000000;")
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
        key = self.master_key_edit.text()
        fernet = Fernet(key)
        config = fernet.decrypt(open(sys.argv[0].replace('config.py','config'), 'rb').read()).decode()
        config_edit.import_encryption(key, config)
        main_window.show()
        key_window.hide()


app = QApplication(sys.argv)

main_window = QMainWindow()
config_edit = Ui_Config()
config_edit.setupUi(main_window)
config_edit.retranslateUi(main_window)

key_window = QWidget()
login = Ui_Login()
login.setupUi(key_window)
login.retranslateUi(key_window)
key_window.show()

app.exec()
