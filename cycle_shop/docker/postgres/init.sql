CREATE USER admin WITH password 'postgres12345';
CREATE DATABASE prod_db;
GRANT ALL PRIVILEGES on DATABASE prod_db TO admin;
