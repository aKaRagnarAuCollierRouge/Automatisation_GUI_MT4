from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

import time
import traceback, sys
import sqlite3


class annonce_supression_ajout(QRunnable):
    def __init__(self,fct,*args,**kwargs):
        super(annonce_supression_ajout,self).__init__()
        self.fct = fct
        self.ajout_suppression=""
        if kwargs['type']=="ajout":
            self.ajout_suppression="ajout"
            self.nom=kwargs['nom']
            self.day=kwargs["d"]
            self.year=kwargs["y"]
            self.mouth=kwargs['m']
            self.hour=kwargs['h']
            self.minute=kwargs['M']
        else:self.ajout_suppression="supprimer"
    @Slot()
    def run(self):
        if self.ajout_suppression=="ajout":
            self.fct(self.year,self.mouth,self.day,self.hour,self.minute,self.nom)
        else:
            self.fct()


class Timer_Annonce(QRunnable):
    def __init__(self,fct,*args,**kwargs):
        super(Timer_Annonce,self).__init__()
        self.fct=fct

    @Slot()
    def run(self):
        self.fct()
        return True
class Play_Musique(QRunnable):
    def __init__(self,fct,*args,**kwargs):
        super(Play_Musique,self).__init__()
        self.fct=fct

    @Slot()
    def run(self):
        self.fct()




