SELECT title FROM movies JOIN stars ON stars.movie_id = movies.id JOIN people ON stars.person_id = people.id WHERE stars.person_id =
(SELECT id FROM people WHERE name = 'Bradley Cooper') AND stars.movie_id IN
(SELECT movies.id from movies JOIN stars ON stars.movie_id = movies.id JOIN people ON stars.person_id = people.id WHERE people.name = 'Jennifer Lawrence');
