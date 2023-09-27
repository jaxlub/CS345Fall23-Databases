SELECT
    course.title
FROM
    course
WHERE
    dept_name = 'Comp. Sci.' and
    credits = 3;
-- Can also be writtin "dept_name ~ 'Comp.*Sci.*' AND"
-- .* mean match 0 or more of any characters

SELECT
    dept_name
FROM department
LIMIT 5 OFFSET 5; -- postgres specific, take the second set of 5


-- Random Sample of 10 from dataset
SELECT
    *
FROM
    takes
ORDER BY
    random() -- postgres specific
LIMIT 10;

SELECT
    student.name, takes.year
FROM
    student, takes, course
WHERE
    student.id = takes.id and
    takes.course_id = course.course_id and
    course.title = 'Calculus'
ORDER BY takes.year, takes.semester;

SELECT
    count(DISTINCT takes.id)
FROM
    course, takes, teaches, instructor
WHERE
    takes.course_id = course.course_id and
    course.course_id = teaches.course_id and
    instructor.id = teaches.id and
    instructor.name = 'Dale' and
    teaches.sec_id = takes.sec_id;

SELECT
    dept_name, count(*) as size
FROM
    instructor
GROUP BY
    dept_name
ORDER BY
    size desc;

-- get avg salary for each department
SELECT
    dept_name, avg(salary)
FROM instructor
group by dept_name;

-- how many instructors per department make over 60K
SELECT
    dept_name, count(*) as count
FROM
    instructor
WHERE
    instructor.salary >= 60000
group by
    dept_name
ORDER BY
    count desc;

-- Which department has max number of instructors
SELECT
    dept_name, count(*) as MaxCount
FROM
    instructor
GROUP BY
    dept_name
HAVING
    count(*) =
    (SELECT
        max(count)
    FROM
        (SELECT
            dept_name, count(*) as count
        FROM
              instructor
        group by
             dept_name
        ORDER BY
            count(*) desc) as counter);


-- Which department has max number of instructors
WITH
    counts as
        (SELECT
            dept_name, count(*) as count
        FROM
            instructor
        group by
             dept_name
        ORDER BY
            count(*) desc)
SELECT
    dept_name, count(*) as MaxCount
FROM
    instructor
GROUP BY
    dept_name
HAVING
    count(*) =
    (SELECT
        max(count)
    FROM
        counts);

-- Set Operations
-- (rel1 union rel2) and must have same structure
-- (rel1 except rel2) = rel1-rel2
-- (rel1 intersect rel2) = rel1 and rel2
-- IN, NOT IN are also technically set operations and return a boolean result

-- What courses has 37809 taken that 77148 has not
    (SELECT
        course_id
    FROM
        takes
    WHERE
        takes.id = '37809')
EXCEPT
    (SELECT
         course_id
     FROM takes
     WHERE
         takes.id = '77148');

-- Instructor 14365 wants to know what other instructor has taught 200
SELECT
     teaches.id
 FROM teaches
 WHERE
     teaches.course_id = '200' and
     teaches.id != '14365';

-- JOIN Syntax
-- get a list of courses that dale teaches

SELECT
    teaches.id, course_id, semester, year
FROM
    teaches, instructor
WHERE
    instructor.name = 'Dale' and
    teaches.id = instructor.id; -- This is the join condition
-- Now using a join
SELECT
    id, course_id, semester, year
FROM
    teaches natural join instructor -- joins on ALL COMMON attribute names
WHERE
    instructor.name = 'Dale';

-- Get all of the student ID's who were taught by Dale
SELECT
    takes.id
FROM
    takes join (instructor natural join teaches) using (course_id, sec_id, semester, year)
WHERE
    instructor.name = 'Dale';

-- Insert two new instructors into instructor relation
INSERT INTO instructor VALUES ('99999', 'Angstadt', 'Comp. Sci.', 100000),
                              ('99998', 'Torrey', 'Comp. Sci.', 100000);

-- Create a table of advisor IDs and a count of how many students they advise
SELECT
    advisor.i_id, count(*) as Advisee_Count
FROM advisor
group by advisor.i_id;

-- How can we find people with no advisees
(SELECT
     instructor.id
 FROM
     instructor
 ) EXCEPT (SELECT
               advisor.i_id
           FROM advisor);
-- or....
SELECT
    id
FROM
    instructor
WHERE
    id not in (SELECT i_id
               FROM
                   advisor);
-- Now union these two together to include those with and without advisees
WITH
    advisor_counts as ((SELECT
                           advisor.i_id, count(*) as Advisee_Count
                       FROM advisor
                       group by advisor.i_id) UNION ((SELECT
                                                          instructor.id, 0
                                                      FROM
                                                          instructor) EXCEPT
                                                                      (SELECT
                                                                           advisor.i_id, 0
                                                                       FROM
                                                                           advisor))
                                                                       ORDER BY
                                                                           Advisee_Count)
SELECT
    instructor.name, instructor.id, advisor_counts.Advisee_Count
FROM instructor join advisor_counts on instructor.id = advisor_counts.i_id; -- join on IDs to pull the names

-- Re-writing but with CORRELATION query
SELECT
    instructor.name, instructor.id, (SELECT
                                         count(s_id)
                                     FROM
                                         advisor
                                     WHERE advisor.i_id = instructor.id)
FROM
    instructor;
-- Similar to nested-for loops to join, for every row in instructor (loop1) we iterate through
-- advisor (loop2) and count up total

-- OUTER JOINS

-- done in jalubk20 DB
/*
CREATE TABLE R1 (
    a int,
    b int,
    c int);
CREATE TABLE R2 (
    a int,
    b int,
    d int);
insert into R1 values (1,2,3),
                      (1,3,2),
                      (4,1,3);

insert into R2 values (1,3,3),
                      (1,3,4),
                      (2,2,3);
SELECT
    *
FROM R1 natural join R2;
*/

-- Build name, id and count of advisees using outer joins
-- instructor ID determines instructors name
CREATE VIEW advisee_counts as(
SELECT
    result.name, instructor.id, result.advisees
FROM
    (SELECT
        name, count(s_id) as advisees
    FROM
        instructor left outer join advisor on (instructor.id = advisor.i_id)
    GROUP BY
        id) as result, instructor
WHERE instructor.name = result.name);

BEGIN;
    DELETE FROM takes where id = '58300' and course_id = '408' and
                            semester = 'Spring' and year = 2004;
    INSERT INTO takes values ('58300', '760', '1', 'Spring', 2004);
COMMIT;

-- Integrity constraints
ALTER TABLE course add check (credits < 5);
--ALTER TABLE course DROP constraint course_credits_check;
ALTER TABLE course add constraint credits_less_then_5 check (credits < 5);
ALTER TABLE course add constraint credits_greater_then_0 check (credits > 0);

-- Write a query that makes sure that no classroom is double booked.
SELECT
    semester, year, building, room_number, time_slot_id
FROM
    section
GROUP BY
    semester, year, building, room_number, time_slot_id
HAVING
    count(*) > 1;


-- Adds a new key called rooms_not_double_booked and index
ALTER TABLE section ADD CONSTRAINT rooms_not_double_booked
    UNIQUE (semester, year, building, room_number, time_slot_id);

/* DATES INFO
CREATE TYPE
    semester as ENUM ('Fall', 'Spring', 'Summer');

CREATE table foos(
    sem semester,
    bday date
)

Select
*
FROM X
Where
bday < '2015-01-03' -- not a string;

Select
*
FROM
X
Where
bday between '2015-01-03' and '2015-03-26'

or
bday + interval '4 months'

SELECT extract(month from bday) from X
 */

-- Authorizations
-- REVOKE CONNECT ON DATABASE exam1 FROM public;
-- GRANT CONNECT ON DATABASE exam1 to public;
REVOKE CONNECT ON DATABASE jalubk20_university FROM PUBLIC;
REVOKE CONNECT ON DATABASE jalubk20_university FROM jwcowa20;
GRANT CONNECT ON DATABASE jalubk20_university to bsuns20;
GRANT SELECT (id, name, dept_name) on instructor to bsuns20;






CREATE INDEX takes_id on takes(id); --create index to get fast access based on student ID

/*
 update instructor set salary = case
when salary <= 100000 then salary * 1.05
else salary * 1.03 end

create domain degree level varchar(10)
    constraint degree level
            test check (value in ('Bachelors', 'Masters', 'Doctorate'));

grant references (dept name) on department to Mariano;
 */