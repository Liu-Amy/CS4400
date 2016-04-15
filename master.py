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
        self.registerPage()
        self.registerWin.withdraw()
        ##delete later
        self.loginWin.withdraw()
        #self.homePage()
        self.addSchoolInfo()

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
        userpass = Frame(self.loginWin)#, bg= "gold")
        userpass.grid(row = 1, column = 0, sticky = E)
        ## row 0 - login title
        loginLabel = Label(userpass, text = "Login", font=("Arial", 20))#, bg = "gold")
        loginLabel.grid(row = 0, columnspan = 20, sticky = N+S+W+E, ipady = 20)
        ## row 0 - username
        userLabel = Label(userpass, text = "Username:")#, bg = "gold")
        userLabel.grid(row = 1, column = 18, sticky = E, ipadx = 0, padx = 15)
        userEntry = Entry(userpass, textvariable = self.username, width = 37)
        userEntry.grid(row = 1, column = 19, sticky = E, padx = 15, pady = 15)
        ## row 1 - password
        passLabel = Label(userpass, text = "Password:")#, bg = "gold")
        passLabel.grid(row = 2, column = 18, sticky = E, ipadx = 0, padx = 15)
        passEntry = Entry(userpass, textvariable = self.password, width = 37)
        passEntry.grid(row = 2, column = 19, sticky = E, padx = 15, pady = 15)
        ## creating buttons frame
        self.loginframe = Frame(self.loginWin, bd = 0, width = 50)
        self.loginframe.grid(row = 2, column = 0, sticky = E)
        ## buttons
        register = Button(self.loginframe, text = "Register", command = self.goToRegister)
        register.grid(row = 0, column = 0, sticky = E, ipadx = 10)
        login = Button(self.loginframe, text = "Login")#, command = self.loginCheck)
        login.grid(row = 0, column = 1, sticky = E, ipadx = 10)

    def loginCheck(self):
        ## connect to database
        self.connect()
        cursor = self.connect().cursor()
        ## get username and password
        self.username1 = self.username.get()
        self.password1 = self.password.get()
        ## checking to see if it matches the database
        sql = "SELECT * FROM Users WHERE Username = %s AND (Password LIKE BINARY %s)"
        check = cursor.execute(sql,(self.username1,self.password1))
        ## successful
        if check == 1:
            messagebox.showinfo("Login", "Login Successful!")
            self.driver()
            self.loginWin.withdraw()
        ## unsuccessful
        else:
            messagebox.showerror("Error", "Username/password combo not found")

    def goToRegister(self):
        self.loginWin.withdraw()
        self.registerWin.deiconify()
        
    def registerPage(self):
        ## window setup
        self.registerWin = Toplevel()
        self.registerWin.title("GT Brokers Register Page")
        ## main frame setup
        self.topRegister = Frame(self.registerWin)
        self.topRegister.grid(row = 0, column = 0, pady = 40)
        ## row 0 - label
        titleLabel = Label(self.topRegister, text = "New User Registration", font = ("Arial", 20))
        titleLabel.grid(row = 0, column = 0, columnspan=2, sticky = N+W+S+E, pady = 15)
        ## row 0 - username
        userLabel = Label(self.topRegister, text = "Username:")
        userLabel.grid(row = 1, column = 0, sticky = E, padx = 5)
        self.userStr = StringVar()
        self.userStr.set("")
        userEntry = Entry(self.topRegister, textvariable = self.userStr, width = 60)
        userEntry.grid(row = 1, column = 1, padx = 5)
        ## row 1 - email address
        nameLabel = Label(self.topRegister, text = "Email Address:")
        nameLabel.grid(row = 2, column = 0, sticky = E, padx = 5)
        self.emailStr = StringVar()
        self.emailStr.set("")
        nameEntry = Entry(self.topRegister, textvariable = self.emailStr, width = 60)
        nameEntry.grid(row = 2, column = 1, padx = 5)
        ## row 2 - password
        passLabel = Label(self.topRegister, text = "Password:")
        passLabel.grid(row = 3, column = 0, sticky = E, padx = 5)
        self.passStr = StringVar()
        self.passStr.set("")
        passEntry = Entry(self.topRegister, textvariable = self.passStr, width = 60)
        passEntry.grid(row = 3, column = 1, padx = 5)
        ## row 3 - confirm password
        confirmLabel = Label(self.topRegister, text = "Confirm Password:")
        confirmLabel.grid(row = 4, column = 0, sticky = E, padx = 5)
        self.confirmStr = StringVar()
        self.confirmStr.set("")
        confirmEntry = Entry(self.topRegister, textvariable = self.confirmStr, width = 60)
        confirmEntry.grid(row = 4, column = 1, padx = 5)
        ## buttons frame setup
        self.registerbuttons = Frame(self.registerWin)
        self.registerbuttons.grid(row = 1, column = 0)
        ## buttons
        cancel = Button(self.registerbuttons, text = "Cancel")#, command = self.backToLogin)
        cancel.grid(row = 0, column = 0, ipadx = 60)
        register = Button(self.registerbuttons, text = "Register")#, command = self.registerNew)
        register.grid(row = 0, column = 1, ipadx = 60)

    def backToLogin(self):
        self.registerWin.withdraw()
        self.loginWin.deiconify()
        
    def registerNew(self):
        ## getting strings
        emailStr = self.emailStr.get()
        passStr = self.passStr.get()
        userStr = self.userStr.get()
        confirmStr = self.confirmStr.get()
        ## finding numbers and capital letters in the password
        numCheck = re.findall('[0-9]', passStr)
        capitalCheck = re.findall('[A-Z]', passStr)
        ## connecting to database
        self.connect()
        cursor = self.connect().cursor()
        ## checking if username or email is already in database
        usersql = "SELECT Username FROM Users WHERE Username = %s"
        emailsql = "SELECT Email FROM Customers WHERE Email = %s" 
        userCheck = cursor.execute(usersql,(userStr))
        emailCheck = cursor.execute(emailsql, (emailStr))
        ## checking if passwords match
        if passStr != confirmStr:
            messagebox.showerror("Error", "Passwords do not match")
        ## checking if username or password field is blank
        elif userStr == "" or passStr == "" or emailStr == "":
            messagebox.showerror("Error", "A field is blank")
        ## checking if email already in system
        elif emailCheck !=0:
            messagebox.showerror("Error", "Email already in use")
        ## checking if the username already exists
        elif userCheck != 0:
            messagebox.showerror("Error", "Username already in use")
        else:
            ## inserting new user when there is a fullname
            ##
            ##
            ##
            ##
            ##
            ##
            ##
            ## need to insert things into users AND customers
            ##sql = "INSERT INTO GTBrokerageUsers (Fullname, Username, Password, Balance) VALUES (%s, %s, %s, %s)"
            ##insert = cursor.execute(sql,(nameStr, userStr, passStr, 100000.00))
            ## closing stuff after a successful registration
            cursor.close()
            self.connect().commit()
            messagebox.showinfo("Registration", "Registration successful!")
            self.backToLogin()
            
    def connect(self):
        ## connect to database
        try:
            self.db = pymysql.connect(host = "academic-mysql.cc.gatech.edu",
                                 passwd = 'zMRDk9FA', user = 'cs4400_Team_29', db = 'cs4400_Team_29')
            return self.db
        except:
            messagebox.showerror("Error", "Check your internet connection")

    def homePage(self):
        ## window set up
        self.homeWin = Toplevel()
        self.homeWin.title("Choose Functionality")
        chooseLabel = Label(self.homeWin, text = "Choose Functionality", font = "Arial 20", pady = 20, padx = 30)
        chooseLabel.grid(row = 0, column = 0)
        ## buttons
        buttonframe = Frame(self.homeWin, pady = 30)
        buttonframe.grid(row = 1, column = 0)
        button00 = Button(buttonframe, text = "View Train Schedule",
                          padx=10,pady=5, font = "Arial 10", command = self.viewSchedule)
        button00.pack(fill=X)
        button01 = Button(buttonframe, text = "Make a new reservation",
                          padx=10,pady=5, font = "Arial 10", command = self.makeReservation)
        button01.pack(fill=X)
        button02 = Button(buttonframe, text = "Update a reservation",
                          padx=10,pady=5, font = "Arial 10", command = self.updateReservation)
        button02.pack(fill=X)
        button03 = Button(buttonframe, text = "Cancel a reservation",
                          padx=10,pady=5, font = "Arial 10", command = self.cancelReservation)
        button03.pack(fill=X)
        button04 = Button(buttonframe, text = "Give review",
                          padx=10,pady=5, font = "Arial 10", command = self.giveReview)
        button04.pack(fill=X)
        button05 = Button(buttonframe, text = "Add school info",
                          padx=10,pady=5, font = "Arial 10", command = self.addSchoolInfo)
        button05.pack(fill=X)

        logout = Button(self.homeWin, text = "Log Out", command = self.logOut)
        logout.grid(row = 2, column = 0, pady = 10)
        ## finding today's date in YYYY/MM/DD format
        currentTime = datetime.datetime.now()
        self.date = currentTime.strftime("%Y/%m/%d")
        
    def viewSchedule(self):
        pass
    def makeReservation(self):
        pass
    def updateReservation(self):
        pass
    def cancelReservation(self):
        pass
    def giveReview(self):
        pass
    def addSchoolInfo(self):
        #self.homewin.withdraw()
        self.addSchoolWin = Toplevel()
        self.addSchoolWin.title("Add School Info")
        addLabel = Label(self.addSchoolWin, text = "Add School Info", font = "Arial 20", pady = 20, padx = 30)
        addLabel.grid(row = 0, column = 0)
        emailLabel = Label(self.addSchoolWin, text = "School Email Address:")
        emailLabel.grid(row = 1, column = 0)
        emailStr = StringVar()
        emailStr.set("")
        emailEntry = Entry(self.addSchoolWin, textvariable = emailStr, width = 30)
        emailEntry.grid(row = 1, column = 1)
        noteLabel = Label(self.addSchoolWin, text = "Your school email address ends with .edu")
        noteLabel.grid(row = 2, column = 0, columnspan = 2)
        ## buttons
        back = Button(self.addSchoolWin, text = "Back")
        back.grid(row = 3, column = 0)
        submit = Button(self.addSchoolWin, text = "Submit")
        submit.grid(row = 3, column = 1)
        
    def logOut(self):
        pass
rootWin = Tk()
app = gtTrains(rootWin)
rootWin.mainloop()
