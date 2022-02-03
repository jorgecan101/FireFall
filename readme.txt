DATA: 
http://federalgovernmentzipcodes.us/download.html

-- kaggle training data
 https://www.kaggle.com/elikplim/forest-fires-data-set   


// brew install git

// generate SSH keys on local (do it once)

//  add keys to github

//Access Posgres server
psql -h #### -U hackutd -d hackutd
password = #####



//Create sql table

create table forestfires_train (
x integer ,
y integer ,
month text ,
day text ,
ffmc numeric ,
dmc numeric ,
dc numeric ,
isi numeric ,
temp numeric ,
rh numeric ,
wind numeric ,
rain numeric ,
area numeric
);

create table simulated (
zipcode text ,
ffmc numeric ,
dmc numeric ,
dc numeric ,
isi numeric ,
temp numeric ,
rh numeric ,
wind numeric ,
rain numeric ,
area numeric ,
created_ts timestamp default current_timestamp
);


alter table simulated drop column animal_type_popular;
alter table simulated drop column nomral_animal_percentage;
alter table simulated drop column nomral_camper_percentage;


alter table simulated drop column type_popular;

alter table simulated add animal_type text;
alter table simulated add animal_percentage numeric;
alter table simulated add camper_percentage numeric;



drop table zipcode_city;

create table zipcode_city (
RecordNumber int primary key,
Zipcode text,
ZipCodeType text,
City text,
State text,
LocationType text,
Lat numeric,
Long numeric,
Xaxis numeric,
Yaxis numeric,
Zaxis numeric,
WorldRegion text,
Country text,
LocationText text,
Location text,
Decommisioned text,
TaxReturnsFiled text,
EstimatedPopulation text,
TotalWages text,
Notes text);


//load data from csv into table
\COPY zipcode_city FROM 'free-zipcode-database.csv' DELIMITER ',' CSV HEADER;

//Add column names riskscore to already existing table
alter table zipcode_city add risk_score numeric;


create table zipcode (
Zipcode text primary key,
ZipCodeType text,
City text,
State text,
LocationType text,
Lat numeric,
Long numeric,
Location text,
Decommisioned text,
TaxReturnsFiled text,
EstimatedPopulation text,
TotalWages text);

alter table zipcode add animal_type_popular text;
alter table zipcode add nomral_animal_percentage numeric;
alter table zipcode add nomral_camper_percentage numeric;

UPDATE zipcode
SET animal_type_popular = (
SELECT CASE WHEN zipcode.animal_type_popular is NOT DISTINCT FROM zipcode.animal_type_popular then animal end
FROM animal_type
ORDER BY random()
LIMIT 1
);

update zipcode
set nomral_animal_percentage =
(
SELECT CASE WHEN zipcode.nomral_animal_percentage is NOT DISTINCT FROM zipcode.nomral_animal_percentage then rnd end
from (select floor(random() * 100 + 1)::int as rnd) x
)
,
nomral_camper_percentage =
(
SELECT CASE WHEN zipcode.nomral_camper_percentage is NOT DISTINCT FROM zipcode.nomral_camper_percentage then rnd end
from (select floor(random() * 100 + 1)::int as rnd) x
)
;

select id, animal_type_popular, nomral_animal_percentage, nomral_camper_percentage
from zipcode order by zipcode;


\COPY zipcode FROM '/Users/akadado/Downloads/free-zipcode-database-Primary.csv' DELIMITER ',' CSV HEADER;

alter table zipcode add risk_score numeric;

//Creates id of type BigSerial
alter table zipcode add id BIGSERIAL;



//table for animal types
create table animal_type (id bigserial, animal text);
create unique index animal_type_idx1 on animal_type(animal);

insert into animal_type(animal) values ('bees');
insert into animal_type(animal) values ('butterflies');
insert into animal_type(animal) values ('fox');
insert into animal_type(animal) values ('wolf');
insert into animal_type(animal) values ('coyote');
insert into animal_type(animal) values ('hummingbird');
insert into animal_type(animal) values ('praire_dog');

//Install Grafana

brew update
brew install grafana

To have launchd start grafana now and restart at login:
  brew services start grafana

//Defauly Grafana local site
http://localhost:3000/login


query to user for monitorin:
SELECT zipcode, city, state, risk_score from zipcode order by risk_score desc


//Set up python
pip install anaconda
pip install psycopg2
or
conda install psycopg2


//sample python program with postgres 
import psycopg2
pgcon = psycopg2.connect(user="###",password="###",host="###",port="5432",database="hackutd")
pgcur = pgcon.cursor()

v_sql = "select * from forestfires_train"
pgcur.execute(v_sql)

fire = pgcur.fetchall()

########################################################################
#//sample python program with postgres using pandas dataframes
import psycopg2
import pandas as pd

def fnc_update_zipcode_score(p_con,p_cur,p_zipcode,p_score):
   v_sql = "update zipcode set risk_score = {p_score} where zipcode = '{p_zipcode}'".format(p_score=p_score,p_zipcode=p_zipcode)
   p_cur.execute(v_sql)
   p_con.commit()

def fnc_gen_data():
   p_ffmc=89.2
   p_dmc=44.6
   p_dc=77.5
   p_isi=7.1
   p_temp=8.3
   p_rh=78
   p_wind=0.9
   p_rain=0.2
   p_area=0
   return p_ffmc, p_dmc, p_dc, p_isi, p_temp, p_rh, p_wind,p_rain,p_area

def fnc_risk_score(p_ffmc, p_dmc, p_dc, p_isi, p_temp, p_rh, p_wind, p_rain, p_area):
   return 5

# make a function that generates simulated data 
def fnc_process_data():
   # data is somehow generated for a certain zipcode
   (p_ffmc, p_dmc, p_dc, p_isi, p_temp, p_rh, p_wind,p_rain,p_area) = fnc_gen_data()
   v_zipcode = "00631"
   # here it needs to be scored
   v_score = fnc_risk_score(p_ffmc, p_dmc, p_dc, p_isi, p_temp, p_rh, p_wind, p_rain, p_area)
   # update the database with score
   fnc_update_zipcode_score(pgcon,pgcur,v_zipcode,v_score)

if __name__ == '__main__':
   pgcon = psycopg2.connect(user="hackutd",password="hackutd2019",host="69.164.204.53",port="5432",database="hackutd")
   pgcur = pgcon.cursor()

   v_sql = "select * from forestfires_train"
   fire = pd.read_sql(v_sql, pgcon)
   fnc_process_data()



---------------------------------------------------------

Install webserver

Docroot is: /usr/local/var/www

The default port has been set in /usr/local/etc/nginx/nginx.conf to 8080 so that
nginx can run without sudo.

nginx will load all files in /usr/local/etc/nginx/servers/.

To have launchd start nginx now and restart at login:
  brew services start nginx
Or, if you don't want/need a background service you can just run:
  nginx
==> Summary
🍺  /usr/local/Cellar/nginx/1.17.3_1: 25 files, 2MB
==> Caveats
==> nginx
Docroot is: /usr/local/var/www

The default port has been set in /usr/local/etc/nginx/nginx.conf to 8080 so that
nginx can run without sudo.

nginx will load all files in /usr/local/etc/nginx/servers/.

To have launchd start nginx now and restart at login:
  brew services start nginx
Or, if you don't want/need a background service you can just run:
  nginx



