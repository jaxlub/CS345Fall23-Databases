-- Jax Lubkowitz
-- HW3
-- 9/8/23

--3.13) Write SQL DDL corresponding to the schema in Figure 3.17. Make any reason- able assumptions about data types,
-- and be sure to declare primary and foreign keys.

--DROP table participated CASCADE;

-- Build DDL based on 3.17 schema

DROP DATABASE IF EXISTS jalubk20_insurance;
CREATE DATABASE jalubk20_insurance;
\c jalubk20_insurance



DROP TABLE IF EXISTS person;
CREATE TABLE person(
    driver_id char(6) NOT NULL,
    name char(30),
    PRIMARY KEY(driver_id)
);

DROP TABLE IF EXISTS car;
CREATE TABLE car(
    license_plate char(8) NOT NULL,
    model char(10),
    year integer,
    PRIMARY KEY(license_plate)
);

DROP TABLE IF EXISTS accident;
CREATE TABLE accident(
    report_number char(6) NOT NULL,
    year integer,
    location char(10),
    PRIMARY KEY(report_number)
);

DROP TABLE IF EXISTS owns;
CREATE TABLE owns(
    driver_id char(6) NOT NULL,
    license_plate char(8) NOT NULL,
    PRIMARY KEY(driver_id, license_plate),
    FOREIGN KEY (driver_id) references person(driver_id),
    FOREIGN KEY (license_plate) references car(license_plate)
);

DROP TABLE IF EXISTS participated;
CREATE TABLE participated(
    report_number char(6) NOT NULL,
    license_plate char(8) NOT NULL,
    driver_id char(6),
    damage_amount numeric,
    PRIMARY KEY(report_number, license_plate),
    FOREIGN KEY (driver_id) references person(driver_id),
    FOREIGN KEY (report_number) references accident(report_number),
    FOREIGN KEY (license_plate) references car(license_plate)
);


--3.14)Consider the insurance database of Figure 3.17, where the primary keys are underlined. Construct the following
-- SQL queries for this relational database.

--a. Find the number of accidents involving a car belonging to a person named “John Smith”.

--In this query, the number of participated accidents with licence plates belonging to John Smith's ID.
SELECT
    count(*)
FROM
    participated, accident
WHERE
    participated.license_plate in (SELECT
                                       owns.license_plate
                                   FROM
                                       owns
                                   WHERE
                                       owns.driver_id in (SELECT
                                                              driver_id
                                                          FROM
                                                              person
                                                          WHERE
                                                              name = 'John Smith')
                                   ) and
    participated.report_number = accident.report_number;

--testing
INSERT INTO person values ('123456', 'John Smith');
INSERT into person values ('654321', 'Bob');
INSERT INTO car values('ABCDE', 'Suburu', 2003);
INSERT INTO car values('BOBLO', 'Tesla', 2020);
INSERT INTO accident values ('CR1234', 2005, 'China');
INSERT INTO owns values ('123456', 'ABCDE');
INSERT INTO owns values ('654321', 'BOBLO');
INSERT INTO participated values ('CR1234','ABCDE','123456',3000);
INSERT INTO participated values ('CR1234','BOBLO','654321',5000);

INSERT INTO accident values ('AR2197',2023,'Turkey');
INSERT INTO car values('AABB2000', 'PORSCHE', 2023);
INSERT INTO owns values ('123456', 'AABB2000');
INSERT INTO participated values ('AR2197','AABB2000','123456',1000);




--b. Update the damage amount for the car with license plate “AABB2000” in the accident with report
-- number “AR2197” to $3000.

-- This query changes the participated damage amount for a particular plate and report number. 
UPDATE participated set damage_amount = 3000 where
                                                 participated.report_number = 'AR2197' and
                                                 participated.license_plate = 'AABB2000';