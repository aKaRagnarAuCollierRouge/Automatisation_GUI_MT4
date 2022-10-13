import sqlite3
import sys
import random
from tinydb import TinyDB, where, Query
from PySide6 import QtGui
from PySide6.QtCore import QSize, QPoint
from PySide6.QtGui import QAction, QIcon,QPixmap
from PySide6.QtWidgets import QTabWidget, QPushButton, QWidget, QGridLayout, QVBoxLayout, QApplication, QMainWindow, \
    QDoubleSpinBox, QLabel, QSpinBox, QAbstractSpinBox, QComboBox, QMessageBox, QToolBar, QStatusBar, QLineEdit, \
    QRadioButton



class Supprimer_devise_Windows(QWidget):
    def __init__(self):
        super().__init__()
        #base de donnée/ titre_icon
        c=sqlite3.connect("DB.sq3")
        cu=c.cursor()
        self.setWindowTitle("Supprimer devise")
        self.setWindowIcon(QtGui.QIcon("image/gear_second.jpg"))

        #layout
        layout=QGridLayout()
        #création de Widget
        self.Label_paires=QLabel('Paire à supprimer: ')
        self.paires=QComboBox()
        self.paires.addItem("Selectionner paire")
        cu.execute("SELECT paire FROM Valeur_pip")
        liste_items = []
        p = cu.fetchone()
        while p is not None:
            liste_items.append(p[0])
            p = cu.fetchone()
        c.close()
        self.paires.addItems(liste_items)

        self.btn_delete=QPushButton('Supprimer paire')
        self.btn_delete.setStyleSheet("""background-color: black;
            color:white;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px""")

        self.Confirmation_suppression=QLabel("")
        #connexion de widget
        self.btn_delete.clicked.connect(self.delete_paire)

        #ajout dans layout widget

        layout.addWidget(self.Label_paires,0,0)
        layout.addWidget(self.paires,0,1)
        layout.addWidget(self.btn_delete,1,0,1,2)
        layout.addWidget(self.Confirmation_suppression,2,0,1,2)
        self.setLayout(layout)
        #fonction pour supprimer

    def delete_paire(self):
        paire = self.paires.currentText()
        if paire!="Selectionner paire":
            c=sqlite3.connect("DB.sq3")
            cu=c.cursor()
            cu.execute("DELETE FROM Valeur_pip WHERE paire=?",[paire])

            c.commit()
            c.close()
            index_item=self.paires.currentIndex()
            self.Confirmation_suppression.setText(f"SUPPRESSION OK: la paire {paire} à bien été supprimé")
            self.paires.removeItem(index_item)
            self.paires.setCurrentIndex(0)
        else:
            self.Confirmation_suppression.setText("ERROR: Veuillez selectionner une paire")
