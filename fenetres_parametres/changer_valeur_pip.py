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


class ChangerPipsWindow(QWidget):

    def __init__(self):
        super().__init__()
        #Base de donnée et item_paires
        c=sqlite3.connect("DB.sq3")
        cu=c.cursor()
        cu.execute("SELECT paire FROM Valeur_pip ")
        liste_items = []
        p = cu.fetchone()
        while p is not None:
            liste_items.append(p[0])
            p = cu.fetchone()
        c.close()
        #parametre principaux pour custom
        self.setWindowTitle("changer les valeurs du pips")
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
        self.Label_Paires=QLabel("Paire: ")
        self.Paires=QComboBox()
        self.Paires.addItem("Selectionner paire")
        self.Paires.addItems(liste_items)

        self.Label_modifier_pip=QLabel('Valeur du pip: ')
        self.modifier_pip=QDoubleSpinBox()
        self.modifier_pip.setDecimals(5)

        self.Modifier_pip_btn=QPushButton('Modifier valeur pip')
        self.Modifier_pip_btn.setStyleSheet("""background-color: black;
    color:white;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: beige;
    font: bold 14px;
    min-width: 10em;
    padding: 6px""")


        self.Confirmation_Modification=QLabel('')
        # création des différents signaux pour modifier pip
        self.Modifier_pip_btn.clicked.connect(self.fct_modifier_pips)
        self.Paires.currentTextChanged.connect(self.fct_combo_box_change)

        #ajout dans le layout
        layout.addWidget(self.Label_Paires,0,0)
        layout.addWidget(self.Paires,0,1)

        layout.addWidget(self.Label_modifier_pip,1,0)
        layout.addWidget(self.modifier_pip,1,1)

        layout.addWidget(self.Modifier_pip_btn,2,0,1,2)
        layout.addWidget(self.Confirmation_Modification,3,0,1,2)
        self.setLayout(layout)


#fonction pour modifier pip quand on appuie sur modifier
    def fct_modifier_pips(self):
        c=sqlite3.connect("DB.sq3")
        cu=c.cursor()
        paire=self.Paires.currentText()
        pip=self.modifier_pip.value()
        if pip==0 or paire=="Selectionner paire":
            if pip==0:
                self.Confirmation_Modification.setText("ERREUR: la valeur du pip ne peut pas être égale à 0. ")
            elif paire=="Selectionner paire":
                self.Confirmation_Modification.setText("ERREUR:  Veuillez selectionner une paire.")
        else:
            sql=f"UPDATE Valeur_pip SET valeur_pip={pip} WHERE paire=?"
            cu.execute(sql,[paire])
            c.close()
            self.Confirmation_Modification.setText(f'Valeur du pips  sur {paire}: {str(pip)}')

            self.modifier_pip.setValue(0.0000)
            self.Paires.setCurrentIndex(0)

    def fct_combo_box_change(self):
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        paire = self.Paires.currentText()
        if paire!="Selectionner paire":
            sql=f"SELECT valeur_pip FROM Valeur_pip WHERE paire=? "
            cu.execute(sql,[paire])
            value_pips=cu.fetchone()[0]
            self.modifier_pip.setValue(value_pips)

        c.close()
