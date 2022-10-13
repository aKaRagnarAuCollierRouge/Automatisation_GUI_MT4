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
class AjouterPaireWindow(QWidget):
    def __init__(self):
        super().__init__()
        #titre window et layout
        self.setWindowTitle("Ajouter une paire.")
        self.setWindowIcon(QtGui.QIcon("image/gear_second.jpg"))

        layout=QVBoxLayout()
        #création de widget

        self.Label_paire_devise=QLabel("paire devise(ex: XXX/JPY): ")
        self.paire_devise=QLineEdit()

        self.Label_valeur_du_pips=QLabel("valeur du pips: ")
        self.valeur_du_pips=QDoubleSpinBox()
        self.valeur_du_pips.setDecimals(5)
        self.ajouter=QPushButton('Ajouter')
        self.ajouter.setStyleSheet("""background-color: black;
    color:white;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: beige;
    font: bold 14px;
    min-width: 10em;
    padding: 6px""")

        self.confirmation_ajouter=QLabel("Veuillez ajouter une paire puis appuyer sur le bouton 'ajouter'.")
        #connexions
        self.ajouter.clicked.connect(self.création_devise)

        #ajout des widget dans layout
        layout.addWidget(self.Label_paire_devise)
        layout.addWidget(self.paire_devise)

        layout.addWidget(self.Label_valeur_du_pips)
        layout.addWidget(self.valeur_du_pips)

        layout.addWidget(self.ajouter)
        self.setLayout(layout)


    #fonction qui créer une devise
    def création_devise(self):
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        paire=self.paire_devise.text()
        pip=self.valeur_du_pips.value()
        value=[paire,pip]
        sql="INSERT INTO Valeur_pip(paire,valeur_pip)VALUES(?,?)"
        cu.execute(sql,value)
        self.confirmation_ajouter.setText(f'La paire {paire} à bien été ajouté , ca valeur de pip est:{str(pip)}')
        self.paire_devise.setText("")
        self.valeur_du_pips.setValue(0.00000)
        c.commit()
        c.close()

