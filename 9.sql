SELECT name FROM people JOIN stars ON person_id = people.id JOIN movies ON movie_id = movies.id WHERE year = 2004 GROUP BY name ORDER BY birth;
