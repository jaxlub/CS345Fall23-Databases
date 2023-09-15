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
     teaches.id != '14365'