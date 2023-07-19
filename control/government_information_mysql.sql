/*
 * database  government_information
 */ 
create database government_information DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
use government_information;

/*
 * air pm2.5
 */ 
create table air_pm25(
no int not null PRIMARY key AUTO_INCREMENT , 
r_year year null,
r_month varchar(30) null,
r_day varchar(10) null,
r_time time null,
publish_time datetime null,
county varchar(30) null,
site_name varchar(30) null,    
pm25 varchar(30) null  
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


/*
 * air aqi
 */ 
create table air_aqi(
no int not null PRIMARY key AUTO_INCREMENT , 
publish_time datetime null,
r_year year null,
r_month varchar(30) null,
r_day date null,
r_time time null,
site_name varchar(30) null,    
county varchar(30) null,
site_id varchar(30) null,
aqi varchar(30) null,
pollutant varchar(30) null,
now_status varchar(30) null, 
so2 varchar(30) null,
co varchar(30) null,
o3 varchar(30) null,
o3_8hr varchar(30) null,
pm10 varchar(30) null,
pm25 varchar(30) null,  
no2 varchar(30) null,
nox varchar(30) null,
wind_speed varchar(30) null,
wind_direc varchar(30) null,
co_8hr varchar(30) null,
pm25_avg varchar(30) null,
pm10_avg varchar(30) null,
so2_avg varchar(30) null,
longitude varchar(50) null,
latitude varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

