import sys
import random
from tinydb import TinyDB, where, Query
from PySide6 import QtGui
from PySide6.QtCore import QSize, QPoint
from PySide6.QtGui import QAction, QIcon,QPixmap
from PySide6.QtWidgets import QTabWidget, QPushButton, QWidget, QGridLayout, QVBoxLayout, QApplication, QMainWindow, \
    QDoubleSpinBox, QLabel, QSpinBox, QAbstractSpinBox, QComboBox, QMessageBox, QToolBar, QStatusBar, QLineEdit, \
    QRadioButton
import sqlite3

class modifier_pallier_Window(QWidget):
    def __init__(self):
        super().__init__()

        c=sqlite3.connect("DB.sq3")
        cursor=c.cursor()

        #parametre par default:
        # parametre table DD
        # pallier1
        cursor.execute("SELECT activation FROM DD WHERE pallier=0")
        pallier0_activation = cursor.fetchone()[0]
        cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=0")
        pallier0_risque = cursor.fetchone()[0]
        cursor.execute("SELECT trade_pris FROM DD WHERE pallier=0")
        pallier0_trade_pris = cursor.fetchone()[0]
        # pallier1
        cursor.execute("SELECT activation FROM DD WHERE pallier=1")
        pallier1_activation = cursor.fetchone()[0]
        cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=1")
        pallier1_risque = cursor.fetchone()[0]
        cursor.execute("SELECT trade_pris FROM DD WHERE pallier=1")
        pallier1_trade_pris = cursor.fetchone()[0]
        # pallier2
        cursor.execute("SELECT activation FROM DD WHERE pallier=2")
        pallier2_activation = cursor.fetchone()[0]
        cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=2")
        pallier2_risque = cursor.fetchone()[0]
        cursor.execute("SELECT trade_pris FROM DD WHERE pallier=2")
        pallier2_trade_pris = cursor.fetchone()[0]
        # pallier3
        cursor.execute("SELECT activation FROM DD WHERE pallier=2")
        pallier3_activation = cursor.fetchone()[0]
        cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=3")
        pallier3_risque = cursor.fetchone()[0]
        cursor.execute("SELECT trade_pris FROM DD WHERE pallier=3")
        pallier3_trade_pris = cursor.fetchone()[0]
        # pallier4
        cursor.execute("SELECT activation FROM DD WHERE pallier=4")
        pallier4_activation = cursor.fetchone()[0]
        cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=4")
        pallier4_risque = cursor.fetchone()[0]
        cursor.execute("SELECT trade_pris FROM DD WHERE pallier=4")
        pallier4_trade_pris = cursor.fetchone()[0]
        # pallier5
        cursor.execute("SELECT activation FROM DD WHERE pallier=5")
        pallier5_activation = cursor.fetchone()[0]
        cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=5")
        pallier5_risque = cursor.fetchone()[0]
        cursor.execute("SELECT trade_pris FROM DD WHERE pallier=5")
        pallier5_trade_pris = cursor.fetchone()[0]

        #parametre principaux pour custom
        self.setWindowTitle("Changer pallier DD")
        self.setWindowIcon(QtGui.QIcon("image/gear_second.jpg"))

        self.setStyleSheet("""QPushButton{background-color: black;color:white;border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: beige;
    font: bold 14px;
    min-width: 10em;
    padding: 6px}""")

        layout = QGridLayout()
        # création des widgets


        self.Label_Pallier0_risque=QLabel("Risque de base:")
        self.Pallier0_risque=QDoubleSpinBox()
        self.Pallier0_risque.setDecimals(2)
        self.Pallier0_risque.setMaximum(100)
        self.Pallier0_risque.setValue(pallier0_risque)
        self.Pallier0_risque.setSuffix('%')

        self.Label_Pallier1_activation=QLabel("Activation pallier 1 (%DD): ")
        self.Activation_Pallier1=QDoubleSpinBox()
        self.Activation_Pallier1.setDecimals(2)
        self.Activation_Pallier1.setMaximum(100)
        self.Activation_Pallier1.setSuffix('%')
        self.Activation_Pallier1.setValue(pallier1_activation)
        self.Label_Pallier1_diviser_risque_base=QLabel("Risque pallier n°1: ")
        self.Pallier1_diviser_risque_base = QDoubleSpinBox()
        self.Pallier1_diviser_risque_base.setSuffix('%')
        self.Pallier1_diviser_risque_base.setDecimals(2)
        self.Pallier1_diviser_risque_base.setMaximum(100)
        self.Pallier1_diviser_risque_base.setValue(pallier1_risque)

        self.Label_Pallier2_activation = QLabel("Activation pallier 2 (%DD):: ")
        self.Activation_Pallier2 = QDoubleSpinBox()
        self.Activation_Pallier2.setDecimals(2)
        self.Activation_Pallier2.setMaximum(100)
        self.Activation_Pallier2.setValue(pallier2_activation)
        self.Activation_Pallier2.setSuffix('%')
        self.Label_Pallier2_diviser_risque_base = QLabel("Risque Pallier n°2: ")
        self.Pallier2_diviser_risque_base = QDoubleSpinBox()
        self.Pallier2_diviser_risque_base.setDecimals(2)
        self.Pallier2_diviser_risque_base.setSuffix("%")
        self.Pallier2_diviser_risque_base.setMaximum(100)
        self.Pallier2_diviser_risque_base.setValue(pallier2_risque)

        self.Label_Pallier3_activation = QLabel("Activation pallier 3 (%DD):: ")
        self.Activation_Pallier3 = QDoubleSpinBox()
        self.Activation_Pallier3.setDecimals(2)
        self.Activation_Pallier3.setMaximum(100)
        self.Activation_Pallier3.setValue(pallier3_activation)
        self.Activation_Pallier3.setSuffix('%')
        self.Label_Pallier3_diviser_risque_base = QLabel("Risque pallier n°3: ")
        self.Pallier3_diviser_risque_base = QDoubleSpinBox()
        self.Pallier3_diviser_risque_base.setDecimals(2)
        self.Pallier3_diviser_risque_base.setMaximum(100)
        self.Pallier3_diviser_risque_base.setSuffix('%')
        self.Pallier3_diviser_risque_base.setValue(pallier3_risque)

        self.Label_Pallier4_activation = QLabel("Activation pallier 4 (%DD): ")
        self.Activation_Pallier4 = QDoubleSpinBox()
        self.Activation_Pallier4.setDecimals(2)
        self.Activation_Pallier4.setMaximum(100)
        self.Activation_Pallier4.setSuffix('%')
        self.Activation_Pallier4.setValue(pallier4_activation)
        self.Label_Pallier4_diviser_risque_base = QLabel("Risque pallier n°4 ")
        self.Pallier4_diviser_risque_base = QDoubleSpinBox()
        self.Pallier4_diviser_risque_base.setDecimals(2)
        self.Pallier4_diviser_risque_base.setSuffix('%')
        self.Pallier4_diviser_risque_base.setMaximum(100)
        self.Pallier4_diviser_risque_base.setValue(pallier4_risque)

        self.Label_Pallier5_activation = QLabel("Activation pallier 5 (%DD):")
        self.Activation_Pallier5 = QDoubleSpinBox()
        self.Activation_Pallier5.setDecimals(2)
        self.Activation_Pallier5.setMaximum(100)
        self.Activation_Pallier5.setValue(pallier5_activation)
        self.Activation_Pallier5.setSuffix('%')
        self.Label_Pallier5_diviser_risque_base = QLabel("Risque pallier n°5: ")
        self.Pallier5_diviser_risque_base = QDoubleSpinBox()
        self.Pallier5_diviser_risque_base.setDecimals(2)
        self.Pallier5_diviser_risque_base.setSuffix('%')
        self.Pallier5_diviser_risque_base.setMaximum(100)
        self.Pallier5_diviser_risque_base.setValue(pallier5_risque)

        self.btn_changer_pallier=QPushButton("Changer les palliers")

        self.Confirmation_pallier=QLabel("Veuillez remplir les différents champs; à noter que si un pallier à un niveau d'activation 0"
                                    "il ne sera pas compté")



        # création des différents signaux pour pallier DD

        self.btn_changer_pallier.clicked.connect(self.fct_modification_pallier)


        #ajout dans le layout
        layout.addWidget(self.Label_Pallier0_risque,0,0)
        layout.addWidget(self.Pallier0_risque,0,1)

        layout.addWidget(self.Label_Pallier1_activation,1,0)
        layout.addWidget(self.Activation_Pallier1,1,1)
        layout.addWidget(self.Label_Pallier1_diviser_risque_base,2,0)
        layout.addWidget(self.Pallier1_diviser_risque_base,2,1)

        layout.addWidget(self.Label_Pallier2_activation,3,0)
        layout.addWidget(self.Activation_Pallier2,3,1)
        layout.addWidget(self.Label_Pallier2_diviser_risque_base,4,0)
        layout.addWidget(self.Pallier2_diviser_risque_base,4,1)

        layout.addWidget(self.Label_Pallier3_activation,5,0)
        layout.addWidget(self.Activation_Pallier3,5,1)
        layout.addWidget(self.Label_Pallier3_diviser_risque_base,6,0)
        layout.addWidget(self.Pallier3_diviser_risque_base,6,1)

        layout.addWidget(self.Label_Pallier4_activation,7,0)
        layout.addWidget(self.Activation_Pallier4,7,1)
        layout.addWidget(self.Label_Pallier4_diviser_risque_base,8,0)
        layout.addWidget(self.Pallier4_diviser_risque_base,8,1)

        layout.addWidget(self.Label_Pallier5_activation,9,0)
        layout.addWidget(self.Activation_Pallier5,9,1)
        layout.addWidget(self.Label_Pallier5_diviser_risque_base,10,0)
        layout.addWidget(self.Pallier5_diviser_risque_base,10,1)

        layout.addWidget(self.btn_changer_pallier,11,0,1,2)

        layout.addWidget(self.Confirmation_pallier,12,0,1,2)
        self.setLayout(layout)


    def fct_modification_pallier(self):
        c=sqlite3.connect("DB.sq3")
        cursor=c.cursor()

        value_activation_pallier1=self.Activation_Pallier1.value()
        value_activation_pallier2 = self.Activation_Pallier2.value()
        value_activation_pallier3 = self.Activation_Pallier3.value()
        value_activation_pallier4 = self.Activation_Pallier4.value()
        value_activation_pallier5 = self.Activation_Pallier5.value()

        value_division_pallier0=self.Pallier0_risque.value()
        value_division_pallier1=self.Pallier1_diviser_risque_base.value()
        value_division_pallier2 = self.Pallier2_diviser_risque_base.value()
        value_division_pallier3 = self.Pallier3_diviser_risque_base.value()
        value_division_pallier4 = self.Pallier4_diviser_risque_base.value()
        value_division_pallier5 = self.Pallier5_diviser_risque_base.value()



        if value_activation_pallier2!=0 and value_activation_pallier1>value_activation_pallier2:
            QMessageBox.critical(self,'Error','La valeur d\'activation du pallier 2 est supérieur au pallier 1, elle doit être plus petite',buttons=QMessageBox.Ok)

        elif value_activation_pallier3!=0 and value_activation_pallier2>value_activation_pallier3:
            QMessageBox.critical(self,'Error',
                                 'La valeur d\'activation du pallier 2 est supérieur au pallier 3, elle doit être plus petite',buttons=QMessageBox.Ok)
        elif value_activation_pallier4 != 0 and value_activation_pallier3 > value_activation_pallier4:
            QMessageBox.critical(self,'Error',
                                 'La valeur d\'activation du pallier 3 est supérieur au pallier 4, elle doit être plus petite',buttons=QMessageBox.Ok)
        elif value_activation_pallier5 != 0 and value_activation_pallier4 > value_activation_pallier5:
            QMessageBox.critical(self,'Error',
                                 'La valeur d\'activation du pallier 4 est supérieur au pallier 5, elle doit être plus petite',buttons=QMessageBox.Ok)

        else:
            sql = "UPDATE DD SET risque_pourcentage = ? WHERE pallier = ?"
            value = [(value_division_pallier0, 0), (value_division_pallier1, 1), (value_division_pallier2, 2),(value_division_pallier3,3),(value_division_pallier4,4),(value_division_pallier5,5)]
            cursor.executemany(sql,value)
            sql = "UPDATE DD SET activation = ? WHERE pallier = ?"
            value = [ (value_activation_pallier1, 1), (value_activation_pallier2, 2),
                     (value_activation_pallier3, 3), (value_activation_pallier4, 4), (value_activation_pallier5, 5)]
            cursor.executemany(sql, value)
            c.commit()
            c.close()






