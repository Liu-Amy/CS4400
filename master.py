# CS 4400 Project
# Zoya Mahmood - Section A - zmahmood6@gatech.edu
# June Ding - Section A - jding39@gatech.edu
# Amy Liu - Section C - aliu66@gatech.edu

from random import randrange
from re import findall
from tkinter import *
import urllib.request
import datetime
import pymysql
import time
import csv

class gtTrains:
    def __init__(self, rootWin):
        self.rootWin = rootWin
        self.loginPage(self.rootWin)

    def loginPage(self, rootWin):
        

rootWin = Tk()
app = gtTrains(rootWin)
rootWin.mainloop()
