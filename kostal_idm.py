#!/usr/bin/env python

import pymodbus
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

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

if __name__ == "__main__":  
    print ("##### START #####")
    try:
        #change the IP address and port:
        inverter_ip="192.168.1.5"
        inverter_port="1502"
        idm_ip="192.168.1.3"
        idm_port="502"  
        feed_in_limit=1000  
        #feed_in_limit=1     
        #no more changes required
        
        print ("##### reading KOSTAL", inverter_ip)
        inverterclient = ModbusTcpClient(inverter_ip,port=inverter_port)            
        inverterclient.connect()
        
        gridvalue = ReadFloat(inverterclient,108,71)
        print ("##### gridvalue: ", gridvalue)
        
        inverterclient.close()       
        
        #feed in must be above our limit
        feed_in = -gridvalue;
        if feed_in > feed_in_limit:
            print ("##### feed-in reached: ", feed_in)               
            feed_in = feed_in/1000
        else:
            print ("##### feed-in not reached: ", feed_in)  
            feed_in = 0
        
        print ("##### send to iDM: ", idm_ip)
        idmclient = ModbusTcpClient(idm_ip,port=idm_port)            
        idmclient.connect()        
       
        WriteFloat(idmclient,74,feed_in,1)
            
        #read from iDM
        idmvalue = ReadFloat(idmclient,74,1)
        print ("##### iDM: ", idmvalue)
            
        idmclient.close()   
        
        print ("##### END #####")
        
    except Exception as ex:
        print ("ERROR :", ex)    
        
    
