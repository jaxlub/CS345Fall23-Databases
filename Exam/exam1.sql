-- Exam 1
-- Jax Lubkowitz

-- Question 1
-- Ed: Good. Could have used a natural join instead of the explicit join, but good
-- for using join syntax.
SELECT
    firstname, lastname, title, releaseyear, director, charactername
FROM
    (actors join actsin on (actors.actorid = actsin.actorid)) join movies on (actsin.movieid = movies.movieid)

ORDER BY lastname, releaseyear;


-- Question 2
-- Ed. Good. Should have used JOIN syntax for clarity and brevity
-- for a better answer. -1

WITH
    counter as (SELECT
                    actsin.actorid, count(actsin.actorid)
                FROM
                    actsin
                GROUP BY
                    actsin.actorid),
    max as (SELECT max(counter.count) as movie_count
            FROM counter)
SELECT
    actors.lastname, counter.actorid, counter.count as movie_count
FROM actors, counter, max
WHERE counter.actorid = actors.actorid and
      max.movie_count = counter.count;


