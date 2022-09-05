import sys
import random
from tinydb import TinyDB, where, Query
from PySide6 import QtGui
from PySide6.QtCore import QSize, QPoint
from PySide6.QtGui import QAction, QIcon,QPixmap
from PySide6.QtWidgets import QTabWidget, QPushButton, QWidget, QGridLayout, QVBoxLayout, QApplication, QMainWindow, \
    QDoubleSpinBox, QLabel, QSpinBox, QAbstractSpinBox, QComboBox, QMessageBox, QToolBar, QStatusBar, QLineEdit

import rentrer_position_partiel
from rentrer_position_partiel import execution_direct, execution_différé
import sys


#------------------------------FENETRES DE LA BARRE D'OUTILS----------------------------

#fenetre pour changer la valeur des pips
class ChangerPipsWindow(QWidget):

    def __init__(self):
        super().__init__()

        db=TinyDB('Paires.json',indent=4)
        table_paire=db.table("Valeur pip")
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

        layout = QVBoxLayout()
        # création des widgets
        self.Label_Paires=QLabel("Paire: ")
        self.Paires=QComboBox()
        self.Paires.addItem("Selectionner paire")
        paires=[i['paire'] for i in table_paire]
        self.Paires.addItems(paires)

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


        self.Confirmation_Modification=QLabel('Veuillez rentrez la paire, la valeur du pips et appuyer sur le bouton.')
        # création des différents signaux pour modifier pip
        self.Modifier_pip_btn.clicked.connect(self.fct_modifier_pips)
        self.Paires.currentTextChanged.connect(self.fct_combo_box_change)

        #ajout dans le layout
        layout.addWidget(self.Label_Paires)
        layout.addWidget(self.Paires)

        layout.addWidget(self.Label_modifier_pip)
        layout.addWidget(self.modifier_pip)

        layout.addWidget(self.Modifier_pip_btn)
        layout.addWidget(self.Confirmation_Modification)
        self.setLayout(layout)


    #fonction pour modifier pip quand on appuie sur modifier
    def fct_modifier_pips(self):
        db=TinyDB('Paires.json',indent=4)
        table_paires=db.table('Valeur pip')
        paire=self.Paires.currentText()
        pip=self.modifier_pip.value()
        if pip==0 or paire=="Selectionner paire":
            if pip==0:
                self.Confirmation_Modification.setText("ERREUR: la valeur du pip ne peut pas être égale à 0. ")
            elif paire=="Selectionner paire":
                self.Confirmation_Modification.setText("ERREUR:  Veuillez selectionner une paire.")
        else:

            table_paires.update({"valeur_pip":pip},where('paire')==paire)
            self.Confirmation_Modification.setText(f'La valeur du pips a été modifier sur {paire}: {str(pip)}')

            self.modifier_pip.setValue(0.0000)
            self.Paires.setCurrentIndex(0)

    def fct_combo_box_change(self):
        db = TinyDB('Paires.json', indent=4)
        Q=Query()
        table_paires = db.table('Valeur pip')
        paire = self.Paires.currentText()
        if paire!="Selectionner paire":
            value_pips=table_paires.search(Q.paire==paire)[0]['valeur_pip']
            self.modifier_pip.setValue(value_pips)





class AjouterPaireWindow(QWidget):
    def __init__(self):
        super().__init__()
        #base de donnée
        db=TinyDB('Paires.json',indent=4)
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
        db=TinyDB("Paires.json",indent=4)
        table=db.table("Valeur pip")
        paire=self.paire_devise.text()
        pip=self.valeur_du_pips.value()
        table.insert({"paire":paire,"valeur_pip":pip})
        self.confirmation_ajouter.setText(f'La paire {paire} à bien été ajouté , ca valeur de pip est:{str(pip)}')
        self.paire_devise.setText("")
        self.valeur_du_pips.setValue(0.00000)


class Supprimer_devise_Windows(QWidget):
    def __init__(self):
        super().__init__()
        #base de donnée/ titre_icon
        db=TinyDB('Paires.json',indent=4)
        table=db.table('Valeur pip')
        self.setWindowTitle("Supprimer devise")
        self.setWindowIcon(QtGui.QIcon("image/gear_second.jpg"))

        #layout
        layout=QVBoxLayout()
        #création de Widget
        self.Label_paires=QLabel('Paires: ')
        self.paires=QComboBox()
        self.paires.addItem("Selectionner paire")
        paires=[i['paire'] for i in table]
        self.paires.addItems(paires)

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

        self.Confirmation_suppression=QLabel("Veuillez entrée la paire puis appuyer seur le bouton supprimer pour"
                                           "supprimer une paire")
        #connexion de widget
        self.btn_delete.clicked.connect(self.delete_paire)

        #ajout dans layout widget
        layout.addWidget(self.Label_paires)
        layout.addWidget(self.paires)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.Confirmation_suppression)
        self.setLayout(layout)

    #fonction pour supprimer

    def delete_paire(self):
        paire = self.paires.currentText()
        if paire!="Selectionner paire":
            db=TinyDB('Paires.json',indent=4)
            table=db.table('Valeur pip')

            table.remove(where('paire') == paire)
            index_item=self.paires.currentIndex()
            self.Confirmation_suppression.setText(f"SUPPRESSION OK: la paire {paire} à bien été supprimé")
            self.paires.removeItem(index_item)
            self.paires.setCurrentIndex(0)
        else:
            self.Confirmation_suppression.setText("ERROR: Veuillez selectionner une paire")


class Modifier_paramètre_default_Window(QWidget):
    def __init__(self):
        super().__init__()


        #db/titre_icon
        db=TinyDB('Paires.json',indent=4)
        tb=db.table('parametre_default')
        self.setWindowTitle("Modifier paramètre par default")
        self.setWindowIcon(QtGui.QIcon("image/gear_second.jpg"))

        #valeur actuelle
        Q=Query()

        value_commission = tb.search(Q.type == "commission")[0]['value']
        value_account = tb.search(Q.type == "account")[0]['value']
        value_risque = tb.search(Q.type == "risque")[0]['value']
        value_paire = tb.search(Q.type == "paire")[0]['value']
        value_partiel = tb.search(Q.type == "nombre de partiel")[0]['value']
        value_SL = tb.search(Q.type == "Stop Loss")[0]['value']
        value_Entrée = tb.search(Q.type == "Entree")[0]['value']




        #layout
        layout=QGridLayout()
        #widgets pour commission
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
        tb_paire=db.table("Valeur pip")
        l_paires=[i['paire'] for i in tb_paire]
        self.paire.addItems(l_paires)
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


        #ajout widget dans layout
        #ajout widget pour commission
        layout.addWidget(self.Label_Commissions,0,0)
        layout.addWidget(self.Commissions,0,1)

        layout.addWidget(self.btn_commission,0,2)
        layout.addWidget(self.Confirmation,0,3)

        #ajout widget pour risque
        layout.addWidget(self.Label_risque)
        layout.addWidget(self.Risque)
        layout.addWidget(self.btn_risque)
        layout.addWidget(self.confirmer_risque)

        #ajout widget pour account
        layout.addWidget(self.Label_account)
        layout.addWidget(self.account)
        layout.addWidget(self.btn_account)
        layout.addWidget(self.confirmer_account)

        #ajout widget pour paire par default
        layout.addWidget(self.Label_paire)
        layout.addWidget(self.paire)
        layout.addWidget(self.btn_paire)
        layout.addWidget(self.confirmer_paire)

        #ajout pour le nb de partiel
        layout.addWidget(self.Label_partiel)
        layout.addWidget(self.partiel)
        layout.addWidget(self.btn_partiel)
        layout.addWidget(self.confirmer_partiel)


        #add pour SL
        layout.addWidget(self.Label_SL)
        layout.addWidget(self.SL)
        layout.addWidget(self.btn_SL)
        layout.addWidget(self.confirmer_SL)

        #addpour Entrée
        layout.addWidget(self.Label_Entrée)
        layout.addWidget(self.Entrée)
        layout.addWidget(self.btn_Entrée)
        layout.addWidget(self.confirmer_Entrée)


        self.setLayout(layout)

        #signaux
        self.btn_commission.clicked.connect(self.modifier_commission)
        self.btn_risque.clicked.connect(self.modifier_risque)
        self.btn_account.clicked.connect(self.modifier_account)
        self.btn_paire.clicked.connect(self.modifier_paire)
        self.btn_partiel.clicked.connect(self.modifier_partiel)
        self.btn_Entrée.clicked.connect(self.modifier_Entrée)
        self.btn_SL.clicked.connect(self.modifier_SL)


    def modifier_commission(self):
        db=TinyDB('Paires.json',indent=4)
        tb=db.table("parametre_default")
        comm=self.Commissions.value()

        tb.update({"value":comm},where("type")=="commission")
        self.Confirmation.setText(f"La commission par default a bien été modifié, sa valeur est {comm}")

    def modifier_risque(self):
        db=TinyDB('Paires.json',indent=4)
        tb=db.table("parametre_default")
        risque=self.Risque.value()
        tb.update({"value":risque},where("type")=="risque")
        self.confirmer_risque.setText(f"La commission par default a bien été modifié, sa valeur est {risque}")

    def modifier_account(self):
        db = TinyDB('Paires.json', indent=4)
        tb = db.table("parametre_default")
        account = self.account.value()
        tb.update({"value": account},where("type")=="account")
        self.confirmer_account.setText(f"La commission par default a bien été modifié, sa valeur est {account}")

    def modifier_paire(self):
        db = TinyDB('Paires.json', indent=4)
        tb = db.table("parametre_default")
        paire = self.paire.currentText()
        tb.update({"value": paire}, where("type") == "paire")
        self.confirmer_paire.setText(f"La nouvelle paire par default est: {paire}")

    def modifier_partiel(self):
        db = TinyDB('Paires.json', indent=4)
        tb = db.table("parametre_default")
        partiel = self.partiel.value()
        tb.update({"value":partiel}, where("type") == "nombre de partiel")
        self.confirmer_partiel.setText(f"Le nombre de partiel par default  est: {partiel}")

    def modifier_SL(self):
        db = TinyDB('Paires.json', indent=4)
        tb = db.table("parametre_default")
        SL = self.SL.value()
        tb.update({"value": SL}, where("type") == "Stop Loss")
        self.confirmer_Entrée.setText(f"Le SL par default  est: {SL}")

    def modifier_Entrée(self):
        db = TinyDB('Paires.json', indent=4)
        tb = db.table("parametre_default")
        Entrée = self.Entrée.value()
        tb.update({"value": Entrée}, where("type") == "Entree")
        self.confirmer_Entrée.setText(f"L'entrée par default  est: {Entrée}")









        #-------------------------------------------------FIN-------------------------------------


#--------------------------------------------FENETRE PRINCIPALE-------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #base de données
        db=TinyDB('Paires.json', indent=4)
        #titre/icone/custum
        self.setWindowIcon(QtGui.QIcon('image/gear_second.jpg'))
        self.setWindowTitle("Gear Secondo!")
        self.setMaximumWidth(200)


        self.setStyleSheet("""QPushButton{background-color: black;
    color:white;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: beige;
    font: bold 14px;
    min-width: 10em;
    padding: 6px}
QLabel{color:green; font-widght}

 """)
        # création du widget des onglets

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.South)
        # création des différents onglets
        W_entrée_directe = QWidget()
        W_entrée_différée = QWidget()
        W_calcul_lot=QWidget()
        # création de layout qu'on va venir ajouter au widget à la fin
        layout_entrée_directe = QGridLayout()
        layout_entrée_différée = QGridLayout()
        layout_calcul_lot=QGridLayout()

        #valeur par default pour l'ajouter dans différents widget
        tb_default = db.table("parametre_default")
        Q = Query()

        value_partiel = tb_default.search(Q.type == "nombre de partiel")[0]['value']
        value_entrée=tb_default.search(Q.type == "Entree")[0]['value']
        value_SL=tb_default.search(Q.type == "Stop Loss")[0]['value']

        value_commission = tb_default.search(Q.type == "commission")[0]['value']
        value_account = tb_default.search(Q.type == "account")[0]['value']
        value_risque = tb_default.search(Q.type == "risque")[0]['value']
        value_paire = tb_default.search(Q.type == "paire")[0]['value']


        # création des différents widgets de l'onglet entrée_direct
        Label_lot_direct=QLabel("Volume(obligatoire): ")
        Label_lot_direct.setStyleSheet("""color:red""")
        self.Lot_direct= QDoubleSpinBox()
        self.Lot_direct.setDecimals(2)

        Label_stop_loss_direct = QLabel("Stop Loss: ")
        self.Stop_loss_direct = QDoubleSpinBox()
        self.Stop_loss_direct.setValue(value_SL)
        self.Stop_loss_direct.setDecimals(5)

        Label_take_profit_direct = QLabel("Take profit: ")
        self.Take_profit_direct = QDoubleSpinBox()
        self.Take_profit_direct.setDecimals(5)

        Label_nombre_partiel_direct = QLabel("Nombre de partiel: ")
        self.Nombre_partiel_direct = QSpinBox()
        self.Nombre_partiel_direct.setMinimum(1)
        self.Nombre_partiel_direct.setValue(value_partiel)

        self.Button_acheteur = QPushButton('Acheter')
        self.Button_acheteur.setStyleSheet("""background-color: green;
    
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: beige;
    font: bold 14px;
    min-width: 10em;
    padding: 6px"""
)
        self.Button_vendeur = QPushButton('Vendre')
        self.Button_vendeur.setStyleSheet("""background-color: red;
    
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: beige;
    font: bold 14px;
    min-width: 10em;
    padding: 6px"""
)



        # création des différents widgets de l'onglet entrée différée



        Label_lot_différé=QLabel('Volume(obligatoire) :')
        Label_lot_direct.setStyleSheet("""color:red;font-weight:bold""")
        self.lot_différé=QDoubleSpinBox()
        self.lot_différé.setDecimals(2)

        Label_prix_entrée = QLabel("Entrée(obligatoire):")
        Label_prix_entrée.setStyleSheet("""color:red;font-weight:bold""")
        self.prix_entrée = QDoubleSpinBox()
        self.prix_entrée.setValue(value_entrée)
        self.prix_entrée.setDecimals(5)

        Label_stop_loss_différée = QLabel("Stop Loss:")
        self.Stop_loss_différée = QDoubleSpinBox()
        self.Stop_loss_différée.setValue(value_SL)
        self.Stop_loss_différée.setDecimals(5)

        Label_profit_différée = QLabel("Take Profit:")
        self.Take_profit_différée = QDoubleSpinBox()
        self.Take_profit_différée.setDecimals(5)

        Label_nombre_partiel_différée = QLabel("Nombre de partiel:")
        self.Nombre_partiel_différée = QSpinBox()
        self.Nombre_partiel_différée.setMinimum(1)
        self.Nombre_partiel_différée.setValue(value_partiel)

        self.Button_validé_position = QPushButton("Go!")


        Label_type_ordre=QLabel("Type d'ordre(obligatoire) :")
        Label_type_ordre.setStyleSheet("""color:red;font-weight:bold""")
        self.Liste_ordres=QComboBox()
        self.Liste_ordres.addItems(["Buy Limit","Sell Limit","Buy Stop","Sell Stop"])

        #Création des différents widgets de l'onglet "Calcul lot"






        self.Label_account=QLabel("Account(obligatoire): ")
        self.Label_account.setStyleSheet("""color:red;font-weight:bold""")
        self.account_montant=QDoubleSpinBox()
        self.account_montant.setMaximum(100000000)
        self.account_montant.setDecimals(2)
        self.account_montant.setValue(value_account)
#--------------
        self.Label_paires=QLabel("Paire de devise(facultatif) :")
        self.combobox_paires=QComboBox()
        table_paire=db.table('Valeur pip')
        liste_items=[i['paire'] for i in table_paire]
        self.combobox_paires.addItems(liste_items)
        self.combobox_paires.setCurrentText(value_paire)

        self.Label_valeur_pips=QLabel("Valeur du pip(obligatoire) :")
        self.Label_valeur_pips.setStyleSheet("""color:red;font-weight:bold""")
        self.valeur_pips=QDoubleSpinBox()
        self.valeur_pips.setDecimals(5)
        for i in table_paire:
            if i['paire']==self.combobox_paires.currentText():
                self.valeur_pips.setValue(i['valeur_pip'])
                break
#----------------


        self.Label_Commision=QLabel("Commission(facultatif):")
        self.Commision=QDoubleSpinBox()
        self.Commision.setDecimals(2)
        self.Commision.setValue(value_commission)

        self.Label_risque_pourcentage=QLabel("Risque(obligatoire): ")
        self.Label_risque_pourcentage.setStyleSheet("""color:red;font-weight:bold""")
        self.risque_pourcentage=QDoubleSpinBox()
        self.risque_pourcentage.setDecimals(2)
        self.risque_pourcentage.setValue(value_risque)

        self.Label_Entrée_calcul_lot=QLabel("Entrée(facultatif): ")
        self.Entrée_calcul_lot=QDoubleSpinBox()
        self.Entrée_calcul_lot.setValue(value_entrée)
        self.Entrée_calcul_lot.setDecimals(5)

        self.Label_Stop_loss_calcul_lot=QLabel('Stop loss(facultatif): ' )
        self.Stop_loss_calcul_lot=QDoubleSpinBox()
        self.Stop_loss_calcul_lot.setValue(value_SL)
        self.Stop_loss_calcul_lot.setDecimals(5)

        self.Label_Take_profit_calcul_lot=QLabel("Take profit(facultatif): ")
        self.Take_profit_calcul_lot=QDoubleSpinBox()
        self.Take_profit_calcul_lot.setDecimals(5)

        self.Label_taille_SL=QLabel("Taille SL en pip(obligatoire): ")
        self. Label_taille_SL.setStyleSheet("""color:red;font-weight:bold""")
        self.taille_SL=QDoubleSpinBox()
        self.taille_SL.setMaximum(30000)
        self.taille_SL.setDecimals(1)


        self.btn_calcul_lot=QPushButton("Calculer Lot")



        self.Label_Lot=QLabel("Lot: ")
        self.Lot=QDoubleSpinBox()
        self.Lot.setMaximum(100000)
        self.Lot.setDecimals(2)

        self.verification_validation_calcul=QLabel("Veuillez remplir au moins les champs obligatoires, (risque>0, \n"
                                                   "taille_SL>0,account>0")
        self.verification_validation_calcul.setStyleSheet("""color:purple""")

        #création de la barre d'outils/Menu
        #Création des actions de la barres d'outils et connexion à leur fonctions
        self.changer_valeur_des_pips=QAction("Changer valeur des pips",self)
        self.changer_valeur_des_pips.triggered.connect(self.Affichage_fenetre_changer_pips)

        self.Ajouter_paire=QAction("Ajouter paire de devise",self)
        self.Ajouter_paire.triggered.connect(self.fct_ajouter_paire)

        self.Supprimer_paire=QAction("Supprimer paires",self)
        self.Supprimer_paire.triggered.connect(self.supprimer_paire)

        self.Modifier_paramètre_default=QAction("Modifier paramètre par default",self)
        self.Modifier_paramètre_default.triggered.connect(self.fct_modifier_paramètre_default)



        self.Actualiser=QAction('Actualiser',self)
        self.Actualiser.triggered.connect(self.fct_Actualiser)
        # création menu et toolbar
        self.menubar = self.menuBar()
        self.toolbar = QToolBar("toolbar")
        self.addToolBar(self.toolbar)
        menu_changement_valeur_pips=self.menubar.addMenu("&paramètres")
        menu_changement_valeur_pips.addAction(self.changer_valeur_des_pips)
        menu_changement_valeur_pips.addAction(self.Ajouter_paire)
        menu_changement_valeur_pips.addAction(self.Supprimer_paire)
        menu_changement_valeur_pips.addAction(self.Modifier_paramètre_default)

        #ajout outils dans toolbar
        self.toolbar.addAction(self.Actualiser)






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


        #ajout de signaux pour l'onglet calcul de lot

        self.combobox_paires.currentTextChanged.connect(self.Change_paires_valeur_pip)
        self.btn_calcul_lot.clicked.connect(self.click_btn_calcul_lot)




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

        # ajout des widgets dans le layout qu'on va ajouter au widget:layout_calcul_lot
        layout_calcul_lot.addWidget(self.Label_risque_pourcentage)
        layout_calcul_lot.addWidget(self.risque_pourcentage)

        layout_calcul_lot.addWidget(self.Label_account)
        layout_calcul_lot.addWidget(self.account_montant)

        layout_calcul_lot.addWidget(self.Label_paires)
        layout_calcul_lot.addWidget(self.combobox_paires)

        layout_calcul_lot.addWidget(self.Label_valeur_pips)
        layout_calcul_lot.addWidget(self.valeur_pips)


        layout_calcul_lot.addWidget(self.Label_Commision)
        layout_calcul_lot.addWidget(self.Commision)

        layout_calcul_lot.addWidget(self.Label_Entrée_calcul_lot)
        layout_calcul_lot.addWidget(self.Entrée_calcul_lot)

        layout_calcul_lot.addWidget(self.Label_Stop_loss_calcul_lot)
        layout_calcul_lot.addWidget(self.Stop_loss_calcul_lot)

        layout_calcul_lot.addWidget(self.Label_Take_profit_calcul_lot)
        layout_calcul_lot.addWidget(self.Take_profit_calcul_lot)

        layout_calcul_lot.addWidget(self.Label_taille_SL)
        layout_calcul_lot.addWidget(self.taille_SL)

        layout_calcul_lot.addWidget(self.btn_calcul_lot)

        layout_calcul_lot.addWidget(self.Label_Lot)
        layout_calcul_lot.addWidget(self.Lot)

        layout_calcul_lot.addWidget((self.verification_validation_calcul))
        # ajout des layout dans le set de layout du widget
        W_entrée_directe.setLayout(layout_entrée_directe)
        W_entrée_différée.setLayout(layout_entrée_différée)
        W_calcul_lot.setLayout(layout_calcul_lot)

        # ajout des widgets qui vont servir d'onglet dans tabs
        tabs.addTab(W_entrée_directe, 'Ordre direct')
        tabs.addTab(W_entrée_différée, 'Ordre différé')
        tabs.addTab(W_calcul_lot,'Calcul lot/gestion risque')
        self.setCentralWidget(tabs)

     #fonction pour signaux buttons

    def Acheter_instantanée(self):
        if self.Lot_direct.value()==0:
            Message=QMessageBox.critical(self,'Lot error','veuillez rentrer un nombre valide de lot',buttons=
                                         QMessageBox.Ok)
        else:
            Take_profit=self.Take_profit_direct.value()
            Stop_Loss=self.Stop_loss_direct.value()
            Nombre_partielle=self.Nombre_partiel_direct.value()
            Lots=self.Lot_direct.value()
            type_ordre="achat"
            rentrer_position_partiel.execution_direct(lot=float(Lots),SL=float(Stop_Loss),nb_partiel=int(Nombre_partielle),vente_ou_achat=type_ordre,TP=float(Take_profit))

    def Vendre_instantanée(self):
        if self.Lot_direct.value()==0:
            Message=QMessageBox.critical(self,'Lot error','veuillez rentrer un nombre valide de lot',buttons=
                                         QMessageBox.Ok)


        else:
            Take_profit=self.Take_profit_direct.value()
            Stop_Loss=self.Stop_loss_direct.value()
            Nombre_partiel=self.Nombre_partiel_direct.value()
            Lots=self.Lot_direct.value()
            type_ordre="vente"

            rentrer_position_partiel.execution_direct(lot=float(Lots), SL=float(Stop_Loss), nb_partiel=int(Nombre_partiel),
                                                   vente_ou_achat=type_ordre, TP=float(Take_profit))

    def Position_différée(self):
        if self.lot_différé.value()==0:
            Message_error_lot=QMessageBox.critical(self,'Lot error','Veuillez rentrer un nombre valide de lot: nombre de lot ne peut pas être égale à 0.',buttons=
                                         QMessageBox.Ok)
        elif self.prix_entrée.value()==0:
            Message_erreur_entrée=QMessageBox.critical(self,'Entrée invalide!','Le prix d\'entré ne peut pas être égal à 0.',
                                                       buttons=QMessageBox.Ok)
        else:
            Entrée=self.prix_entrée.value()
            Take_Profit=self.Take_profit_différée.value()
            Stop_Loss=self.Stop_loss_différée.value()
            Nombre_partiel=self.Nombre_partiel_direct.value()
            Lots=self.lot_différé.value()
            type_ordre=self.Liste_ordres.currentText()
            #vérification que les entrées soient bonnes pour chaque type d'ordre.
            #Pour Buy Stop
            if type_ordre=="Buy Stop" and Stop_Loss!=0 and Stop_Loss>=Entrée-0.00001:
               message= QMessageBox.critical(self,'Stop Loss Invalide','Votre Stop loss est supérieur à votre entrée.',buttons=QMessageBox.Ok)
            elif type_ordre=="Buy Stop" and Take_Profit!=0 and Take_Profit<=Entrée:
               message= QMessageBox.critical(self,'Take Profit invalide',"Votre Take profit se situe en dessous du niveau d'entrée.",buttons=QMessageBox.Ok)
            #Pour Sell Stop
            elif type_ordre=="Sell Stop" and Stop_Loss!=0 and Stop_Loss<=Entrée+0.00001:
                message = QMessageBox.critical(self,'Stop Loss Invalide',"Votre Stop loss est inférieur à votre niveau d'entrée",buttons=QMessageBox.Ok)
            elif type_ordre=="Sell Stop" and Take_Profit!=0 and Take_Profit>=Entrée:
                message=QMessageBox.critical(self,"Take Profit Invalid","Votre Take profit est supérieur au niveau d'entrée",buttons=QMessageBox.Ok)
            #Pour Buy_Limit
            elif type_ordre=="Buy Limit" and Stop_Loss!=0 and Stop_Loss<=Entrée:
                message=QMessageBox.critical(self,"Stop Loss Invalid","Votre Stop loss est supérieur au niveau d'entrée",buttons=QMessageBox.Ok)
            elif type_ordre=="Buy Limit" and Take_Profit!=0 and Take_Profit>=Entrée:
                message=QMessageBox.critical(self,"Take Profit Invalid","Votre Take Profit est inférieur au niveau d'entrée",buttons=QMessageBox.Ok)
            #Pour Sell Limit
            elif type_ordre=="Sell Limit" and Stop_Loss!=0 and Stop_Loss>=Entrée:
                message=QMessageBox.critical(self,"Stop Loss Invalid","Votre Stop loss est supérieur au niveau de l'entrée",buttons=QMessageBox.Ok)
            elif type_ordre=="Sell Limit" and Take_Profit!=0 and Take_Profit<=Entrée:
                message=QMessageBox.critical(self,"Take Profit Invalid","Votre Take profit est inférieur au niveau de l'entrée",buttons=QMessageBox.Ok)
            #Validation
            else:
                Confirmation_envoie=QMessageBox.question(self,f'Confirmation',f'Entrée:{Entrée}\nLots:{Lots}\nNombre_partielle:{Nombre_partiel}\n '
                                                                       f'type d\'ordre:{type_ordre}\nSL:{Stop_Loss}\nTP:{Take_Profit}\n Appuyer sur Yes pour confirmer',
                                                     buttons=QMessageBox.Yes |QMessageBox.No)
                if Confirmation_envoie==QMessageBox.Yes:
                    rentrer_position_partiel.execution_différé(lot=float(Lots),entrée=float(Entrée),nb_partiel=int(Nombre_partiel),
                                                    SL=float(Stop_Loss),TP=float(Take_Profit),type_ordre=type_ordre)



    #fonction signaux de calcul de risque et lot

    def click_btn_calcul_lot(self):
        valeur_pips=self.valeur_pips.value()
        montant=self.account_montant.value()

        risque=self.risque_pourcentage.value()
        Commision=self.Commision.value()
        taille_SL=self.taille_SL.value()
        if risque==0 or taille_SL==0 or valeur_pips==0:


            if risque==0:

                self.verification_validation_calcul.setText("INVALIDATION:RISQUE EST EGALE A 0.")

            elif taille_SL==0:
                self.verification_validation_calcul.setText("INVALIDATION:TAILLE SL EST EGALE A 0")

            elif valeur_pips==0:
                self.verification_validation_calcul.setText("INVALIDATION:VALEUR PIPS EST EGALE A 0")


        else:
            lot=(montant * risque/100)/taille_SL/valeur_pips

            nombre_argent_par_lot=montant/lot

            risque_lot=nombre_argent_par_lot*(risque/100)

            Risque_etCommision=(Commision+risque_lot)*lot

            risque_en_argent=montant*(risque/100)
            lot_réél=(risque_en_argent/Risque_etCommision)*lot
            self.Lot.setValue(round(lot_réél,2))

            #ajout des valeurs de quand on calcul le lot aux autres onglets
            if self.Take_profit_calcul_lot.value()!=0:
                self.Take_profit_direct.setValue(self.Take_profit_calcul_lot.value())
                self.Take_profit_différée.setValue(self.Take_profit_calcul_lot.value())
            if self.Stop_loss_calcul_lot.value()!=0:
                self.Stop_loss_direct.setValue(self.Stop_loss_calcul_lot.value())
                self.Stop_loss_différée.setValue(self.Stop_loss_calcul_lot.value())
            if self.Entrée_calcul_lot.value()!=0:
                self.prix_entrée.setValue(self.Entrée_calcul_lot.value())
            self.lot_différé.setValue(round(lot_réél,2))
            self.Lot_direct.setValue(round(lot_réél,2))
            self.verification_validation_calcul.setText("Calcul de lot réussi")
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

    #fonction pour afficher fenêtre pour changer les pips des devises
    def Affichage_fenetre_changer_pips(self):
        self.w=ChangerPipsWindow()
        self.w.resize(300,200)
        self.w.show()

    #fonction pour afficher fenêtre ajouter paire

    def fct_ajouter_paire(self):
        self.w=AjouterPaireWindow()
        self.w.resize(300,200)
        self.w.show()

    #fonction pour afficher fenêtre supprimer paire
    def supprimer_paire(self):
        self.w=Supprimer_devise_Windows()
        self.w.resize(300,200)
        self.w.show()


        # fonction pour afficher fenetre commision_par_default

    def fct_modifier_paramètre_default(self):
        self.w=Modifier_paramètre_default_Window()
        self.w.resize(300,200)
        self.w.show()


    #fonction pour actualiser window , bouton dans barre d'outils

    def fct_Actualiser(self):
        db = TinyDB('Paires.json', indent=4)
        table_paire = db.table('Valeur pip')
        table_default=db.table('parametre_default')
        Q=Query()
        #valeur par default
        l_paire=[i['paire'] for i in table_paire]
        value_partiel = table_default.search(Q.type == "nombre de partiel")[0]['value']
        value_entrée = table_default.search(Q.type == "Entree")[0]['value']
        value_SL = table_default.search(Q.type == "Stop Loss")[0]['value']
        value_Commission=table_default.search(Q.type=="commission")[0]['value']
        value_paire=table_default.search(Q.type=="paire")[0]['value']
        value_account=table_default.search(Q.type=="account")[0]['value']
        value_risque=table_default.search(Q.type=="risque")[0]['value']

        self.combobox_paires.clear()
        self.combobox_paires.addItems(l_paire)
        self.combobox_paires.setCurrentText(value_paire)
        value_paire=self.combobox_paires.currentText()
        value_pip=0
        for i in table_paire:
            if i['paire']==value_paire:
                value_pip=i['valeur_pip']
                break

        self.Stop_loss_calcul_lot.setValue(value_SL)
        self.Entrée_calcul_lot.setValue(value_entrée)
        self.Commision.setValue(value_Commission)
        self.valeur_pips.setValue(value_pip)
        self.prix_entrée.setValue(value_entrée)
        self.Nombre_partiel_différée.setValue(value_partiel)
        self.Nombre_partiel_direct.setValue(value_partiel)
        self.account_montant.setValue(value_account)
        self.risque_pourcentage.setValue(value_risque)


    #fonction pour changer la valeur du pips lorsque l'on change le combobox

    def Change_paires_valeur_pip(self):
        db=TinyDB('Paires.json',indent=4)
        table_paire=db.table('Valeur pip')
        for i in table_paire:
            if i['paire']==self.combobox_paires.currentText():
                self.valeur_pips.setValue(i['valeur_pip'])
                break



app = QApplication(sys.argv)
window = MainWindow()
window.resize(400, 250)
window.setGeometry(0,0,0,0)
window.show()
app.exec_()
