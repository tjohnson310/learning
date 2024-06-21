SELECT name from people JOIN stars ON stars.person_id = people.id JOIN movies ON stars.movie_id = movies.id WHERE stars.person_id !=
(SELECT people.id FROM people WHERE people.name = 'Kevin Bacon' AND people.birth = 1958) AND stars.movie_id IN
(SELECT movies.id FROM movies JOIN stars ON stars.movie_id = movies.id JOIN people ON stars.person_id = people.id WHERE people.name =
'Kevin Bacon' and people.birth = 1958);
