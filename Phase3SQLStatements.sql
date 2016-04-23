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

// Figure 4: Add school info
// Status: Works
UPDATE Customers
SET Customers.Student= "yes"
WHERE Customers.Username = %s AND Customers.Email LIKE '%@%.edu%'

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
// Account for multiple legs of a train
// HOW DA FUQ DOES IT DO THAT???
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

// NOT TESTED
// Figure 8: Travel extras and passenger info
Update ReservationDetails
SET Baggage = %s, PassengerName = %s
WHERE ReservationID = %s

// Figure 8: Make reservation 1 use card dropdown
SELECT CardNumber
FROM PaymentInfo
WHERE Username = %s

// Figure 8: Make reservation 1 Student or nah
SELECT Customers.Student
FROM Customers
WHERE Customers.Username = %s

// Figure 8: Make reservation 1
-- SELECT
--   TrainRoutes.TrainNumber,
--   DepartureStop.DepartureTime,
--   ArrivalStop.ArrivalTime,
--   TIMEDIFF(ArrivalStop.ArrivalTime ,DepartureStop.DepartureTime) as Duration,
--   DepartureStop.StationName as DepartsFrom,
--   ArrivalStop.StationName as ArrivesAt,
--   CASE WHEN ReservationDetails.Class = "First Class" THEN TrainRoutes.FirstClassPrice as Price,
--        WHEN ReservationDetails.Class - "Second Class" Then TrainRoutes.SecondClassPrice as Price,
--   END CASE
--   ReservationDetails.Baggage as NumBaggages,
--   ReservationDetails.PassengerName
-- FROM TrainRoutes
-- INNER JOIN ReservationDetails ON ReservationDetails.TrainNumber = TrainRoutes.TrainNumber
-- INNER JOIN Stops as ArrivalStop ON TrainRoutes.TrainNumber = ArrivalStop.TrainNumber
-- INNER JOIN Stops as DepartureStop ON TrainRoutes.TrainNumber = DepartureStop.TrainNumber
-- WHERE DepartureStop.StationName = %s
--   AND ArrivalStop.StationName = %s
--   AND TIMEDIFF(ArrivalStop.ArrivalTime ,DepartureStop.DepartureTime) > "00:00:00"

// Figure 10: Payment info Add card
INSERT INTO PaymentInfo
VALUES (%s, %s, %s, %s, Username)

// Figure 10: Payment info Find Card to Delete dropdown
-- SELECT PaymentInfo.CardNummber
-- FROM PaymentInfo
-- INNER JOIN Customers ON PaymentInfo.Username = Customers.Username
-- WHERE Customers = %s
SELECT CardNumber
FROM PaymentInfo
WHERE Username = %s


// NOT TESTED
// Figure 10: Payment info Delete Card
DELETE PaymentInfo
FROM PaymentInfo
INNER JOIN Customers ON PaymentInfo.Username = Customers.Username
INNER JOIN Reservations ON PaymentInfo.CardNummber = Reservations.CardNummber
WHERE Customers = %s AND
  Reservations.Status = 0; --0 bit means the reservation was canceled

DELETE PaymentInfo.*
FROM PaymentInfo
INNER JOIN Customers ON PaymentInfo.Username = Customers.Username
INNER JOIN Reservations ON PaymentInfo.CardNumber = Reservations.CardNumber
WHERE Customers.Username = "aliu3" AND
  Reservations.Status = 0


// Pigure 11: Confirmation screen
// Add to Reservations
INSERT INTO Reservations
VALUES (%s, %s, %s, %s, %s)

// Pigure 11: Confirmation screen
// Add to ReservationDetails
INSERT INTO Customers
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

// Figure 13: Update reservation 2
SELECT
FROM ReservationDetails
INNER JOIN Reservations ON ReservationDetails.ReservationID = Reservations.ReservationID
INNER JOIN TrainRoutes On ReservationDetails.TrainNumber = TrainRoutes.TrainNumber
INNER JOIN Stops as ArrivalStop ON TrainRoutes.TrainNumber = ArrivalStop.TrainNumber
INNER JOIN Stops as DepartureStop on TrainNumber.TrainNumber = DepartureStop.TrainNumber
WHERE Reservations.ReservationID = %s AND
  Reservations.Status = 1 AND
  -- TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) > "00:00:00"

// Figure 14: Update reservation 3

// Figure 15: Cancel reservation

// Figure 16: View review
SELECT Rating, Comment
FROM Reviews
WHERE TrainNumber = %s

// Figure 17: Give review
INSERT INTO Reviews
VALUES (%s, %s, %s, %s, %s)

// Figure 19: Manager - View revenue report
// Call it three times for the most recent three monthes
SELECT DATEPART(mm, DepartureDate), SUM(Reservations.TotalSum)
FROM Reservations
INNER JOIN ReservationDetails ON ReservationDetails.ReservationID = Reservations.Reservations
WHERE DATEPART(mm, DepartureDate) = %s

// Las figure: Manager - View popular route report
SELECT DATEPART(mm, DepartureDate), TrainNumber, COUNT(*)
FROM ReservationDetails
INNER JOIN TrainRoutes ON ReservationDetails.ReservationID = Reservations.ReservationID
WHERE DATEPART(mm, DepartureDate) = %s
GROUP BY TrainNumber
