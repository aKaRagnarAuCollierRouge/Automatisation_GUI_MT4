import sqlite3
import sys
import random
from tinydb import TinyDB, where, Query
from PySide6 import QtGui
from PySide6.QtCore import QSize, QPoint
from PySide6.QtGui import QAction, QIcon,QPixmap
from PySide6.QtWidgets import QTabWidget, QPushButton, QWidget, QGridLayout, QVBoxLayout, QApplication, QMainWindow, \
    QDoubleSpinBox, QLabel, QSpinBox, QAbstractSpinBox, QComboBox, QMessageBox, QToolBar, QStatusBar, QLineEdit, \
    QRadioButton, QHBoxLayout


class ManagerTradeWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Parametre Manager Trade")
        self.setWindowIcon(QtGui.QIcon("image/gear_second.jpg"))

        self.setStyleSheet("""QPushButton{background-color: black;color:white;border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px}""")

        layout = QHBoxLayout()
        #valeur default base de donnée
        c=sqlite3.connect("DB.sq3")
        cu=c.cursor()

        cu.execute("SELECT value FROM parametre_default WHERE type='ordre manager'")
        value_ordre_default=cu.fetchone()[0]
        c.close()

        #creation widget

        Label_combobox_ordre_default=QLabel("Management par default:")
        self.choix_manager_ordre_default=QComboBox()
        self.choix_manager_ordre_default.addItems(["sl-tp","fermeture"])
        self.choix_manager_ordre_default.setCurrentText(value_ordre_default)

        self.btn_modifier_parametre=QPushButton("Modifier ordre default")
        self.label_changement_effectué=QLabel('')
        #ajout des widget au layout
        layout.addWidget(Label_combobox_ordre_default)
        layout.addWidget(self.choix_manager_ordre_default)
        layout.addWidget(self.btn_modifier_parametre)
        layout.addWidget(self.label_changement_effectué)
        self.setLayout(layout)
        #connexion widget avec methode
        self.btn_modifier_parametre.clicked.connect(self.modifier_parametre_management)
    def modifier_parametre_management(self):
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        value_combobox_ordre_default=self.choix_manager_ordre_default.currentText()
        cu.execute(f"UPDATE parametre_default SET value=? WHERE type='ordre manager'",[value_combobox_ordre_default])
        c.commit()
        c.close()
        self.label_changement_effectué.setText("Les changements ont bien été effectués")

