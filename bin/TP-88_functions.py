# -*- coding: utf-8 -*-
import serial
import pyvisa as visa

class TP88:
    def __init__(self, threshold):
        self.isTemperatureReady = False
        self.current_temp = None
        self.threshold = threshold

    def start(self):
        self.ser = serial.Serial(
        port='COM1',
        baudrate=1200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        timeout=1
        )
        return
    
    def end(self):
        self.ser.close()
        return

    def set_point_and_start_ramp(self, temp):
        if self.ser.isOpen():
            self.ser.write("SPn" + str(temp).encode() + b"\n")
        else:
            print("Error: RS232 Serial TP-88 port is not open.")
        return

    def autotune(self, switch):           
        return

    def get_temperature(self):
        self.current_temp = self._tls.bvt_server.GetTemperature
        if self._tls.bvt_server.IsTemperatureOK: #verify if the mesured temperature is the desired temperature 
            self.isTemperatureReady = True
        else:
            self.isTemperatureReady = False

class TP88:
    def __init__(self, threshold):
        self.isTemperatureReady = False
        self.current_temp = None
        self.desired_temp = None
        self.threshold = threshold

    def start(self):
        self.rm = visa.ResourceManager()
        self.rm.list_resources() #list all the connected devices, to check if the TP-88 is connected and on which port
        self.visa_inst = self.rm.open_resource('GPIB0::5::INSTR')
        return
    
    def end(self):
        self.visa_inst.close()
        self.rm.close()
        return

    def set_point_and_start_ramp(self, temp):
        self.desired_temp = temp
        if self.visa_inst.query('*IDN?'):
            self.visa_inst.write("SPn" + str(temp).encode() + b"\n")
        else:
            print("Error: GPIB IEE-488 TP-88 port is not open.")
        return

    def autotune(self, switch):           
        return

    def get_temperature(self):
        try:
            self.current_temp = float(self.visa_inst.query("?SP").strip()) #strip() removes any leading/trailing whitespace characters
            if abs(self.current_temp-self.desired_temp)<self.threshold: #verify if the mmesured temperature is the desired temperature 
                self.isTemperatureReady = True
            else:
                self.isTemperatureReady = False
            if self.current_temp is not None and self.desired_temp is not None:
                if abs(self.current_temp-self.desired_temp)<self.threshold: #verify if the mmesured temperature is the desired temperature 
                    self.isTemperatureReady = True
                else:
                    self.isTemperatureReady = False
        except Exception as e:
            print("ERROR IN READING TEMPERATURES", e)
        finally:
            self.visa_inst.close()

