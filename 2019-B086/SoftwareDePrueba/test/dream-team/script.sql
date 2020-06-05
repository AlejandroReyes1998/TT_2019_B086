CREATE USER 'dt_admin'@'localhost' IDENTIFIED BY 'dt2016';
-- drop database if exists dreamteam_db;
create database dreamteam_db;
GRANT ALL PRIVILEGES ON dreamteam_db . * TO 'dt_admin'@'localhost';


