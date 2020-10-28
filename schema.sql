create table Artist (
id  integer primary key autoincrement,
name  varchar(64) not null,
hometown varchar(64) not null
);

create table Venue (
id integer primary key autoincrement,
name varchar(64) not null,
location varchar(64) not null
);

create table Event (
id integer primary key autoincrement,
name varchar(64) not null,
date varcher(64) not null,
venueID integer not null,
    foreign key (venueID) references Venue(id)
);

create table artistToEvent(
id integer primary key autoincrement,
artistID integer not null,
eventID integer not null,
    foreign key (eventID) references Event(id),
    foreign key (artistID) references Artist(id)
);

