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

def fnc_risk_score(p_ffmc, p_dmc, p_dc, p_isi, p_temp, p_rh, p_wind,p_rain,p_area):
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

