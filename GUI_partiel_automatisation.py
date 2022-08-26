import sys
import random

from PySide6 import QtGui
from PySide6.QtWidgets import QTabWidget, QPushButton, QWidget, QGridLayout, QVBoxLayout, QApplication, QMainWindow, \
    QDoubleSpinBox, QLabel, QSpinBox, QAbstractSpinBox, QComboBox

import rentrer_position_partiel
from rentrer_position_partiel import execution_direct, execution_différé
import sys






class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('image/gear_second.jpg'))
        self.setWindowTitle("Gear Secondo!")
        # création du widget des onglets

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.South)
        # création des différents onglets
        W_entrée_directe = QWidget()
        W_entrée_différée = QWidget()
        # création de layout qu'on va venir ajouter au widget à la fin
        layout_entrée_directe = QGridLayout()
        layout_entrée_différée = QGridLayout()

        # création des différents widgets de l'onglet entrée_direct
        Label_lot_direct=QLabel("Volume :")
        self.Lot_direct= QDoubleSpinBox()
        self.Lot_direct.setDecimals(2)

        Label_stop_loss_direct = QLabel("Stop Loss:")
        self.Stop_loss_direct = QDoubleSpinBox()
        self.Stop_loss_direct.setDecimals(5)

        Label_take_profit_direct = QLabel("Take profit:")
        self.Take_profit_direct = QDoubleSpinBox()
        self.Take_profit_direct.setDecimals(5)

        Label_nombre_partiel_direct = QLabel("Nombre de partiel: ")
        self.Nombre_partiel_direct = QSpinBox()
        self.Nombre_partiel_direct.setMinimum(1)

        self.Button_acheteur = QPushButton('Acheter')
        self.Button_vendeur = QPushButton('Vendre')

        # création des différents widgets de l'onglet entrée différée
        Label_lot_différé=QLabel('Volume :')
        self.lot_différé=QDoubleSpinBox()
        self.lot_différé.setDecimals(2)

        Label_prix_entrée = QLabel("Entrée:")
        self.prix_entrée = QDoubleSpinBox()
        self.prix_entrée.setDecimals(5)

        Label_stop_loss_différée = QLabel("Stop Loss:")
        self.Stop_loss_différée = QDoubleSpinBox()
        self.Stop_loss_différée.setDecimals(5)

        Label_profit_différée = QLabel("Take Profit:")
        self.Take_profit_différée = QDoubleSpinBox()
        self.Take_profit_différée.setDecimals(5)

        Label_nombre_partiel_différée = QLabel("Nombre de partiel:")
        self.Nombre_partiel_différée = QSpinBox()
        self.Nombre_partiel_différée.setMinimum(1)

        self.Button_validé_position = QPushButton("Go!")

        Label_type_ordre=QLabel("Type d'ordre :")
        self.Liste_ordres=QComboBox()
        self.Liste_ordres.addItems(["Buy Limit","Sell Limit","Buy Stop","Sell Stop"])

        #Ajout des signaux pour l'onglet ordre instantanée
        self.Button_acheteur.clicked.connect(self.Acheter_instantanée)
        self.Button_vendeur.clicked.connect(self.Vendre_instantanée)

        self.Take_profit_direct.valueChanged.connect(self.Change_TP_différé)
        self.Stop_loss_direct.valueChanged.connect(self.Change_Stop_loss_différé)
        self.Lot_direct.valueChanged.connect(self.Change_Lot_différé)
        self.Nombre_partiel_direct.valueChanged.connect(self.Change_nombre_partiel_différé)


        #ajout signaux pour l'onglet ordre différée
        self.Button_validé_position.clicked.connect(self.Position_différée)
        self.Take_profit_différée.valueChanged.connect(self.Change_TP_direct)
        self.Stop_loss_différée.valueChanged.connect(self.Change_Stop_loss_direct)
        self.lot_différé.valueChanged.connect(self.Change_Lot_direct)
        self.Nombre_partiel_différée.valueChanged.connect(self.Change_nombre_partiel_direct)





        # ajout des widgets dans le layout qu'on va ajouter au widget:layout_entrée_directe
        layout_entrée_directe.addWidget(Label_stop_loss_direct)
        layout_entrée_directe.addWidget(self.Stop_loss_direct)

        layout_entrée_directe.addWidget(Label_take_profit_direct)
        layout_entrée_directe.addWidget(self.Take_profit_direct)

        layout_entrée_directe.addWidget(Label_lot_direct)
        layout_entrée_directe.addWidget(self.Lot_direct)

        layout_entrée_directe.addWidget(Label_nombre_partiel_direct)
        layout_entrée_directe.addWidget(self.Nombre_partiel_direct)

        layout_entrée_directe.addWidget(self.Button_acheteur)
        layout_entrée_directe.addWidget(self.Button_vendeur)

        # ajout des widget dans le layout qu'on va ajouter au widget:layout_entrée_différée
        layout_entrée_différée.addWidget(Label_prix_entrée)
        layout_entrée_différée.addWidget(self.prix_entrée)

        layout_entrée_différée.addWidget(Label_stop_loss_différée)
        layout_entrée_différée.addWidget(self.Stop_loss_différée)

        layout_entrée_différée.addWidget(Label_profit_différée)
        layout_entrée_différée.addWidget(self.Take_profit_différée)

        layout_entrée_différée.addWidget(Label_lot_différé)
        layout_entrée_différée.addWidget(self.lot_différé)

        layout_entrée_différée.addWidget(Label_type_ordre)
        layout_entrée_différée.addWidget(self.Liste_ordres)

        layout_entrée_différée.addWidget(Label_nombre_partiel_différée)
        layout_entrée_différée.addWidget(self.Nombre_partiel_différée)

        layout_entrée_différée.addWidget(self.Button_validé_position)







        # ajout des layout dans le set de layout du widget
        W_entrée_directe.setLayout(layout_entrée_directe)
        W_entrée_différée.setLayout(layout_entrée_différée)

        # ajout des widgets qui vont servir d'onglet dans tabs
        tabs.addTab(W_entrée_directe, 'Ordre direct')
        tabs.addTab(W_entrée_différée, 'Ordre différé')
        self.setCentralWidget(tabs)

     #fonction pour signaux buttons

    def Acheter_instantanée(self):
        Take_profit=self.Take_profit_direct.value()
        Stop_Loss=self.Stop_loss_direct.value()
        Nombre_partielle=self.Nombre_partiel_direct.value()
        Lots=self.Lot_direct.value()
        type_ordre="achat"
        rentrer_postition_partiel.execution_direct(lot=float(Lots),SL=float(Stop_Loss),nb_partiel=int(Nombre_partielle),vente_ou_achat=type_ordre,TP=float(Take_profit))

    def Vendre_instantanée(self):

        Take_profit=self.Take_profit_direct.value()
        Stop_Loss=self.Stop_loss_direct.value()
        Nombre_partiel=self.Nombre_partiel_direct.value()
        Lots=self.Lot_direct.value()
        type_ordre="vente"

        rentrer_postition_partiel.execution_direct(lot=float(Lots), SL=float(Stop_Loss), nb_partiel=int(Nombre_partiel),
                                                   vente_ou_achat=type_ordre, TP=float(Take_profit))

    def Position_différée(self):
        Entrée=self.prix_entrée.value()
        Take_Profit=self.Take_profit_différée.value()
        Stop_Loss=self.Stop_loss_différée.value()
        Nombre_partiel=self.Nombre_partiel_direct.value()
        Lots=self.lot_différé.value()
        type_ordre=self.Liste_ordres.currentText()
        rentrer_postition_partiel.execution_différé(lot=float(Lots),entrée=float(Entrée),nb_partiel=int(Nombre_partiel),
                                                    SL=float(Stop_Loss),TP=float(Take_Profit),type_ordre=type_ordre)


    #fonctions signaux coordination champs entrée/différé

    #direct
    def Change_TP_direct(self):
        current= self.Take_profit_différée.value()
        self.Take_profit_direct.setValue(current)

    def Change_Lot_direct(self):
        current = self.lot_différé.value()
        self.Lot_direct.setValue(current)

    def Change_Stop_loss_direct(self):
        current = self.Stop_loss_différée.value()
        self.Stop_loss_direct.setValue(current)

    def Change_nombre_partiel_direct(self):
        current=self.Nombre_partiel_différée.value()
        self.Nombre_partiel_direct.setValue(current)

    #différé
    def Change_TP_différé(self):
        current = self.Take_profit_direct.value()
        self.Take_profit_différée.setValue(current)

    def Change_Stop_loss_différé(self):
        current = self.Stop_loss_direct.value()
        self.Stop_loss_différée.setValue(current)

    def Change_Lot_différé(self):
        current = self.Lot_direct.value()
        self.lot_différé.setValue(current)

    def Change_nombre_partiel_différé(self):
        current=self.Nombre_partiel_direct.value()
        self.Nombre_partiel_différée.setValue(current)




app = QApplication(sys.argv)
window = MainWindow()
window.resize(400, 250)
window.show()
app.exec_()
