create database sakurai;

create table artist
  (artist_id smallint auto_increment not null primary key,
  artist_name varchar(100));

insert into artist (artist_name) values('Mr.Children');

create table title
  (title_id smallint auto_increment not null primary key,
  title varchar(100),
  artist_id smallint);

create table lyric
 (title_id smallint,
  phrase_id int auto_increment not null primary key,
  phrase varchar(1000),
  score float,
  sentiment tinyint);
