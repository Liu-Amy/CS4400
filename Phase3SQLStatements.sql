// Figure 1: Log in
// Status: Works
SELECT *
FROM Users
WHERE BINARY Username = %s AND BINARY Password = %s

// Check if user is Manager
// Status: Works
SELECT *
FROM Managers
WHERE BINARY Username = %s

// Check if user is Customer
// Status: Works
SELECT *
FROM Customers
WHERE BINARY Username = %s

// Figure 2: New user registration
// Status: Works
INSERT INTO Customers
VALUES (%s, %s, %s)

INSERT INTO Users
VALUES (%s, %s)

// Check if username has been used
SELECT *
FROM Users
WHERE BINARY Username = %s

// Unique email or nah
SELECT *
FROM Customers
WHERE Email = %s

// Valid email or nah
SELECT *
FROM Customers
WHERE %s LIKE '&&@%%.%%'

// Figure 4: Add school info
// Status: Works
UPDATE Customers
SET Customers.Student= "yes"
WHERE Customers.Username = %s AND %s LIKE '%@%.edu'

// Figure 5: View train schedule
// Status: Works
SELECT ArrivalTime, DepartureTime, StationName
FROM Stops
WHERE TrainNumber = %s
ORDER BY ArrivalTime

// Figure 6: Make a reservation dropdown
// Status: Works
SELECT CONCAT(StationName," (", Location, ")") as dropdownChoices, StationName
FROM Stations

// Figure 7: Select departure
// Status: Works
SELECT
  TrainRoutes.TrainNumber, CONCAT(DepartureStop.DepartureTime," - ",
    ArrivalStop.ArrivalTime, "\n", TIMEDIFF(ArrivalStop.ArrivalTime,
    DepartureStop.DepartureTime)) as Time,
  DepartureStop.DepartureTime,
  ArrivalStop.ArrivalTime,
  TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) as Duration,
  TrainRoutes.FirstClassPrice,
  TrainRoutes.SecondClassPrice
FROM TrainRoutes
INNER JOIN Stops as ArrivalStop ON TrainRoutes.TrainNumber = ArrivalStop.TrainNumber
INNER JOIN Stops as DepartureStop ON TrainRoutes.TrainNumber = DepartureStop.TrainNumber
WHERE DepartureStop.StationName = %s AND
  ArrivalStop.StationName = %s AND
  TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) > "00:00:00"
  -- TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) <> "NULL"

// Figure 8: Travel extras and passenger info - Number of Baggage dropdown
// Status: Works
SELECT SystemInfo.MaxBaggage
FROM SystemInfo

// Figure 8: Make reservation 1 use card dropdown
// Status: Works
SELECT Right(CardNumber, 4)
FROM PaymentInfo
WHERE Username = %s

// Figure 8: Make reservation 1 Student or nah
// Status: Works
SELECT Customers.Student
FROM Customers
WHERE Customers.Username = %s

// Figure 10: Payment info Add card
// Status: Works
INSERT INTO PaymentInfo
VALUES (%s, %s, %s, %s, Username)

// Figure 10: Does the customer already have this card in the database?
// Status: Works
SELECT *
FROM PaymentInfo
WHERE PaymentInfo.CardNumber = %s AND PaymentInfo.Username = %s

// Figure 10: Payment info - Find Card to Delete dropdown
// Status: Works
SELECT Right(CardNumber, 4)
FROM PaymentInfo
WHERE Username = %s

// Figure 10: Payment info  Delete Card
// Status: Works
DELETE PaymentInfo
FROM PaymentInfo
INNER JOIN Customers ON PaymentInfo.Username = Customers.Username
LEFT OUTER JOIN Reservations ON PaymentInfo.CardNumber = Reservations.CardNumber
WHERE Customers.Username = %s AND
  (Reservations.Status = 0 OR Reservations.Status is NULL) AND
  (PaymentInfo.CardNumber = %s OR PaymentInfo.CardNumber is NULL)

// Figure 11: Confirmation screen
// Status: Works
// Number of bags over max free
SELECT %s - SystemInfo.FreeBaggage
FROM SystemInfo

// Figure 11: Confirmation screen
// Status: Nope (SHOULD WORK WITH AUTOINCREMENT???)
// Add to Reservations - IF CUSTOMER IS A STUDENT
// Next ReservationID is generated using auto-increment
// VALUES (%s, %s, 1, (PriceOfTicket + NumBagsOverTwo*30)*0.8)
INSERT INTO Reservations(Username, CardNumber, Status, TotalCost)
VALUES (%s, %s, 1, ((%s + %s*30)*0.08))

// Figure 11: Confirmation screen
// Status: Nope (SHOULD WORK WITH AUTOINCREMENT???)
// Add to Reservations - IF CUSTOMER IS NOT A STUDENT
// Next ReservationID is generated using auto-increment
// VALUES (%s, %s, 1, (PriceOfTicket + NumBagsOverTwo*30))
INSERT INTO Reservations(Username, CardNumber, Status, TotalCost)
VALUES (%s, %s, 1, ((%s + %s*30)))

// Figure 11: Confirmation screen
// Status: Works
// Add to ReservationDetails
INSERT INTO ReservationDetails (ReservationID, TrainNumber, PassengerName, Baggage, Class, DepartureDate, DepartsFrom, ArrivesAt)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

// Figure 13: Update reservation 2
// Returns number of tickets there are in a reservation
// Status: Works
// %s = ReservationID
SELECT COUNT(*)
FROM Reservations
WHERE Reservations.ReservationID = %s

// Figure 13: Update reservation 2
// Status: Works
// Get DepartsFrom in ReservationDetails; Used to generate table
SELECT DepartsFrom
FROM ReservationDetails
WHERE ReservationID = %s

// Figure 13: Update reservation 2
// Status: Works
// Get ArrivesAt in ReservationDetails
SELECT ArrivesAt
FROM ReservationDetails
WHERE ReservationID = %s

// Figure 13: Update reservation 2
// Status: Works
// Shows table of details of reservation; Used to generate table
SELECT TrainRoutes.TrainNumber,
  CONCAT(ReservationDetails.DepartureDate, " " , DepartureStop.DepartureTime," - ", ArrivalStop.ArrivalTime, "\n",
    TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime)) as Time,
  CONCAT(DepartureStation.Location, "(", DepartureStation.StationName, ")") as DepartsFrom,
  CONCAT(ArrivalStation.Location, "(", ArrivalStation.StationName, ")") as ArrivesAt,
  TrainRoutes.FirstClassPrice,
  TrainRoutes.SecondClassPrice,
  ReservationDetails.Baggage,
  ReservationDetails.PassengerName
FROM TrainRoutes
INNER JOIN ReservationDetails on TrainRoutes.TrainNumber = ReservationDetails.TrainNumber
INNER JOIN Reservations on ReservationDetails.ReservationID = Reservations.ReservationID
INNER JOIN Stops as ArrivalStop on TrainRoutes.TrainNumber = ArrivalStop.TrainNumber
INNER JOIN Stops as DepartureStop on TrainRoutes.TrainNumber = DepartureStop.TrainNumber
INNER JOIN Stations as ArrivalStation on ArrivalStop.StationName = ArrivalStation.StationName
INNER JOIN Stations as DepartureStation on DepartureStop.StationName = DepartureStation.StationName
WHERE ReservationDetails.ReservationID = %s
  Reservations.Username = %s AND
  DepartureStop.StationName = %s AND
  ArrivalStop.StationName = %s AND
  TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) > "00:00:00"

// Figure 14: Update reservation 3
UPDATE ReservationDetails
SET DepartureTime = %s
WHERE ReservationID = %s AND TrainNumber = %

// Figure 14: Update reservation 3 - shows the Change Fee
SELECT ChangeFee
FROM SystemInfo

// Figure 14: Update reservation 3
UPDATE Reservations
SET TotalCost = TotalCost + 50
WHERE ReservationID = %s

// Figure 15: Cancel reservation
UPDATE Reservations
SET Status = 0
WHERE ReservationID = %s

// Figure 15: Cancel reservation
// Shows TotalCost of reservation
SELECT TotalCost
FROM Reservations
WHERE ReservationID = %s

// Figure 16: View review
SELECT Rating, Comment
FROM Reviews
WHERE TrainNumber = %s

// Figure 17: Give review
INSERT INTO Reviews
VALUES (%s, %s, %s, %s, %s)

// Figure 19: Manager - View revenue report
// Call it three times for the most recent three monthes
SELECT MONTH(NOW()), SUM(Reservations.TotalCost)
FROM Reservations
WHERE Reservations.ReservationID in (
  SELECT ReservationID
  FROM ReservationDetails
  WHERE MONTH(DepartureDate) = MONTH(NOW())
)
UNION
SELECT MONTH(NOW())-1, SUM(Reservations.TotalCost)
FROM Reservations
WHERE Reservations.ReservationID in (
  SELECT ReservationID
  FROM ReservationDetails
  WHERE MONTH(DepartureDate) = MONTH(NOW()) - 1
)
UNION
SELECT MONTH(NOW())-2, SUM(Reservations.TotalCost)
FROM Reservations
WHERE Reservations.ReservationID in (
  SELECT ReservationID
  FROM ReservationDetails
  WHERE MONTH(DepartureDate) = MONTH(NOW())-2
)

// Las figure: Manager - View popular route report
SELECT MONTH(NOW()) AS Month, TrainNumber AS Train, COUNT(TrainNumber) AS Num
FROM ReservationDetails
INNER JOIN Reservations ON ReservationDetails.ReservationID = Reservations.ReservationID
WHERE MONTH(DepartureDate) = MONTH(NOW())
GROUP BY Month
UNION
SELECT MONTH(NOW())-1 AS Month, TrainNumber AS Train, COUNT(TrainNumber) AS Num
FROM ReservationDetails
INNER JOIN Reservations ON ReservationDetails.ReservationID = Reservations.ReservationID
WHERE MONTH(DepartureDate) = MONTH(NOW())-1
GROUP BY Month
UNION
SELECT MONTH(NOW())-2 AS Month, TrainNumber AS Train, COUNT(TrainNumber) AS Num
FROM ReservationDetails
INNER JOIN Reservations ON ReservationDetails.ReservationID = Reservations.ReservationID
WHERE MONTH(DepartureDate) = MONTH(NOW())-2
GROUP BY Month
ORDER BY Month ASC, Num DESC
