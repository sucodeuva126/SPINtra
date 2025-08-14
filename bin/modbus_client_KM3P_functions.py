# -*- coding: utf-8 -*-
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.transaction import ModbusRtuFramer
import logging

class KM3P:
    def __init__(self, threshold):
        logging.getLogger("pymodbus").setLevel(logging.WARNING) #turn off pymodbus infernal loggings messages
        self.isTemperatureReady = False
        self.current_temp = None
        self.threshold = threshold
        self.UNIT = 0x1
        self.client = ModbusSerialClient(method='rtu', port='COM6', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1)

    def start(self):
        return

    def set_sensor(self):
        S = str(input("Choose the sensor type(j for thermocouple, c for Pt100):")).lower()
        if S == 'c': #Pt100 sensor is value 7 on manual
            rr = self.client.write_register(640, 7, unit = self.UNIT)
            rq = self.client.read_holding_registers(640, 1, unit = self.UNIT)
            self.client.close()
        elif S == 'j': #Thermocouple sensor is value 0 on manual
            rr = self.client.write_register(640, 0, unit = self.UNIT)
            rq = self.client.read_holding_registers(640, 1, unit = self.UNIT)
            self.client.close()
        assert(not rr.isError())
        return None

    def autotune(self, switch):
        if switch == True:
            self.client.connect()
            self.client.write_register(0x2B8, 1 , unit=self.UNIT) #Manual autotunning start
            self.client.close()
        if switch == False:
            self.client.connect()
            self.client.write_register(0x2B8, 0 , unit=self.UNIT) #Manual autotunning turn off
            self.client.close()
        
        return None

    def set_output(self): #Output seetings for O_1 = Analogic current
        O_1 = 0x1
        self.client.connect()
        rq1 = self.client.write_register(0x28B, 0, unit=self.UNIT)
        rq2 = self.client.write_register(0x28C, O_1, unit = self.UNIT)
        rr1 = self.client.read_holding_registers(0x28B, unit = self.UNIT)
        rr2 = self.client.read_holding_registers(0x28C, unit = self.UNIT)

        assert(not rq1.isError())     # test that we are not an error 
        assert(not rq1.isError())     # test that we are not an error
        assert(rr1.registers[0] == 0 ) 
        assert(rr2.registers[0] == O_1 )       # test the expected value
        self.client.close()
        return None

    def set_point_and_start_ramp(self, temp):
        temp = str(temp)
        if "." in temp:
            raw_temp = int(str(temp).replace(".", "")) #just adjusting for the writing in the registers, for example, km3p reads 500 as 50°, and 5 as 50° 
        else:
            raw_temp = int(temp)*10
        try:
            self.client.connect()
            rq = self.client.write_register(717, raw_temp, unit = self.UNIT)
            rr = self.client.read_holding_registers(717, 1, unit = self.UNIT)
        except Exception as e:
            print("ERROR IN SETTING POINT", e)
        self.client.close()
        return None

    def get_temperature(self): #thread function
        try:
            self.client.connect()
            rq = self.client.read_holding_registers(1, 1, unit=self.UNIT) #reads the mesured temperature register for KM3P
            temp = float(rq.registers[0])/10 #just converting again the reading temperature, for example from 500(50° at KM3P) to 50
            self.current_temp = temp #saves the temperature read
        except Exception as e:
            print("ERROR IN READING TEMPERATURES", e)
        finally:
            self.client.close()

    def check_temperature(self, temp): #thread function
                if self.current_temp is not None:
                    if abs(self.current_temp-temp)<self.threshold: #verify if the mmesured temperature is the desired temperature 
                        self.isTemperatureReady = True
                    else:
                        self.isTemperatureReady = False

  



   

