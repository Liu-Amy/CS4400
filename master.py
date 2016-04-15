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
        # window setup
        self.loginWin = rootWin
        self.loginWin.title("GT Trains Login Page")
        ## create stringvars for logging in
        self.username = StringVar()
        self.username.set("")
        self.password = StringVar()
        self.password.set("")
        ## creating main frame
        userpass = Frame(self.loginWin, bg= "gold")
        userpass.grid(row = 1, column = 0, sticky = E)
        ## row 0 - username
        userLabel = Label(userpass, text = "Username:", bg = "gold")
        userLabel.grid(row = 0, column = 18, sticky = E, ipadx = 0)
        userEntry = Entry(userpass, textvariable = self.username, width = 37)
        userEntry.grid(row = 0, column = 19, sticky = E, padx = 5, pady = 5)
        ## row 1 - password
        passLabel = Label(userpass, text = "Password:", bg = "gold")
        passLabel.grid(row = 1, column = 18, sticky = E, ipadx = 0)
        passEntry = Entry(userpass, textvariable = self.password, width = 37)
        passEntry.grid(row = 1, column = 19, sticky = E, padx = 5, pady = 5)
        ## creating buttons frame
        self.loginframe = Frame(self.loginWin, bd = 0, width = 50)
        self.loginframe.grid(row = 2, column = 0, sticky = E)
        ## buttons
        cancel = Button(self.loginframe, text = "Cancel", command = self.cancelLogin)
        cancel.grid(row = 0, column = 0, sticky = E, ipadx = 10)
        register = Button(self.loginframe, text = "Register", command = self.goToRegister)
        register.grid(row = 0, column = 1, sticky = E, ipadx = 10)
        login = Button(self.loginframe, text = "Login", command = self.loginCheck)
        login.grid(row = 0, column = 2, sticky = E, ipadx = 10)


rootWin = Tk()
app = gtTrains(rootWin)
rootWin.mainloop()
