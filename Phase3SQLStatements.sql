// Figure 1: Log in
SELECT *
FROM Users
WHERE BINARY Username = %s AND BINARY Password = %s

// Check if user is Manager
SELECT *
FROM Managers
WHERE BINARY Username %s

// Check if user is Customer
SELECT *
FROM Customers
WHERE BINARY Username %s

// Figure 2: New user registration
INSERT INTO Customers
VALUES (%s, %s, %s)

// Figure 4: Add school info
UPDATE Customers
SET Student = “yes”
WHERE Username = %s

// Figure 5: View train schedule
SELECT ArrivalTime, DepartureTime, StationName
FROM Stops
WHERE TrainNumber = %s

// Figure 6: Make a reservation dropdown
SELECT CONCAT(StationName," (", Location, ")"), StationName
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

// Figure 8: Travel extras and passenger info
Update ReservationDetails
SET Baggage = %s, PassengerName = %s
WHERE ReservationID = %s

// Figure 8: Make reservation 1 use card dropdown
SELECT PaymentInfo.CardNummber
FROM PaymentInfo
WHERE PaymentInfo.Username = %s

// Figure 8: Make reservation 1 Student or nah
SELECT Customers.Student
FROM Customers
WHERE Customers.Username

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
Update PaymentInfo
SET CardNummber = %s, NameOnCard = %s, CVV = %s, ExpDate = %s
WHERE PaymentInfo.Username = %s

// Figure 10: Payment info Find Card to Delete
SELECT PaymentInfo.CardNummber
FROM PaymentInfo
INNER JOIN Customers ON PaymentInfo.Username = Customers.Username
WHERE Customers = %s

// Figure 10: Payment info Delete Card
DELETE PaymentInfo
FROM PaymentInfo
INNER JOIN Customers ON PaymentInfo.Username = Customers.Username
INNER JOIN Reservations ON PaymentInfo.CardNummber = Reservations.CardNummber
WHERE Customers = %s AND
  Reservations.Status = 0; --0 bit means the reservation was canceled

// Pigure 11: Confirmation screen
// Add to Reservations
INSERT INTO Reservations
VALUES (%s, %s, %s, %s)

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

// NEED SOMETHING FOR UPDATE TOTAL COST
// HOW TO GET TOTAL COST THOUGH???
// ADD TOTAL COST ATTRIBUTE

// Cancel reservation

// View review

// Give review

// Manager - View revenue report

// Manager - View popular route report
