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


class Modifier_paramètre_default_Window(QWidget):
    def __init__(self):
        super().__init__()


        #titre_icon
        self.setWindowTitle("Modifier paramètre par default")
        self.setWindowIcon(QtGui.QIcon("image/gear_second.jpg"))

        #valeur actuelle/base de données
        c=sqlite3.connect("DB.sq3")
        cu=c.cursor()

        cu.execute("SELECT value FROM parametre_default WHERE type='commission'")
        value_commission = cu.fetchone()[0]
        cu.execute("SELECT value FROM parametre_default WHERE type='account'")
        value_account =cu.fetchone()[0]
        cu.execute("SELECT risque_pourcentage FROM DD WHERE pallier=0")
        value_risque = cu.fetchone()[0]
        cu.execute("SELECT value FROM parametre_default WHERE type='paire'")
        value_paire = cu.fetchone()[0]
        cu.execute("SELECT value FROM parametre_default WHERE type='nombre de partiel'")
        value_partiel = cu.fetchone()[0]
        cu.execute("SELECT value FROM parametre_default WHERE type='Stop Loss'")
        value_SL = cu.fetchone()[0]
        cu.execute("SELECT value FROM parametre_default WHERE type='Entree'")
        value_Entrée =cu.fetchone()[0]
        cu.execute("SELECT value FROM parametre_default WHERE type='metatrader'")
        value_metatrader=cu.fetchone()[0]

        cu.execute("SELECT paire FROM Valeur_pip")
        liste_items = []
        p = cu.fetchone()
        while p is not None:
            liste_items.append(p[0])
            p = cu.fetchone()
        c.close()

        #layout
        layout=QGridLayout()
        #widgets pour commission
        self.Label_DrawDown_Entrée=QLabel(f"DRAWDOWN")
        self.Label_Commissions=QLabel("Commission: ")
        self.Commissions=QDoubleSpinBox()
        self.Commissions.setDecimals(2)
        self.Commissions.setValue(value_commission)

        self.btn_commission=QPushButton("Modifier Commission")
        self.btn_commission.setStyleSheet("""background-color: black;
            color:white;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px""")
        self.Confirmation=QLabel("Veuillez rentrer la commission par défault")

        #widget pour risque
        self.Label_risque=QLabel("Risque:")
        self.Risque=QDoubleSpinBox()

        self.Risque.setDecimals(2)
        self.Risque.setValue(value_risque)
        self.btn_risque=QPushButton('Modifier Risque')
        self.btn_risque.setStyleSheet("""background-color: black;
            color:white;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px""")

        self.confirmer_risque=QLabel("Veuillez modifier le risque par default")

        #widget pour account
        self.Label_account=QLabel("Account:")
        self.account=QDoubleSpinBox()
        self.account.setMaximum(100000000)
        self.account.setDecimals(2)
        self.account.setValue(value_account)
        self.btn_account=QPushButton('Modifier Account')
        self.btn_account.setStyleSheet("""background-color: black;
            color:white;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px""")

        self.confirmer_account=QLabel('Veuiller modifier le compte par default.')

        #widget pour paire

        self.Label_paire = QLabel("Paire:")
        self.paire = QComboBox()
        self.paire.addItems(liste_items)
        self.paire.setCurrentText(value_paire)
        self.btn_paire = QPushButton('Modifier Paire')
        self.btn_paire.setStyleSheet("""background-color: black;
                    color:white;
                    border-style: outset;
                    border-width: 2px;
                    border-radius: 10px;
                    border-color: beige;
                    font: bold 14px;
                    min-width: 10em;
                    padding: 6px""")

        self.confirmer_paire = QLabel('Veuiller modifier la paire par default.')



        # widget pour partiel

        self.Label_partiel = QLabel("Nombre de partiel:")
        self.partiel = QSpinBox()
        self.partiel.setValue(value_partiel)
        self.btn_partiel = QPushButton('Modifier Nb Partiel')
        self.btn_partiel.setStyleSheet("""background-color: black;
                         color:white;
                         border-style: outset;
                         border-width: 2px;
                         border-radius: 10px;
                         border-color: beige;
                         font: bold 14px;
                         min-width: 10em;
                         padding: 6px""")

        self.confirmer_partiel = QLabel('Veuiller modifier le nombre de partiel par default')

        #widget pour SL

        self.Label_SL = QLabel("Stop Loss: ")
        self.SL = QDoubleSpinBox()
        self.SL.setValue(value_SL)
        self.btn_SL = QPushButton('Modifier Stop loss')
        self.btn_SL.setStyleSheet("""background-color: black;
                                color:white;
                                border-style: outset;
                                border-width: 2px;
                                border-radius: 10px;
                                border-color: beige;
                                font: bold 14px;
                                min-width: 10em;
                                padding: 6px""")

        self.confirmer_SL = QLabel('Veuiller modifier Stop Loss par default')

        #widget pour Entrée

        self.Label_Entrée = QLabel("Entrée : ")
        self.Entrée = QDoubleSpinBox()
        self.Entrée.setDecimals(5)
        self.Entrée.setValue(value_Entrée)
        self.btn_Entrée = QPushButton('Modifier l\'entrée')
        self.btn_Entrée.setStyleSheet("""background-color: black;
                                        color:white;
                                        border-style: outset;
                                        border-width: 2px;
                                        border-radius: 10px;
                                        border-color: beige;
                                        font: bold 14px;
                                        min-width: 10em;
                                        padding: 6px""")

        self.confirmer_Entrée = QLabel('Veuiller modifier l\' Entrée par défault')

        # widgets pour metatrader
        self.Label_metatrader = QLabel("Metatrader: ")
        self.metatrader= QComboBox()
        self.metatrader.addItems(['mt4','mt5'])
        self.metatrader.setCurrentText(value_metatrader)

        self.btn_metatrader = QPushButton("Modifier version metatrader")
        self.btn_metatrader.setStyleSheet("""background-color: black;
                   color:white;
                   border-style: outset;
                   border-width: 2px;
                   border-radius: 10px;
                   border-color: beige;
                   font: bold 14px;
                   min-width: 10em;
                   padding: 6px""")
        self.Confirmation_metatrader = QLabel("Veuillez rentrer la version de metratrader par default")

        #ajout widget dans layout
        #ajout widget pour commission
        layout.addWidget(self.Label_Commissions,0,0)
        layout.addWidget(self.Commissions,0,1)

        layout.addWidget(self.btn_commission,0,2)
        layout.addWidget(self.Confirmation,0,3)

        #ajout widget pour risque
        layout.addWidget(self.Label_risque,1,0)
        layout.addWidget(self.Risque,1,1)
        layout.addWidget(self.btn_risque,1,2)
        layout.addWidget(self.confirmer_risque,1,3)

        #ajout widget pour account
        layout.addWidget(self.Label_account,2,0)
        layout.addWidget(self.account,2,1)
        layout.addWidget(self.btn_account,2,2)
        layout.addWidget(self.confirmer_account,2,3)

        #ajout widget pour paire par default
        layout.addWidget(self.Label_paire,3,0)
        layout.addWidget(self.paire,3,1)
        layout.addWidget(self.btn_paire,3,2)
        layout.addWidget(self.confirmer_paire,3,3)

        #ajout pour le nb de partiel
        layout.addWidget(self.Label_partiel,4,0)
        layout.addWidget(self.partiel,4,1)
        layout.addWidget(self.btn_partiel,4,2)
        layout.addWidget(self.confirmer_partiel,4,3)


        #add pour SL
        layout.addWidget(self.Label_SL,5,0)
        layout.addWidget(self.SL,5,1)
        layout.addWidget(self.btn_SL,5,2)
        layout.addWidget(self.confirmer_SL,5,3)

        #addpour Entrée
        layout.addWidget(self.Label_Entrée,6,0)
        layout.addWidget(self.Entrée,6,1)
        layout.addWidget(self.btn_Entrée,6,2)
        layout.addWidget(self.confirmer_Entrée,6,3)
        # add metatrader

        layout.addWidget(self.Label_metatrader,7,0)
        layout.addWidget(self.metatrader,7,1)
        layout.addWidget(self.btn_metatrader,7,2)
        layout.addWidget(self.Confirmation_metatrader,7,3)
        self.setLayout(layout)

        #signaux
        self.btn_commission.clicked.connect(self.modifier_commission)
        self.btn_risque.clicked.connect(self.modifier_risque,)
        self.btn_account.clicked.connect(self.modifier_account)
        self.btn_paire.clicked.connect(self.modifier_paire)
        self.btn_partiel.clicked.connect(self.modifier_partiel)
        self.btn_Entrée.clicked.connect(self.modifier_Entrée)
        self.btn_SL.clicked.connect(self.modifier_SL)
        self.btn_metatrader.clicked.connect(self.modifier_metatrader)


    def modifier_commission(self):
        c=sqlite3.connect("DB.sq3")
        cu=c.cursor()
        comm=self.Commissions.value()
        cu.execute("UPDATE parametre_default SET value=? WHERE type='commission'",[comm])
        c.commit()
        c.close()
        self.Confirmation.setText(f"La commission par default a bien été modifié, sa valeur est {comm}")

    def modifier_risque(self):
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        risque=self.Risque.value()
        cu.execute("UPDATE DD SET risque_pourcentage=? WHERE pallier=0",[risque])
        c.close()
        self.confirmer_risque.setText(f"La commission par default a bien été modifié, sa valeur est {risque}")

    def modifier_account(self):
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        account = self.account.value()
        cu.execute("UPDATE parametre_default SET value=? WHERE type='account'",[account])
        self.confirmer_account.setText(f"La commission par default a bien été modifié, sa valeur est {account}")

    def modifier_paire(self):
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        paire = self.paire.currentText()
        cu.execute("UPDATE parametre_default SET value=? WHERE type='paire'",[paire])
        self.confirmer_paire.setText(f"La nouvelle paire par default est: {paire}")

    def modifier_partiel(self):
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        partiel = self.partiel.value()
        cu.execute("UPDATE parametre_default SET value=? WHERE type='nombre de partiel'",[partiel])
        self.confirmer_partiel.setText(f"Le nombre de partiel par default  est: {partiel}")

    def modifier_SL(self):
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        SL = self.SL.value()
        cu.execute("UPDATE parametre_default SET value=? WHERE type='Stop Loss'",[SL])
        self.confirmer_Entrée.setText(f"Le SL par default  est: {SL}")

    def modifier_Entrée(self):
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        Entrée = self.Entrée.value()
        cu.execute(f"UPDATE parametre_default SET value=? WHERE type='Entree'",[Entrée])
        self.confirmer_Entrée.setText(f"L'entrée par default  est: {Entrée}")

    def modifier_metatrader(self):
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        metatrader_version= self.metatrader.currentText()
        cu.execute("UPDATE parametre_default SET value=? WHERE type='metatrader'",[metatrader_version])
        self.Confirmation_metatrader.setText(f"La version de metatrader par default  est: {metatrader_version}")








