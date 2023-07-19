#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20230328
# Update   : 20230328
# Function : realtime monitor government information air aqi

############
# air aqi
############
g_air = {'aqi_url':'https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate desc&format=JSON',
         'pm25_url':'https://data.epa.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=JSON'}

#################
# tinfar_mysql
#################
tinfar_VM = {'host':'61.220.205.143' , 'port':5306,'user':'backup' , 'pwd':'SLbackup#123' , 'db':'government_information' , 'charset':'utf8'}