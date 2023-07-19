#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20230328
# Update   : 20230601
# Function : realtime monitor government information air aqi

import pymysql , json , logging , time , requests
from control.dao import *

################################################################################################################################################
#
# realtime_airplane
#
################################################################################################################################################
class realtime_airplane:
    
    ### log 
    log_format = "%(asctime)s %(message)s"
    logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")

    def __init__(self):
        self.main()
    
    def main(self):
        pass

################################################################################################################################################
#
# air_pm25
#
################################################################################################################################################
class air_pm25:
    ### log 
    log_format = "%(asctime)s %(message)s"
    logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")

    #########
    # init
    #########
    def __init__(self):
        self.main()

    #########
    # main
    #########
    def main(self):
        url      = g_air['pm25_url']
        data     = requests.get(url)
        data_val = data.json()

        try:
            for val in data_val['records']:
                print( val['datacreationdate'] + ' , ' + val['county'] + ' , ' + val['site'] + ' , pm2.5 : ' + val['pm25'] + ' ' + val['itemunit'])

                #################
                # tinfar mysql
                #################
                r_year  = time.strftime("%Y" , time.localtime())
                r_month = time.strftime("%m" , time.localtime())
                r_day   = time.strftime("%d" , time.localtime()) 
                b_month = time.strftime("%Y_%m" , time.localtime())
                r_time  = time.strftime("%H:%M:%S" , time.localtime())


                conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
                curr = conn.cursor()

                try:
                    sql = "create table {0}_pm25(no int not null PRIMARY key AUTO_INCREMENT, r_year year null , r_month varchar(30) null , r_day varchar(10) null , r_time time null , publish_time datetime null , county varchar(30) null , site_name varchar(30) null , pm25 varchar(30) null )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci".format(b_month)
                    curr.execute(sql)

                except Exception as e:
                    sql = "insert into {8}_pm25(publish_time , r_year  , r_month , r_day , r_time , site_name , county , pm25) values('{0}' , '{1}' , '{2}' , '{3}' , '{4}' , '{5}' , '{6}' , '{7}')".format(val['datacreationdate'] , r_year , r_month , r_day , r_time , val['site'] , val['county'] , val['pm25'] , b_month)
                    curr.execute(sql)
                    
                finally:
                    conn.commit()
                    conn.close()
            
        except Exception as e:
            logging.info('< Error > air pm2.5 : ' + str(e))
        finally:
            pass

################################################################################################################################################
#
# air_aqi
#
################################################################################################################################################
class air_aqi:
    
    ### log 
    log_format = "%(asctime)s %(message)s"
    logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")

    #########
    # init
    #########
    def __init__(self):
        self.main()

    #########
    # main
    #########
    def main(self):
        url      = g_air['aqi_url']
        data     = requests.get(url)
        data_val = data.json()

        try:
            for val in data_val['records']:
                print(val['publishtime'] + ' : ' + val['county'] + ' ( ' + val['sitename'] + ' ) , AQI : ' + val['aqi'] + ' , pm2.5 : ' + val['pm2.5'] + ' ug/m3' + ' , pm1.0 : ' + val['pm10'] + ' ug/m3')
                
                ################
                # line notify
                ################
                if str(val['sitename']) == '新北(樹林)':
                    res = val['sitename'] + ' 空氣品質 ' + val['status']
                    #self.line_notify_ming(res)
                
                if str(val['sitename']) == '二林':
                    res = val['sitename'] + ' 空氣品質 ' + val['status']
                    #self.line_notify_ming(res)
                
                if str(val['sitename']) == '士林':
                    res = val['sitename'] + ' 空氣品質 ' + val['status']
                    #self.line_notify_ming(res)

                #################
                # tinfar mysql
                #################
                r_year  = time.strftime("%Y" , time.localtime())
                r_month = time.strftime("%m" , time.localtime())
                r_day   = time.strftime("%Y-%m-%d" , time.localtime()) 
                r_time  = time.strftime("%H:%M:%S" , time.localtime())
                b_month   = time.strftime("%Y_%m" , time.localtime()) 

                conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
                curr = conn.cursor()

                try:
                    sql = "create table {0}_aqi(no int not null PRIMARY key AUTO_INCREMENT , publish_time datetime null,r_year year null,r_month varchar(30) null,r_day date null,r_time time null,site_name varchar(30) null,county varchar(30) null,site_id varchar(30) null,aqi varchar(30) null,pollutant varchar(30) null,now_status varchar(30) null, so2 varchar(30) null,co varchar(30) null,o3 varchar(30) null,o3_8hr varchar(30) null,pm10 varchar(30) null,pm25 varchar(30) null,no2 varchar(30) null,nox varchar(30) null,wind_speed varchar(30) null,wind_direc varchar(30) null,co_8hr varchar(30) null,pm25_avg varchar(30) null,pm10_avg varchar(30) null,so2_avg varchar(30) null,longitude varchar(50) null,latitude varchar(50) null)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;".format(b_month)
                    curr.execute(sql)

                except Exception as e:
                    if len(val["status"]) == 0:
                        val["status"] = '斷線'

                    if len(val['pm2.5']) == 0:
                        val['pm2.5'] = 0
                    
                    if len(val["pm10"]) == 0:
                        val["pm10"] = 0

                    sql = "insert into {27}_aqi(publish_time , site_name , county , site_id , aqi , pollutant , now_status , so2 , co , o3 , o3_8hr , pm10 , pm25 , no2 , nox , wind_speed , wind_direc , co_8hr , pm25_avg , pm10_avg , so2_avg , longitude , latitude , r_year , r_month , r_day , r_time) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}','{23}','{24}','{25}','{26}')".format(val['publishtime'],val['sitename'],val['county'],val['siteid'],val['aqi'],val['pollutant'],val['status'],val['so2'],val['co'],val['o3'],val['o3_8hr'],val['pm10'] , val['pm2.5'] , val['no2'] , val['nox'] , val['wind_speed'] , val['wind_direc'] , val['co_8hr'] , val['pm2.5_avg'] , val['pm10_avg'] , val['so2_avg'] , val['longitude'] , val['latitude'] , r_year , r_month , r_day , r_time , b_month)
                    curr.execute(sql)
                    #logging.info('< Error > air aqi insert DB : ' + str(e))

                finally:
                    conn.commit()
                    conn.close()

        except Exception as e:
            logging.info('< Error > air_aqi : ' + str(e))
        finally:
            pass


    #####################
    # line_notify_ming
    #####################
    def line_notify_ming(self , msg):
        try:
            ### varuables
            self.msg = msg

            ### record time
            r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            r_year  = time.strftime("%Y" , time.localtime())
            r_month = time.strftime("%m" , time.localtime())
            r_day   = time.strftime("%d" , time.localtime()) 

            ##########################
            # line notify - 阿明一家
            ##########################
            
            token2  = 'ESwsm3lrwhMsvDKP906sn6vAAsTeR7UNSYAU9drcaxI'
            headers = {'Authorization':'Bearer ' + token2}
            message = self.msg
            data    = {'message':message}

            try:
                res = requests.post("https://notify-api.line.me/api/notify" , headers=headers , data=data)
                if res:
                    logging.info('< line notify success > ' + message)
                else:
                    logging.info('< line notify Fail > ' + message)
            except Exception as e:
                logging.info('< Error > line notify : ' + str(e))

        except Exception as e:
            logging.info('< Error > line_notify_ming : ' + str(e))
        finally:
            pass

################################################################################################################################################
#
# start
#
################################################################################################################################################
if __name__ == '__main__':
    
    ### monitor air PM2.5
    m_air_pm25 = air_pm25()
    
    ### monitor air AQI
    m_air_aqi = air_aqi()



