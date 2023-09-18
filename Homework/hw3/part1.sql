-- Jax Lubkowitz
-- HW3
-- 9/8/23

--3.11
-- a) Find every student who has taken a CS class in the database.

--This query pulls distinct student ID's and names using info from student, takes and course relations.
-- Then uses the student ID to see what each student takes, and then using the course ID finds the department
-- and makes sure it is a CS class
SELECT DISTINCT
    student.id, student.name
FROM
    student, takes, course
WHERE
    student.id = takes.id and
    takes.course_id = course.course_id and
    course.dept_name = 'Comp. Sci.'
ORDER BY
    student.name;

--b) Find the ID and name of each student who has not taken any course offered before 2017.

-- This query finds the ID's and names from students where the ID is not in the result of a query of classes taken before 2005.

SELECT DISTINCT
    student.id, student.name
FROM
    student
WHERE
    id NOT IN (SELECT
                    takes.id
                FROM
                    takes
                WHERE
                    takes.year < 2005);


--c) For each department, find the maxi salary of instructors in department.
-- You may assume that every department has at least one instructor.

-- This query selects distinct departments from instructor in addition to selecting the max salary where
-- it correlates to each distinct department.
SELECT DISTINCT
    dept_name,
    (SELECT
        max(salary) as max_salary
     FROM
         instructor as instructor2
    WHERE
        instructor2.dept_name = instructor1.dept_name)
FROM
    instructor as instructor1
ORDER BY
    dept_name;

-- Other solution after reading chapter 3.7
--ELECT dept_name, max(salary) as max_salary
--FROM instructor
--GROUP BY dept_name
--ORDER BY
--    dept_name;

--d) Find the lowest, across all departments, of the per-department maximum salary computed by the
-- preceding query.

-- Starting from the inner-most nested query, this finds the max salary of each department. Which then selects the lowest
-- one and then pulls the corresponding department from the initial list based off which has the matching salary.
SELECT
    instruct1.dept_name, min.min_max
FROM
    instructor as instruct1,
    (SELECT
         min(max_salary) as min_max
    FROM
        (SELECT
             dept_name, max(salary) as max_salary
        FROM
            instructor
        GROUP BY dept_name) as max) as min
WHERE
    min.min_max = instruct1.salary;

--3.12
--a) Create a new course “CS-001”, titled “Weekly Seminar”, with 0 credits.
-- This command inserts into the table course ID = 999, Title = weekly Seminar, Dept = Comp. Sci, Credits = 0

-- Drop Constraint
ALTER TABLE course DROP CONSTRAINT course_credits_check;
-- Re-add constraint allowing for 0 credit classes
ALTER TABLE course ADD CONSTRAINT course_credits_check CHECK (credits >= (0)::numeric);

INSERT INTO course values('999', 'Weekly Seminar', 'Comp. Sci.', 0);
-- ERROR: new row for relation "course" violates check constraint "course_credits_check"
-- Detail: Failing row contains (999, Weekly Seminar, Comp. Sci., 0).

-- b.) Create a section of this course in Fall 2017, with sec id of 1, and with the location of this
-- section not yet specified.
-- inserting in section class with no time or location
INSERT INTO section VALUES ('999', '1', 'Fall', 2017);

-- c.) Enroll every CS student in ^ section.

-- This query inserts into takes all the necesary column and uses hardcoded values for the class info and selects
-- all CS majors from students.

INSERT INTO
    takes(id, course_id, sec_id, semester, year, grade)
SELECT
    student.id, '999', '1', 'Fall', 2017, null
FROM
    student
WHERE
    student.dept_name = 'Comp. Sci.';

-- Test that part C worked
--SELECT
--    *
--FROM
--    takes
--WHERE
--    takes.course_id = '999';

--d) Delete enrollments of above section for student ID 12345
-- This deletes from the relation takes, all cases where student 12345 is in the course 999
DELETE FROM
    takes
WHERE
    takes.id = '12345' and
    takes.course_id = '999';

--e) Delete the CS-001 course. WHat happens if you run this before deleting the sections?
--If you delete from course without also deleting all of the sections, then there is would be an inconsistency in the
-- database where there are sections of a not-real course, However SQL deletes all instances within takes as well as
-- the course course_ID is a foreign key of takes.

DELETE FROM
           course
WHERE course.course_id = '999';


--f) Delete all tuples with "advanced" in the title

-- This query deletes from the takes relation the tuples where the course_id has the same course_id as the classes with
-- advanced in the title.

--testing by adding course, a section and 1 student in it
--INSERT INTO course values ('997','zdk Advanced comp', 'Mech. Eng.', '4' );
--insert into takes values ('98140','997', '1','Fall','2010','B-');
--INSERT into section values ('997','1','Fall','2010','Chandler','804','N');

--DELETE FROM course where course_id = '997';
--DELETE from section where course_id = '997';

DELETE FROM
           takes
WHERE
       takes.course_id = (SELECT
            course.course_id
        FROM
            course
        WHERE
            lower(course.title) like '%advanced%');

--3.24) Find the name and ID of accounting students advised by a physics instructor.
-- This query takes the ids of the physics instructors and sees which ones are advisors and takes there advisees and
-- matches that to their names in student.
SELECT DISTINCT
    student.ID, student.name
FROM
    student
WHERE
    student.dept_name = 'Accounting' and
    student.id in (SELECT DISTINCT
                        s_id
                    FROM
                        advisor
                    WHERE
                        i_id in (SELECT
                                     id
                                 FROM
                                     instructor
                                 WHERE
                                     dept_name = 'Physics'));


--3.25) Find departments who's budget is higher then philosophy and list them in alphabetical order.
-- This query finds the languages budget and then finds departments with higher budgets.
WITH
    lang_budget as (
        SELECT
            department.budget as budget
        FROM
            department
        WHERE dept_name = 'Languages')
SELECT
    dept_name
FROM department, lang_budget
WHERE department.budget >  lang_budget.budget;

--3.26) For all triple-takes, show the course_ID and student_ID, no duplicate rows.

-- This query finds all ids that have taken each course and where there is 3 of that ID then it returns there
-- ID and then matches it to the course ID for output.
SELECT DISTINCT
    takes.id, takes.course_id
FROM
    takes
WHERE
    takes.id in
    (SELECT
        takes.id
    FROM
        takes
    GROUP BY
        takes.id, takes.course_id
    HAVING
        count(*) >= 3) and
    takes.course_id in
    (SELECT
        takes.course_id
    FROM
        takes
    GROUP BY
        takes.id, takes.course_id
    HAVING
        count(*) >= 3)
ORDER BY
    course_id, id;

--3.27) Using the university schema, write an SQL query to find the IDs of those stu- dents who have retaken at least
-- three distinct courses at least once (i.e, the student has taken the course at least two times).

-- This query finds all IDs and Classes that have been retaken (as classes) and then finds the IDs on there that have
-- retaken 3 classes.

WITH classes as (SELECT DISTINCT
        takes.id, takes.course_id
    FROM
        takes
    GROUP BY
        takes.id, takes.course_id
    HAVING
        count(*) >= 2)

SELECT
    classes.id
FROM
    classes
GROUP BY
    classes.id
HAVING count(id) >= 3;
