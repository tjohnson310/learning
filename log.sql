-- 1. Look at the crime reports:
SELECT description, month, day, year, street FROM crime_scene_reports WHERE
(year = 2023 AND month = 7 AND day = 28 AND street LIKE "%Humphrey%");

-- From the crime reports, three witness state that the theft took place at 10:15am at the bakery on Humphrey Street
-- (the street more sure than the time)

-- 2. Look at who was interviewed at the scene and what was said
SELECT name, transcript FROM interviews WHERE (month = 7 AND day = 28 AND year = 2023);

-- Jose says a man might've traveled to Bohemia. Eugene says Holmes mentioned Windibank is back from France. Barbara says an annoyed German is speaking cryptically.
-- Ruth says she saw the thief get into a car and leave, within 10 minutes after the theft. Eugene recognized the thief from the ATM at Leggett Street withdrawing money.
-- Raymond says the thief plans the catch the earliest flight on July 29, 2023.  Lily's sons just traveled to Paris.

-- 3. Check the license_pltes leaving the bakery around 10m after 10:15am
SELECT activity, month, day, year, hour, minute, license_plate FROM bakery_security_logs WHERE
(year = 2023 AND month = 7 AND day = 28 AND hour = 10);

-- 5P2BI95 was seen leaving at 10:16a, 94KL13X at 10:18, 6P58WS2 10:18a, 4328GD8 at 10:19a, G412CB7 at 10:20a, L93JTIZ at 10:21a, 322W7JE at 10:23a, and 0NTHK55 at 10:23a.

-- 3. Look into the people who are associated with these license plate numbers
SELECT name, id, passport_number, phone_number, license_plate FROM people WHERE (license_plate = 'G412CB7' OR license_plate = '94KL13X'
OR license_plate = '5P2BI95' OR license_plate = '6P58WS2' OR license_plate = '4328GD8' OR license_plate = 'L93JTIZ' OR license_plate = '322W7JE' OR license_plate = '0NTHK55');

-- Vanessa - 221103:2963008352:(725) 555-4692 , Barry - 243696:7526138472:(301) 555-4174, Sofia - 398010:1695452385:(130) 555-0289, Bruce - 686048:5773159633:(367) 555-5533,
-- Iman - 396669:7049073643:(829) 555-5269, Luca - 467400:8496433585:(389) 555-5198, Diana - 514354:3592750733:(770) 555-1861, Kelsey - 560886:8294398571:(499) 555-9472

-- 4. Look to see which of these people withdrew money from the atm at Leggett Street
SELECT name, atm_transactions.transaction_type, atm_transactions.atm_location, atm_transactions.month, atm_transactions.day, atm_transactions.year FROM people JOIN bank_accounts ON person_id = people.id JOIN atm_transaction
s ON atm_transactions.account_number = bank_accounts.account_number WHERE (atm_location LIKE '%Leggett%' AND atm_transactions.month = 7 AND atm_transactions.day = 28 AND atm_transactions.year = 2023);

-- Of the owners of the cars seen leaving the scene of the crime, the following also made withdrawals from the atm at Leggett Street that day: Bruce, Diana, Luca, Iman

-- 5. Let's see which of these people caught the first plane out of town on July 29, 2023
SELECT name, airports.city, airports.full_name, flights.destination_airport_id, flights.hour, flights.minute FROM people
JOIN passengers ON passengers.passport_number = people.passport_number
JOIN flights on passengers.flight_id = flights.id JOIN airports ON flights.origin_airport_id = airports.id WHERE
(flights.month = 7 AND flights.day = 29 AND flights.year = 2023 AND
(people.name = 'Bruce' OR people.name = 'Diana' OR people.name = 'Luca' OR people.name = 'Iman')) ORDER BY flights.hour DESC;


-- Of the four people seen leaving the scene of the crime who also withdrew money from the atm at Leggett Street, Bruce and Luca caught the first plane out of dodge the next day. They were both headed to
-- airport id 4

-- 6. Determine the destination airport
SELECT city, full_name FROM airports WHERE id = 4;

-- Destination: Laguardia Airport in NYC

-- 7. Lastly, let's figure out who called who (as told by Raymond). The thief called the accomplice. We have the following information for Bruce and Luca from Step 3:
-- Bruce - 686048:5773159633:(367) 555-5533, Luca - 467400:8496433585:(389) 555-5198
SELECT caller, receiver, duration FROM phone_calls WHERE (month = 7 AND day = 28 AND year = 2023 AND (caller = '(367) 555-5533' OR caller = '(389) 555-5198')) ORDER BY caller;

-- From the results of this query, we seen that Bruce made 4 calls on July 28, 2023. In a twist of events, none of which were made to Luca. But we have determined that Bruce is the thief.
-- Bruce called the following numbers on this day: (375) 555-8161, (344) 555-9601, (022) 555-4052, (704) 555-5790

-- 8. Let's figure out who Bruce was calling
SELECT name FROM people WHERE (phone_number = '(704) 555-5790' OR phone_number = '(022) 555-4052' OR phone_number = '(344) 555-9601' OR phone_number = '(375) 555-8161');

-- We find that Bruce called Gregory, Carl, Robin, and Deborah

-- 9. Let's see which of them may have purchased the plane ticket for Bruce
SELECT name, atm_transactions.transaction_type, atm_transactions.month, atm_transactions.day, atm_transactions.year, atm_transactions.atm_location, atm_transactions.amount FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE (people.name = 'Gregory' OR people.name = 'Carl' OR people.name = 'Robin' OR people.name = 'Deborah');

-- Robin made deposits to her account from different ATMs on the days before and after the theft. Both deposits were small relative to a standard plane ticket.
