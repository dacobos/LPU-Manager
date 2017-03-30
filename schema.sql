drop table if exists interfaces;
drop table if exists devices;
drop table if exists category;
drop table if exists utilization;

PRAGMA foreign_keys = ON;

create table interfaces (
  device text not null,
  category text not null,
  foc integer,
  current integer,
  lpu integer,
  capexLPU money,
  foreign key (device) references devices(device),
  foreign key (category) references category(category)
);

create table devices (
  device text not null primary key,
  ipAddress text not null
);

create table category (
  category text not null primary key,
  capexCat money not null
);

create table utilization (
  device text not null,
  category text not null,
  interface text not null,
  peakUtilization integer not null,
  kpi boolean not null,
  foreign key (device) references devices(device),
  foreign key (category) references category(category)

);
