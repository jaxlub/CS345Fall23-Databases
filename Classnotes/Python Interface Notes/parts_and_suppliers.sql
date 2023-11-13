drop database if exists cslabtes_parts_and_suppliers;
create database cslabtes_parts_and_suppliers;
\c cslabtes_parts_and_suppliers
drop table if exists shipments;
drop table if exists supplier;
drop table if exists parts;

create table supplier ( 
   sno int not null,
   sname text not null,
   status int not null,
   city text not null,
   primary key(sno));

create table parts (
   pno int not null,
   pname text not null,
   color text not null,
   weight double precision not null,
   location text,
   primary key (pno));

create table shipments (
	pno int not null,
	sno int not null,
	quantity int not null,
	primary key (pno,sno),
	foreign key (pno) references parts(pno),
	foreign key (sno) references supplier(sno));

\copy supplier from 'suppliers.csv' with (format csv);
\copy parts from 'parts.csv' with (format csv);
\copy shipments from 'shipments.csv' with (format csv);

-- clean up 
update parts set pname=trim(pname),color=trim(color),location=trim(location);
update supplier set sname=trim(sname),city=trim(city);