--create database ecommerce;
--use ecommerce;

create table Customer(
cust_id int primary key,
phone_no int,
email varchar(50),
full_name varchar(100)
);

create table Product(
prod_id int PRIMARY KEY,
prod_name varchar(100),
price decimal(13,3)
);

create table Review(
review_id int PRIMARY KEY,
cust_id int REFERENCES Customer(cust_id),
prod_id int REFERENCES Product(prod_id),
rating int,
comment varchar(500)
);

  