DROP TABLE IF EXISTS component  ;

DROP TABLE IF EXISTS file;

DROP TABLE IF EXISTS screen;

DROP TABLE IF EXISTS application;

create table application
   (id			varchar(10)	not null unique,
    name		varchar(200) not null,
    primary key(id));
    
create table file
	(id			varchar(10) not null unique,
	 app_id		varchar(10) not null references application(id) on delete cascade,
	 name       varchar(200) not null,
	 total_comps varchar(1500) not null,
	 xml        varchar(60000) not null,
     primary key(id),
     foreign key (app_id) REFERENCES application(id));
    
create table component
   (id			varchar(10) not null unique,
	file_id	varchar(10) not null references file(id) on delete cascade,
	parent_id	varchar(20)	not null,
    name 		varchar(100) not null,
    android_id          varchar(100),
    src                 varchar(100),
	xmlns_android       varchar(100),
	orientation         varchar(100),
    layout_height		varchar(100),
	layout_width		varchar(100),
	layout_weight       varchar(100),
    layout_gravity      varchar(100),
    gravity             varchar(100),
    layout_margin       varchar(100),
    layout_marginLeft   varchar(100),
    layout_marginTop    varchar(100),
    layout_marginRight  varchar(100),
    layout_marginBottom varchar(100),
    padding     varchar(100),
    paddingLeft         varchar(100),
    paddingTop          varchar(100),
    paddingRight        varchar(100),
    paddingBottom       varchar(100),
    clickable   varchar(100),
    text		varchar(500),
    textColor   varchar(100),
    textSize    varchar(100),
    textStyle   varchar(100),
    textAppearance      varchar(100),
    color		varchar(100),
    background  varchar(100),
    num_occurrences int(10),
    primary key(id),
    foreign key (file_id) REFERENCES file(id));
