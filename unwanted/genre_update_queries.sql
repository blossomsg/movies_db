
-- SELECT genre FROM movies GROUP BY genre ORDER BY genre
SELECT genre, COUNT(*) FROM movies GROUP BY genre ORDER BY COUNT(*)
-- SELECT genre FROM movies WHERE genre ~'(com)' ORDER BY genre 
-- SELECT genre, genre_copy FROM movies ORDER BY genre
-- SELECT (genre) FROM movies WHERE genre ~'(com)' ORDER BY genre 
-- SELECT REGEX_REPLACE(SELECT genre FROM movies WHERE genre ~'(com)' ORDER BY genre '^com' 'Comedy')
-- UPDATE movies SET genre = INITCAP(genre) WHERE genre ~'(com)'
-- UPDATE movies SET genre = REGEXP_REPLACE(genre, 'Comdy', 'Comedy') WHERE genre ~* 'Comdy'
-- SELECT REGEXP_REPLACE(genre, 'Comdy', 'Comedy') FROM movies WHERE genre ~* 'Comdy';

