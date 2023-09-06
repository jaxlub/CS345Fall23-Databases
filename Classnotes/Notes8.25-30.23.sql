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

-- aggreagtion function counts to see how many rows are there
SELECT 
	count(*) 
FROM
	zips;

-- find Canton, Ny row in tables
SELECT * 
FROM
	zips
WHERE
	-- convert to all lower case before checking
	lower(city) = 'canton'
and 
	state = 'NY';

SELECT *
FROM
	zips
WHERE
	zip = '42223';

-- Printing one column of table excluding 'DC'
SELECT DISTINCT
	state
FROM
	zips
WHERE
	state <> 'DC';

-- All zips north of Canton 13617 - 44.592442
SELECT count(*)
FROM
	zips
WHERE
	lat > '44.592442';

-- or in one querry (bug: only if one row with area code)
SELECT 
	count(*)
FROM
	zips
WHERE
	lat > (SELECT 
				lat 
			FROM 
				zips 
			WHERE 
				zip = '13617');


-- Columns are not always directly from tables, they are sometimes computed.
SELECT 1;
SELECT pi()/180 as Answer;

-- convert lat/lon coordinates to radians
SELECT
    zip, state, city, lon*pi()/180 as lon, lat*pi()/180 as lat
FROM
    zips
LIMIT 10;

-- Find the geographic center of lon/lat in lower 48
SELECT
    avg(lon), avg(lat)
FROM
    zips
WHERE
    state NOT IN ('AK','HI','PR','DC', 'VI');
    -- state != 'AK' and state != 'HI' and state != 'PR' and state != 'VI';
