#!/usr/bin/env python

import pymodbus
from datetime import datetime
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

def boolstr_to_floatstr(v):
    if v == 'True':
        return '1'
    elif v == 'False':
        return '0'
    else:
        return v

#-----------------------------------------
# Routine to read a float    
def readfloat(client,myadr_dec,unitid):
    r1=client.read_holding_registers(myadr_dec,count=2,slave=unitid)
    # print(str(r1.registers))
    FloatRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    # print(FloatRegister.decode_32bit_float())
    result_FloatRegister = round(FloatRegister.decode_32bit_float(),2)
    # the new code is giving strange values...])
    # FloatRegister = client.convert_from_registers(r1.registers, client.DATATYPE.FLOAT32)
    # print(FloatRegister)
    # result_FloatRegister = round(FloatRegister,2)
    return(result_FloatRegister)

def read(inverter_ip, inverter_port):  
    try:

        #connection Kostal
        client = ModbusTcpClient(inverter_ip,port=inverter_port)            
        client.connect()

        result = {}

        powerToGrid = -readfloat(client,252,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " powerToGrid: ", powerToGrid)  
        result["powerToGrid"] = powerToGrid
        
        return result      
    except Exception as ex:
        print ("ERROR Kostal: ", ex) 
    finally:
        client.close() 
      