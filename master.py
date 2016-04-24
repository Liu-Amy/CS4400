# CS 4400 Project
# Zoya Mahmood - Section A - zmahmood6@gatech.edu
# June Ding - Section A - jding39@gatech.edu
# Amy Liu - Section C - aliu66@gatech.edu

from tkinter import *
import datetime
import pymysql
import time
import csv
import copy

class gtTrains:
    def __init__(self, rootWin):
        self.rootWin = rootWin
        self.loginPage(self.rootWin)
        self.registerPage()
        self.registerWin.withdraw()
        
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
        userpass = Frame(self.loginWin)
        userpass.grid(row = 1, column = 0, sticky = E)
        ## row 0 - login title
        loginLabel = Label(userpass, text = "Login", font="Arial 20")
        loginLabel.grid(row = 0, columnspan = 20, sticky = N+S+W+E, ipady = 20)
        ## row 0 - username
        userLabel = Label(userpass, text = "Username:")
        userLabel.grid(row = 1, column = 18, sticky = E, ipadx = 0, padx = 15)
        userEntry = Entry(userpass, textvariable = self.username, width = 37)
        userEntry.grid(row = 1, column = 19, sticky = E, padx = 15, pady = 15)
        ## row 1 - password
        passLabel = Label(userpass, text = "Password:")
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
        self.user =self.username.get()
        self.pw = self.password.get()
        ## checking to see if username/password matches database
        sql = "SELECT * FROM Users WHERE Username = %s AND (Password LIKE BINARY %s)"
        check = cursor.execute(sql,(self.user,self.pw))
        ## successful
        if check == 1:
            messagebox.showinfo("Login", "Login Successful!")
            self.startRes = True
            sql="SELECT * FROM Managers WHERE Username = %s"
            cursor.execute(sql, self.user)
            if cursor.rowcount==1:
                cursor.close()
                self.loginWin.withdraw()
                self.managerHome()
            else:
                cursor.close()
                self.loginWin.withdraw()
                self.customerHome()
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
        cancel = Button(self.registerbuttons, text = "Cancel", command = self.backToLogin)
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
        ## checking if email valid
        elif "@" not in emailStr or "." not in emailStr:
            messagebox.showerror("Error", "Email is not valid")
        ## checking if email already in system
        elif emailCheck !=0:
            messagebox.showerror("Error", "Email already in use")
        ## checking if the username already exists
        elif userCheck != 0:
            messagebox.showerror("Error", "Username already in use")
        else:
            sql = "INSERT INTO Users (Username, Password) VALUES (%s, %s)"
            cursor.execute(sql,(userStr, passStr))
            sql = "INSERT INTO Customers (Username, Email, Student) VALUES (%s, %s, %s)"
            cursor.execute(sql,(userStr, emailStr, 'no'))
            #closing stuff after a successful registration
            cursor.close()
            self.connect().commit()
            messagebox.showinfo("Registration", "Registration successful!")
            self.backToLogin()
    
    def customerHome(self):
        ## window set up
        self.loginWin.withdraw()
        self.custHomeWin = Toplevel()
        self.custHomeWin.title("Choose Functionality")
        chooseLabel = Label(self.custHomeWin, text = "Choose Functionality", font = "Arial 20", pady = 20, padx = 30)
        chooseLabel.grid(row = 0, column = 0)
        ## buttons
        buttonframe = Frame(self.custHomeWin, pady = 30)
        buttonframe.grid(row = 1, column = 0)
        button00 = Button(buttonframe, text = "View Train Schedule",
                          padx=10,pady=5, font = "Arial 10", command = self.viewSchedule)
        button00.pack(fill=X)
        button01 = Button(buttonframe, text = "Make a new reservation",
                          padx=10,pady=5, font = "Arial 10", command = self.trainSearch)
        button01.pack(fill=X)
        button02 = Button(buttonframe, text = "Update a reservation",
                          padx=10,pady=5, font = "Arial 10", command = self.updateReservation)
        button02.pack(fill=X)
        button03 = Button(buttonframe, text = "Cancel a reservation",
                          padx=10,pady=5, font = "Arial 10", command = self.cancelReservation)
        button03.pack(fill=X)
        button04 = Button(buttonframe, text = "View review",
                          padx=10,pady=5, font = "Arial 10", command = self.viewReview)
        button04.pack(fill=X)
        button05 = Button(buttonframe, text = "Give review",
                          padx=10,pady=5, font = "Arial 10", command = self.giveReview)
        button05.pack(fill=X)
        button06 = Button(buttonframe, text = "Add school info",
                          padx=10,pady=5, font = "Arial 10", command = self.addSchoolInfo)
        button06.pack(fill=X)

        logout = Button(self.custHomeWin, text = "Log Out", command = self.logOut)
        logout.grid(row = 2, column = 0, pady = 10)
        
    def viewSchedule(self):
        self.custHomeWin.withdraw()
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
        search = Button(self.viewSchedWin, text = "Search", command = self.searchSchedule)
        search.grid(row = 2, column = 1, columnspan = 2, pady = 10)
        back = Button(self.viewSchedWin, text="Back", command=self.vtsToHome)
        back.grid(row=2, column=0, pady=10)
        
    def vtsToHome(self):
        self.viewSchedWin.withdraw()
        self.customerHome()

    def searchSchedule(self):
        ## connecting to database
        self.trainString = self.trainStr.get()
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
            schedLen = len(trainSchedList)
            for i in range(schedLen):
                arrival = Label(z, text = trainSchedList[i][0], width = 15)
                arrival.grid(row = i+1, column = 1, sticky=W+E+N+S)
                departure = Label(z, text = trainSchedList[i][1], width = 15)
                departure.grid(row = i+1, column = 2, sticky=W+E+N+S)
                stationName = Label(z, text = trainSchedList[i][2], width = 15)
                stationName.grid(row = i+1, column = 3, sticky=W+E+N+S)
            sql="SELECT DISTINCT TrainNumber FROM Stops WHERE TrainNumber=%s"
            cursor.execute(sql, self.trainString)
            for record in cursor:
                trainNoStr = record
            trainNo = Label(z, text = trainNoStr)
            trainNo.grid(row = 1, column = 0)
            cursor.close()
            back = Button(self.viewSchedWin2, text = "Back", padx = 6, command = self.backtoViewTrain)
            back.grid(row = 2, column = 0, pady=10)
            home = Button(self.viewSchedWin2, text ="Choose Functionality", command = self.vts2toHome)
            home.grid(row=2,column=1,pady=10)
            
    def vts2toHome(self):
        self.viewSchedWin2.withdraw()
        self.customerHome()

    def backtoViewTrain(self):
        self.viewSchedWin2.withdraw()
        self.viewSchedWin.deiconify()
        
    def trainSearch(self):
        self.custHomeWin.withdraw()
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
        currentTime = datetime.date.today().strftime("%m/%d/%Y")
        self.date = StringVar(mframe)
        self.date.set(currentTime)
        dateEntry = Entry(mframe, textvariable = self.date, width = 40)
        dateEntry.grid(row=2, column = 1)
        findtrain = Button(self.trainSearchWin, text = "Find Trains", command=self.selectDepart)
        findtrain.grid(row=2, column=0, pady = 5)
        back = Button(self.trainSearchWin, text = "Back", command=self.tsBack)
        back.grid(row=3,column=0, pady = 10)
        
    def tsBack(self):
        self.trainSearchWin.withdraw()
        self.customerHome()
        
    def selectDepart(self):
        cursor = self.connect().cursor()
        sql = "SELECT TrainRoutes.TrainNumber, CONCAT(DepartureStop.DepartureTime,' - ', ArrivalStop.ArrivalTime, '\n', TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime)), DepartureStop.DepartureTime, ArrivalStop.ArrivalTime, TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) as Duration, TrainRoutes.FirstClassPrice, TrainRoutes.SecondClassPrice FROM TrainRoutes INNER JOIN Stops as ArrivalStop ON TrainRoutes.TrainNumber = ArrivalStop.TrainNumber INNER JOIN Stops as DepartureStop ON TrainRoutes.TrainNumber = DepartureStop.TrainNumber WHERE DepartureStop.StationName = %s AND ArrivalStop.StationName = %s AND TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) > '00:00:00'"
        depart = self.stationDict[self.departVar.get()]
        arrive = self.stationDict[self.arriveVar.get()]
        date = self.date.get()
        try:
            self.departdate = datetime.datetime.strptime(date, "%m/%d/%Y").date()
            self.selectDepartList = []
            check = cursor.execute(sql, (depart,arrive))
            if check == 0:
                messagebox.showerror("Error", "No routes available")
            elif self.departdate == datetime.date.today():
                messagebox.showerror("Error", "This is today's date")
            elif self.departdate < datetime.date.today():
                messagebox.showerror("Error", "This date is in the past")
            elif self.departdate > datetime.datetime.strptime("05/31/2016", "%m/%d/%Y").date():
                messagebox.showerror("Error", "Too far in the future. No routes available")
            else:
                self.trainSearchWin.withdraw()
                self.selectDepartWin = Toplevel()
                self.selectDepartWin.title("Select Departure")
                title = Label(self.selectDepartWin, text="Select Departure", font="Arial 20")
                title.grid(row=0,column=0, columnspan=2)
                table = Frame(self.selectDepartWin)
                table.grid(row=1,column=0, columnspan=2)
                labelList = ["Train \n (Train Number)", "Time \n (Duration)", "1st Class Price", "2nd Class Price"]
                for i in range(len(labelList)):
                    header = Label(table, text = labelList[i])
                    header.grid(row = 0, column = i)
                cursor.execute(sql,(depart,arrive))
                firstClass = []
                secondClass = []
                count = 0
                firstcount = ["a",0]
                secondcount = ["b",1]
                for record in cursor:
                    self.selectDepartList.append([record[0], record[1], record[5], record[6]])
                    firstcount[0] = count
                    firstClass.append((record[5], firstcount[:]))
                    secondcount[0] = count
                    secondClass.append((record[6], secondcount[:]))
                    count+=1
                cursor.close()
                self.v = StringVar()
                self.v.set("")
                for i in range(len(self.selectDepartList)):
                    train = Label(table, text = self.selectDepartList[i][0])
                    train.grid(row=i+1, column = 0)
                    time = Label(table, text = self.selectDepartList[i][1])
                    time.grid(row=i+1, column = 1)
                    first = Radiobutton(table, text=firstClass[i][0], variable=self.v, value=firstClass[i][1])
                    first.grid(row=i+1, column = 2)
                    second = Radiobutton(table, text=secondClass[i][0], variable=self.v, value=secondClass[i][1])
                    second.grid(row=i+1, column = 3)
                back = Button(self.selectDepartWin, text = "Back", command=self.depToSearch)
                back.grid(row=2, column=0, pady = 15)
                nxt = Button(self.selectDepartWin, text = "Next", command=self.passengerInfo)
                nxt.grid(row=2, column=1, pady=15)
        except:
            messagebox.showerror("Error", "Not a valid date")
            
    def depToSearch(self):
        self.selectDepartWin.withdraw()
        self.trainSearch()
        
    def passengerInfo(self):
        if self.v.get() == "":
            messagebox.showerror("Error", "You must select a ticket")
        else:
            self.selectDepartWin.withdraw()
            self.passengerInfoWin = Toplevel()
            self.passengerInfoWin.title("Travel Extras & Passenger Info")
            title = Label(self.passengerInfoWin, text = "Travel Extras & Passenger Info", font="Arial 20")
            title.grid(row = 0, column=0, columnspan=2, padx = 30, pady=20)
            mframe = Frame(self.passengerInfoWin)
            mframe.grid(row=1, column=0, columnspan=2)
            labelB = Label(mframe, text="Number of Baggage")
            labelB.grid(row = 0, column = 0)
            self.baggage = Spinbox(mframe, from_=0, to=4, state="readonly")
            self.baggage.grid(row = 0, column = 1)
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
            if self.startRes == True:
                self.resList = []
                self.startRes = False
            vIndex = self.v.get()
            routeIndex = int(vIndex[0])
            classIndex = int(vIndex[2]) + 2
            tempHolder = self.selectDepartList[routeIndex]
            tempHolder[1] = self.departdate.strftime("%b %d") +" "+ tempHolder[1]
            b = tempHolder[classIndex]
            self.a = copy.deepcopy(tempHolder[:2])
            self.a.append(self.departVar.get())
            self.a.append(self.arriveVar.get())
            if classIndex == 2:
                self.a.append("1st Class")
            else:
                self.a.append("2nd Class")
            self.a.append(b)
        
    def backSelectDep(self):
        self.passengerInfoWin.withdraw()
        self.selectDepartWin.deiconify()
        
    def makeReservation(self):
        if self.passenger.get() == "":
            messagebox.showerror("Error", "A field is blank")            
        else:
            if self.a != []:
                self.a.append(self.passenger.get())
                self.a.append(self.baggage.get())
                self.resList.append(copy.deepcopy(self.a))
            self.a=[]
            self.passengerInfoWin.withdraw()
            self.makeResWin = Toplevel()
            self.makeResWin.title("Make Reservation")
            title = Label(self.makeResWin, text = "Make Reservation", font="Arial 20")
            title.grid(row=0, column=0, columnspan=200, pady = 20)
            currentselect = Label(self.makeResWin, text = "Currently Selected")
            currentselect.grid(row=1, column=0, padx=20)
            table = Frame(self.makeResWin)
            table.grid(row=2, column=0, columnspan=200, pady=20, padx=20)
            hList = ["Train\n(Train Number)", "Time\n(Duration)", "Departs From", "Arrives At", "Class", "Price", "Passenger Name", "# of Baggage", "Remove"]
            for i in range(len(hList)):
                header = Label(table, text = hList[i])
                header.grid(row = 0, column = i)
            sql = "SELECT Customers.Student FROM Customers WHERE Customers.Username = %s"
            self.var = IntVar()
            for i in range(len(self.resList)):
                for j in range(len(self.resList[0])):
                    qwerty = Label(table, text=self.resList[i][j])
                    qwerty.grid(row = i+1, column = j)
                remove = Checkbutton(table, text="Remove", variable=self.var, onvalue = i+1, command=self.removeTicket)
                remove.grid(row=i+1, column = 8)
            cursor = self.connect().cursor()
            cursor.execute(sql, self.user)
            student = ""
            for record in cursor:
                student = record[0]
            if student == "yes":
                sda = Label(self.makeResWin, text = "Student Discount Applied")
                sda.grid(row=3, column=0, columnspan=30, sticky=W, padx = 20, pady=15)
            tc = Label(self.makeResWin, text="Total Cost")
            tc.grid(row=4, column=0)
             ## calculate the total cost
            ticPrice = []
            baggageCost = []
            for res in self.resList:
                ticPrice.append(int(res[5]))
                if int(res[7]) > 2:
                    baggageCost.append(30)
            totalCost = sum(ticPrice) + sum(baggageCost)
            if student == "yes":
                totalCost = totalCost*0.8
            self.tcV = StringVar()
            self.tcV.set("$" + str(totalCost))
            self.tc = totalCost
            tcE = Entry(self.makeResWin, textvariable = self.tcV, state="readonly")
            tcE.grid(row=4, column=1)
            uc = Label(self.makeResWin, text="Use Card")
            uc.grid(row=5, column=0)
            ## options list of different cards in the system
            sql = "SELECT Right(CardNumber,4) FROM PaymentInfo WHERE Username = %s"
            cursor.execute(sql, self.user)
            cardList = []
            for record in cursor:
                cardList.append(record[0])
            try:
                self.payWith = StringVar(self.makeResWin)
                self.payWith.set(cardList[0])
                ucOM = OptionMenu(self.makeResWin, self.payWith, *cardList)
                ucOM.grid(row=5, column=1, padx = 5)
            except:
                pass
            ucB = Button(self.makeResWin, text="Add Card", command=self.payInfo)
            ucB.grid(row=5, column=2)
            cat = Button(self.makeResWin, text="Add Train", command=self.addTrain)
            cat.grid(row=6,column=0)
            back = Button(self.makeResWin, text="Back", command=self.backPassInfo)
            back.grid(row=7, column=0, columnspan=70, pady=20)
            submit = Button(self.makeResWin, text="Submit", command=self.submitRes)
            submit.grid(row=7, column=80, columnspan=100, pady=20)

    def addTrain(self):
        self.makeResWin.withdraw()
        self.trainSearch()
        
    def removeTicket(self):
        if len(self.resList) == 1:
            removeValue = self.resList[self.var.get()-1]
            self.resList.remove(removeValue)
            messagebox.showerror("Error", "Your cart is now empty. Press OK to return to Choose Functionality")
            self.makeResWin.withdraw()
            self.customerHome()
        else:
            removeValue = self.resList[self.var.get()-1]
            self.resList.remove(removeValue)
            self.makeResWin.withdraw()
            self.makeReservation()
    
    def payInfo(self):
        cursor = self.connect().cursor()
        self.makeResWin.withdraw()
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
        self.exp = StringVar()
        self.exp.set("")
        nocEntry = Entry(aFrame, textvariable=self.nameOnCard, width=25)
        nocEntry.grid(row = 1, column=1, sticky=W)
        cNoEntry = Entry(aFrame, textvariable=self.cardNo, width=25)
        cNoEntry.grid(row = 2, column=1, sticky=W)
        cvvEntry = Entry(aFrame, textvariable=self.cvv, width=10)
        cvvEntry.grid(row = 3, column=1, sticky=W)
        expEntry = Entry(aFrame, textvariable=self.exp, width=10)
        expEntry.grid(row=4, column=1, sticky=W)
        addSub = Button(aFrame, text="Submit", command=self.addCard)
        addSub.grid(row=5, column=0, columnspan=2)
        dc = Label(aFrame, text="Delete Card", font="Arial 14", width=30)
        dc.grid(row=0, column=3, columnspan=2)
        cn=Label(aFrame, text="Card Number")
        cn.grid(row=1, column=3)
        sql = "SELECT Right(CardNumber, 4) FROM PaymentInfo WHERE Username = %s"
        cursor.execute(sql, self.user)
        cardList = []
        for record in cursor:
            cardList.append(record[0])
        self.payWith = StringVar(aFrame)
        try:
            self.payWith.set(cardList[0])
            ucOM = OptionMenu(aFrame, self.payWith, *cardList)
            ucOM.grid(row=1, column=4)
        except:
            delSub = Button(aFrame, text="Submit", command=self.deleteCard)
            delSub.grid(row=5, column=3, columnspan=2)
        
    def addCard(self):
        name = self.nameOnCard.get()
        cardNo = self.cardNo.get()
        cvv = self.cvv.get()
        exp = self.exp.get()
        count = 0
        if name == "" or cardNo == "" or cvv == "" or exp == "":
            messagebox.showerror("Error", "A field is blank")
            count += 1
        if cardNo != "":
            for char in cardNo:
                if char not in "1234567890":
                    messagebox.showerror("Error", "Check Card Number!")
                    count += 1
        if len(cardNo) != 16:
            messagebox.showerror("Error", "Check Card Number!")
            count += 1
        if len(cvv) != 3:
            messagebox.showerror("Error", "Check CVV!")
            count += 1
        if count == 0:
            cursor = self.connect().cursor()
            sql = "INSERT INTO PaymentInfo VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (cardNo, name, cvv, exp, self.user))
            cursor.close()
            self.connect().commit()
            self.payWin.withdraw()
            self.makeResWin.withdraw()
            self.makeReservation()
            
    def deleteCard(self):
        cardNo = self.payWith.get()
        cursor = self.connect().cursor()
        sql = "DELETE FROM PaymentInfo WHERE Right(CardNumber, 4) = %s AND Username = %s"
        cursor.execute(sql, (cardNo, self.user))
        cursor.close()
        self.connect().commit()
        self.payWin.withdraw()
        self.makeResWin.withdraw()
        self.makeReservation()
        
    def backPassInfo(self):
        self.makeResWin.withdraw()
        self.passengerInfoWin.deiconify()
        
    def submitRes(self):
        cardNo = self.payWith.get()
        totalCost = self.tc
        cursor = self.connect().cursor()
        sql = "SELECT COUNT(*) FROM Reservations"
        cursor.execute(sql)
        count = cursor.fetchall()
        resID = count[0][0] + 1
        sql = "SELECT CardNumber FROM PaymentInfo WHERE Right(CardNumber, 4) = %s AND Username = %s"
        cursor.execute(sql, (cardNo, self.user))
        raw = cursor.fetchall()
        fullcardNo = raw[0][0]
        sql = "INSERT INTO Reservations (ReservationID, Username, CardNumber, Status, TotalCost) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (resID, self.user, fullcardNo, '1', totalCost))
        date = self.departdate
        for res in self.resList:
            sql = "INSERT INTO ReservationDetails (ReservationID, TrainNumber, PassengerName, Baggage, Class, DepartsFrom, ArrivesAt, DepartureDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            split = res[2].split("(")
            departs = split[0]
            split2 = res[3].split("(")
            arrives = split2[0]
            if res[4] == "1st Class":
                classs = "First Class"
            else:
                classs = "Second Class"
            cursor.execute(sql, (resID, res[0], res[6], res[7], classs, departs, arrives, date))
        cursor.close()
        self.connect().commit()
        self.makeResWin.withdraw()
        self.startRes = True
        self.confirmWin = Toplevel()
        self.confirmWin.title("Confirmation")
        title = Label(self.confirmWin, text="Confirmation", font="Arial 20")
        title.grid(row = 0, column = 0, columnspan = 2)
        res = Label(self.confirmWin, text= "Reservation ID")
        res.grid(row = 1, column=0)
        self.resID = StringVar()
        self.resID.set(resID)
        resEntry = Entry(self.confirmWin, textvariable = self.resID, state="readonly")
        resEntry.grid(row = 1, column=1)
        d = Label(self.confirmWin, text="Thank you for your purchase! Please save reservation ID for your records.")
        d.grid(row=2, column=0, columnspan=2)
        b = Button(self.confirmWin, text="Back to Choose Functionality", command=self.backHome)
        b.grid(row=3, column=0, columnspan=2)
        
    def backHome(self):        
        self.confirmWin.withdraw()
        self.customerHome()
        
    def updateReservation(self):
        self.custHomeWin.withdraw()
        self.updateResWin = Toplevel()
        self.updateResWin.title("Update Reservation")
        title = Label(self.updateResWin, text = "Update Reservation", font="Arial 20")
        title.grid(row=0, column=0, columnspan = 3)
        resL = Label(self.updateResWin, text = "ReservationID")
        resL.grid(row=1, column=0)
        self.resID = StringVar()
        self.resID.set("")
        resEntry = Entry(self.updateResWin, textvariable=self.resID)
        resEntry.grid(row=1, column=1)
        search = Button(self.updateResWin, text = "Search", command=self.searchRes)
        search.grid(row=1, column=2)
        back = Button(self.updateResWin, text="Back", command=self.updateToFunc)
        back.grid(row=2, column=0, columnspan=3)
        
    def updateToFunc(self):
        self.updateResWin.withdraw()
        self.customerHome()
        
    def searchRes(self):
        ## throw error if resID not found or not made by customer
        ## cant update a cancelled reservation
        ##sql statements lol
        ## also, radiobuttons
        ##
        ##
        ##
        ##
        self.v2 = IntVar()
        self.updateResWin.withdraw()
        self.selectResWin = Toplevel()
        self.selectResWin.title("Update Reservation")
        title = Label(self.selectResWin, text="Update Reservation", font="Arial 20")
        title.grid(row=0,column=0, columnspan=100)
        table = Frame(self.selectResWin)
        table.grid(row=1, column=0, columnspan=100, pady=20, padx=20)
        hList = ["Select", "Train\n(Train Number)", "Time\n(Duration)", "Departs From", "Arrives At", "Class", "Price", "# of Baggage(s)", "Passenger Name"]
        for i in range(len(hList)):
            header = Label(table, text = hList[i])
            header.grid(row = 0, column = i)
        ##sqllist = blahblah
        ##for i in range(len(sqllist)):
            ##r = Radiobutton(table, variable=self.v2, value=i+1)
            ##r.grid(row=i+1, column=0)
            ##for j in range(len(sqllist[0])):
                ##l = Label(table, text=sqllist[i][j])
                ##l.grid(row=i+1, column=i+1)                    
        back = Button(self.selectResWin, text="Back", command=self.searchToSelectRes)
        back.grid(row=2, column=5)
        nxt = Button(self.selectResWin, text="Next", command=self.selectToUpdateRes)
        nxt.grid(row=2, column=15)
        
    def searchToSelectRes(self):
        self.selectResWin.withdraw()
        self.updateResWin.deiconify()

    def selectToUpdateRes(self):
        pass
        ## check that the current date is at least a day before departure day
        ## 
        ##
        ##
        ##
        ##
        ##
        #self.selectResWin.withdraw()
        #do like all of this function LOL
        #
        #
        #self.newdate = StringVar()
        #self.newdate.set("")
        #new = Label(self., text="New Departure Date")
        #new.grid(row=, column=0)
        #ndate = Entry(self., textvariable=self.newdate)
        #ndate.grid(row=, column=1)
        #avail = Button(Self., text="Search Availability", command=self.checkAvail)
        #avail.grid(row=, column=2)
        #up = Label(self. , text="Updated Train Ticket")
        #up.grid(row=,column=0)
        #change = Label(self. , text="Change Fee")
        #change.grid(row=, column=0)
        #changeE = Entry(self. , text="50", state="readonly")
        #changeE.grid(row=, column=1)
        #cost = Label(self. , text="Updated Total Cost")
        #cost.grid(row=, column=0)
        #costE = Entry(self. , text=, state="readonly")
        #costE.grid(row=, column=1)
        
    def cancelReservation(self):
        self.custHomeWin.withdraw()
        self.cancelResIDWin = Toplevel()
        self.cancelResIDWin.title("Cancel Reservation")
        title = Label(self.cancelResIDWin, text = "Cancel Reservation", font="Arial 20")
        title.grid(row=0, column=0, columnspan = 3)
        resID = Label(self.cancelResIDWin, text = "ReservationID")
        resID.grid(row=1, column=0)
        resEntry = Label(self.cancelResIDWin)
        resEntry.grid(row=1, column=1)
        search = Button(self.cancelResIDWin, text = "Search", command=self.cancelRes)
        search.grid(row=1, column=2)
        back = Button(self.cancelResIDWin, text="Back", command=self.cancelToFunc)
        back.grid(row=2, column=0, columnspan=3)
        
    def cancelToFunc(self):
        self.cancelResIDWin.withdraw()
        self.customerHome()
        
    def cancelRes(self):
        # sql statement for list
        # populate the table
        # import total cost
        # import amount to be refunded
        ### 80% of total cost refunded if cancelled 7 days earlier
        # than the earliest departure date
        ### 50% refunded if cancelled more than 1 day earlier but less than 7 days earlier
        # $50 cancellation fee, deducted from refund
        ### cannot cancel a cancelled reservation
        # commit changes
        # refund can't be negatiive
        # 
        #
        #
        #
        #
        #
        #self.cancelResIDWin.withdraw()
        self.cancelResWin = Toplevel()
        self.cancelResWin.title("Cancel Reservation")
        title = Label(self.cancelResWin, text="Cancel Reservation", font="Arial 20")
        title.grid(row=0,column=0, columnspan=100)
        table = Frame(self.cancelResWin)
        table.grid(row=1, column=0, columnspan=100, pady=20, padx=20)
        hList = ["Train\n(Train Number)", "Time\n(Duration)", "Departs From", "Arrives At", "Class", "Price", "# of Baggage(s)", "Passenger Name"]
        for i in range(len(hList)):
            header = Label(table, text = hList[i])
            header.grid(row = 0, column = i)
        aFrame = Frame(self.cancelResWin)
        aFrame.grid(row=2, column=0, pady=10, padx=20, sticky=W)
        acList = ["Total Cost of Reservation", "Date of Cancellation", "Amount to be Refunded"]
        for i in range(len(acList)):
            header = Label(aFrame, text = acList[i])
            header.grid(row = i, column = 0)
        tc = Entry(aFrame, state="readonly")
        tc.grid(row=0, column=1)
        currentTime = datetime.date.today().strftime("%m/%d/%Y")
        date = StringVar()
        date.set(currentTime)
        dc = Entry(aFrame, textvariable=date, state="readonly")
        dc.grid(row=1, column=1)
        ar = Entry(aFrame, state="readonly")
        ar.grid(row=2, column=1)
        back = Button(self.cancelResWin, text="Back", command=self.cancelBack)
        back.grid(row=3, column=0)
        sbt = Button(self.cancelResWin, text="Submit", command=self.cancelSubmit)
        sbt.grid(row=3, column=1)
        
    def cancelBack(self):
        self.cancelResWin.withdraw()
        self.cancelReservation()
        
    def cancelSubmit(self):
        ## make the thing happen in the database
        ## recalculate total cost and update it
        ##
        ##
        ##
        ##
        ##
        self.cancelResWin.withdraw()
        #sql changes
        self.customerHome()
        
    def viewReview(self):
        self.custHomeWin.withdraw()
        self.viewReviewWin = Toplevel()
        self.viewReviewWin.title("View Review")
        title = Label(self.viewReviewWin, text = "View Review", font="Arial 20")
        title.grid(row=0, column=0, columnspan = 2)
        train = Label(self.viewReviewWin, text = "Train Number")
        train.grid(row=1, column=0)
        self.trainNo = StringVar()
        self.trainNo.set("")
        trainEntry = Entry(self.viewReviewWin, textvariable=self.trainNo)
        trainEntry.grid(row=1, column=1)
        back = Button(self.viewReviewWin, text="Back", command=self.viewToHome)
        back.grid(row=2, column=0)
        nxt = Button(self.viewReviewWin, text = "Next", command=self.viewReviews)
        nxt.grid(row=2, column=1)
        
    def viewToHome(self):
        self.viewReviewWin.withdraw()
        self.customerHome()
        
    def viewReviews(self):
        cursor=self.connect().cursor()
        sql= "SELECT Rating, Comment FROM Reviews WHERE TrainNumber = %s"
        check=cursor.execute(sql,self.trainNo)
        if check==0:
            messagebox.showerror("Error","Train Number Invalid")
        else:
            self.viewReviewWin.withdraw()
            self.viewReviewsWin = Toplevel()
            self.viewReviewsWin.title("View Reviews")
            title = Label(self.viewReviewsWin, text = "View Reviews", font="Arial 20")
            title.grid(row=0, column=0, columnspan = 100)
            table = Frame(self.viewReviewsWin)
            table.grid(row=1, column=0, columnspan=100, pady=20, padx=20)
            hList = ["Rating", "Comment"]
            for i in range(len(hList)):
                header = Label(table, text = hList[i])
                header.grid(row = 0, column = i)
            reviewList=[]
            for record in cursor:
                reviewList.append([record[0], record[1]])
            cursor.close()
            for i in range(len(reviewList)):
                for j in range(2):
                    r = Label(table, text=reviewList[i][j])
                    r.grid(row=i+1, column=j)
            back=Button(self.viewReviewsWin, text="Back to Choose Functionality", command=self.viewReviewsToHome)
            back.grid(row=2, column=0, columnspan=100)
            
    def viewReviewsToHome(self):
        self.viewReviewsWin.withdraw()
        self.customerHome()
        
    def giveReview(self):
        self.custHomeWin.withdraw()
        self.giveReviewWin = Toplevel()
        self.giveReviewWin.title("Give Review")
        title = Label(self.giveReviewWin, text = "Give Review", font="Arial 20")
        title.grid(row=0, column=0)
        hList = ["Train Number", "Rating", "Comment"]
        hFrame = Frame(self.giveReviewWin)
        hFrame.grid(row=1, column=0)
        for i in range(len(hList)):
            header = Label(hFrame, text = hList[i])
            header.grid(row = i, column = 0)
        sql = "SELECT TrainNumber FROM TrainRoutes"
        cursor = self.connect().cursor()
        cursor.execute(sql)
        trainList=[]
        for record in cursor:
            trainList.append(record[0])
        self.trainNo = StringVar(hFrame)
        self.trainNo.set(trainList[0])
        train = OptionMenu(hFrame, self.trainNo, *trainList)
        train.grid(row=0, column=1, sticky=W)
        ratingList=["Very Good", "Good", "Neutral", "Bad", "Very Bad"]
        self.rVar = StringVar()
        self.rVar.set(ratingList[0])
        rating=OptionMenu(hFrame, self.rVar, *ratingList)
        rating.grid(row=1, column=1, sticky=W)
        self.comment=StringVar()
        self.comment.set("")
        comment = Entry(hFrame, textvariable=self.comment, width=25)
        comment.grid(row=2, column=1, sticky=W)
        back = Button(self.giveReviewWin, text="Submit", command=self.submitReview)
        back.grid(row=2, column=0)
        
    def submitReview(self):
        self.user="serena"
        cursor=self.connect().cursor()
        sql= "INSERT INTO Reviews VALUES (NULL, %s, %s, %s, %s)"
        cursor.execute(sql,(self.comment.get(),self.rVar.get(),self.trainNo.get(), self.user))
        if cursor.rowcount==0:
            messagebox.showerror("Error","Train Number Invalid")
        cursor.close()
        self.connect().commit()
        self.giveReviewWin.withdraw()
        self.customerHome()
    
    def addSchoolInfo(self):
        self.custHomeWin.withdraw()
        self.addSchoolWin = Toplevel()
        self.addSchoolWin.title("Add School Info")
        addLabel = Label(self.addSchoolWin, text = "Add School Info", font = "Arial 20", pady = 20, padx = 30)
        addLabel.grid(row = 0, column = 0, columnspan=2)
        emailLabel = Label(self.addSchoolWin, text = "School Email Address:")
        emailLabel.grid(row = 1, column = 0, sticky = E, padx = 10)
        self.schoolStr = StringVar()
        self.schoolStr.set("")
        emailEntry = Entry(self.addSchoolWin, textvariable = self.schoolStr, width = 30)
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
        self.customerHome()
        
    def submitSchoolInfo(self):
        cursor = self.connect().cursor()
        sql = "UPDATE Customers SET Customers.Student= '1' WHERE Customers.Username = %s AND %s LIKE '%%@%%.edu'"
        school = self.schoolStr.get()
        cursor.execute(sql, (self.user,school))
        sql = "SELECT Customers.Username FROM Customers WHERE Customers.Username = %s AND Customers.Student = '1'"
        check = cursor.execute(sql, self.user)
        if check == 0:
            messagebox.showerror("Error", "This is not a valid email address")
        else:
            messagebox.showinfo("Student Discount", "Student Discount Applied")
            self.addSchoolWin.withdraw()
            self.customerHome()
            cursor.close()
            self.connect().commit()
            
    def managerHome(self):
        #self.loginWin.withdraw()
        self.mgrHomeWin=Toplevel()
        self.mgrHomeWin.title("Choose Functionality")
        title = Label(self.mgrHomeWin, text = "Choose Functionality", font = "Arial 20", pady = 20, padx = 30)
        title.grid(row = 0, column = 0)
        ## buttons
        buttonframe = Frame(self.mgrHomeWin, pady = 30)
        buttonframe.grid(row = 1, column = 0)
        button00 = Button(buttonframe, text = "View Revenue Report",
                          padx=10,pady=5, font = "Arial 10", command = self.revReport)
        button00.pack(fill=X)
        button01 = Button(buttonframe, text = "View Popular Route Report",
                          padx=10,pady=5, font = "Arial 10", command = self.popRoute)
        button01.pack(fill=X)
        logout = Button(self.mgrHomeWin, text = "Log Out", command = self.mgrLogOut)
        logout.grid(row = 2, column = 0, pady = 10)
        
    def revReport(self):
        self.mgrHomeWin.withdraw()
        self.revenueWin=Toplevel()
        self.revenueWin.title("View Revenue Report")
        title = Label(self.revenueWin, text = "View Revenue Report", font = "Arial 20", pady = 20, padx = 30)
        title.grid(row = 0, column = 0)
        table=Frame(self.revenueWin)
        table.grid(row=1, column=0)
        hList=["Month", "Revenue"]
        for i in range(len(hList)):
            h = Label(table, text=hList[i])
            h.grid(row=0, column=i)
        back = Button(self.revenueWin, text="Back", command=self.revToHome)
        back.grid(row=2, column=0)
##        sql=""
##        self.connect()
##        cursor=self.connect().cursor()
##        cursor.execute(sql)
##        tableList=[]
##        for record in cursor:
##            tableList.append(record)
##        cursor.close()
    def revToHome(self):
        self.revenueWin.withdraw()
        self.mgrHomeWin.deiconify()
    def popRoute(self):
        self.mgrHomeWin.withdraw()
        self.popularWin=Toplevel()
        self.popularWin.title("View Popular Route Report")
        title = Label(self.popularWin, text = "View Popular Route Report", font = "Arial 20", pady = 20, padx = 30)
        title.grid(row = 0, column = 0)
        table=Frame(self.popularWin)
        table.grid(row=1, column=0)
        hList=["Month", "Train Number", "# of Reservations"]
        for i in range(len(hList)):
            h = Label(table, text=hList[i])
            h.grid(row=0, column=i)
        back = Button(self.popularWin, text="Back", command=self.popToHome)
        back.grid(row=2, column=0)
    def popToHome(self):
        self.popularWin.withdraw()
        self.mgrHomeWin.deiconify()
        
##        sql=""
##        cursor=self.connect().cursor()
##        cursor.execute(sql)
##        tableList=[]
##        for record in cursor:
##            tableList.append(record)
##        cursor.close()
##
        
    def mgrLogOut(self):
        self.mgrHomeWin.withdraw()
        self.loginWin.deiconify()
        self.connect().close()
        
    def logOut(self):
        self.custHomeWin.withdraw()
        self.loginWin.deiconify()
        self.connect().close()
rootWin = Tk()
app = gtTrains(rootWin)
rootWin.mainloop()
