// Figure 1: Log in
SELECT * FROM Users WHERE Username = %s AND (Password LIKE BINARY %s)
// Check if user is Manager
SELECT * FROM Managers WHERE Username = %s


// Figure 2: New user registration
// checking if username or email in use (case-insensitive)
SELECT Username FROM Users WHERE Username = %s
SELECT Email FROM Customers WHERE Email = %s
// inserting new user/customer
INSERT INTO Users (Username, Password) VALUES (%s, %s)
INSERT INTO Customers (Username, Email, Student) VALUES (%s, %s, %s)


// Figure 4: Add school info
// checks if valid email address, for throwing errors
SELECT Customers.Username FROM Customers WHERE Customers.Username = %s AND Customers.Student = '1'
// update student status
UPDATE Customers SET Customers.Student= '1' WHERE Customers.Username = %s AND %s LIKE '%%@%%.edu'


// Figure 5: View train schedule
SELECT ArrivalTime, DepartureTime, StationName FROM Stops WHERE TrainNumber = %s ORDER BY ArrivalTime
SELECT DISTINCT TrainNumber FROM Stops WHERE TrainNumber=%s


// Figure 6: Make a reservation dropdown
SELECT CONCAT(StationName,' (', Location, ')'), StationName FROM Stations


// Figure 7: Select departure
SELECT TrainRoutes.TrainNumber, 
  CONCAT(DepartureStop.DepartureTime,' - ', 
  ArrivalStop.ArrivalTime, '\n', 
  TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime)), 
  DepartureStop.DepartureTime, ArrivalStop.ArrivalTime, 
  TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) as Duration, 
  TrainRoutes.FirstClassPrice, 
  TrainRoutes.SecondClassPrice 
FROM TrainRoutes 
INNER JOIN Stops as ArrivalStop ON TrainRoutes.TrainNumber = ArrivalStop.TrainNumber 
INNER JOIN Stops as DepartureStop ON TrainRoutes.TrainNumber = DepartureStop.TrainNumber 
WHERE DepartureStop.StationName = %s AND ArrivalStop.StationName = %s 
AND TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) > '00:00:00'"


// Figure 8: Make reservation 1 
SELECT Customers.Student FROM Customers WHERE Customers.Username = %s
SELECT Right(CardNumber,4) FROM PaymentInfo WHERE Username = %s


// Figure 10: Payment info Add card
INSERT INTO PaymentInfo VALUES (%s, %s, %s, %s, %s)


// Figure 10: Does the customer already have this card in the database?
SELECT * FROM PaymentInfo WHERE PaymentInfo.CardNumber = %s AND PaymentInfo.Username = %s


// Figure 10: Payment info  Delete Card
DELETE PaymentInfo
FROM PaymentInfo
INNER JOIN Customers ON PaymentInfo.Username = Customers.Username
LEFT OUTER JOIN Reservations ON PaymentInfo.CardNumber = Reservations.CardNumber
WHERE Customers.Username = %s AND
  (Reservations.Status = 0 OR Reservations.Status is NULL) AND
  (PaymentInfo.CardNumber = %s OR PaymentInfo.CardNumber is NULL)


// Figure 11: Confirmation screen
SELECT COUNT(*) FROM Reservations
SELECT CardNumber FROM PaymentInfo WHERE Right(CardNumber, 4) = %s AND Username = %s
INSERT INTO Reservations (ReservationID, Username, CardNumber, Status, TotalCost) VALUES (%s, %s, %s, %s, %s)
INSERT INTO ReservationDetails (ReservationID, TrainNumber, PassengerName, Baggage, Class, DepartsFrom, ArrivesAt, DepartureDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)


// Figures 13-14: Update reservation 
SELECT * FROM Reservations WHERE Reservations.ReservationID = %s
SELECT * FROM Reservations WHERE Username = %s AND ReservationID=%s
SELECT Status FROM Reservations WHERE ReservationID = %s
SELECT TrainRoutes.TrainNumber, 
CONCAT(DepartureStop.DepartureTime,' - ', ArrivalStop.ArrivalTime, '\n', 
  TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime)), 
  DepartureStop.DepartureTime, ArrivalStop.ArrivalTime, 
  TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) as Duration, 
  TrainRoutes.FirstClassPrice, TrainRoutes.SecondClassPrice 
  FROM TrainRoutes 
  INNER JOIN Stops as ArrivalStop  ON TrainRoutes.TrainNumber = ArrivalStop.TrainNumber 
  INNER JOIN Stops as DepartureStop ON TrainRoutes.TrainNumber = DepartureStop.TrainNumber 
  WHERE DepartureStop.StationName = %s AND ArrivalStop.StationName = %s 
  AND TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) > '00:00:00'"
SELECT ChangeFee FROM SystemInfo
SELECT TotalCost FROM Reservations WHERE ReservationID = %s
UPDATE ReservationDetails SET DepartureDate = %s WHERE ReservationID = %s AND TrainNumber = %s
UPDATE Reservations SET TotalCost = TotalCost + 50 WHERE ReservationID = %s


// Figure 15: Cancel reservation 
SELECT * FROM ReservationDetails WHERE ReservationID = %s
SELECT * FROM Reservations WHERE Username = %s AND ReservationID=%s
SELECT Status FROM Reservations WHERE ReservationID = %s
SELECT TrainRoutes.TrainNumber, CONCAT(DepartureStop.DepartureTime,' - ', ArrivalStop.ArrivalTime, '\n', 
  TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime)), DepartureStop.DepartureTime, 
  ArrivalStop.ArrivalTime, TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) as Duration, 
  TrainRoutes.FirstClassPrice, TrainRoutes.SecondClassPrice FROM TrainRoutes 
  INNER JOIN Stops as ArrivalStop ON TrainRoutes.TrainNumber = ArrivalStop.TrainNumber 
  INNER JOIN Stops as DepartureStop ON TrainRoutes.TrainNumber = DepartureStop.TrainNumber 
  WHERE DepartureStop.StationName = %s AND ArrivalStop.StationName = %s 
  AND TIMEDIFF(ArrivalStop.ArrivalTime, DepartureStop.DepartureTime) > '00:00:00'"
SELECT TotalCost FROM Reservations WHERE ReservationID = %s
UPDATE Reservations SET Status = '0' WHERE ReservationID = %s
UPDATE Reservations SET TotalCost = %s WHERE ReservationID = %s


// Figure 16: View review
SELECT Rating, Comment FROM Reviews WHERE TrainNumber = %s


// Figure 17: Give review
SELECT TrainNumber FROM TrainRoutes
INSERT INTO Reviews VALUES (NULL, %s, %s, %s, %s)


// Figure 19: Manager - View revenue report
SELECT MONTH(NOW())-2, CONCAT('$',SUM(Reservations.TotalCost))FROM Reservations WHERE Reservations.ReservationID in 
(SELECT ReservationID FROM ReservationDetails WHERE MONTH(DepartureDate) = MONTH(NOW())-2)
UNION 
SELECT MONTH(NOW())-1, CONCAT('$',SUM(Reservations.TotalCost)) FROM Reservations WHERE Reservations.ReservationID in 
(SELECT ReservationID FROM ReservationDetails WHERE MONTH(DepartureDate) = MONTH(NOW())-1) 
UNION 
SELECT MONTH(NOW()), CONCAT('$',SUM(Reservations.TotalCost)) FROM Reservations WHERE Reservations.ReservationID in 
(SELECT ReservationID FROM ReservationDetails WHERE MONTH(DepartureDate) = MONTH(NOW()))"


// Figure 20: Manager - View popular route report
SELECT MONTH(NOW())-2, TrainNumber, COUNT( TrainNumber ) FROM ReservationDetails 
  INNER JOIN Reservations ON ReservationDetails.ReservationID = Reservations.ReservationID 
  WHERE MONTH( DepartureDate ) = Month(NOW())-2 
  GROUP BY TrainNumber 
  ORDER BY Count(TrainNumber) DESC 
  LIMIT 3
SELECT MONTH(NOW())-1, TrainNumber, COUNT( TrainNumber ) FROM ReservationDetails 
  INNER JOIN Reservations ON ReservationDetails.ReservationID = Reservations.ReservationID 
  WHERE MONTH( DepartureDate ) = Month(NOW())-1 
  GROUP BY TrainNumber ORDER BY Count(TrainNumber) DESC 
  LIMIT 3
SELECT MONTH(NOW()), TrainNumber, COUNT( TrainNumber ) FROM ReservationDetails 
  INNER JOIN Reservations ON ReservationDetails.ReservationID = Reservations.ReservationID 
  WHERE MONTH( DepartureDate ) = Month(NOW()) 
  GROUP BY TrainNumber ORDER BY Count(TrainNumber) DESC 
  LIMIT 3
        
