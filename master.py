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
        #self.loginWin.withdraw()
        #self.homePage()
        #self.addSchoolInfo()
        #self.viewSchedule()
        self.trainSearch()
        #self.passengerInfo()
        #self.makeReservation()
        #self.pay()
        
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
        login = Button(self.loginframe, text = "Login", command = self.loginCheck)
        login.grid(row = 0, column = 1, sticky = E, ipadx = 10)
        
    def connect(self):
        ## connect to database
        try:
            self.db = pymysql.connect(host = "academic-mysql.cc.gatech.edu",
                                 passwd = 'zMRDk9FA', user = 'cs4400_Team_29', db = 'cs4400_Team_29')
            return self.db
        except:
            messagebox.showerror("Error", "Check your internet connection")
            
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
            self.homePage()
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
        self.registerWin.title("GT Trains Register Page")
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
        register = Button(self.registerbuttons, text = "Register", command = self.registerNew)
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
            sql = "INSERT INTO Users (Username, Password) VALUES (%s, %s)"
            insert = cursor.execute(sql,(userStr, passStr))
            sql2 = "INSERT INTO Customers (Username, Email, Student) VALUES (%s, %s, %s)"
            insert = cursor.execute(sql2,(userStr, emailStr, 'no'))
            #closing stuff after a successful registration
            cursor.close()
            self.connect().commit()
            messagebox.showinfo("Registration", "Registration successful!")
            self.backToLogin()
            
    
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
        self.viewSchedWin = Toplevel()
        self.viewSchedWin.title("View Train Schedule")
        viewLabel = Label(self.viewSchedWin, text = "View Train Schedule", font="Arial 20", pady = 20, padx = 30)
        viewLabel.grid(row = 0, column = 0, columnspan = 2)
        trainLabel = Label(self.viewSchedWin, text = "Train Number", padx = 20, pady = 15)
        trainLabel.grid(row = 1, column = 0)
        self.trainStr = StringVar()
        self.trainStr.set("")
        trainEntry = Entry(self.viewSchedWin, textvariable = self.trainStr, width = 30)
        trainEntry.grid(row = 1, column = 1, padx = 5)
        
        searchbutton = Button(self.viewSchedWin, text = "Search", command = self.searchSchedule)
        searchbutton.grid(row = 2, column = 0, columnspan = 2, pady = 10)

    def searchSchedule(self):
        ## things to fix:
        ## use the train name from table instead of user inputted string
        ## connecting to database
        self.trainString = self.trainStr.get()
        self.connect()
        cursor = self.connect().cursor()
        sql = "SELECT ArrivalTime, DepartureTime, StationName FROM Stops WHERE TrainNumber = %s ORDER BY ArrivalTime"
        check = cursor.execute(sql, self.trainString)
        if check == 0:
            messagebox.showerror("Error", "Train Number Invalid")
        else:
            self.viewSchedWin.withdraw()
            self.viewSchedWin2 = Toplevel()
            self.viewSchedWin2.title("View Train Schedule")
            viewLabel = Label(self.viewSchedWin2, text = "View Train Schedule", font="Arial 20", pady = 20, padx = 30)
            viewLabel.grid(row = 0, column = 0, columnspan = 2)
            ##creating table
            z = Frame(self.viewSchedWin2, bd = 1, relief = "raised")
            z.grid(row = 1, column = 0, columnspan = 2)
            ## top labels
            labelList = ["Train", "Arrival Time", "Departure Time", "Station"]
            for i in range(len(labelList)):
                header = Label(z, text = labelList[i])
                header.grid(row = 0, column = i)
            ## getting data
            trainSchedList = []
            for record in cursor:
                trainSchedList.append(record)
            #print(trainSchedList)
            schedLen = len(trainSchedList)
            for i in range(schedLen):
                arrival = Label(z, text = trainSchedList[i][0], width = 15)
                arrival.grid(row = i+1, column = 1, sticky=W+E+N+S)
                departure = Label(z, text = trainSchedList[i][1], width = 15)
                departure.grid(row = i+1, column = 2, sticky=W+E+N+S)
                stationName = Label(z, text = trainSchedList[i][2], width = 15)
                stationName.grid(row = i+1, column = 3, sticky=W+E+N+S)
            trainNo = Label(z, text = self.trainString)
            trainNo.grid(row = 1, column = 0)
            cursor.close()
            back = Button(self.viewSchedWin2, text = "Back", padx = 6, command = self.backtoViewTrain)
            back.grid(row = 2, column = 0, pady=10)

    def backtoViewTrain(self):
        self.viewSchedWin2.withdraw()
        self.viewSchedWin.deiconify()
        
    def trainSearch(self):
        #self.homePage.withdraw()
        self.connect()
        cursor = self.connect().cursor()
        sql = "SELECT CONCAT(StationName,' (', Location, ')'), StationName FROM Stations"
        cursor.execute(sql)
        self.stationDict={}
        for record in cursor:
            self.stationDict[record[0]] = record[1]
        cursor.close()
        stationList = list(self.stationDict.keys())
        self.trainSearchWin = Toplevel()
        self.trainSearchWin.title("Search Train")
        title = Label(self.trainSearchWin, text = "Search Train", font = "Arial 20")
        title.grid(row=0, column=0)
        mframe = Frame(self.trainSearchWin)
        mframe.grid(row=1,column=0)
        dlabel = Label(mframe, text = "Departs From")
        dlabel.grid(row=0, column=0)
        self.departVar = StringVar(mframe)
        self.departVar.set(stationList[0])
        self.arriveVar = StringVar(mframe)
        self.arriveVar.set(stationList[1])
        doption = OptionMenu(mframe, self.departVar, *stationList)
        doption.grid(row=0, column=1)
        alabel = Label(mframe, text = "Arrives At")
        alabel.grid(row=1,column=0)
        aoption = OptionMenu(mframe, self.arriveVar, *stationList)
        aoption.grid(row=1,column=1)
        ddlabel = Label(mframe, text = "Departure Date")
        ddlabel.grid(row=2, column=0)
        currentTime = datetime.datetime.now()
        self.date2 = StringVar(mframe)
        self.date2.set(currentTime.strftime("%m/%d/%Y"))
        dateEntry = Entry(mframe, textvariable = self.date2, width = 37)
        dateEntry.grid(row=2, column = 1)
        findtrain = Button(self.trainSearchWin, text = "Find Trains", command=self.selectDepart)
        findtrain.grid(row=2, column=0, pady = 5)
        
    def selectDepart(self):
        self.trainSearchWin.withdraw()
        self.connect()
        cursor = self.connect().cursor()
        ## tell amy to fix SQL
        sql = "SELECT TrainRoutes.TrainNumber, CONCAT(DepartureStop.DepartureTime,' - ', ArrivalStop.ArrivalTime, '\n', TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime)), DepartureStop.DepartureTime, ArrivalStop.ArrivalTime, TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) as Duration, TrainRoutes.FirstClassPrice, TrainRoutes.SecondClassPrice FROM TrainRoutes INNER JOIN Stops as ArrivalStop ON TrainRoutes.TrainNumber = ArrivalStop.TrainNumber INNER JOIN Stops as DepartureStop ON TrainRoutes.TrainNumber = DepartureStop.TrainNumber WHERE DepartureStop.StationName = %s AND ArrivalStop.StationName = %s AND TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) > '00:00:00'"
        depart = self.stationDict[self.departVar.get()]
        arrive = self.stationDict[self.arriveVar.get()]
        currentTime = datetime.datetime.now()
        date = self.date2.get()
        selectDepartList = []
        check = cursor.execute(sql, (depart,arrive))
        if check == 0:
            messagebox.showerror("Error", "No routes available")
            self.trainSearchWin.deiconify()
        if date == currentTime.strftime("%m/%d/%Y"):
            messagebox.showerror("Error", "This is today's date")
            self.trainSearchWin.deiconify()
        if date < currentTime.strftime("%m/%d/%Y"):
            messagebox.showerror("Error", "This date is in the past")
            self.trainSearchWin.deiconify()
        else:
            self.selectDepartWin = Toplevel()
            self.selectDepartWin.title("Select Departure")
            title = Label(self.selectDepartWin, text="Select Departure", font="Arial 20")
            title.grid(row=0,column=0)
            table = Frame(self.selectDepartWin)
            table.grid(row=1,column=0)
            labelList = ["Train \n (Train Number)", "Time \n (Duration)", "1st Class Price", "2nd Class Price"]
            for i in range(len(labelList)):
                header = Label(table, text = labelList[i])
                header.grid(row = 0, column = i)
            cursor.execute(sql, (depart,arrive))
            for record in cursor:
                selectDepartList.append([record[0], record[1].decode("utf-8"), record[5], record[6]])
            print(selectDepartList)
            #print(type(selectDepartList[0][1]))
            cursor.close()
            for i in range(len(selectDepartList)):
                train = Label(table, text = selectDepartList[i][0])
                train.grid(row=i+1, column = 0)
                time = Label(table, text = selectDepartList[i][1])
                time.grid(row=i+1, column = 1)

                ##finish this fucking function


                
                #first = Label(table, text = selectDepartList[i][2])
                #first.grid(row=i+1, column = 2)
                #second = Label(table, text = selectDepartList[i][3])
                #second.grid(row=i+1, column = 3)
            MODES = [("a", "1"), ("B", "2"), ("C", "3")]
            v = StringVar()
            v.set("1")
            for i in range(len(MODES)):
                b = Radiobutton(self.selectDepartWin, text=MODES[i][0], variable=v, value=MODES[i][1])
                b.grid(row=i+2, column=0)
                
    def passengerInfo(self):
        #self.selectDepart.withdraw()
        self.passengerInfoWin = Toplevel()
        self.passengerInfoWin.title("Travel Extras & Passenger Info")
        title = Label(self.passengerInfoWin, text = "Travel Extras & Passenger Info", font="Arial 20")
        title.grid(row = 0, column=0, columnspan=2, padx = 30, pady=20)
        mframe = Frame(self.passengerInfoWin)
        mframe.grid(row=1, column=0, columnspan=2)
        labelB = Label(mframe, text="Number of Baggage")
        labelB.grid(row = 0, column = 0)
        self.baggage = Spinbox(mframe, from_=0, to=4)
        self.baggage.grid(row = 0, column = 1)
        #number is self.baggage.get()
        labelD = Label(mframe, text="Every passenger can bring up to 4 baggage. 2 free of charge, 2 for $30 per bag", font="Arial 8")
        labelD.grid(row=1, column=0, columnspan=2)
        labelP = Label(mframe, text = "Passenger Name")
        labelP.grid(row=2, column=0)
        self.passenger = StringVar()
        self.passenger.set("")
        entryP = Entry(mframe, textvariable = self.passenger)
        entryP.grid(row = 2, column=1)
        back = Button(self.passengerInfoWin, text = "Back", command=self.backSelectDep)
        back.grid(row=2, column=0, pady = 15)
        nextb = Button(self.passengerInfoWin, text = "Next", command=self.makeReservation)
        nextb.grid(row=2, column=1, pady=15)
        
    def backSelectDep(self):
        self.passengerInfoWin.withdraw()
        self.selectDepartWin.deiconify()
        
    def makeReservation(self):
        #self.passengerInfo.withdraw()
        self.makeResWin = Toplevel()
        self.makeResWin.title("Make Reservation")
        title = Label(self.makeResWin, text = "Make Reservation", font="Arial 20")
        title.grid(row=0, column=0, columnspan=200, pady = 20)
        currentselect = Label(self.makeResWin, text = "Currently Selected")
        currentselect.grid(row=1, column=0, padx=20)
        table = Frame(self.makeResWin)
        table.grid(row=2, column=0, columnspan=200, pady=20, padx=20)
        hList = ["Train\n(Train Number)", "Time\n(Duration)", "Departs From", "Arrives At", "Class", "Price", "# of Baggage(s)", "Passenger Name", "Remove"]
        for i in range(len(hList)):
            header = Label(table, text = hList[i])
            header.grid(row = 0, column = i)
        #if she or he is a student:
        #sda = Label(self.makeResWin, text = "Student Discount Applied")
        #sda.grid(row=3, column=0)
        tc = Label(self.makeResWin, text="Total Cost")
        tc.grid(row=4, column=0)
        ## mark entry as closed, import the total cost
        tcE = Entry(self.makeResWin)
        tcE.grid(row=4, column=1)
        uc = Label(self.makeResWin, text="Use Card")
        uc.grid(row=5, column=0)
        #options list of different cards in the system
        #ucOM = OptionMenu(self.makeResWin, var, *#nameofoptionslist
        #ucOM.grid(row=5, column=1)
        #ucLabel = Label(self.makeResWin, text="Add Card", command=self.pay)
        #ucLabel.grid(row=5, column=2)
        #cat = link or button to continue adding a train command=self.addTrain)
        #cat.grid(row=6,column=0)
        back = Button(self.makeResWin, text="Back", command=self.backPassInfo)
        back.grid(row=7, column=0, columnspan=70, pady=20)
        submit = Button(self.makeResWin, text="Submit", command=self.submitRes)
        submit.grid(row=7, column=80, columnspan=100, pady=20)
    def addTrain(self):
        pass
    def pay(self):
        #self.makeReservation.withdraw()
        self.payWin=Toplevel()
        self.payWin.title("Payment Information")
        title=Label(self.payWin, text="Payment Information", font="Arial 20")
        title.grid(row=0, column=0, columnspan=2)
        aFrame=Frame(self.payWin)
        aFrame.grid(row=1, column=0)
        ac = Label(aFrame, text="Add Card", font="Arial 14", width=30)
        ac.grid(row=0, column=0, columnspan=2)
        acList = ["Name on Card", "Card Number", "CVV", "Expiration Date"]
        for i in range(len(acList)):
            header = Label(aFrame, text = acList[i])
            header.grid(row = i+1, column = 0)
        self.nameOnCard = StringVar()
        self.nameOnCard.set("")
        self.cardNo = StringVar()
        self.cardNo.set("")
        self.cvv = StringVar()
        self.cvv.set("")
        nocEntry = Entry(aFrame, textvariable=self.nameOnCard)
        nocEntry.grid(row = 1, column=1)
        cNoEntry = Entry(aFrame, textvariable=self.cardNo)
        cNoEntry.grid(row = 2, column=1)
        cvvEntry = Entry(aFrame, textvariable=self.cvv)
        cvvEntry.grid(row = 3, column=1)
        addSub = Button(aFrame, text="Submit", command=self.addCard)
        addSub.grid(row=5, column=0, columnspan=2)
        dc = Label(aFrame, text="Delete Card", font="Arial 14", width=30)
        dc.grid(row=0, column=3, columnspan=2)
        cn=Label(aFrame, text="Card Number")
        cn.grid(row=1, column=3)
        #optionslist
        #cnMenu = OptionMenu(aFrame, var, *#nameofoptionslist
        #cnMenu.grid(row=1, column=4)
        delSub = Button(aFrame, text="Submit", command=self.deleteCard)
        delSub.grid(row=5, column=3, columnspan=2)
        
    def addCard(self):
        pass
    def deleteCard(self):
        pass
    def backPassInfo(self):
        self.makeResWin.withdraw()
        self.passengerInfoWin.deiconify()
    def submitRes(self):
        pass
    def updateReservation(self):
        pass
    def cancelReservation(self):
        pass
    def giveReview(self):
        pass
    
    def addSchoolInfo(self):
        self.homewin.withdraw()
        self.addSchoolWin = Toplevel()
        self.addSchoolWin.title("Add School Info")
        addLabel = Label(self.addSchoolWin, text = "Add School Info", font = "Arial 20", pady = 20, padx = 30)
        addLabel.grid(row = 0, column = 0, columnspan=2)
        emailLabel = Label(self.addSchoolWin, text = "School Email Address:")
        emailLabel.grid(row = 1, column = 0, sticky = E, padx = 10)
        emailStr = StringVar()
        emailStr.set("")
        emailEntry = Entry(self.addSchoolWin, textvariable = emailStr, width = 30)
        emailEntry.grid(row = 1, column = 1, padx = 10)
        noteLabel = Label(self.addSchoolWin, text = "Your school email address ends with .edu")
        noteLabel.grid(row = 2, column = 0, columnspan = 2, pady = 10)
        ## buttons
        buttonframe = Frame(self.addSchoolWin)
        buttonframe.grid(row = 3, column = 0, columnspan = 2)
        back = Button(buttonframe, text = "Back",command=self.schoolInfoBack)
        back.grid(row = 0, column = 0, sticky = E, ipadx = 10)
        submit = Button(buttonframe, text = "Submit", command=self.submitSchoolInfo)
        submit.grid(row = 0, column = 1, sticky = W, ipadx = 5)
        
    def schoolInfoBack(self):
        self.addSchoolWin.withdraw()
        self.homeWin.deiconify()
        
    def submitSchoolInfo(self):
        pass
    ## checking if valid school address
    ## if so, set student to yes
    ## create a discount
    
    def logOut(self):
        pass
rootWin = Tk()
app = gtTrains(rootWin)
rootWin.mainloop()
