import sqlite3
import random
import threading
from datetime import datetime, timedelta
from operator import itemgetter
from pathlib import Path

import pandas as pd
from PySide6.QtMultimedia import QSoundEffect

from Threads import *

from PySide6 import QtGui, QtCore
from PySide6.QtCore import QSize, QPoint, QDateTime, QTime, QDate, QAbstractItemModel, QTimer, QItemSelectionModel, \
    QThreadPool
from PySide6.QtGui import QAction, QIcon, QPixmap, QBrush, QColor, QFont, Qt
from PySide6.QtWidgets import QTabWidget, QPushButton, QWidget, QGridLayout, QVBoxLayout, QApplication, QMainWindow, \
    QDoubleSpinBox, QLabel, QSpinBox, QAbstractSpinBox, QComboBox, QMessageBox, QToolBar, QStatusBar, QLineEdit, \
    QRadioButton, QHBoxLayout, QDateEdit, QDateTimeEdit, QTimeEdit, QListWidget, QListWidgetItem, QTableView, \
    QHeaderView, QTableWidget, QTableWidgetItem
from fenetre_DD.modifier_pallier import *
from fenetres_manager_trade.parametre_manager import ManagerTradeWindow
from fenetres_parametres.ajouter_paires import *
from fenetres_parametres.supprimer_devise import *
from fenetres_parametres.changer_valeur_pip import *
from fenetres_parametres.modifier_paramettre_default import *

from rentrer_position_partiel import execution_direct, execution_différé, execution_différé_MT5, execution_direct_MT5, \
    fast_change_tp_sl_mt4, fast_change_tp_sl_mt5, fast_fermeture_ordre_mt4, fast_fermeture_ordre_mt5
import sys

from Abstract_Widget.Table_annonce import TableModelAnnonce

# import des différents styles
from style_widgets.style_général import *


# --------------------------------------------FENETRE PRINCIPALE-------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # titre/icone/custum:

        self.setMaximumWidth(200)

        # création du widget des onglets

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.East)
        # création des différents onglets
        self.W_entrée_directe = QWidget()

        self.W_entrée_différée = QWidget()

        self.W_calcul_lot = QWidget()

        self.W_change_fast_sl_tp = QWidget()

        self.W_calcul_stratégie_DD = QWidget()

        self.W_Annonce_économique = QWidget()

        # création de layout qu'on va venir ajouter au widget à la fin
        layout_entrée_directe = QGridLayout()
        layout_entrée_différée = QGridLayout()
        layout_calcul_lot = QGridLayout()
        layout_change_fast_sl_tp = QGridLayout()
        layout_calcul_strategie_DD = QGridLayout()
        layout_Annonce_économique = QGridLayout()
        # valeur par default base de donnée sqlite3
        connexion=sqlite3.connect("DB.sq3")
        cursor=connexion.cursor()

        #valeur par default de la table parametre_default
        cursor.execute("SELECT value FROM parametre_default WHERE type='commission'")
        self.value_commission=cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='account'")
        self.value_account = cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='paire'")
        self.value_paire = cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='nombre de partiel'")
        self.value_partiel = cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='Entree'")
        self.value_entrée = cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='Stop Loss'")
        self.value_SL=cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='couleur'")
        self.couleur = cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='metatrader'")
        self.value_metatrader=cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='ordre manager'")
        self.manager_trade = cursor.fetchone()[0]
        cursor.execute("SELECT valeur_pip FROM Valeur_pip WHERE paire=?",[self.value_paire])
        self.value_pip=cursor.fetchone()[0]
        #parametre table DD
        #pallier1
        cursor.execute("SELECT activation FROM DD WHERE pallier=0")
        self.pallier0_activation = cursor.fetchone()[0]
        cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=0")
        self.pallier0_risque=cursor.fetchone()[0]
        cursor.execute("SELECT trade_pris FROM DD WHERE pallier=0")
        self.pallier0_trade_pris=cursor.fetchone()[0]
        #pallier1
        cursor.execute("SELECT activation FROM DD WHERE pallier=1")
        self.pallier1_activation = cursor.fetchone()[0]
        cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=1")
        self.pallier1_risque = cursor.fetchone()[0]
        cursor.execute("SELECT trade_pris FROM DD WHERE pallier=1")
        self.pallier1_trade_pris = cursor.fetchone()[0]
        #pallier2
        cursor.execute("SELECT activation FROM DD WHERE pallier=2")
        self.pallier2_activation = cursor.fetchone()[0]
        cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=2")
        self.pallier2_risque = cursor.fetchone()[0]
        cursor.execute("SELECT trade_pris FROM DD WHERE pallier=2")
        self.pallier2_trade_pris = cursor.fetchone()[0]
        # pallier3
        cursor.execute("SELECT activation FROM DD WHERE pallier=2")
        self.pallier3_activation = cursor.fetchone()[0]
        cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=3")
        self.pallier3_risque = cursor.fetchone()[0]
        cursor.execute("SELECT trade_pris FROM DD WHERE pallier=3")
        self.pallier3_trade_pris = cursor.fetchone()[0]
        # pallier4
        cursor.execute("SELECT activation FROM DD WHERE pallier=4")
        self.pallier4_activation = cursor.fetchone()[0]
        cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=4")
        self.pallier4_risque = cursor.fetchone()[0]
        cursor.execute("SELECT trade_pris FROM DD WHERE pallier=4")
        self.pallier4_trade_pris = cursor.fetchone()[0]
        # pallier5
        cursor.execute("SELECT activation FROM DD WHERE pallier=5")
        self.pallier5_activation = cursor.fetchone()[0]
        cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=5")
        self.pallier5_risque = cursor.fetchone()[0]
        cursor.execute("SELECT trade_pris FROM DD WHERE pallier=5")
        self.pallier5_trade_pris = cursor.fetchone()[0]

        #valeur de la table  parametre_DD _activation

        cursor.execute("SELECT mise_en_marche FROM parametre_DD_activation")
        self.mise_en_marche=cursor.fetchone()[0]

        cursor.execute("SELECT compte_av_dd FROM parametre_DD_activation")
        self.value_av_drawdown=cursor.fetchone()[0]
        cursor.execute("SELECT pourcentage_DD FROM parametre_DD_activation")
        self.pourcentage_DD=cursor.fetchone()[0]


        drawdown = round(100 - (self.value_account / self.value_av_drawdown) * 100, 2)


        #liste des paires
        cursor.execute("SELECT paire FROM Valeur_pip")
        liste_items=[]
        p = cursor.fetchone()
        while p is not None:
            liste_items.append(p[0])
            p = cursor.fetchone()
        connexion.close()

        #Creation des Différents threads qui peut avoir lieu
        self.thread_timer=QThreadPool()
        self.thread_play_musique=QThreadPool()
        self.thread_annonce_suppression_annonce=QThreadPool()

        # création des différents widgets de l'onglet entrée_direct
        # variation du Label en fonction du drawdown
        self.Label_DrawDown_Entrée = QLabel("")

        self.Label_MT_entrée = QLabel("Choix de Metatrader:")
        self.Radio_MT4_entrée = QRadioButton("MT4")
        self.Radio_MT5_entrée = QRadioButton("MT5")

        self.Label_lot_direct = QLabel("Volume(obligatoire): ")
        self.Label_lot_direct.setStyleSheet("""color:red""")
        self.Lot_direct = QDoubleSpinBox()
        self.Lot_direct.setDecimals(2)

        self.Label_stop_loss_direct = QLabel("Stop Loss: ")
        self.Stop_loss_direct = QDoubleSpinBox()
        self.Stop_loss_direct.setValue(self.value_SL)
        self.Stop_loss_direct.setDecimals(5)
        self.Stop_loss_direct.setMaximum(100000)

        self.Label_take_profit_direct = QLabel("Take profit: ")
        self.Take_profit_direct = QDoubleSpinBox()
        self.Take_profit_direct.setDecimals(5)
        self.Take_profit_direct.setMaximum(1000000)

        self.Label_nombre_partiel_direct = QLabel("Nombre de partiel: ")
        self.Nombre_partiel_direct = QSpinBox()
        self.Nombre_partiel_direct.setMinimum(1)
        self.Nombre_partiel_direct.setValue(self.value_partiel)

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

        self.Label_DrawDown_Différé = QLabel("")

        self.Label_MT_différée = QLabel("Choix du metatrader:")
        self.Radio_MT4_différée = QRadioButton("MT4")
        self.Radio_MT5_différée = QRadioButton("MT5")
        self.Label_lot_différé = QLabel('Volume(obligatoire) :')

        self.lot_différé = QDoubleSpinBox()
        self.lot_différé.setDecimals(2)

        self.Label_prix_entrée = QLabel("Entrée(obligatoire):")

        self.prix_entrée = QDoubleSpinBox()
        self.prix_entrée.setValue(self.value_entrée)
        self.prix_entrée.setDecimals(5)
        self.prix_entrée.setMaximum(1000000)

        self.Label_stop_loss_différée = QLabel("Stop Loss:")
        self.Stop_loss_différée = QDoubleSpinBox()
        self.Stop_loss_différée.setValue(self.value_SL)
        self.Stop_loss_différée.setDecimals(5)
        self.Stop_loss_différée.setMaximum(1000000)

        self.Label_profit_différée = QLabel("Take Profit:")
        self.Take_profit_différée = QDoubleSpinBox()
        self.Take_profit_différée.setDecimals(5)
        self.Take_profit_différée.setMaximum(10000000)

        self.Label_nombre_partiel_différée = QLabel("Nombre de partiel:")
        self.Nombre_partiel_différée = QSpinBox()
        self.Nombre_partiel_différée.setMinimum(1)
        self.Nombre_partiel_différée.setValue(self.value_partiel)

        self.Button_validé_position = QPushButton("Go!")

        self.Label_type_ordre = QLabel("Type d'ordre(obligatoire) :")
        self.Liste_ordres = QComboBox()

        self.Label_Prix_Stop_Limit = QLabel("Prix Stop Limit(obligatoire): ")
        self.Prix_Stop_Limit = QDoubleSpinBox()
        self.Prix_Stop_Limit.setDecimals(5)

        # rendre disable Prix_Stop_limit si ordre =! de ceux de MT5

        if self.Liste_ordres.currentText() == "Sell Stop Limit" or self.Liste_ordres.currentText() == "Buy Stop Limit":
            self.Prix_Stop_Limit.setDisabled(False)
        else:
            self.Prix_Stop_Limit.setDisabled(True)

        # Création des différents widgets de l'onglet "Calcul lot"

        self.Label_DrawDown_Calcul_lot = QLabel("")

        self.Label_account = QLabel("Account(obligatoire): ")
        self.account_montant = QDoubleSpinBox()
        self.account_montant.setMaximum(100000000)
        self.account_montant.setDecimals(2)
        self.account_montant.setValue(self.value_account)
        # --------------
        self.Label_paires = QLabel("Paire de devise(facultatif) :")
        self.combobox_paires = QComboBox()

        self.combobox_paires.addItems(liste_items)
        self.combobox_paires.setCurrentText(self.value_paire)

        self.Label_valeur_pips = QLabel("Valeur du pip(obligatoire) :")

        self.valeur_pips = QDoubleSpinBox()
        self.valeur_pips.setDecimals(5)
        self.valeur_pips.setValue(self.value_pip)


        self.Label_Commision = QLabel("Commission(facultatif):")
        self.Commision = QDoubleSpinBox()
        self.Commision.setDecimals(2)
        self.Commision.setValue(self.value_commission)

        self.Label_risque_pourcentage = QLabel("Risque(obligatoire): ")

        self.risque_pourcentage = QDoubleSpinBox()
        self.risque_pourcentage.setDecimals(2)
        self.risque_pourcentage.setValue(self.pallier0_risque)

        self.Label_Entrée_calcul_lot = QLabel("Entrée(facultatif): ")
        self.Entrée_calcul_lot = QDoubleSpinBox()
        self.Entrée_calcul_lot.setValue(self.value_entrée)
        self.Entrée_calcul_lot.setDecimals(5)
        self.Entrée_calcul_lot.setMaximum(1000000)

        self.Label_Stop_loss_calcul_lot = QLabel('Stop loss(facultatif): ')
        self.Stop_loss_calcul_lot = QDoubleSpinBox()
        self.Stop_loss_calcul_lot.setValue(self.value_SL)
        self.Stop_loss_calcul_lot.setDecimals(5)
        self.Stop_loss_calcul_lot.setMaximum(1000000)

        self.Label_Take_profit_calcul_lot = QLabel("Take profit(facultatif): ")
        self.Take_profit_calcul_lot = QDoubleSpinBox()
        self.Take_profit_calcul_lot.setDecimals(5)
        self.Take_profit_calcul_lot.setMaximum(1000000)

        self.Label_taille_SL = QLabel("Taille SL en pip(obligatoire): ")

        self.taille_SL = QDoubleSpinBox()
        self.taille_SL.setMaximum(30000)
        self.taille_SL.setDecimals(1)


        self.btn_calcul_lot = QPushButton("Calculer Lot")

        self.Label_Lot = QLabel("Lot: ")
        self.Lot = QDoubleSpinBox()
        self.Lot.setMaximum(100000)
        self.Lot.setDecimals(2)

        self.verification_validation_calcul = QLabel("")

        # création des widgets pour l'onglet MANAGER TRADE
        self.Label_choix_manager = QLabel("Quel type d'ordre voulez vous effectuer:")

        self.Radio_manager_SL_TP = QRadioButton("Manager Sell Stop et Take Profit")
        self.Radio_fermé_position = QRadioButton("Fermer des position")

        self.Label_MT_sl_tp_fast = QLabel("Choix de Metatrader:")

        self.Radio_MT4_sl_tp_fast = QRadioButton("MT4")
        self.Radio_MT5_sl_tp_fast = QRadioButton("MT5")
        # 1) pour btn radio changer sl_tp
        self.label_SL = QLabel('SL:')

        self.SL = QDoubleSpinBox()
        self.SL.setDecimals(5)
        self.SL.setMaximum(99999999)
        self.label_TP = QLabel('TP:')

        self.TP = QDoubleSpinBox()
        self.TP.setDecimals(5)
        self.TP.setMaximum(99999999)
        self.label_nb_changement = QLabel("Nombre de trade à changer:")

        self.nb_changement = QSpinBox()
        self.nb_changement.setMinimum(1)
        self.changer_fast = QPushButton("ManagerSL/TP")

        # 2) pour btn radio fermer des positions
        self.label_nb_ordre_fermé = QLabel("Nombre d'ordre à fermer: ")

        self.nb_ordre_fermé = QSpinBox()
        self.nb_ordre_fermé.setMinimum(1)
        self.fermer_ordre_fast = QPushButton("Fermer ordres")

        # creation des widgets pour l'onglet calcul_strategie_DD
        self.label_account_calcul_dd = QLabel("Account(av DD):")
        self.account_dd_av_actuel = QDoubleSpinBox()
        self.account_dd_av_actuel.setDecimals(2)
        self.account_dd_av_actuel.setMaximum(999999999)
        self.account_dd_av_actuel.setValue(self.value_av_drawdown)
        self.button_account_dd_calcul = QPushButton('Remettre paramètres default')
        self.label_OK1_DD = QLabel("")

        self.label_trade_avant_pallier1 = QLabel("Trade pris pallier 0:")
        self.trade_avant_pallier1 = QSpinBox()
        self.trade_avant_pallier1.setValue(self.pallier0_trade_pris)
        self.label_OK2_DD = QLabel("")
        self.trade_perte1 = QLabel("")

        self.label_risque_base = QLabel("risque de base:")
        self.risque_de_base = QDoubleSpinBox()
        self.risque_de_base.setDecimals(2)
        self.risque_de_base.setSuffix('%')
        self.risque_de_base.setValue(self.pallier0_risque)
        self.label_OK3_DD = QLabel("")

        self.label_trade_avant_pallier2 = QLabel("Trade pris pallier 1 :")
        self.trade_avant_pallier2 = QSpinBox()
        self.trade_avant_pallier2.setValue(self.pallier1_trade_pris)
        self.label_OK4_DD = QLabel("")
        self.trade_perte2 = QLabel("")

        self.label_division_risque_pallier1 = QLabel("Risque pallier n°1: ")
        self.division_risque_pallier1 = QDoubleSpinBox()
        self.division_risque_pallier1.setDecimals(2)
        self.division_risque_pallier1.setSuffix("%")
        self.division_risque_pallier1.setValue(self.pallier1_risque)
        self.label_OK5_DD = QLabel("")

        self.label_trade_avant_pallier3 = QLabel("Trade pris pallier2 :")
        self.trade_avant_pallier3 = QSpinBox()
        self.trade_avant_pallier3.setValue(self.pallier2_trade_pris)
        self.label_OK6_DD = QLabel("")
        self.trade_perte3 = QLabel("")

        self.label_division_risque_pallier2 = QLabel("Risque pallier n°2: ")
        self.division_risque_pallier2 = QDoubleSpinBox()
        self.division_risque_pallier2.setDecimals(2)
        self.division_risque_pallier2.setSuffix("%")
        self.division_risque_pallier2.setValue(self.pallier2_risque)
        self.label_OK7_DD = QLabel("")

        self.label_trade_avant_pallier4 = QLabel("Trade pris pallier 3 :")
        self.trade_avant_pallier4 = QSpinBox()
        self.trade_avant_pallier4.setValue(self.pallier3_trade_pris)
        self.label_OK8_DD = QLabel("")
        self.trade_perte4 = QLabel("")

        self.label_division_risque_pallier3 = QLabel("Risque pallier n°3: ")
        self.division_risque_pallier3 = QDoubleSpinBox()
        self.division_risque_pallier3.setDecimals(2)
        self.division_risque_pallier3.setSuffix("%")
        self.division_risque_pallier3.setValue(self.pallier3_risque)
        self.label_OK9_DD = QLabel("")

        self.label_trade_avant_pallier5 = QLabel("Trade pris pallier 4 :")
        self.trade_avant_pallier5 = QSpinBox()
        self.trade_avant_pallier5.setValue(self.pallier4_trade_pris)
        self.trade_perte5 = QLabel("")
        self.label_OK10_DD = QLabel("")

        self.label_division_risque_pallier4 = QLabel("Risque pallier n°4 :")
        self.division_risque_pallier4 = QDoubleSpinBox()
        self.division_risque_pallier4.setDecimals(2)
        self.division_risque_pallier4.setSuffix("%")
        self.division_risque_pallier4.setValue(self.pallier4_risque)
        self.label_OK11_DD = QLabel("")

        self.label_trade_après_pallier5 = QLabel("Trade pris pallier 5 :")
        self.trade_après_pallier5 = QSpinBox()
        self.trade_après_pallier5.setMaximum(999999)
        self.trade_après_pallier5.setValue(self.pallier5_trade_pris)
        self.trade_perte_après5 = QLabel("")
        self.label_OK12_DD = QLabel("")

        self.label_division_risque_pallier5 = QLabel("Risque pallier n°5 :")
        self.division_risque_pallier5 = QDoubleSpinBox()
        self.division_risque_pallier5.setDecimals(2)
        self.division_risque_pallier5.setSuffix("%")
        self.division_risque_pallier5.setValue(self.pallier5_risque)
        self.label_OK13_DD = QLabel("")

        self.button_calculer_perte_pallier = QPushButton("Calculer les pertes par palliers (%/somme)")
        self.button_appliquer = QPushButton("Appliquer la stratégie")

        # creation des widget de annonce économique
        self.label_Nom_annonce = QLabel("Nom de l'annonce : ")
        self.Nom_annonce = QLineEdit()
        self.label_date_annonce = QLabel("Date de l'annonce : ")
        self.date_annonce = QDateEdit()
        now=datetime.today()
        d=QDate(now.year,now.month,now.day)

        self.date_annonce.setMinimumDate(d)
        t=QTime(int(now.hour),int(now.minute))
        self.label_heure_annonce = QLabel("Heure annonce : ")
        self.heure_annonce = QTimeEdit()
        self.heure_annonce.setTime(t)
        self.ajouter_annonce = QPushButton("Ajouter l'annonce")
        self.table_annonce = QTableView()
        self.label_prochaine_annonce_timer=QLabel("")

        #récupération des données de la table annonce


        c=sqlite3.connect("DB.sq3")
        cu=c.cursor()
        cu.execute("SELECT * FROM Annonces")
        self.columns=["Nom","Date","Heure"]
        #on convertit la liste en datetime pour la triée par la date puis on l'a renvoie
        liste=cu.fetchall()
        print(len(liste))
        for count, value in enumerate(liste):
            liste[count] = list(value)
            date=f'{liste[count][1]}-{liste[count][2]}'
            liste[count][1]=datetime.strptime(date,"%Y-%m-%d-%H:%M")


        items_supprimés=[]

        for i in liste:

            if i[1]<=datetime.now():
                sql = "DELETE FROM Annonces WHERE nom=?"
                cu.execute(sql, [i[0]])

                items_supprimés.append(i)
                print("succes remove Han Han")

        for i in items_supprimés:
            liste.remove(i)

        c.commit()
        c.close()
        liste.sort(key=itemgetter(1))

        for i in range (len(liste)):
            liste[i][1]=f"{str(liste[i][1].year).zfill(2)}-{str(liste[i][1].month).zfill(2)}-{str(liste[i][1].day).zfill(2)}"



        self.data=pd.DataFrame(liste,columns=self.columns)
        self.model = TableModelAnnonce(self.data)
        self.table_annonce.setModel(self.model)

        if len(liste)>0:
            self.label_prochaine_annonce_timer.setText(f"Prochaine annonce : {liste[0][1]}")

        else:
            self.label_prochaine_annonce_timer.setText("No annonce!!! Oh")


    #Creation du timer et mise en route pour la prochaine annonce
        #sys.set_int_max_str_digits permet de changer le nombre max d'un nombre que peut stocker python ici 999999999=11,5740740625jours maximum

        self.Chrono_seconde=QTimer()
        self.Chrono_seconde.setInterval(1000) # chrono tout les seconds
        self.Chrono_seconde.start()


        self.btn_supprimer_modifier_annonce=QPushButton("Modifier ou supprimer annonce")

        self.sound_annonce=QSoundEffect()
        self.sound_annonce.setSource(QUrl.fromLocalFile("sound_annonce/second_bell.wav"))
        self.sound_annonce.play()


        # modification des label OK

        if self.division_risque_pallier1.value() != 0:
            self.label_OK5_DD.setText("Ok!")
        else:
            self.label_OK5_DD.setText("")

        if self.division_risque_pallier2.value() != 0:
            self.label_OK7_DD.setText("Ok!")
        else:
            self.label_OK7_DD.setText("")

        if self.division_risque_pallier3.value() != 0:
            self.label_OK9_DD.setText("Ok!")
        else:
            self.label_OK9_DD.setText("")

        if self.division_risque_pallier4.value() != 0:
            self.label_OK11_DD.setText("Ok!")
        else:
            self.label_OK11_DD.setText("")

        if self.division_risque_pallier5.value() != 0:
            self.label_OK13_DD.setText("Ok!")
        else:
            self.label_OK13_DD.setText("")

        if self.risque_de_base.value() != 0:
            self.label_OK3_DD.setText("Ok!")
        else:
            self.label_OK3_DD.setText("")

        if self.trade_avant_pallier1.value() != 0:
            self.label_OK2_DD.setText("Ok!")
        else:
            self.label_OK2_DD.setText("")

        if self.trade_avant_pallier2.value() != 0:
            self.label_OK4_DD.setText("Ok!")
        else:
            self.label_OK4_DD.setText("")

        if self.trade_avant_pallier3.value() != 0:
            self.label_OK6_DD.setText("Ok!")
        else:
            self.label_OK6_DD.setText("")

        if self.trade_avant_pallier4.value() != 0:
            self.label_OK8_DD.setText("Ok!")
        else:
            self.label_OK8_DD.setText("")

        if self.trade_avant_pallier5.value() != 0:
            self.label_OK10_DD.setText("Ok!")
        else:
            self.label_OK10_DD.setText("")

        if self.trade_après_pallier5.value() != 0:
            self.label_OK12_DD.setText("Ok!")
        else:
            self.label_OK12_DD.setText("")

        if self.account_dd_av_actuel.value() != 0:
            self.label_OK1_DD.setText("Ok!")
        else:
            self.label_OK1_DD.setText("")

        # modification des label de DD

        if drawdown < self.pallier1_activation:
            self.risque_pourcentage.setValue(self.pallier0_risque)
            self.changer_label_drawdown("0", drawdown, self.value_av_drawdown)
        elif self.pallier1_activation < drawdown < self.pallier2_activation:
            self.risque_pourcentage.setValue(self.pallier1_risque)
            self.changer_label_drawdown("1", drawdown, self.value_av_drawdown)
        elif self.pallier2_activation < drawdown < self.pallier3_activation:
            self.risque_pourcentage.setValue(self.pallier2_risque)
            self.changer_label_drawdown("2", drawdown, self.value_av_drawdown)
        elif self.pallier3_activation < drawdown < self.pallier4_activation:
            self.risque_pourcentage.setValue(self.pallier3_risque)
            self.changer_label_drawdown("3", drawdown, self.value_av_drawdown)
        elif self.pallier4_activation < drawdown < self.pallier5_activation:
            self.risque_pourcentage.setValue(self.pallier4_risque)
            self.changer_label_drawdown("4", drawdown, self.value_av_drawdown)
        elif drawdown > self.pallier5_activation:
            self.risque_pourcentage.setValue(self.pallier5_risque)
            self.changer_label_drawdown("5", drawdown, self.value_av_drawdown)

        # CHANGER LES COCHAGES ET LES CHANGEMENTS DE WIDGETS EN FONCTION DES PARAMETRES DE BASE
        # changer la valeur de metatradeur cochage pour tout les onglets avec cochage metatrader 4/5

        # faire une condition pour si jamais la valeur par default est MT5 , changer la liste des items et rajouter les 2 autres ordres
        if self.value_metatrader== "mt4":
            self.Liste_ordres.addItems(["Buy Limit", "Sell Limit", "Buy Stop", "Sell Stop"])
            self.Radio_MT4_différée.setChecked(True)
            self.Radio_MT4_entrée.setChecked(True)
            self.Radio_MT4_sl_tp_fast.setChecked(True)
            self.Prix_Stop_Limit.setHidden(True)
            self.Label_Prix_Stop_Limit.setHidden(True)
        elif self.value_metatrader == "mt5":
            self.Liste_ordres.addItems(
                ["Buy Limit", "Sell Limit", "Buy Stop", "Sell Stop", "Buy Stop Limit", "Sell Stop Limit"])
            self.Radio_MT5_différée.setChecked(True)
            self.Radio_MT5_entrée.setChecked(True)
            self.Radio_MT5_sl_tp_fast.setChecked(True)
            self.Prix_Stop_Limit.setHidden(False)
            self.Label_Prix_Stop_Limit.setHidden(False)

        # changer les widgets de l'onglet manager trade en fonction de ce qui est coché

        if self.manager_trade== "fermeture":
            self.label_nb_changement.setHidden(True)
            self.nb_changement.setHidden(True)
            self.label_SL.setHidden(True)
            self.SL.setHidden(True)
            self.label_TP.setHidden(True)
            self.TP.setHidden(True)
            self.changer_fast.setHidden(True)
            self.Radio_fermé_position.setChecked(True)

        elif self.manager_trade == "sl-tp":
            self.label_nb_ordre_fermé.setHidden(True)
            self.nb_ordre_fermé.setHidden(True)
            self.fermer_ordre_fast.setHidden(True)
            self.Radio_manager_SL_TP.setChecked(True)



        # else:

        # création de la barre d'outils/Menu
        # Création des actions de la barres d'outils et connexion à leur fonctions
        self.changer_valeur_des_pips = QAction("Changer valeur des pips", self)
        self.changer_valeur_des_pips.triggered.connect(self.Affichage_fenetre_changer_pips)

        self.Ajouter_paire = QAction("Ajouter paire de devise", self)
        self.Ajouter_paire.triggered.connect(self.fct_ajouter_paire)

        self.Supprimer_paire = QAction("Supprimer paires", self)
        self.Supprimer_paire.triggered.connect(self.supprimer_paire)

        self.Modifier_paramètre_default = QAction("Modifier paramètre par default", self)
        self.Modifier_paramètre_default.triggered.connect(self.fct_modifier_paramètre_default)

        # bouton action pour actualiser le logiciel avec les données changer dans les paramètres
        self.Actualiser = QAction('Actualiser', self)
        self.Actualiser.triggered.connect(self.fct_Actualiser)

        # bouton pour rollback la stratégie de drawdown et retourner à l'ancienne
        self.Rollback_strategie_DD = QAction("Rollback ancienne strategie DD")
        self.Rollback_strategie_DD.triggered.connect(self.fct_Rollback_strategie_DD)

        #bouton permettant de desactiver la musique du Timer
        c=sqlite3.connect("DB.sq3")
        cursor=c.cursor()
        cursor.execute("SELECT value FROM parametre_default WHERE type=='activation_musique_timer'")
        activation_musique=cursor.fetchall()[0][0]

        c.close()
        self.Activer_Musique_Timer=QAction("Musique Timer Activée",self)
        if activation_musique=="True":
            self.Activer_Musique_Timer.setText("arrêter musique")
        else:
            self.Activer_Musique_Timer.setText("Activer musique")

        self.Activer_Musique_Timer.triggered.connect(self.fct_Activer_Musique_Timer)

        # création menu et toolbar
        self.menubar = self.menuBar()
        self.toolbar = QToolBar("toolbar")
        self.addToolBar(self.toolbar)
        # chanagement parametre Paire/default/pips...
        menu_changement_valeur_pips = self.menubar.addMenu("&paramètres")
        menu_changement_valeur_pips.addAction(self.changer_valeur_des_pips)
        menu_changement_valeur_pips.addAction(self.Ajouter_paire)
        menu_changement_valeur_pips.addAction(self.Supprimer_paire)
        menu_changement_valeur_pips.addAction(self.Modifier_paramètre_default)

        # menu barre d'outils DD
        menu_DD = self.menubar.addMenu('&DrawDown')

        self.Pallier_DD = QAction("Modifier pallier de Drawdown", self)
        self.Pallier_DD.triggered.connect(self.fct_modifier_pallier)
        self.Activation_stratégie = QAction("", self)
        if self.mise_en_marche == True:
            self.Activation_stratégie.setText("Desactiver stratégie drawdown")
        elif self.mise_en_marche == False:
            self.Activation_stratégie.setText("Activer stratégie drawdown")
        self.Activation_stratégie.triggered.connect(self.activation_Strategie_DD)

        self.Remettre_zero_strategie_dd = QAction("Remettre à zéro la stratégie de DD")
        self.Remettre_zero_strategie_dd.triggered.connect(self.remise_zero_strategie_DD)

        # menu barre d'outils changer de mode
        menu_mode_visuel = self.menubar.addMenu("&changer visuel")
        self.mode_white = QAction('Mode Blanc')
        self.mode_sombre = QAction('Mode Sombre')
        self.mode_nature = QAction('Mode nature')
        self.mode_white.triggered.connect(self.change_mode_white)
        self.mode_sombre.triggered.connect(self.change_mode_sombre)
        self.mode_nature.triggered.connect(self.change_mode_nature)

        # ajout action dans menu_visuel
        menu_mode_visuel.addAction(self.mode_white)
        menu_mode_visuel.addAction(self.mode_sombre)
        menu_mode_visuel.addAction(self.mode_nature)

        # menu barre d'outils changer de parametre default onglet management
        menu_manager_trade = self.menuBar().addMenu("&Manager Trade")
        self.paramètre_manager = QAction("changer paramètres")
        self.paramètre_manager.triggered.connect(self.fct_fenetre_parametre_manager)
        # ajout action dans menu Management trade
        menu_manager_trade.addAction(self.paramètre_manager)

        # ajout action dans menu_DD
        menu_DD.addAction(self.Remettre_zero_strategie_dd)
        menu_DD.addAction(self.Pallier_DD)
        menu_DD.addAction(self.Activation_stratégie)


        # ajout outils dans toolbar
        self.toolbar.addAction(self.Actualiser)
        self.toolbar.addAction(self.Rollback_strategie_DD)
        self.toolbar.addAction(self.Activer_Musique_Timer)

        # Ajout des signaux pour l'onglet ordre instantanée
        self.Button_acheteur.clicked.connect(self.Acheter_instantanée)
        self.Button_vendeur.clicked.connect(self.Vendre_instantanée)

        self.Take_profit_direct.valueChanged.connect(self.Change_TP_différé)
        self.Stop_loss_direct.valueChanged.connect(self.Change_Stop_loss_différé)
        self.Lot_direct.valueChanged.connect(self.Change_Lot_différé)
        self.Nombre_partiel_direct.valueChanged.connect(self.Change_nombre_partiel_différé)
        self.Radio_MT4_entrée.toggled.connect(self.change_Radio_entrée)
        self.Radio_MT5_entrée.toggled.connect(self.change_Radio_entrée)

        # ajout signaux pour l'onglet ordre différée
        self.Button_validé_position.clicked.connect(self.Position_différée)
        self.Take_profit_différée.valueChanged.connect(self.Change_TP_direct)
        self.Stop_loss_différée.valueChanged.connect(self.Change_Stop_loss_direct)
        self.lot_différé.valueChanged.connect(self.Change_Lot_direct)
        self.Nombre_partiel_différée.valueChanged.connect(self.Change_nombre_partiel_direct)
        self.Radio_MT4_différée.clicked.connect(self.change_Radio_différée)
        self.Radio_MT5_différée.clicked.connect(self.change_Radio_différée)
        self.Liste_ordres.currentTextChanged.connect(self.change_type_ordre)

        # ajout de signaux pour l'onglet calcul de lot
        self.account_montant.valueChanged.connect(self.Calcul_drawdown)
        self.combobox_paires.currentTextChanged.connect(self.Change_paires_valeur_pip)
        self.btn_calcul_lot.clicked.connect(self.click_btn_calcul_lot)

        # ajout des signaux à l'ongler  calculer startegie DD
        self.button_calculer_perte_pallier.clicked.connect(self.fct_calculer_perte_pallier)
        self.button_account_dd_calcul.clicked.connect(self.afficher_account_av_dd)
        self.button_appliquer.clicked.connect(self.fct_appliquer_strategie)
        self.division_risque_pallier1.valueChanged.connect(self.fct_DD_OK)
        self.division_risque_pallier2.valueChanged.connect(self.fct_DD_OK)
        self.division_risque_pallier3.valueChanged.connect(self.fct_DD_OK)
        self.division_risque_pallier4.valueChanged.connect(self.fct_DD_OK)
        self.division_risque_pallier5.valueChanged.connect(self.fct_DD_OK)
        self.risque_de_base.valueChanged.connect(self.fct_DD_OK)
        self.trade_avant_pallier1.valueChanged.connect(self.fct_DD_OK)
        self.trade_avant_pallier2.valueChanged.connect(self.fct_DD_OK)
        self.trade_avant_pallier3.valueChanged.connect(self.fct_DD_OK)
        self.trade_avant_pallier4.valueChanged.connect(self.fct_DD_OK)
        self.trade_avant_pallier5.valueChanged.connect(self.fct_DD_OK)
        self.account_dd_av_actuel.valueChanged.connect(self.fct_DD_OK)

        # ajouter signaux pour l'onglet  Manager Trade
        self.Radio_MT4_sl_tp_fast.clicked.connect(self.change_Radio_change_fast)
        self.Radio_MT5_sl_tp_fast.clicked.connect(self.change_Radio_change_fast)
        self.changer_fast.clicked.connect(self.fct_changer_tp_sl_fast)
        self.Radio_manager_SL_TP.clicked.connect(self.change_radio_manager_trade)
        self.Radio_fermé_position.clicked.connect(self.change_radio_manager_trade)
        self.fermer_ordre_fast.clicked.connect(self.fct_fermer_ordre)

        # ajout de signaux pour l'onglet annonce
        self.ajouter_annonce.clicked.connect(self.fct_ajout_supression_annonce_threading)
        self.btn_supprimer_modifier_annonce.clicked.connect(self.fct_ajout_supression_annonce_threading)
        self.Chrono_seconde.timeout.connect(self.thread_time_out_annonce)
        # ajout de signaux lorsque l'on change d'onglet:
        self.tabs.currentChanged.connect(self.change_titre_onglet)

        # ajout des widgets dans le layout qu'on va ajouter au widget:layout_entrée_directe
        layout_entrée_directe.addWidget(self.Label_DrawDown_Entrée)
        layout_entrée_directe.addWidget(self.Label_MT_entrée)
        layout_entrée_directe.addWidget(self.Radio_MT4_entrée)
        layout_entrée_directe.addWidget(self.Radio_MT5_entrée)

        layout_entrée_directe.addWidget(self.Label_stop_loss_direct)
        layout_entrée_directe.addWidget(self.Stop_loss_direct)

        layout_entrée_directe.addWidget(self.Label_take_profit_direct)
        layout_entrée_directe.addWidget(self.Take_profit_direct)

        layout_entrée_directe.addWidget(self.Label_lot_direct)
        layout_entrée_directe.addWidget(self.Lot_direct)

        layout_entrée_directe.addWidget(self.Label_nombre_partiel_direct)
        layout_entrée_directe.addWidget(self.Nombre_partiel_direct)

        layout_entrée_directe.addWidget(self.Button_acheteur)
        layout_entrée_directe.addWidget(self.Button_vendeur)

        # ajout des widget dans le layout qu'on va ajouter au widget:layout_entrée_différée
        layout_entrée_différée.addWidget(self.Label_DrawDown_Différé)
        layout_entrée_différée.addWidget(self.Label_MT_différée)
        layout_entrée_différée.addWidget(self.Radio_MT4_différée)
        layout_entrée_différée.addWidget(self.Radio_MT5_différée)

        layout_entrée_différée.addWidget(self.Label_prix_entrée)
        layout_entrée_différée.addWidget(self.prix_entrée)

        layout_entrée_différée.addWidget(self.Label_stop_loss_différée)
        layout_entrée_différée.addWidget(self.Stop_loss_différée)

        layout_entrée_différée.addWidget(self.Label_profit_différée)
        layout_entrée_différée.addWidget(self.Take_profit_différée)

        layout_entrée_différée.addWidget(self.Label_lot_différé)
        layout_entrée_différée.addWidget(self.lot_différé)

        layout_entrée_différée.addWidget(self.Label_type_ordre)
        layout_entrée_différée.addWidget(self.Liste_ordres)

        layout_entrée_différée.addWidget(self.Label_Prix_Stop_Limit)
        layout_entrée_différée.addWidget(self.Prix_Stop_Limit)

        layout_entrée_différée.addWidget(self.Label_nombre_partiel_différée)
        layout_entrée_différée.addWidget(self.Nombre_partiel_différée)

        layout_entrée_différée.addWidget(self.Button_validé_position)

        # ajout des widgets dans le layout qu'on va ajouter au widget:layout_calcul_lot
        layout_calcul_lot.addWidget(self.Label_DrawDown_Calcul_lot)
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
        layout_calcul_lot.addWidget(self.verification_validation_calcul)

        # ajout des widgets dans le layout qu'on va ajouter au widget:layout_change_fast_sl_tp
        layout_change_fast_sl_tp.addWidget(self.Label_choix_manager)
        layout_change_fast_sl_tp.addWidget(self.Radio_fermé_position)
        layout_change_fast_sl_tp.addWidget(self.Radio_manager_SL_TP)
        layout_change_fast_sl_tp.addWidget(self.Label_MT_sl_tp_fast)
        layout_change_fast_sl_tp.addWidget(self.Radio_MT4_sl_tp_fast)
        layout_change_fast_sl_tp.addWidget(self.Radio_MT5_sl_tp_fast)

        layout_change_fast_sl_tp.addWidget(self.label_nb_ordre_fermé)
        layout_change_fast_sl_tp.addWidget(self.nb_ordre_fermé)

        layout_change_fast_sl_tp.addWidget(self.fermer_ordre_fast)
        layout_change_fast_sl_tp.addWidget(self.label_SL)
        layout_change_fast_sl_tp.addWidget(self.SL)

        layout_change_fast_sl_tp.addWidget(self.label_TP)
        layout_change_fast_sl_tp.addWidget(self.TP)

        layout_change_fast_sl_tp.addWidget(self.label_nb_changement)

        layout_change_fast_sl_tp.addWidget(self.nb_changement)
        layout_change_fast_sl_tp.addWidget(self.changer_fast)

        # ajout des widgets dans le layout :layout_calcul_strategie_DD

        layout_calcul_strategie_DD.addWidget(self.button_account_dd_calcul, 0, 0, 1, 2)
        layout_calcul_strategie_DD.addWidget(self.label_account_calcul_dd, 1, 0)
        layout_calcul_strategie_DD.addWidget(self.account_dd_av_actuel, 1, 1)
        layout_calcul_strategie_DD.addWidget(self.label_OK1_DD, 1, 2)

        layout_calcul_strategie_DD.addWidget(self.label_trade_avant_pallier1, 2, 0)
        layout_calcul_strategie_DD.addWidget(self.trade_avant_pallier1, 2, 1)
        layout_calcul_strategie_DD.addWidget(self.label_OK2_DD, 2, 2)
        layout_calcul_strategie_DD.addWidget(self.label_risque_base, 3, 0)
        layout_calcul_strategie_DD.addWidget(self.risque_de_base, 3, 1)
        layout_calcul_strategie_DD.addWidget(self.label_OK3_DD, 3, 2)
        layout_calcul_strategie_DD.addWidget(self.trade_perte1, 4, 0, 1, 2)

        layout_calcul_strategie_DD.addWidget(self.label_trade_avant_pallier2, 5, 0)
        layout_calcul_strategie_DD.addWidget(self.trade_avant_pallier2, 5, 1)
        layout_calcul_strategie_DD.addWidget(self.label_OK4_DD, 5, 2)
        layout_calcul_strategie_DD.addWidget(self.label_division_risque_pallier1, 6, 0)
        layout_calcul_strategie_DD.addWidget(self.division_risque_pallier1, 6, 1)
        layout_calcul_strategie_DD.addWidget(self.label_OK5_DD, 6, 2)
        layout_calcul_strategie_DD.addWidget(self.trade_perte2, 7, 0, 1, 2)

        layout_calcul_strategie_DD.addWidget(self.label_trade_avant_pallier3, 8, 0)
        layout_calcul_strategie_DD.addWidget(self.trade_avant_pallier3, 8, 1)
        layout_calcul_strategie_DD.addWidget(self.label_OK6_DD, 8, 2)
        layout_calcul_strategie_DD.addWidget(self.label_division_risque_pallier2, 9, 0)
        layout_calcul_strategie_DD.addWidget(self.division_risque_pallier2, 9, 1)
        layout_calcul_strategie_DD.addWidget(self.label_OK7_DD, 9, 2)
        layout_calcul_strategie_DD.addWidget(self.trade_perte3, 10, 0, 1, 2)

        layout_calcul_strategie_DD.addWidget(self.label_trade_avant_pallier4, 11, 0)
        layout_calcul_strategie_DD.addWidget(self.trade_avant_pallier4, 11, 1)
        layout_calcul_strategie_DD.addWidget(self.label_OK8_DD, 11, 2)
        layout_calcul_strategie_DD.addWidget(self.label_division_risque_pallier3, 12, 0)
        layout_calcul_strategie_DD.addWidget(self.division_risque_pallier3, 12, 1)
        layout_calcul_strategie_DD.addWidget(self.label_OK9_DD, 12, 2)
        layout_calcul_strategie_DD.addWidget(self.trade_perte4, 13, 0, 1, 2)

        layout_calcul_strategie_DD.addWidget(self.label_trade_avant_pallier5, 14, 0)
        layout_calcul_strategie_DD.addWidget(self.trade_avant_pallier5, 14, 1)
        layout_calcul_strategie_DD.addWidget(self.label_OK10_DD, 14, 2)
        layout_calcul_strategie_DD.addWidget(self.label_division_risque_pallier4, 15, 0)
        layout_calcul_strategie_DD.addWidget(self.division_risque_pallier4, 15, 1)
        layout_calcul_strategie_DD.addWidget(self.label_OK11_DD, 15, 2)
        layout_calcul_strategie_DD.addWidget(self.trade_perte5, 16, 0, 1, 2)

        layout_calcul_strategie_DD.addWidget(self.label_trade_après_pallier5, 17, 0)
        layout_calcul_strategie_DD.addWidget(self.trade_après_pallier5, 17, 1)
        layout_calcul_strategie_DD.addWidget(self.label_OK12_DD, 17, 2)
        layout_calcul_strategie_DD.addWidget(self.label_division_risque_pallier5, 18, 0)
        layout_calcul_strategie_DD.addWidget(self.division_risque_pallier5, 18, 1)
        layout_calcul_strategie_DD.addWidget(self.label_OK13_DD, 18, 2)
        layout_calcul_strategie_DD.addWidget(self.trade_perte_après5, 19, 0, 1, 2)

        layout_calcul_strategie_DD.addWidget(self.button_calculer_perte_pallier, 20, 0, 1, 3)
        layout_calcul_strategie_DD.addWidget(self.button_appliquer, 21, 0, 1, 3)
        layout_calcul_strategie_DD.setHorizontalSpacing(0)
        layout_calcul_strategie_DD.setRowStretch(14, 100)

        # ajout des widgets dans le layout annonce economique
        layout_Annonce_économique.addWidget(self.label_prochaine_annonce_timer)
        layout_Annonce_économique.addWidget(self.label_Nom_annonce)
        layout_Annonce_économique.addWidget(self.Nom_annonce)
        layout_Annonce_économique.addWidget(self.label_date_annonce)
        layout_Annonce_économique.addWidget(self.date_annonce)
        layout_Annonce_économique.addWidget(self.label_heure_annonce)
        layout_Annonce_économique.addWidget(self.heure_annonce)
        layout_Annonce_économique.addWidget(self.ajouter_annonce)
        layout_Annonce_économique.addWidget(self.table_annonce)
        layout_Annonce_économique.addWidget(self.btn_supprimer_modifier_annonce)
        # ajout des layout dans le set de layout du widget
        self.W_entrée_directe.setLayout(layout_entrée_directe)
        self.W_entrée_différée.setLayout(layout_entrée_différée)
        self.W_calcul_lot.setLayout(layout_calcul_lot)
        self.W_change_fast_sl_tp.setLayout(layout_change_fast_sl_tp)
        self.W_calcul_stratégie_DD.setLayout(layout_calcul_strategie_DD)
        self.W_Annonce_économique.setLayout(layout_Annonce_économique)

        # ajout des widgets qui vont servir d'onglet dans tabs
        self.tabs.addTab(self.W_entrée_directe, 'Ordre direct')
        self.tabs.addTab(self.W_entrée_différée, 'Ordre différé')
        self.tabs.addTab(self.W_calcul_lot, 'Calcul lot/gestion risque')
        self.tabs.addTab(self.W_change_fast_sl_tp, 'Manager Trade')
        self.tabs.addTab(self.W_calcul_stratégie_DD, "Calculer Stratégie DD")
        self.tabs.addTab(self.W_Annonce_économique, "Annonces économiques")
        self.setCentralWidget(self.tabs)

        # ---------style------
        # changement de style principale pour les différents layout
        self.W_entrée_directe.setStyleSheet(style_main_QLabel)

        self.W_entrée_différée.setStyleSheet(style_main_QLabel)

        self.W_calcul_lot.setStyleSheet(style_main_QLabel)

        self.W_change_fast_sl_tp.setStyleSheet(style_main_QLabel)

        self.W_calcul_stratégie_DD.setStyleSheet(style_main_QLabel)

        # changer la couleur en fonction des infos dans base de donnée
        self.label_obligatoire = [self.Label_lot_direct, self.Label_lot_différé, self.Label_prix_entrée,
                                  self.Label_type_ordre, self.Label_Prix_Stop_Limit, self.Label_account,
                                  self.Label_valeur_pips, self.Label_risque_pourcentage, self.Label_taille_SL]
        self.label_facultatif = [self.Label_stop_loss_direct, self.Label_take_profit_direct,
                                 self.Label_nombre_partiel_direct, self.Label_stop_loss_différée,
                                 self.Label_profit_différée, self.Label_nombre_partiel_différée, self.Label_paires,
                                 self.Label_Commision, self.Label_Entrée_calcul_lot, self.Label_Stop_loss_calcul_lot,
                                 self.Label_Take_profit_calcul_lot]
        self.label_neutre = [self.Label_MT_entrée, self.Label_MT_différée, self.Label_Lot, self.Label_choix_manager,
                             self.Label_MT_sl_tp_fast, self.label_SL, self.label_TP, self.label_nb_changement,
                             self.label_nb_ordre_fermé, self.label_account_calcul_dd, self.label_trade_avant_pallier1,
                             self.label_risque_base, self.label_trade_avant_pallier2,
                             self.label_division_risque_pallier1, self.label_trade_avant_pallier3,
                             self.label_division_risque_pallier2, self.label_trade_avant_pallier4,
                             self.label_division_risque_pallier3, self.label_trade_avant_pallier5,
                             self.label_division_risque_pallier4, self.label_trade_après_pallier5,
                             self.label_division_risque_pallier5]
        self.label_vérication = [self.verification_validation_calcul]
        self.label_OK = [self.label_OK1_DD, self.label_OK2_DD, self.label_OK3_DD, self.label_OK4_DD, self.label_OK5_DD,
                         self.label_OK6_DD, self.label_OK7_DD, self.label_OK8_DD, self.label_OK9_DD, self.label_OK10_DD,
                         self.label_OK11_DD, self.label_OK12_DD, self.label_OK13_DD]

        if self.couleur == "none":
            pass
        elif self.couleur == "white":
            self.tabs.setStyleSheet(theme_clair_background)
            self.setStyleSheet(theme_clair_widgets)
            self.fct_appliquer_style(style=style_label_obligatoire_clair, widgets=self.label_obligatoire)
            self.fct_appliquer_style(style=style_label_vérification_clair, widgets=self.label_vérication)
            self.fct_appliquer_style(style=style_label_facultatif_clair, widgets=self.label_facultatif)
            self.fct_appliquer_style(style=style_label_neutre_clair, widgets=self.label_neutre)
            self.fct_appliquer_style(style=style_label_OK_clair, widgets=self.label_OK)
        elif self.couleur == "sombre":
            self.tabs.setStyleSheet(theme_sombre_background)
            self.setStyleSheet(theme_sombre_widgets)
            self.fct_appliquer_style(style=style_label_obligatoire_sombre, widgets=self.label_obligatoire)
            self.fct_appliquer_style(style=style_label_vérification_sombre, widgets=self.label_vérication)
            self.fct_appliquer_style(style=style_label_facultatif_sombre, widgets=self.label_facultatif)
            self.fct_appliquer_style(style=style_label_neutre_sombre, widgets=self.label_neutre)
            self.fct_appliquer_style(style=style_label_OK_sombre, widgets=self.label_OK)
        elif self.couleur == "nature":
            self.tabs.setStyleSheet(theme_nature_background)
            self.setStyleSheet(theme_nature_widgets)
            self.fct_appliquer_style(style=style_label_obligatoire_nature, widgets=self.label_obligatoire)
            self.fct_appliquer_style(style=style_label_vérification_nature, widgets=self.label_vérication)
            self.fct_appliquer_style(style=style_label_facultatif_nature, widgets=self.label_facultatif)
            self.fct_appliquer_style(style=style_label_neutre_nature, widgets=self.label_neutre)
            self.fct_appliquer_style(style=style_label_OK_nature, widgets=self.label_OK)

    # cachement du label_dradown en fonction de la mise en marche

        if self.Activation_stratégie.text() == "Activer stratégie drawdown":
            self.Label_DrawDown_Calcul_lot.setHidden(True)
            self.Label_DrawDown_Entrée.setHidden(True)
            self.Label_DrawDown_Différé.setHidden(True)

        elif self.Activation_stratégie.text() == "Desactiver stratégie drawdown":
            self.Label_DrawDown_Différé.setHidden(False)
            self.Label_DrawDown_Entrée.setHidden(False)
            self.Label_DrawDown_Calcul_lot.setHidden(False)

    # Fonction servant à changer le titre de la fenêtre en fonction de l'onglet
    def change_titre_onglet(self):
        if self.tabs.currentIndex() == 0:
            self.setWindowTitle("Gear Secondo!/Ordre Direct")
        elif self.tabs.currentIndex() == 1:
            self.setWindowTitle("Gear Secondo!/Ordre Différé")
        elif self.tabs.currentIndex() == 2:
            self.setWindowTitle("Gear Secondo!/Calculer le lot")
        elif self.tabs.currentIndex() == 3:
            self.setWindowTitle("Gear Secondo!/ Management rapide trade")
        elif self.tabs.currentIndex() == 4:
            self.setWindowTitle("Gear Secondo!/ Stratégie de DD")
        elif self.tabs.currentIndex() == 5:
            self.setWindowTitle("Gear Secondo!/Annonces économique")

    def Acheter_instantanée(self):
        if self.Lot_direct.value() == 0:
            Message = QMessageBox.critical(self, 'Lot error', 'veuillez rentrer un nombre valide de lot', buttons=
            QMessageBox.Ok)
        else:
            Take_profit = self.Take_profit_direct.value()
            Stop_Loss = self.Stop_loss_direct.value()
            Nombre_partielle = self.Nombre_partiel_direct.value()
            Lots = self.Lot_direct.value()
            type_ordre = "achat"
            if self.Radio_MT4_entrée.isChecked():
                execution_direct(lot=Lots, SL=Stop_Loss, nb_partiel=Nombre_partielle, vente_ou_achat=type_ordre,
                                 TP=Take_profit)
            elif self.Radio_MT5_entrée.isChecked():
                execution_direct_MT5(lot=float(Lots), SL=float(Stop_Loss),
                                     nb_partiel=int(Nombre_partielle), vente_ou_achat=type_ordre,
                                     TP=float(Take_profit))

    def Vendre_instantanée(self):
        if self.Lot_direct.value() == 0:
            Message = QMessageBox.critical(self, 'Lot error', 'veuillez rentrer un nombre valide de lot', buttons=
            QMessageBox.Ok)


        else:
            Take_profit = self.Take_profit_direct.value()
            Stop_Loss = self.Stop_loss_direct.value()
            Nombre_partiel = self.Nombre_partiel_direct.value()
            Lots = self.Lot_direct.value()
            type_ordre = "vente"
            if self.Radio_MT4_entrée.isChecked():
                execution_direct(lot=float(Lots), SL=float(Stop_Loss), nb_partiel=int(Nombre_partiel),
                                 vente_ou_achat=type_ordre, TP=float(Take_profit))
            elif self.Radio_MT5_entrée.isChecked():
                execution_direct_MT5(lot=float(Lots), SL=float(Stop_Loss), nb_partiel=int(Nombre_partiel),
                                     vente_ou_achat=type_ordre, TP=float(Take_profit))

    def Position_différée(self):
        if self.lot_différé.value() == 0:
            Message_error_lot = QMessageBox.critical(self, 'Lot error',
                                                     'Veuillez rentrer un nombre valide de lot: nombre de lot ne peut pas être égale à 0.',
                                                     buttons=
                                                     QMessageBox.Ok)
        elif self.prix_entrée.value() == 0:
            Message_erreur_entrée = QMessageBox.critical(self, 'Entrée invalide!',
                                                         'Le prix d\'entré ne peut pas être égal à 0.',
                                                         buttons=QMessageBox.Ok)
        else:
            Entrée = self.prix_entrée.value()
            Take_Profit = self.Take_profit_différée.value()
            Stop_Loss = self.Stop_loss_différée.value()
            Nombre_partiel = self.Nombre_partiel_direct.value()
            Lots = self.lot_différé.value()
            type_ordre = self.Liste_ordres.currentText()
            Prix_Stop_Limit = 0
            if type_ordre == "Buy Stop Limit" or type_ordre == "Sell Stop Limit":
                Prix_Stop_Limit = self.Prix_Stop_Limit.value()
            # vérification que les entrées soient bonnes pour chaque type d'ordre.
            # Pour Buy Stop
            if type_ordre == "Buy Stop" and Stop_Loss != 0 and Stop_Loss >= Entrée - 0.00001:
                message = QMessageBox.critical(self, 'Stop Loss Invalide',
                                               'Votre Stop loss est supérieur à votre entrée.', buttons=QMessageBox.Ok)
            elif type_ordre == "Buy Stop" and Take_Profit != 0 and Take_Profit <= Entrée:
                message = QMessageBox.critical(self, 'Take Profit invalide',
                                               "Votre Take profit se situe en dessous du niveau d'entrée.",
                                               buttons=QMessageBox.Ok)
            # Pour Sell Stop
            elif type_ordre == "Sell Stop" and Stop_Loss != 0 and Stop_Loss <= Entrée + 0.00001:
                message = QMessageBox.critical(self, 'Stop Loss Invalide',
                                               "Votre Stop loss est inférieur à votre niveau d'entrée",
                                               buttons=QMessageBox.Ok)
            elif type_ordre == "Sell Stop" and Take_Profit != 0 and Take_Profit >= Entrée:
                message = QMessageBox.critical(self, "Take Profit Invalid",
                                               "Votre Take profit est supérieur au niveau d'entrée",
                                               buttons=QMessageBox.Ok)
            # Pour Buy_Limit
            elif type_ordre == "Buy Limit" and Stop_Loss != 0 and Stop_Loss >= Entrée:
                message = QMessageBox.critical(self, "Stop Loss Invalid",
                                               "Votre Stop loss est inférieur au niveau d'entrée",
                                               buttons=QMessageBox.Ok)
            elif type_ordre == "Buy Limit" and Take_Profit != 0 and Take_Profit >= Entrée:
                message = QMessageBox.critical(self, "Take Profit Invalid",
                                               "Votre Take Profit est inférieur au niveau d'entrée",
                                               buttons=QMessageBox.Ok)
            # Pour Sell Limit
            elif type_ordre == "Sell Limit" and Stop_Loss != 0 and Stop_Loss <= Entrée:
                message = QMessageBox.critical(self, "Stop Loss Invalid",
                                               "Votre Stop loss est supérieur au niveau de l'entrée",
                                               buttons=QMessageBox.Ok)
            elif type_ordre == "Sell Limit" and Take_Profit != 0 and Take_Profit <= Entrée:
                message = QMessageBox.critical(self, "Take Profit Invalid",
                                               "Votre Take profit est inférieur au niveau de l'entrée",
                                               buttons=QMessageBox.Ok)
            elif type_ordre == "Sell Stop Limit" and Entrée >= Prix_Stop_Limit:
                message = QMessageBox.critical(self, "Prix Stop Limit invalid",
                                               "Votre Prix Stop Limit est invalide , celui ci doit être supérieur à l\'entrée",
                                               buttons=QMessageBox.Ok)
            elif type_ordre == "Sell Stop Limit" and Stop_Loss != 0 and Stop_Loss >= Entrée:
                message = QMessageBox.critical(self, "Prix Stop Loss invalid",
                                               "SL invalide celui ci doit être inférieur au niveau d'entrée",
                                               buttons=QMessageBox.Ok)
            elif type_ordre == "Sell Stop Limit" and Take_Profit != 0 and Take_Profit <= Entrée:
                message = QMessageBox.critical(self, "Take Profit invalid",
                                               "Take Profit invalide celui ci doit être supérieur au niveau d'entrée",
                                               buttons=QMessageBox.Ok)
            elif type_ordre == "Buy Stop Limit" and Entrée <= Prix_Stop_Limit:
                message = QMessageBox.critical(self, "Prix Stop Limit invalid",
                                               "Votre Prix Stop Limit doit être inférieur à votre niveau d'entrée",
                                               buttons=QMessageBox.Ok)
            elif type_ordre == "Buy Stop Limit" and Take_Profit != 0 and Take_Profit <= Entrée:
                message = QMessageBox.critical(self, "Take Profit invalid",
                                               "Votre Take Profit doit être supérieur à votre prix d'entrée",
                                               buttons=QMessageBox.Ok)
            elif type_ordre == "Buy Stop Limit" and Stop_Loss != 0 and Stop_Loss >= Entrée:
                message = QMessageBox.critical(self, "Stop Loss invalid",
                                               "Votre Take Profit doit être supérieur à votre prix d'entrée",
                                               buttons=QMessageBox.Ok)

            # Validation
            else:

                Confirmation_envoie = QMessageBox.question(self, f'Confirmation',
                                                           f'Entrée:{Entrée}\nLots:{Lots}\nNombre_partielle:{Nombre_partiel}\n '
                                                           f'type d\'ordre:{type_ordre}\nSL:{Stop_Loss}\nTP:{Take_Profit}\n Appuyer sur Yes pour confirmer',

                                                           buttons=QMessageBox.Yes | QMessageBox.No)
                if Confirmation_envoie == QMessageBox.Yes:
                    if self.Radio_MT4_différée.isChecked():
                        execution_différé(lot=float(Lots), entrée=float(Entrée), nb_partiel=int(Nombre_partiel),
                                          SL=float(Stop_Loss), TP=float(Take_Profit), type_ordre=type_ordre)
                    elif self.Radio_MT5_différée.isChecked():

                        execution_différé_MT5(lot=float(Lots), entrée=float(Entrée), nb_partiel=int(Nombre_partiel),
                                              SL=float(Stop_Loss), TP=float(Take_Profit), type_ordre=type_ordre,
                                              Prix_Stop_Limit=float(Prix_Stop_Limit))

    # fonction signaux de calcul de risque et lot

    def click_btn_calcul_lot(self):

        valeur_pips = self.valeur_pips.value()
        montant = self.account_montant.value()

        risque = self.risque_pourcentage.value()
        Commision = self.Commision.value()
        taille_SL = self.taille_SL.value()

        if risque == 0 or taille_SL == 0 or valeur_pips == 0:

            if risque == 0:

                self.verification_validation_calcul.setText("INVALIDATION:RISQUE EST EGALE A 0.")

            elif taille_SL == 0:
                self.verification_validation_calcul.setText("INVALIDATION:TAILLE SL EST EGALE A 0")

            elif valeur_pips == 0:
                self.verification_validation_calcul.setText("INVALIDATION:VALEUR PIPS EST EGALE A 0")


        else:
            lot = (montant * risque / 100) / taille_SL / valeur_pips

            nombre_argent_par_lot = montant / lot

            risque_lot = nombre_argent_par_lot * (risque / 100)

            Risque_etCommision = (Commision + risque_lot) * lot

            risque_en_argent = montant * (risque / 100)
            lot_réél = (risque_en_argent / Risque_etCommision) * lot
            self.Lot.setValue(round(lot_réél, 2))

            # ajout des valeurs de quand on calcul le lot aux autres onglets
            if self.Take_profit_calcul_lot.value() != 0:
                self.Take_profit_direct.setValue(self.Take_profit_calcul_lot.value())
                self.Take_profit_différée.setValue(self.Take_profit_calcul_lot.value())
            if self.Stop_loss_calcul_lot.value() != 0:
                self.Stop_loss_direct.setValue(self.Stop_loss_calcul_lot.value())
                self.Stop_loss_différée.setValue(self.Stop_loss_calcul_lot.value())
            if self.Entrée_calcul_lot.value() != 0:
                self.prix_entrée.setValue(self.Entrée_calcul_lot.value())
            self.lot_différé.setValue(round(lot_réél, 2))
            self.Lot_direct.setValue(round(lot_réél, 2))
            self.verification_validation_calcul.setText("Calcul de lot réussi")

            # changer la valeur du compte par défault si modifier
            c=sqlite3.connect('DB.sq3')
            cursor=c.cursor()
            cursor.execute("SELECT compte_av_dd FROM parametre_DD_activation")
            compte_av_dd = cursor.fetchone()[0]
            cursor.execute("SELECT value FROM parametre_default WHERE type='account'")

            account_courant = cursor.fetchone()[0]
            if montant != account_courant:
                sql="UPDATE parametre_default SET value=? WHERE type='account'"
                cursor.execute(sql,[montant])
                c.commit()
                #UPDATE A FAIRE------------------------------------------------>>>>>>>
            if montant > compte_av_dd:
                sql="UPDATE parametre_DD_activation SET compte_av_dd=?"
                cursor.execute(sql,[montant])
                c.commit()
            drawdown = round(100 - ((montant / compte_av_dd) * 100), 2)

            if montant < compte_av_dd:
                sql = "UPDATE parametre_DD_activation SET pourcentage_DD=?"
                cursor.execute(sql,[drawdown])
                c.commit()
            c.close()

    # fonctions signaux coordination champs entrée/différé

    # direct
    def Change_TP_direct(self):
        current = self.Take_profit_différée.value()
        self.Take_profit_direct.setValue(current)

    def Change_Lot_direct(self):
        current = self.lot_différé.value()
        self.Lot_direct.setValue(current)

    def Change_Stop_loss_direct(self):
        current = self.Stop_loss_différée.value()
        self.Stop_loss_direct.setValue(current)

    def Change_nombre_partiel_direct(self):
        current = self.Nombre_partiel_différée.value()
        self.Nombre_partiel_direct.setValue(current)

    # différé
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
        current = self.Nombre_partiel_direct.value()
        self.Nombre_partiel_différée.setValue(current)

    # fonction pour afficher fenêtre pour changer les pips des devises
    def Affichage_fenetre_changer_pips(self):
        self.w = ChangerPipsWindow()
        self.w.resize(300, 100)
        self.w.show()

    # fonction pour afficher fenêtre ajouter paire

    def fct_ajouter_paire(self):
        self.w = AjouterPaireWindow()
        self.w.resize(300, 100)
        self.w.show()

    # fonction pour afficher fenêtre supprimer paire
    def supprimer_paire(self):
        self.w = Supprimer_devise_Windows()
        self.w.resize(300, 100)
        self.w.show()

        # fonction pour afficher fenetre commision_par_default


    def fct_modifier_paramètre_default(self):
        self.w = Modifier_paramètre_default_Window()
        self.w.resize(300, 200)
        self.w.show()

    def fct_Activer_Musique_Timer(self):
        c=sqlite3.connect("DB.sq3")
        cu=c.cursor()
        activation_musique=cu.execute("SELECT value FROM parametre_default WHERE type='activation_musique_timer'")
        activation=activation_musique.fetchone()[0]
        print(activation)
        if activation=="True":
            self.Activer_Musique_Timer.setText("Activer musique")
            cu.execute("UPDATE parametre_default SET value='False' WHERE type=='activation_musique_timer'")
            if self.sound_annonce.isPlaying():
                self.sound_annonce.stop()
        else:
            self.Activer_Musique_Timer.setText("Arrêter musique")
            cu.execute("UPDATE parametre_default SET value='True' WHERE type=='activation_musique_timer'")

        c.commit()
        c.close()

    # fonction pour actualiser window , bouton dans barre d'outils

    def fct_Actualiser(self):
        connexion = sqlite3.connect("DB.sq3")
        cursor = connexion.cursor()

        # valeur par default de la table parametre_default
        cursor.execute("SELECT value FROM parametre_default WHERE type='commission'")
        value_commission = cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='account'")
        value_account = cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='paire'")
        value_paire = cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='nombre de partiel'")
        value_partiel = cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='Entree'")
        value_entrée = cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='Stop Loss'")
        value_SL = cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='couleur'")
        couleur = cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='metatrader'")
        value_metatrader = cursor.fetchone()[0]
        cursor.execute("SELECT value FROM parametre_default WHERE type='ordre manager'")
        manager_trade = cursor.fetchone()[0]
        cursor.execute(f"SELECT valeur_pip FROM Valeur_pip WHERE paire=?",[value_paire])
        value_pip=cursor.fetchone()[0]
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

        # valeur de la table  parametre_DD _activation

        cursor.execute("SELECT mise_en_marche FROM parametre_DD_activation")
        mise_en_marche = cursor.fetchone()[0]

        cursor.execute("SELECT compte_av_dd FROM parametre_DD_activation")
        value_av_drawdown = cursor.fetchone()[0]
        cursor.execute("SELECT pourcentage_DD FROM parametre_DD_activation")
        pourcentage_DD = cursor.fetchone()[0]

        drawdown = round(100 - (self.value_account / self.value_av_drawdown) * 100, 2)

        # liste des paires
        cursor.execute("SELECT paire FROM Valeur_pip")
        liste_items = []
        p = cursor.fetchone()
        while p is not None:
            liste_items.append(p[0])
            p = cursor.fetchone()
        connexion.close()

        if value_metatrader == "mt4":
            self.Radio_MT4_entrée.setChecked(True)
            self.Radio_MT4_différée.setChecked(True)
            self.Radio_MT4_sl_tp_fast.setChecked(True)
        elif value_metatrader == "mt5":
            self.Radio_MT5_entrée.setChecked(True)
            self.Radio_MT5_différée.setChecked(True)
            self.Radio_MT5_sl_tp_fast.setChecked(True)

        self.combobox_paires.clear()
        self.combobox_paires.addItems(liste_items)
        self.combobox_paires.setCurrentText(value_paire)
        value_paire = self.combobox_paires.currentText()


        self.Stop_loss_calcul_lot.setValue(value_SL)
        self.Entrée_calcul_lot.setValue(value_entrée)
        self.Commision.setValue(value_commission)
        self.valeur_pips.setValue(value_pip)
        self.prix_entrée.setValue(value_entrée)
        self.Nombre_partiel_différée.setValue(value_partiel)
        self.Nombre_partiel_direct.setValue(value_partiel)
        self.account_montant.setValue(value_account)

        # actualiser l'onglet strategie DD
        self.account_dd_av_actuel.setValue(value_av_drawdown)
        self.risque_de_base.setValue(pallier0_risque)
        self.division_risque_pallier1.setValue(pallier1_risque)
        self.division_risque_pallier2.setValue(pallier2_risque)
        self.division_risque_pallier3.setValue(pallier3_risque)
        self.division_risque_pallier4.setValue(pallier4_risque)
        self.division_risque_pallier5.setValue(pallier5_risque)
        self.trade_avant_pallier1.setValue(pallier0_trade_pris)
        self.trade_avant_pallier2.setValue(pallier1_trade_pris)
        self.trade_avant_pallier3.setValue(pallier2_trade_pris)
        self.trade_avant_pallier4.setValue(pallier3_trade_pris)
        self.trade_avant_pallier5.setValue(pallier4_trade_pris)
        self.trade_après_pallier5.setValue(pallier5_trade_pris)
        self.trade_perte1.setText('')
        self.trade_perte2.setText('')
        self.trade_perte3.setText('')
        self.trade_perte4.setText('')
        self.trade_perte5.setText('')
        self.trade_perte_après5.setText('')

        # fonction pour changer le label drowdown lorsque l'on actualise et qu'on a changer la strategie de DD
        drawdown = round(100 - (value_account / value_av_drawdown) * 100, 2)

        if drawdown < pallier1_activation:
            self.risque_pourcentage.setValue(pallier0_risque)
            self.changer_label_drawdown("0", drawdown, value_av_drawdown)
        elif pallier1_activation < drawdown < pallier2_activation:
            self.risque_pourcentage.setValue(pallier1_risque)
            self.changer_label_drawdown("1", drawdown, value_av_drawdown)
        elif pallier2_activation < drawdown < pallier3_activation:
            self.risque_pourcentage.setValue(pallier2_risque)
            self.changer_label_drawdown("2", drawdown, value_av_drawdown)
        elif pallier3_activation < drawdown < pallier4_activation:
            self.risque_pourcentage.setValue(pallier3_risque)
            self.changer_label_drawdown("3", drawdown, value_av_drawdown)
        elif pallier4_activation < drawdown < pallier5_activation:
            self.risque_pourcentage.setValue(pallier4_risque)
            self.changer_label_drawdown("4", drawdown, value_av_drawdown)
        elif drawdown > pallier5_activation:
            self.risque_pourcentage.setValue(pallier5_risque)
            self.changer_label_drawdown("5", drawdown, value_av_drawdown)

    # fonction pour changer la valeur du pips lorsque l'on change le combobox

    def Change_paires_valeur_pip(self):
        c=sqlite3.connect("DB.sq3")
        cu=c.cursor()
        sql="SELECT valeur_pip FROM Valeur_pip WHERE paire=?"
        combobox= self.combobox_paires.currentText()
        cu.execute(sql,[combobox])
        paire=cu.fetchone()[0]
        self.valeur_pips.setValue(paire)



        c.close()

    # fonction permettant de faire des changement lorsque l'on change RadioMT4 et MT5 d'entrée
    def change_Radio_entrée(self):
        button = self.sender()
        if button == self.Radio_MT4_entrée:
            self.Liste_ordres.clear()
            self.Liste_ordres.addItems(
                ['Buy Stop', 'Sell Stop', 'Buy Limit', 'Sell Limit'])
            self.Radio_MT4_différée.setChecked(True)
            self.Radio_MT5_différée.setChecked(False)
            self.Radio_MT4_sl_tp_fast.setChecked(True)
            self.Radio_MT5_sl_tp_fast.setChecked(False)
            self.Prix_Stop_Limit.setHidden(True)
            self.Prix_Stop_Limit.setHidden(True)


        elif button == self.Radio_MT5_entrée:
            self.Liste_ordres.clear()
            self.Liste_ordres.addItems(
                ['Buy Stop', 'Sell Stop', 'Buy Limit', 'Sell Limit', "Sell Stop Limit", "Buy Stop Limit"])
            self.Radio_MT4_différée.setChecked(False)
            self.Radio_MT5_différée.setChecked(True)
            self.Radio_MT4_sl_tp_fast.setChecked(False)
            self.Radio_MT5_sl_tp_fast.setChecked(True)
            self.Prix_Stop_Limit.setHidden(False)
            self.Label_Prix_Stop_Limit.setHidden(False)

    # fonction permettant de faire des changement lorsque l'on change RadioMT4MT5 différée
    def change_Radio_différée(self):
        button = self.sender()
        if button == self.Radio_MT4_différée:
            self.Liste_ordres.clear()
            self.Liste_ordres.addItems(['Buy Stop', 'Sell Stop', 'Buy Limit', 'Sell Limit'])
            self.Radio_MT4_entrée.setChecked(True)
            self.Radio_MT5_entrée.setChecked(False)
            self.Radio_MT4_sl_tp_fast.setChecked(True)
            self.Radio_MT5_sl_tp_fast.setChecked(False)
            self.Prix_Stop_Limit.setHidden(True)
            self.Label_Prix_Stop_Limit.setHidden(True)

        elif button == self.Radio_MT5_différée:
            self.Liste_ordres.clear()
            self.Liste_ordres.addItems(
                ['Buy Stop', 'Sell Stop', 'Buy Limit', 'Sell Limit', "Sell Stop Limit", "Buy Stop Limit"])
            self.Radio_MT4_entrée.setChecked(False)
            self.Radio_MT5_entrée.setChecked(True)
            self.Radio_MT4_sl_tp_fast.setChecked(False)
            self.Radio_MT5_sl_tp_fast.setChecked(True)
            self.Prix_Stop_Limit.setHidden(False)
            self.Label_Prix_Stop_Limit.setHidden(False)

    # fonction permettant de faire des changement lorsque l'on change RadioMT4MT5 fast_sl_tp
    def change_Radio_change_fast(self):
        button = self.sender()
        if button == self.Radio_MT4_sl_tp_fast:
            self.Liste_ordres.clear()
            self.Liste_ordres.addItems(['Buy Stop', 'Sell Stop', 'Buy Limit', 'Sell Limit'])
            self.Radio_MT4_entrée.setChecked(True)
            self.Radio_MT5_entrée.setChecked(False)
            self.Radio_MT4_différée.setChecked(True)
            self.Radio_MT5_différée.setChecked(False)
            self.Prix_Stop_Limit.setHidden(True)
            self.Label_Prix_Stop_Limit.setHidden(True)

        elif button == self.Radio_MT5_sl_tp_fast:
            self.Liste_ordres.clear()
            self.Liste_ordres.addItems(
                ['Buy Stop', 'Sell Stop', 'Buy Limit', 'Sell Limit', "Sell Stop Limit", "Buy Stop Limit"])
            self.Radio_MT4_entrée.setChecked(False)
            self.Radio_MT5_entrée.setChecked(True)
            self.Radio_MT4_différée.setChecked(False)
            self.Radio_MT5_différée.setChecked(True)
            self.Prix_Stop_Limit.setHidden(False)
            self.Label_Prix_Stop_Limit.setHidden(False)

    # fonction  qui rendant visible ou ecrivable le widget Prix_Stop_Limit quand on
    # modifie combobox type ordre sur certaine valeur
    def change_type_ordre(self):

        if self.Radio_MT5_entrée.isChecked():
            ordre = self.Liste_ordres.currentText()
            if ordre == 'Sell Stop Limit' or ordre == "Buy Stop Limit":
                self.Prix_Stop_Limit.setDisabled(False)
            else:
                self.Prix_Stop_Limit.setDisabled(True)

    # barre d'outils Drawdown

    def fct_modifier_pallier(self):
        self.w = modifier_pallier_Window()
        self.w.resize(300, 200)
        self.w.show()

    # calcul DD lorsque l'on change la valeur du compte et change le risque automatiquement
    def Calcul_drawdown(self):
        # créer une condition si le bouton de statégie de DrawDown est activé
        connexion=sqlite3.connect("DB.sq3")
        cursor=connexion.cursor()
        cursor.execute("SELECT compte_av_dd FROM parametre_DD_activation")
        value_compte_courant=cursor.fetchone()[0]
        cursor.execute("SELECT mise_en_marche FROM parametre_DD_activation")
        value_mise_en_marche=cursor.fetchone()[0]


        if value_mise_en_marche == True:
            value_compte = self.account_montant.value()
            # calculer drawdown
            drawdown = round(100 - ((value_compte / value_compte_courant) * 100), 2)

            # valeur importante
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

            # pallier2
            cursor.execute("SELECT activation FROM DD WHERE pallier=2")
            pallier2_activation = cursor.fetchone()[0]
            cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=2")
            pallier2_risque = cursor.fetchone()[0]

            # pallier3
            cursor.execute("SELECT activation FROM DD WHERE pallier=2")
            pallier3_activation = cursor.fetchone()[0]
            cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=3")
            pallier3_risque = cursor.fetchone()[0]

            # pallier4
            cursor.execute("SELECT activation FROM DD WHERE pallier=4")
            pallier4_activation = cursor.fetchone()[0]
            cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=4")
            pallier4_risque = cursor.fetchone()[0]

            # pallier5
            cursor.execute("SELECT activation FROM DD WHERE pallier=5")
            pallier5_activation = cursor.fetchone()[0]
            cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=5")
            pallier5_risque = cursor.fetchone()[0]
            connexion.close()

            if drawdown < pallier1_activation:
                self.risque_pourcentage.setValue(pallier0_risque)
                self.changer_label_drawdown("0", drawdown, value_compte_courant)
            elif pallier1_activation <= drawdown < pallier2_activation:

                self.risque_pourcentage.setValue(pallier1_risque)
                self.changer_label_drawdown("1", drawdown, value_compte_courant)
            elif pallier2_activation <= drawdown < pallier3_activation:
                self.risque_pourcentage.setValue(pallier2_risque)
                self.changer_label_drawdown("2", drawdown, value_compte_courant)
            elif pallier3_activation <= drawdown < pallier4_activation:
                self.risque_pourcentage.setValue(pallier3_risque)
                self.changer_label_drawdown("3", drawdown, value_compte_courant)
            elif pallier4_activation <= drawdown < pallier5_activation:
                self.risque_pourcentage.setValue(pallier4_risque)
                self.changer_label_drawdown("4", drawdown, value_compte_courant)
            elif drawdown >= pallier5_activation:
                self.risque_pourcentage.setValue(pallier5_risque)
                self.changer_label_drawdown("5", drawdown, value_compte_courant)

    def changer_label_drawdown(self, value, drowdown, compte_avant_dd):
        connexion = sqlite3.connect("DB.sq3")
        cursor = connexion.cursor()
        cursor.execute("SELECT mise_en_marche FROM parametre_DD_activation")
        mise_en_marche = cursor.fetchone()[0]
        connexion.close()



        self.Label_DrawDown_Entrée.setText(f"DrawDown {value}: {drowdown}%   | Compte avant DD:{compte_avant_dd}")
        self.Label_DrawDown_Différé.setText(f"DrawDown {value}: {drowdown}%   | Compte avant DD:{compte_avant_dd}")
        self.Label_DrawDown_Calcul_lot.setText(
            f"DrawDown {value}: {drowdown}%   | Compte avant DD:{compte_avant_dd}")

        if value == "0":

            self.Label_DrawDown_Entrée.setStyleSheet("""color: #03d894 ;font: bold 14px""")
            self.Label_DrawDown_Différé.setStyleSheet("""color: #03d894 ;font: bold 14px""")
            self.Label_DrawDown_Calcul_lot.setStyleSheet("""color: #03d894 ;font: bold 14px""")
        elif value == "1":
            self.Label_DrawDown_Entrée.setStyleSheet("""color:#e4c817;font: bold 14px""")
            self.Label_DrawDown_Différé.setStyleSheet("""color:#e4c817;font: bold 14px""")
            self.Label_DrawDown_Calcul_lot.setStyleSheet("""color:#e4c817;font: bold 14px""")
        elif value == "2":
            self.Label_DrawDown_Entrée.setStyleSheet("""color:#e4af17;font: bold 14px""")
            self.Label_DrawDown_Différé.setStyleSheet("""color:#e4af17;font: bold 14px""")
            self.Label_DrawDown_Calcul_lot.setStyleSheet("""color:#e4af17;font: bold 14px""")
        elif value == "3":
            self.Label_DrawDown_Entrée.setStyleSheet("""color:#d9730c;font: bold 14px""")
            self.Label_DrawDown_Différé.setStyleSheet("""color:#d9730c;font: bold 14px""")
            self.Label_DrawDown_Calcul_lot.setStyleSheet("""color:#d9730c;font: bold 14px""")
        elif value == "4":
            self.Label_DrawDown_Entrée.setStyleSheet("""color: #c84405 ;font: bold 14px""")
            self.Label_DrawDown_Différé.setStyleSheet("""color: #c84405 ;font: bold 14px""")
            self.Label_DrawDown_Calcul_lot.setStyleSheet("""color: #c84405 ;font: bold 14px""")
        elif value == "5":
            self.Label_DrawDown_Entrée.setStyleSheet("""color:#e50000;font: bold 14px""")
            self.Label_DrawDown_Différé.setStyleSheet("""color:#e50000;font: bold 14px""")
            self.Label_DrawDown_Calcul_lot.setStyleSheet("""color:#e50000;font: bold 14px""")

    # fonction qui permet de désactiver ou activer la stratégie de DD
    def activation_Strategie_DD(self):

        c=sqlite3.connect("DB.sq3")
        cu=c.cursor()
        cu.execute("SELECT risque_pourcentage FROM DD WHERE pallier=0")
        if self.Activation_stratégie.text() == "Activer stratégie drawdown":
            self.Activation_stratégie.setText("Desactiver stratégie drawdown")
            self.Label_DrawDown_Calcul_lot.setHidden(False)
            self.Label_DrawDown_Entrée.setHidden(False)
            self.Label_DrawDown_Différé.setHidden(False)
            self.risque_pourcentage.setValue(cu.fetchone()[0])
            cu.execute("UPDATE parametre_DD_activation SET mise_en_marche=1")

        elif self.Activation_stratégie.text() == "Desactiver stratégie drawdown":
            self.Activation_stratégie.setText("Activer stratégie drawdown")
            self.Label_DrawDown_Différé.setHidden(True)
            self.Label_DrawDown_Entrée.setHidden(True)
            self.Label_DrawDown_Calcul_lot.setHidden(True)
            cu.execute("UPDATE parametre_DD_activation SET mise_en_marche=0")
        c.commit()
        c.close()
    def remise_zero_strategie_DD(self):
        c=sqlite3.connect("DB.sq3")
        cu=c.cursor()
        cu.execute("SELECT value FROM parametre_default WHERE type='account'")
        account=cu.fetchone()[0]
        confirmation = QMessageBox.question(self, "Remettre à zéro stratégie de drawdown",
                                            "Voulez vous remmettre à 0 votre stratégie de drawdown? Votre drawdown sera remis à 0.",
                                            buttons=(QMessageBox.Yes | QMessageBox.No))
        if confirmation == QMessageBox.Yes:
            cu.execute("UPDATE parametre_DD_activation SET compte_av_dd=?",[account])
            self.changer_label_drawdown(0, 0, account)
        c.commit()
        c.close()

    # créer des modes de couleurs qu'on peit régler avec une fenetre dans les parametre:sombre/normal/fete
    # ex: W_entrée_directe.setStyleSheet("background-color:black")
    def change_mode_white(self):
        self.tabs.setStyleSheet(theme_clair_background)
        self.setStyleSheet(theme_clair_widgets)
        self.fct_appliquer_style(style=style_label_obligatoire_clair, widgets=self.label_obligatoire)
        self.fct_appliquer_style(style=style_label_vérification_clair, widgets=self.label_vérication)
        self.fct_appliquer_style(style=style_label_facultatif_clair, widgets=self.label_facultatif)
        self.fct_appliquer_style(style=style_label_neutre_clair, widgets=self.label_neutre)
        self.fct_appliquer_style(style=style_label_OK_clair, widgets=self.label_OK)
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        cu.execute("UPDATE parametre_default SET value='white' WHERE type='couleur'")
        c.commit()
        c.close()


    def change_mode_sombre(self):
        self.tabs.setStyleSheet(theme_sombre_background)
        self.setStyleSheet(theme_sombre_widgets)
        self.fct_appliquer_style(style=style_label_obligatoire_sombre, widgets=self.label_obligatoire)
        self.fct_appliquer_style(style=style_label_vérification_sombre, widgets=self.label_vérication)
        self.fct_appliquer_style(style=style_label_facultatif_sombre, widgets=self.label_facultatif)
        self.fct_appliquer_style(style=style_label_neutre_sombre, widgets=self.label_neutre)
        self.fct_appliquer_style(style=style_label_OK_sombre, widgets=self.label_OK)
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        cu.execute("UPDATE parametre_default SET value='white' WHERE type='couleur'")
        c.commit()
        c.close()

    def change_mode_nature(self):
        self.tabs.setStyleSheet(theme_nature_background)
        self.setStyleSheet(theme_nature_widgets)
        self.fct_appliquer_style(style=style_label_obligatoire_nature, widgets=self.label_obligatoire)
        self.fct_appliquer_style(style=style_label_vérification_nature, widgets=self.label_vérication)
        self.fct_appliquer_style(style=style_label_facultatif_nature, widgets=self.label_facultatif)
        self.fct_appliquer_style(style=style_label_neutre_nature, widgets=self.label_neutre)
        self.fct_appliquer_style(style=style_label_OK_nature, widgets=self.label_OK)
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        cu.execute("UPDATE parametre_default SET value='nature' WHERE type='couleur'")
        c.commit()
        c.close()

    # pour appliquer différents style aux widgets
    def fct_appliquer_style(self, style, widgets):
        for i in widgets:
            i.setStyleSheet(style)

    # methode pour l'onglet strategie DD
    # calculer perte pallier
    def fct_calculer_perte_pallier(self):
        trade_pris = self.trade_avant_pallier1.value()
        trade_pris1 = self.trade_avant_pallier2.value()
        trade_pris2 = self.trade_avant_pallier3.value()
        trade_pris3 = self.trade_avant_pallier4.value()
        trade_pris4 = self.trade_avant_pallier5.value()
        trade_pris5 = self.trade_après_pallier5.value()
        account_av = self.account_dd_av_actuel.value()
        account_dd = self.account_dd_av_actuel.value()
        risque = self.risque_de_base.value()
        risque_pallier1 = self.division_risque_pallier1.value()
        risque_pallier2 = self.division_risque_pallier2.value()
        risque_pallier3 = self.division_risque_pallier3.value()
        risque_pallier4 = self.division_risque_pallier4.value()
        risque_pallier5 = self.division_risque_pallier5.value()

        DD = 0
        for i in range(trade_pris):
            account_dd = account_dd - (account_dd * (risque / 100))
            DD = ((account_av - account_dd) / account_av) * 100
        self.trade_perte1.setText(f"Draw Down: {round(DD, 2)} / Montant du compte: {round(account_dd, 1)}")
        for i in range(trade_pris1):
            account_dd = account_dd - (account_dd * (risque_pallier1 / 100))
            DD = ((account_av - account_dd) / account_av) * 100
        self.trade_perte2.setText(f"Draw Down: {round(DD, 2)} / Montant du compte: {round(account_dd, 1)}")
        for i in range(trade_pris2):
            account_dd = account_dd - (account_dd * (risque_pallier2 / 100))
            DD = ((account_av - account_dd) / account_av) * 100
        self.trade_perte3.setText(f"Draw Down: {round(DD, 2)} / Montant du compte: {round(account_dd, 1)}")
        for i in range(trade_pris3):
            account_dd = account_dd - (account_dd * (risque_pallier3 / 100))
            DD = ((account_av - account_dd) / account_av) * 100
        self.trade_perte4.setText(f"Draw Down: {round(DD, 2)} / Montant du compte: {round(account_dd, 1)}")
        for i in range(trade_pris4):
            account_dd = account_dd - (account_dd * (risque_pallier4 / 100))
            DD = ((account_av - account_dd) / account_av) * 100
        self.trade_perte5.setText(f"Draw Down: {round(DD, 2)} / Montant du compte: {round(account_dd, 1)}")
        for i in range(trade_pris5):
            account_dd = account_dd - (account_dd * (risque_pallier5 / 100))
            DD = ((account_av - account_dd) / account_av) * 100
        self.trade_perte_après5.setText(f"Draw Down: {round(DD, 2)} / Montant du compte: {round(account_dd, 1)}")

    # fct  appliquer la strategie

    def fct_appliquer_strategie(self):
        trade_pris = self.trade_avant_pallier1.value()
        trade_pris1 = self.trade_avant_pallier2.value()
        trade_pris2 = self.trade_avant_pallier3.value()
        trade_pris3 = self.trade_avant_pallier4.value()
        trade_pris4 = self.trade_avant_pallier5.value()
        trade_pris5 = self.trade_après_pallier5.value()
        account_av = self.account_dd_av_actuel.value()
        account_dd = self.account_dd_av_actuel.value()
        risque = self.risque_de_base.value()
        risque_pallier1 = self.division_risque_pallier1.value()
        risque_pallier2 = self.division_risque_pallier2.value()
        risque_pallier3 = self.division_risque_pallier3.value()
        risque_pallier4 = self.division_risque_pallier4.value()
        risque_pallier5 = self.division_risque_pallier5.value()
        c=sqlite3.connect("DB.sq3")
        cu=c.cursor()
        cu.execute("UPDATE DD SET risque_pourcentage=? WHERE pallier=0",[round(risque,2)])
        cu.execute("UPDATE DD SET risque_pourcentage=? WHERE pallier=1",[round(risque_pallier1,2)])
        cu.execute("UPDATE DD SET risque_pourcentage=? WHERE pallier=2",[round(risque_pallier2,2)])
        cu.execute("UPDATE DD SET risque_pourcentage=? WHERE pallier=3",[round(risque_pallier3,2)])
        cu.execute("UPDATE DD SET risque_pourcentage=? WHERE pallier=4",[round(risque_pallier4,2)])
        cu.execute("UPDATE DD SET risque_pourcentage=? WHERE pallier=5",[round(risque_pallier5,2)])

        cu.execute("UPDATE DD SET trade_pris=? WHERE pallier=0",[trade_pris])
        cu.execute("UPDATE DD SET trade_pris=? WHERE pallier=1",[trade_pris1])
        cu.execute("UPDATE DD SET trade_pris=? WHERE pallier=2",[trade_pris2])
        cu.execute("UPDATE DD SET trade_pris=? WHERE pallier=3",[trade_pris3])
        cu.execute("UPDATE DD SET trade_pris=? WHERE pallier=4",[trade_pris4])
        cu.execute("UPDATE DD SET trade_pris=? WHERE pallier=5",[trade_pris5])


        for i in range(trade_pris):
            account_dd = account_dd - (account_dd * (risque / 100))
            DD = ((account_av - account_dd) / account_av) * 100
        cu.execute("UPDATE DD SET activation=? WHERE pallier=1",[round(DD,2)])
        for i in range(trade_pris1):
            account_dd = account_dd - (account_dd * (risque_pallier1 / 100))
            DD = ((account_av - account_dd) / account_av) * 100
        cu.execute("UPDATE DD SET activation=? WHERE pallier=2",[round(DD,2)])
        for i in range(trade_pris2):
            account_dd = account_dd - (account_dd * (risque_pallier2 / 100))
            DD = ((account_av - account_dd) / account_av) * 100
        cu.execute("UPDATE DD SET activation=? WHERE pallier=3",[round(DD,2)])
        for i in range(trade_pris3):
            account_dd = account_dd - (account_dd * (risque_pallier3 / 100))
            DD = ((account_av - account_dd) / account_av) * 100
        cu.execute("UPDATE DD SET activation=? WHERE pallier=4",[round(DD,2)])

        for i in range(trade_pris4):
            account_dd = account_dd - (account_dd * (risque_pallier4 / 100))
            DD = ((account_av - account_dd) / account_av) * 100
        cu.execute("UPDATE DD SET activation=? WHERE pallier=5",[round(DD,2)])
        c.commit()
        c.close()
        # pour update label DD
        self.fct_Actualiser()

    # fct pour afficher account_av_dd
    def afficher_account_av_dd(self):

        c=sqlite3.connect("DB.sq3")
        cu=c.cursor()
        cu.execute("SELECT compte_av_dd FROM parametre_DD_activation ")
        value_av_dd=cu.fetchone()[0]
        cu.execute("SELECT risque_pourcentage FROM DD WHERE pallier=0")
        value_rbase=cu.fetchone()[0]
        cu.execute("SELECT risque_pourcentage FROM DD WHERE pallier=0")
        value_r1 = cu.fetchone()[0]
        cu.execute("SELECT risque_pourcentage FROM DD WHERE pallier=0")
        value_r2 = cu.fetchone()[0]
        cu.execute("SELECT risque_pourcentage FROM DD WHERE pallier=0")
        value_r3 = cu.fetchone()[0]
        cu.execute("SELECT risque_pourcentage FROM DD WHERE pallier=0")
        value_r4 = cu.fetchone()[0]
        cu.execute("SELECT risque_pourcentage FROM DD WHERE pallier=0")
        value_r5 = cu.fetchone()[0]
        cu.execute("SELECT trade_pris FROM DD WHERE pallier=0")
        trade0 = cu.fetchone()[0]
        cu.execute("SELECT trade_pris FROM DD WHERE pallier=1")
        trade1 = cu.fetchone()[0]
        cu.execute("SELECT trade_pris FROM DD WHERE pallier=2")
        trade2 = cu.fetchone()[0]
        cu.execute("SELECT trade_pris FROM DD WHERE pallier=3")
        trade3 = cu.fetchone()[0]
        cu.execute("SELECT trade_pris FROM DD WHERE pallier=4")
        trade4 = cu.fetchone()[0]
        cu.execute("SELECT trade_pris FROM DD WHERE pallier=5")
        trade5 = cu.fetchone()[0]
        c.close()
        self.account_dd_av_actuel.setValue(value_av_dd)
        self.risque_de_base.setValue(value_rbase)
        self.division_risque_pallier1.setValue(value_r1)
        self.division_risque_pallier2.setValue(value_r2)
        self.division_risque_pallier3.setValue(value_r3)
        self.division_risque_pallier4.setValue(value_r4)
        self.division_risque_pallier5.setValue(value_r5)
        self.trade_avant_pallier1.setValue(trade0)
        self.trade_avant_pallier2.setValue(trade1)
        self.trade_avant_pallier3.setValue(trade2)
        self.trade_avant_pallier4.setValue(trade3)
        self.trade_avant_pallier5.setValue(trade4)
        self.trade_après_pallier5.setValue(trade5)
        self.trade_perte1.setText('')
        self.trade_perte2.setText('')
        self.trade_perte3.setText('')
        self.trade_perte4.setText('')
        self.trade_perte5.setText('')
        self.trade_perte_après5.setText('')

    # fonction pour le label ok dans l'onglet stratéfie de DD

    def fct_DD_OK(self):
        w = self.sender()
        if w == self.division_risque_pallier1:
            if self.division_risque_pallier1.value() != 0:
                self.label_OK5_DD.setText("Ok!")
            else:
                self.label_OK5_DD.setText("")
        elif w == self.division_risque_pallier2:
            if self.division_risque_pallier2.value() != 0:
                self.label_OK7_DD.setText("Ok!")
            else:
                self.label_OK7_DD.setText("")
        elif w == self.division_risque_pallier3:
            if self.division_risque_pallier3.value() != 0:
                self.label_OK9_DD.setText("Ok!")
            else:
                self.label_OK9_DD.setText("")
        elif w == self.division_risque_pallier4:
            if self.division_risque_pallier4.value() != 0:
                self.label_OK11_DD.setText("Ok!")
            else:
                self.label_OK11_DD.setText("")
        elif w == self.division_risque_pallier5:
            if self.division_risque_pallier5.value() != 0:
                self.label_OK13_DD.setText("Ok!")
            else:
                self.label_OK13_DD.setText("")
        elif w == self.risque_de_base:
            if self.risque_de_base.value() != 0:
                self.label_OK3_DD.setText("Ok!")
            else:
                self.label_OK3_DD.setText("")
        elif w == self.trade_avant_pallier1:
            if self.trade_avant_pallier1.value() != 0:
                self.label_OK2_DD.setText("Ok!")
            else:
                self.label_OK2_DD.setText("")
        elif w == self.trade_avant_pallier2:
            if self.trade_avant_pallier2.value() != 0:
                self.label_OK4_DD.setText("Ok!")
            else:
                self.label_OK4_DD.setText("")
        elif w == self.trade_avant_pallier3:
            if self.trade_avant_pallier3.value() != 0:
                self.label_OK6_DD.setText("Ok!")
            else:
                self.label_OK6_DD.setText("")
        elif w == self.trade_avant_pallier4:
            if self.trade_avant_pallier4.value() != 0:
                self.label_OK8_DD.setText("Ok!")
            else:
                self.label_OK8_DD.setText("")
        elif w == self.trade_avant_pallier5:
            if self.trade_avant_pallier5.value() != 0:
                self.label_OK10_DD.setText("Ok!")
            else:
                self.label_OK10_DD.setText("")
        elif w == self.trade_après_pallier5:
            if self.trade_après_pallier5.value() != 0:
                self.label_OK12_DD.setText("Ok!")
            else:
                self.label_OK12_DD.setText("")
        elif w == self.account_dd_av_actuel:
            if self.account_dd_av_actuel.value() != 0:
                self.label_OK1_DD.setText("Ok!")
            else:
                self.label_OK1_DD.setText("")

    # rollback ancienne strategie DD
    def fct_Rollback_strategie_DD(self):
        c=sqlite3.connect("DB.sq3")
        cursor=c.cursor()

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Rollback stratégie de DrawDown")
        dlg.setText("Voulez vous rollback la stratégie de DD?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        dlg.setStyleSheet(style_main_QMessageBox)
        confirmation = dlg.exec()

        if confirmation == QMessageBox.Yes:
            # parametre de la table_DD
            # parametre table DD
            # pallier0
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
            # parametre de la table rollback
            cursor.execute("SELECT activation FROM DD WHERE pallier=0")
            pallier0_activation = cursor.fetchone()[0]
            cursor.execute("SELECT risque_pourcentage FROM DD WHERE pallier=0")
            pallier0_risque = cursor.fetchone()[0]
            cursor.execute("SELECT trade_pris FROM DD WHERE pallier=0")
            pallier0_trade_pris = cursor.fetchone()[0]

            #parametre de la table DD_rollaback
            cursor.execute("SELECT activation FROM DD_rollback WHERE pallier=0")
            pallier0_activation_rollback = cursor.fetchone()[0]
            cursor.execute("SELECT risque FROM DD_rollback WHERE pallier=0")
            pallier0_risque_rollback = cursor.fetchone()[0]
            cursor.execute("SELECT trade_pris FROM DD WHERE pallier=0")
            pallier0_trade_pris_rollback = cursor.fetchone()[0]
            # pallier1
            cursor.execute("SELECT activation FROM DD_rollback WHERE pallier=1")
            pallier1_activation_rollback = cursor.fetchone()[0]
            cursor.execute("SELECT risque FROM DD_rollback WHERE pallier=1")
            pallier1_risque_rollback = cursor.fetchone()[0]
            cursor.execute("SELECT trade_pris FROM DD_rollback WHERE pallier=1")
            pallier1_trade_pris_rollback = cursor.fetchone()[0]
            # pallier2
            cursor.execute("SELECT activation FROM DD_rollback WHERE pallier=2")
            pallier2_activation_rollback = cursor.fetchone()[0]
            cursor.execute("SELECT risque FROM DD_rollback WHERE pallier=2")
            pallier2_risque_rollback = cursor.fetchone()[0]
            cursor.execute("SELECT trade_pris FROM DD_rollback WHERE pallier=2")
            pallier2_trade_pris_rollback = cursor.fetchone()[0]
            # pallier3
            cursor.execute("SELECT activation FROM DD WHERE pallier=2")
            pallier3_activation_rollback = cursor.fetchone()[0]
            cursor.execute("SELECT risque FROM DD_rollback WHERE pallier=3")
            pallier3_risque_rollback = cursor.fetchone()[0]
            cursor.execute("SELECT trade_pris FROM DD WHERE pallier=3")
            pallier3_trade_pris_rollback = cursor.fetchone()[0]
            # pallier4
            cursor.execute("SELECT activation FROM DD_rollback WHERE pallier=4")
            pallier4_activation_rollback = cursor.fetchone()[0]
            cursor.execute("SELECT risque FROM DD_rollback DD WHERE pallier=4")
            pallier4_risque_rollback = cursor.fetchone()[0]
            cursor.execute("SELECT trade_pris FROM DD_rollback WHERE pallier=4")
            pallier4_trade_pris_rollback = cursor.fetchone()[0]
            # pallier5
            cursor.execute("SELECT activation FROM DD_rollback WHERE pallier=5")
            pallier5_activation_rollback = cursor.fetchone()[0]
            cursor.execute("SELECT risque FROM DD_rollback WHERE pallier=5")
            pallier5_risque_rollback = cursor.fetchone()[0]
            cursor.execute("SELECT trade_pris FROM DD_rollback WHERE pallier=5")
            pallier5_trade_pris_rollback = cursor.fetchone()[0]
            # update les différents champs de la table DD
            sql = "UPDATE DD SET risque_pourcentage = ? WHERE pallier = ?"
            value=[(pallier0_risque_rollback,0),(pallier1_risque_rollback,1),(pallier2_risque_rollback,2),(pallier3_risque_rollback,3),(pallier4_risque_rollback,4),(pallier5_risque_rollback,5)]
            cursor.executemany(sql,value)
            sql = "UPDATE DD SET trade_pris = ? WHERE pallier = ?"
            value=[(pallier0_trade_pris_rollback,0),(pallier1_trade_pris_rollback,1),(pallier2_trade_pris_rollback,2),(pallier3_trade_pris_rollback,3),(pallier4_trade_pris_rollback,4),(pallier5_trade_pris_rollback,5)]
            cursor.executemany(sql,value)
            sql = "UPDATE DD SET activation = ? WHERE pallier = ?"
            value=[(pallier1_activation,1),(pallier2_activation,2),(pallier3_activation,3),(pallier4_activation,4),(pallier5_activation,5)]
            cursor.executemany(sql,value)

            # update des différents champs de la table  DD_rollaback
            sql="UPDATE DD_rollback SET risque= ? WHERE pallier= ?"
            value=[(pallier0_risque,0),(pallier1_risque,1),(pallier2_risque,2),(pallier3_risque,3),(pallier4_risque,4),(pallier5_risque,5)]
            cursor.executemany(sql,value)
            sql = "UPDATE DD_rollback SET trade_pris= ? WHERE pallier= ?"
            value=[(pallier0_trade_pris,0),(pallier1_trade_pris,1),(pallier2_trade_pris,2),(pallier3_trade_pris,3),(pallier4_trade_pris,4),(pallier5_trade_pris,5)]
            cursor.executemany(sql,value)
            sql="UPDATE DD_rollback SET activation=? WHERE pallier=?"
            value=[(pallier1_activation,1),(pallier2_activation,2),(pallier3_activation,3),(pallier4_activation,4),(pallier5_activation,5)]
            cursor.executemany(sql,value)
            c.commit()
            c.close()

            self.fct_Actualiser()


    # onglet Manager Trade
    # methode pour changer SL et TP rapidement
    def fct_changer_tp_sl_fast(self):
        TP = self.TP.value()
        SL = self.SL.value()
        nb_changement = self.nb_changement.value()
        if self.Radio_MT4_sl_tp_fast.isChecked():
            fast_change_tp_sl_mt4(nombre_à_changer=nb_changement, TP=TP, SL=SL)

        if self.Radio_MT5_sl_tp_fast.isChecked():
            fast_change_tp_sl_mt5(nombre_à_changer=nb_changement, TP=TP, SL=SL)

    # methode pour fermer les ordres rapidement
    def fct_fermer_ordre(self):
        nb = self.nb_ordre_fermé
        if self.Radio_MT4_sl_tp_fast.isChecked():
            fast_fermeture_ordre_mt4(nombre=nb)
        if self.Radio_MT5_sl_tp_fast.isChecked():
            fast_fermeture_ordre_mt5(nombre=nb)

    # methode pour changement lors du checkage
    def change_radio_manager_trade(self):
        button = self.sender()
        if button == self.Radio_fermé_position:
            self.label_nb_changement.setHidden(True)
            self.nb_changement.setHidden(True)
            self.label_SL.setHidden(True)
            self.SL.setHidden(True)
            self.label_TP.setHidden(True)
            self.TP.setHidden(True)
            self.changer_fast.setHidden(True)

            self.label_nb_ordre_fermé.setHidden(False)
            self.nb_ordre_fermé.setHidden(False)
            self.fermer_ordre_fast.setHidden(False)

            self.Radio_fermé_position.setChecked(True)

        elif button == button == self.Radio_manager_SL_TP:
            self.label_nb_ordre_fermé.setHidden(True)
            self.nb_ordre_fermé.setHidden(True)
            self.fermer_ordre_fast.setHidden(True)
            self.label_nb_changement.setHidden(False)
            self.nb_changement.setHidden(False)
            self.label_SL.setHidden(False)
            self.SL.setHidden(False)
            self.label_TP.setHidden(False)
            self.TP.setHidden(False)
            self.changer_fast.setHidden(False)

            self.Radio_manager_SL_TP.setChecked(True)

    def fct_fenetre_parametre_manager(self):
        self.w = ManagerTradeWindow()
        self.w.resize(300, 70)
        self.w.show()

    # fonction pour ajouter des annonces

    def fct_ajouter_annonce(self,year,month,day,hour,minute,name):
        c = sqlite3.connect("DB.sq3")
        cu = c.cursor()
        v_date=f'{str(year).zfill(2)}-{str(month).zfill(2)}-{str(day).zfill(2)}'
        v_hour=f"{str(hour).zfill(2)}:{str(minute).zfill(2)}"
        value=[name,v_date,v_hour]
        sql="INSERT INTO Annonces(nom,date,heure)VALUES(?,?,?)"
        cu.execute(sql,value)
        c.commit()
        c.close()
        insertion_ligne=self.model.insertRow(value)
        self.model.layoutChanged.emit()
        if insertion_ligne[0]:
            date=insertion_ligne[1][1]
            heure=insertion_ligne[1][0]

    def change_timer_new_annonce(self,date:str,heure:str):
        d_annonce=datetime.strptime(f'{date}-{heure}',"%Y-%m-%d-%H:%M")
        intervalle=d_annonce-datetime.now()
        intervalle_seconds=intervalle.total_seconds()




    def fct_supprimer_annonce(self):
        rows = sorted(set(index.row() for index in
                          self.table_annonce.selectedIndexes()))

        self.model.removeRows(0,1,QPersistentModelIndex(self.model.index(0,0)))


    def fct_ajout_supression_annonce_threading(self):
        button = self.sender()
        if button==self.btn_supprimer_modifier_annonce:
            dico={"type":"suppression"}
            fct=annonce_supression_ajout(self.fct_supprimer_annonce,**dico)
            self.thread_annonce_suppression_annonce.start(fct)
        elif button == self.ajouter_annonce:
            value_nom = self.Nom_annonce.text()
            value_date = self.date_annonce.date()
            value_hour = self.heure_annonce.time()
            if datetime.now() > datetime(year=value_date.year(), month=value_date.month(), day=value_date.day(),
                                         hour=value_hour.hour(), minute=value_hour.minute()):
                QMessageBox.critical(self,"Erreur Value", "Erreur date < date courante",buttons=QMessageBox.Ok)
            else:
                dico={"y":value_date.year(),"m":value_date.month(),"d":value_date.day(),"h":value_hour.hour(),"M":value_hour.minute(),"nom":value_nom,"type":'ajout'}
                fct=annonce_supression_ajout(self.fct_ajouter_annonce,**dico)
                self.thread_annonce_suppression_annonce.start(fct)

    def time_out_annonce(self):
        #db récupération d'activaition ou non pour savoir si les musique doivent être joué
        if self.model.rowCount(0)>0:
            annonce = self.model.récupérer_annonce(0)
        else:
            return False

        c=sqlite3.connect("DB.sq3")
        cursor=c.cursor()
        cursor.execute("SELECT value FROM parametre_default WHERE type=='activation_musique_timer'")
        activation=cursor.fetchall()[0][0]
        vérif_activation=activation=='True'

        date=f"{annonce[1]}-{annonce[2]}"
        intervalle=datetime.strptime(date,"%Y-%m-%d-%H:%M")-datetime.now()

        if timedelta(hours=1)>=intervalle>=timedelta(seconds=1):

            self.label_prochaine_annonce_timer.setText(
                f"Timer:{str(intervalle)[0:7]}")
            if timedelta(hours=1)>=intervalle>=timedelta(minutes=59,seconds=59) or timedelta(minutes=10)>=intervalle>=timedelta(minutes=9,seconds=59) or timedelta(minutes=1)>=intervalle>=timedelta(seconds=59) or timedelta(seconds=30)>=intervalle>=timedelta(seconds=29) or timedelta(seconds=12)>=intervalle>=timedelta(seconds=11) or  timedelta(seconds=6)>=intervalle>=timedelta(seconds=5):
                if vérif_activation:
                    self.sound_annonce.setSource(QUrl.fromLocalFile('sound_annonce/Bip-Bip-_-Bruitage.wav'))
                    self.sound_annonce.play()



        elif timedelta(seconds=-1)<intervalle<=timedelta(seconds=0):
            self.label_prochaine_annonce_timer.setText(
                f"LEEEEEEESSSSSSSSSGGGGGGGGGGGGGOOOOOOOOO!!!!")
            if  vérif_activation and timedelta(seconds=0)>=intervalle>=timedelta(seconds=-1):
                self.sound_annonce.setSource(QUrl.fromLocalFile("sound_annonce/Beethoven-Ode-à-la-joie.wav"))
                self.sound_annonce.play()


        elif timedelta(seconds=-39)>=intervalle>=timedelta(seconds=-40):
            c=sqlite3.connect("DB.sq3")
            nom_annonce = self.model.obtenir_nom_annonce(0)
            cu=c.cursor()
            cu.execute("DELETE FROM Annonces WHERE nom=?",[annonce[0]])
            c.commit()
            c.close()
            self.model.removeRows(0,1)
            annonce_suivante=self.model.récupérer_annonce(0)
            if annonce_suivante!=False:
                date = f'{annonce_suivante[1]}-{annonce_suivante[2]}'
                annonce=datetime.strptime(date,"%Y-%d-%m-%H:%M")
                intervalle =annonce - datetime.now()



    def convertir_second_to_hour_minute_secondes(self,secondes):
        heure, secondes_restantes=divmod(secondes,3600)
        minutes,secondes_restantes=(secondes_restantes,60)

        return {'heures':heure,'minutes':minutes,'secondes':secondes_restantes}



    def thread_time_out_annonce(self):
        fct = Timer_Annonce(self.time_out_annonce)
        self.thread_timer.start(fct)











        # créer une boit de dialog


app = QApplication(sys.argv)
window = MainWindow()
window.resize(300, 250)
window.setGeometry(0, 0, 0, 0)
window.show()
app.exec()
