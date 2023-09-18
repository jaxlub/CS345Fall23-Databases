-- Homework 4: University Query
-- Jax Lubkowitz and Jack Cowan
-- 9/20/23

--Create table for grade scale and fill it
DROP Table if exists grade_scale;
DROP TABLE IF EXISTS grade_scale;
CREATE TABLE grade_scale
(
    grade     varchar(2)    NOT NULL,
    gpa_value numeric(3, 2) NOT NULL,
    PRIMARY KEY (grade, gpa_value)
);

INSERT INTO grade_scale
values ('A+', 4.0),
       ('A ', 3.75),
       ('A-', 3.5),
       ('B+', 3.25),
       ('B ', 3.0),
       ('B-', 2.75),
       ('C+', 2.5),
       ('C ', 2.25),
       ('C-', 2.0);


--1. Write a query that calculates the GPA of Knutson
SELECT round((sum(grade_scale.gpa_value * grades.creds) / sum(grades.creds)), 3) as GPA
FROM (SELECT min(student.id)     as id,
             takes.grade,
             sum(course.credits) as creds
      FROM student,
           takes,
           course
      WHERE student.name = 'Knutson'
        and student.id = takes.id
        and takes.course_id = course.course_id
      GROUP BY takes.grade) as grades,
     grade_scale,
     student
WHERE grade_scale.grade = grades.grade
  and grades.id = student.id;

--2. write a query that creates a report of GPAs for all students.
-- The output table is student name, student id, major and GPA.
-- Order the table by major then GPA in the major
select name,
       student.id,
       dept_name as major,
       (SELECT round((sum(grade_scale.gpa_value * grades.creds) / sum(grades.creds)), 3) as GPA
        FROM (SELECT takes.grade,
                     sum(course.credits) as creds
              FROM takes,
                   course,
                   student as stu
              WHERE student.id = stu.id
                and student.id = takes.id
                and takes.course_id = course.course_id
              GROUP BY takes.grade) as grades,
             grade_scale,
             student
        WHERE grade_scale.grade = grades.grade) as gpa
from student
order by major, gpa desc;