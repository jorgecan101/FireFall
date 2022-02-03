import psycopg2
import pandas as pd
import time
from random import seed
from random import random
from random import randint
from arcgis.gis import GIS

#/usr/local/Cellar/grafana/6.4.4/share/grafana/public/dashboards/scripted.js
#this function will generate the data
def gen_data(p_con, p_cur):

    #seed(1)

    #write generate each one of these variables, with certain constraints

#---------------------------------------------------
    #range [18.7 - 96.2] Fine Fuel Moisture Code
    #p_ffmc = 89.2

    p_ffmc = random()
    p_ffmc = round(18.7 + (p_ffmc * (96.2 - 18.7)), 2)

#---------------------------------------------------

    #range [1.1 - 291] Duff Moisture Code
    #p_dmc = 44.6

    p_dmc = random()
    p_dmc = round(1.1 + (p_dmc * (291 - 1.1)), 2)

#---------------------------------------------------

    #range [7.9 - 861] Drought Code
    #p_dc = 77.5
    p_dc = random()
    p_dc = round(7.9 + (p_dc * (861 - 7.9)), 2)

#---------------------------------------------------

    #range [0 - 56.1] Initial Spread Index
    #p_isi = 7.1
    p_isi = random()
    p_isi = round(0 + (p_isi * (56.1 - 0)), 2)

#---------------------------------------------------

    #range [2.2 - 33.3]
    #p_temp = 8.3
    p_temp = random()
    p_temp = round(2.2 + (p_temp * (33.3 - 2.2)), 2)

#---------------------------------------------------

    #range [15 - 100]
    #p_rh = 78
    p_rh = randint(15, 100)

#---------------------------------------------------

    #range [0.4 - 9.4]
    #p_wind = 0.9
    p_wind = random()
    p_wind = round(0.4 + (p_wind * (9.4 - 0.4)), 2)

#---------------------------------------------------

    #range [0 - 6.4]
    #p_rain = 0.2
    p_rain = random()
    p_rain = round(0 + (p_rain * (6.4 - 0)), 2)

#---------------------------------------------------

    #range [0 - 1.09]
    #p_area = 0
    p_area = random()
    p_area = round(0 + (p_area * (1.09 - 0)), 2)

#----------------------------------------------------

    p_zipcode_id = randint(1, 42522)

    v_sql = "select zipcode from zipcode where id = {p_zipcode_id}".format(p_zipcode_id=p_zipcode_id)
    p_cur.execute(v_sql)

    #Gets the element of the array, fetone gets the first row of the table
    p_zipcode = (p_cur.fetchone())[0]


    p_animal_id = randint(1,7)
    v_sql = "select animal from animal_type where id = {p_animal_id}".format(p_animal_id=p_animal_id)
    p_cur.execute(v_sql)

    p_animaltype = (p_cur.fetchone())[0]

    p_current_animal_percentage = randint(0, 100)
    p_current_camper_percentage = randint(0, 100)


    return  p_zipcode, p_ffmc, p_dmc, p_dc, p_isi, p_temp, p_rh, p_wind, p_rain, p_area, p_animaltype, p_current_animal_percentage, p_current_camper_percentage

def insert_gen_data(p_con, p_cur, p_zipcode, p_ffmc, p_dmc, p_dc, p_isi, p_temp, p_rh, p_wind, p_rain, p_area, p_animaltype, p_current_animal_percentage, p_current_camper_percentage):


    v_sql = "insert into simulated(zipcode, ffmc, dmc, dc, isi, temp, rh, wind, rain, area, animal_type, animal_percentage, camper_percentage)"
    v_sql = v_sql + " values ('{p_zipcode}', {p_ffmc}, {p_dmc}, {p_dc}, {p_isi}, {p_temp}, {p_rh}, {p_wind}, {p_rain}, {p_area}, '{p_animaltype}', {p_current_animal_percentage}, {p_current_camper_percentage})"
    v_sql = v_sql.format(p_zipcode=p_zipcode,p_ffmc=p_ffmc,p_dmc=p_dmc, p_dc=p_dc, p_isi=p_isi, p_temp=p_temp, p_rh=p_rh, p_wind=p_wind, p_rain=p_rain, p_area=p_area, p_animaltype=p_animaltype, p_current_animal_percentage=p_current_animal_percentage, p_current_camper_percentage=p_current_camper_percentage)
    p_cur.execute(v_sql)
    p_con.commit()


def process_data(p_con, p_cur):

    # data is somehow generated for a certain zipcode
    (p_zipcode, p_ffmc, p_dmc, p_dc, p_isi, p_temp, p_rh, p_wind,p_rain,p_area, p_animaltype, p_current_animal_percentage, p_current_camper_percentage) = gen_data(p_con, p_cur)


    insert_gen_data(p_con, p_cur, p_zipcode, p_ffmc, p_dmc, p_dc, p_isi, p_temp, p_rh, p_wind, p_rain, p_area, p_animaltype, p_current_animal_percentage, p_current_camper_percentage)

    # here it needs to be scored
    v_score = risk_score(p_con, p_cur, p_zipcode, p_ffmc, p_dmc, p_dc, p_isi, p_temp, p_rh, p_wind, p_rain, p_area, p_animaltype, p_current_animal_percentage, p_current_camper_percentage)

    # update the database with score
    update_zipcode_score(pgcon, pgcur, p_zipcode, v_score)

def reset_database(p_con, p_cur):
    v_sql = "update zipcode set risk_score = 0"
    p_cur.execute(v_sql)
    p_con.commit()

    v_sql = "delete from simulated"
    p_cur.execute(v_sql)
    p_con.commit()


def risk_score(p_con, p_cur, p_zipcode, p_ffmc, p_dmc, p_dc, p_isi, p_temp, p_rh, p_wind, p_rain, p_area, p_animaltype, p_current_animal_percentage, p_current_camper_percentage):
    score = 0
    v_sql = "select normal_animal_percentage, normal_camper_percentage from zipcode where zipcode = '{p_zipcode}'".format(p_zipcode = p_zipcode)
    p_cur.execute(v_sql)
    (p_normal_animal_percentage,p_normal_camper_percentage) = p_cur.fetchone()
    #print("from risk score",p_zipcode,p_normal_animal_percentage,normal_camper_percentage)

    if p_current_animal_percentage < p_normal_animal_percentage:
        score = score + randint(5,10)
    if p_current_camper_percentage > p_normal_camper_percentage:
        score = score + randint(1,3)

    # score = randint(1, 10)
    if score > 10:
        score = 10
    return score



def update_zipcode_score(p_con, p_cur, p_zipcode, p_score):
    v_sql = "update zipcode set risk_score = {p_score} where zipcode = '{p_zipcode}'".format(p_score=p_score,p_zipcode=p_zipcode)
    p_cur.execute(v_sql)
    p_con.commit()

#main function
if __name__ == '__main__':

    #connect to SQL server
    pgcon = psycopg2.connect(user="hackutd",password="hackutd2019",host="69.164.204.53",port="5432",database="hackutd")

    #create cursor
    pgcur = pgcon.cursor()

    reset_database(pgcon, pgcur)

    #store table forestfires_train from forestfire
    v_sql = "select * from forestfires_train"
    fire = pd.read_sql(v_sql, pgcon)

    while (True):
        time.sleep(5)
        process_data(pgcon, pgcur)
