#!/usr/bin/env python

import pymodbus
import configparser
import os
import psycopg2
from datetime import datetime
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

#read config
config = configparser.ConfigParser()

#-----------------------------------------
# Routine to read a float    
def ReadFloat(client,myadr_dec,unitid):
    r1=client.read_holding_registers(myadr_dec,2,unit=unitid)
    FloatRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
    result_FloatRegister =round(FloatRegister.decode_32bit_float(),2)
    return(result_FloatRegister)   
#----------------------------------------- 
# Routine to write float
def WriteFloat(client,myadr_dec,feed_in,unitid):
    builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
    builder.add_32bit_float( feed_in )
    payload = builder.to_registers() 
    client.write_registers(myadr_dec, payload, unit=unitid)

# write metric to TimescaleDB
def WriteTimescaleDb(conn, table, value):
    if conn:
        # create a cursor
        cur = conn.cursor()   
        # execute a statement
        sql = 'insert into '+table+' (time, value) values (now(), %s)'
        cur.execute(sql, (value,))   
        # commit the changes to the database
        conn.commit()
        # close the communication with the PostgreSQL
        cur.close()

if __name__ == "__main__":  
    print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " START #####")
    try:
        #read config
        config.read('kostal_idm.ini')

        #read config and default values
        inverter_ip = config['KostalSection']['inverter_ip']
        inverter_port = config['KostalSection']['inverter_port']
        idm_ip = config['IdmSection']['idm_ip']
        idm_port = config['IdmSection']['idm_port']  
        feed_in_limit = int(config['FeedinSection']['feed_in_limit']) 
        timescaledb_ip = config['MetricSection']['timescaledb_ip']
        timescaledb_username = config['MetricSection']['timescaledb_username']
        timescaledb_password = config['MetricSection']['timescaledb_password']

        # override with environment variables
        if os.getenv('INVERTER_IP','None') != 'None':
            inverter_ip = os.getenv('INVERTER_IP')
            print ("using env: INVERTER_IP")
        if os.getenv('INVERTER_PORT','None') != 'None':
            inverter_port = os.getenv('INVERTER_PORT')
            print ("using env: INVERTER_PORT")
        if os.getenv('IDM_IP','None') != 'None':
            idm_ip = os.getenv('IDM_IP')
            print ("using env: IDM_IP")
        if os.getenv('IDM_PORT','None') != 'None':
            idm_port = os.getenv('IDM_PORT')
            print ("using env: IDM_PORT")
        if os.getenv('FEED_IN_LIMIT','None') != 'None':
            feed_in_limit = os.getenv('FEED_IN_LIMIT')
            print ("using env: FEED_IN_LIMIT")
        if os.getenv('TIMESCALEDB_IP','None') != 'None':
            timescaledb_ip = os.getenv('TIMESCALEDB_IP')
            print ("using env: TIMESCALEDB_IP")
        if os.getenv('TIMESCALEDB_USERNAME','None') != 'None':
            timescaledb_username = os.getenv('TIMESCALEDB_USERNAME')
            print ("using env: TIMESCALEDB_USERNAME")
        if os.getenv('TIMESCALEDB_PASSWORD','None') != 'None':
            timescaledb_password = os.getenv('TIMESCALEDB_PASSWORD')
            print ("using env: TIMESCALEDB_PASSWORD")

        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " inverter_ip: ", inverter_ip)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " inverter_port: ", inverter_port)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " idm_ip: ", idm_ip)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " idm_port: ", idm_port)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " feed_in_limit: ", feed_in_limit)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " timescaledb_ip: ", timescaledb_ip)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " timescaledb_username: ", timescaledb_username)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " timescaledb_password: ", timescaledb_password)

        #init Timescaledb if used
        if timescaledb_ip:
            conn = psycopg2.connect(
                host=timescaledb_ip,
                database="postgres",
                user=timescaledb_username,
                password=timescaledb_password)
        
        #connection Kostal
        inverterclient = ModbusTcpClient(inverter_ip,port=inverter_port)            
        inverterclient.connect()    
        
        consumptionbat = ReadFloat(inverterclient,106,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption battery: ", consumptionbat)
        consumptiongrid = ReadFloat(inverterclient,108,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption grid: ", consumptiongrid)
        consumptionpv = ReadFloat(inverterclient,116,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption pv: ", consumptionpv)
        consumption_total = consumptionbat + consumptiongrid + consumptionpv
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption: ", consumption_total)

        inverter = ReadFloat(inverterclient,172,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " inverter: ", inverter)   
        WriteTimescaleDb(conn, 'solar_kostal_inverter', inverter)      
        
        #this is not exact, but enough for us :-)
        powerToGrid = round(inverter - consumption_total,1)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " powerToGrid: ", powerToGrid)   
        WriteTimescaleDb(conn, 'solar_kostal_powertogrid', powerToGrid)
        
        batteryamp = ReadFloat(inverterclient,200,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " battery (A): ", batteryamp)
        batteryvolt = ReadFloat(inverterclient,216,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " battery (V): ", batteryvolt)
        battery = round(batteryamp * batteryvolt, 2)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " battery (W): ", battery)
        WriteTimescaleDb(conn, 'solar_kostal_battery', battery)
        if batteryamp > 0.1:
            print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " battery: discharge")
            powerToGrid = -1
            WriteTimescaleDb(conn, 'solar_kostal_batteryflag', 1)
        elif batteryamp < -0.1:
            WriteTimescaleDb(conn, 'solar_kostal_batteryflag', -1)
        else:
            WriteTimescaleDb(conn, 'solar_kostal_batteryflag', 0)
        batterypercent = ReadFloat(inverterclient,210,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " battery (%): ", batterypercent)
        WriteTimescaleDb(conn, 'solar_kostal_batterypercent', (batterypercent/100))

        inverterclient.close()       
        
        #feed in must be above our limit
        feed_in = powerToGrid;
        if feed_in > feed_in_limit:
            print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " feed-in reached: ", feed_in)               
            feed_in = feed_in/1000
        else:
            print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " send ZERO: ", feed_in)  
            feed_in = 0
        
        #connection iDM
        idmclient = ModbusTcpClient(idm_ip,port=idm_port)            
        idmclient.connect()        
       
        WriteFloat(idmclient,74,feed_in,1)
        WriteTimescaleDb(conn, 'solar_idm_feedin', (feed_in*1000))
            
        #read from iDM
        idmvalue = ReadFloat(idmclient,74,1)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " iDM: ", idmvalue)
            
        idmclient.close()   
        
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " END #####")
        
    except Exception as ex:
        print ("ERROR :", ex)   
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')   
