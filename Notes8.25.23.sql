-- This is a comment
-- SQL is case insensitive, most capitalize keywords tho
/* Can block comment like this */
SELECT
	*
FROM
	zips
LIMIT 
	10; 

-- column duplication and elimanation of duplicates
SELECT DISTINCT
	state,zip,zip,zip
FROM
	zips
LIMIT
	10;

