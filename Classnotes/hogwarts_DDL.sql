
-- students table
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    id char(6) NOT NULL,
    first_name varchar,
    last_name varchar NOT NULL,
    preferred varchar,
    PRIMARY KEY (id)
);

-- insert sample values into students table
INSERT INTO students values ('1', 'Harold', 'Potter', 'Harry'),
                            ('2', 'Ronald', 'Weasley', 'Ron');

-- courses table
DROP TABLE IF EXISTS courses;
CREATE TABLE courses(
    cnum varchar NOT NULL,
    title varchar,
    PRIMARY KEY (cnum)
);
-- insert sample values into course tables
INSERT INTO courses values ('1', 'Potions'),
                           ('2', 'Defense against the Dark Arts');

-- enrollment tables
DROP TABLE IF EXISTS enrollment;
CREATE TABLE enrollment(
  id char(6) NOT NULL,
  cnum varchar NOT NULL,
  semester varchar NOT NULL,
  year integer NOT NULL,
  PRIMARY KEY(id,cnum,semester,year),
  FOREIGN KEY (id) REFERENCES students(id),
  FOREIGN KEY (cnum) REFERENCES courses(cnum)
);
-- insert sample values into enrollment tables
INSERT INTO enrollment values ('1','1', 'FALL', 1991),
                              ('2','1', 'FALL', 1991),
                              ('1','2', 'FALL', 1991),
                              ('2','2', 'SPRING', 1991);

-- get list of all class Harry Potter has taken
-- output columns: Course ID, Course Title
SELECT
    *
FROM
    students, enrollment, courses
WHERE
    students.id = '1' and
    students.id = enrollment.id and --join
    enrollment.cnum = courses.cnum;

-- finish next time
;

