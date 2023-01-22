CREATE TABLE students (
    uid varchar(255) PRIMARY KEY,
    name varchar(255) NOT NULL,
    degree varchar(255),
    major varchar(200),
    minor varchar(200),
    year_level int,
    email varchar(255)
);
CREATE TABLE advisors (
    uid varchar(255) PRIMARY KEY,
    name varchar(255) NOT NULL,
    degree varchar(255),
    major varchar(200),
    minor varchar(200),
    year_level int,
    calendly_link varchar(500),
    bio varchar(1200),
    email varchar(255)
);