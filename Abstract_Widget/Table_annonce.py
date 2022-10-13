import sqlite3
from datetime import datetime,time,timedelta
from operator import itemgetter
import re

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QTime, QTimer

import sys
from PySide6 import QtCore, QtGui, QtWidgets

import pandas
from PySide6.QtWidgets import QMessageBox
from tinydb import TinyDB, Query, where




class TableModelAnnonce(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModelAnnonce, self).__init__()
        self._data=data
    def data(self, index, role):

        if role == Qt.DisplayRole :
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            value = self._data.iloc[index.row(), index.column()]
            if index.column()==1:

                return value
            #traduction des datetime et affichage de ceux ci pour l'utilisateur

            elif index.column()==2:
                return value


            else:return value

        if role==Qt.BackgroundRole:
            value = self._data.iloc[index.row(), index.column()]
            if index.column()==1:

                if datetime.today().date()==datetime.strptime(value,"%Y-%m-%d").date():
                    return QtGui.QColor("red")

                else:
                    return QtGui.QColor("green")

            if index.column()==2:
                date= self._data.iloc[index.row(), index.column()-1]




                if timedelta(days=1)>datetime.now()-datetime.strptime(f'{date} {value}',"%Y-%m-%d %H:%M") > timedelta(hours=8):
                    return QtGui.QColor("green")
                elif timedelta(hours=8)>datetime.strptime(f'{date} {value}',
                                     "%Y-%m-%d %H:%M")-datetime.now()  >= timedelta(hours=4):
                    return QtGui.QColor("yellow")

                elif timedelta(hours=4) > datetime.strptime(f'{date} {value}',
                                                                     "%Y-%m-%d %H:%M")-datetime.now()>= timedelta(
                    hours=1):
                    return QtGui.QColor("orange")

                elif timedelta(hours=1) >datetime.strptime(f'{date} {value}',
                                                                     "%Y-%m-%d %H:%M") -datetime.now() >= timedelta(
                    seconds=-1):
                    return QtGui.QColor("red")





    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

    def insertRow(self, ajout):

        row = len(self._data)
        self.beginInsertRows(QtCore.QModelIndex(), row, row)

        liste=[[self._data['Nom'][i],self._data['Date'][i],self._data['Heure'][i]] for i in range(len(self._data))]
        liste.append(ajout)
        for count,value in enumerate(liste):
            liste[count][1]=datetime.strptime(f'{value[1]}-{value[2]}',"%Y-%m-%d-%H:%M")
        liste.sort(key=itemgetter(1))
        for i in range(len(liste)):
            liste[i][
                1] = f"{str(liste[i][1].year).zfill(2)}-{str(liste[i][1].month).zfill(2)}-{str(liste[i][1].day).zfill(2)}"
        self._data=pandas.DataFrame(liste,columns=['Nom','Date','Heure'],index=[i for i in range(len(liste))])
        self.endInsertRows()
        if self._data.iloc[0,0]==ajout[0]:
            return [True,ajout]
        else:
            return [False,None]

    def RemoveRows(self,pos,a,QModelIndex):
        self.beginRemoveRows(QModelIndex,pos,a)
        for i in range(a):
            self._data.drop(index=0)
        self.endRemoveRows()




    def flags(self, index):
        if index.column()==1 or index.column()== 2:
            return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable
        else: return Qt.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            c=sqlite3.connect("DB.sq3")
            cu=c.cursor()
            date=self._data.iloc[index.row(),1]
            heure=self._data.iloc[index.row(),2]
            date_datetime=datetime.strptime(f'{date}-{heure}',"%Y-%m-%d-%H:%M")
            date_validate_time=date_datetime>datetime.now()
            if index.column()==1:
                if re.match(r"^20[0-9]{2}-[0-3]{1}[0-9]{1}-[0-3]{1}[0-9]{1}", value) is None or date_validate_time==False:
                    self._data.iloc[index.row(), index.column()]=self._data.iloc[index.row(),index.column()]
                    c.close()
                    return False
                else:
                    v = [value, self._data.iloc[index.row(), 0]]
                    self._data.iloc[index.row(), index.column()] = value
                    sql="UPDATE Annonces SET date=? WHERE nom=?"
                    cu.execute(sql,v)
                    c.commit()
                    c.close()
                    self.trier_dataframe()
                    return True
            elif index.column()==2:
                if re.match(r"^[0-2]{1}[0-9]{1}:[0-5]{1}[0-9]{1}",value) is None or date_validate_time==False:
                    self._data.iloc[index.row(), index.column()] = self._data.iloc[index.row(),index.column()]
                    return False
                else:

                    v = [self._data.iloc[index.row(), index.column()], self._data.iloc[index.row(), 0]]
                    self._data.iloc[index.row(), index.column()] = value
                    sql = "UPDATE Annonces SET heure=? WHERE nom=?"
                    cu.execute(sql,v)
                    c.commit()
                    c.close()

                    first_annonce=self.trier_dataframe()
                    print(first_annonce)
                    if v==first_annonce:

                        return True
                    else:
                        return False



    def trier_dataframe(self):
        liste = [[self._data['Nom'][i], self._data['Date'][i], self._data['Heure'][i]] for i in
                 range(len(self._data))]
        for count, value in enumerate(liste):
            liste[count][1] = datetime.strptime(f'{value[1]}-{value[2]}', "%Y-%m-%d-%H:%M")
        liste.sort(key=itemgetter(1))
        for i in range(len(liste)):
            liste[i][
                1] = f"{str(liste[i][1].year).zfill(2)}-{str(liste[i][1].month).zfill(2)}-{str(liste[i][1].day).zfill(2)}"
        self._data = pandas.DataFrame(liste, columns=['Nom', 'Date', 'Heure'],
                                      index=[i for i in range(len(liste))])

        #retourne le premier intem de la liste
        return self._data.iloc[0,0]

    def rowCount(self, index):
        # The length of the outer list.
        return self._data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self._data.shape[1]

    def obtenir_nom_annonce(self,row):
        if not self._data.iloc[row,0]:
            return False
        else:
            return self._data.iloc[row,0]

    def récupérer_annonce(self,r):
        annonce=[self._data.iloc[r,0],self._data.iloc[r,1],self._data.iloc[r,2]]
        return annonce



#Les seules méthodes requises pour un modèle de tableau
#personnalisé sont data, rowCount et columnCount. Le premier renvoie des données (ou des informations de présentation) pour des emplacements donnés dans
#le tableau, tandis que les deux derniers doivent renvoyer une seule valeur entière pour les dimensions de la source de données.