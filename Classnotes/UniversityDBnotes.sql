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


