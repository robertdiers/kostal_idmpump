#!/usr/bin/env python

import pymodbus
import configparser
import os
import graphyte
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

# read status from Tasmota
def WriteGraphite(graphite_ip, metric, value):
    if graphite_ip:
        graphyte.send(metric, value)

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
        graphite_ip = config['MetricSection']['graphite_ip']

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
        if os.getenv('GRAPHITE_IP','None') != 'None':
            graphite_ip = os.getenv('GRAPHITE_IP')
            print ("using env: GRAPHITE_IP")

        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " inverter_ip: ", inverter_ip)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " inverter_port: ", inverter_port)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " idm_ip: ", idm_ip)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " idm_port: ", idm_port)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " feed_in_limit: ", feed_in_limit)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " graphite_ip: ", graphite_ip)

        #init Graphite if used
        if graphite_ip:
            graphyte.init(graphite_ip)
        
        #connection Kostal
        inverterclient = ModbusTcpClient(inverter_ip,port=inverter_port)            
        inverterclient.connect()       
        
        consumptionbat = ReadFloat(inverterclient,106,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption battery: ", consumptionbat)
        WriteGraphite(graphite_ip, 'solar.kostal.consumption.battery', consumptionbat)
        consumptiongrid = ReadFloat(inverterclient,108,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption grid: ", consumptiongrid)
        WriteGraphite(graphite_ip, 'solar.kostal.consumption.grid', consumptiongrid)
        consumptionpv = ReadFloat(inverterclient,116,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption pv: ", consumptionpv)
        WriteGraphite(graphite_ip, 'solar.kostal.consumption.pv', consumptionpv)
        consumption_total = consumptionbat + consumptiongrid + consumptionpv
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption: ", consumption_total)
        WriteGraphite(graphite_ip, 'solar.kostal.consumption.total', consumption_total)
        
        #inverter = ReadFloat(inverterclient,100,71)
        #print ("##### inverter: ", inverter) 
        #inverter_phase1 = ReadFloat(inverterclient,156,71)
        #print ("##### inverter_phase1: ", inverter_phase1)  
        #inverter_phase2 = ReadFloat(inverterclient,162,71)
        #print ("##### inverter_phase2: ", inverter_phase2)  
        #inverter_phase3 = ReadFloat(inverterclient,168,71)
        #print ("##### inverter_phase3: ", inverter_phase3)   
        #inverter = inverter_phase1 + inverter_phase2 + inverter_phase3
        #print ("##### inverter: ", inverter)
        inverter = ReadFloat(inverterclient,172,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " inverter: ", inverter)   
        WriteGraphite(graphite_ip, 'solar.kostal.inverter', inverter)      
        
        #this is not exact, but enough for us :-)
        powerToGrid = round(inverter - consumption_total,1)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " powerToGrid: ", powerToGrid)   
        WriteGraphite(graphite_ip, 'solar.kostal.powertogrid', powerToGrid)
        
        battery = ReadFloat(inverterclient,200,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " battery: ", battery)
        WriteGraphite(graphite_ip, 'solar.kostal.battery', battery)
        if battery > 0.1:
            print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " battery: discharge")
            powerToGrid = -1    
        
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
        WriteGraphite(graphite_ip, 'solar.idm.feedin', feed_in)
            
        #read from iDM
        idmvalue = ReadFloat(idmclient,74,1)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " iDM: ", idmvalue)
            
        idmclient.close()   
        
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " END #####")
        
    except Exception as ex:
        print ("ERROR :", ex)    
        
    
