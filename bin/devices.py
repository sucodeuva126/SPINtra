import bvt_functions as bvt
import modbus_client_KM3P_functions as km3p
import threading
import pythoncom

class Device:
    def __init__(self, name, tolerance):
        self.stop_get = threading.Event()
        self.stop_check = threading.Event()
        self.lock = threading.Lock()
        self.tolerance = tolerance
        self.current_temp = None
        self.isTemperatureReady = False
        if name == "BVT":
            self.device = bvt.BVT(self.tolerance)
        elif name == "KM3P":
            self.device = km3p.KM3P(self.tolerance)
        else:
            raise ValueError("DEVICE " + name + " DOESNT EXIST.")
    
    def start(self, **kwargs):
        return self.device.start(**kwargs)

    def get_temperature(self, interrupt):
        pythoncom.CoInitialize() #creates the COM object in this thread
        while not self.stop_get.is_set()  and not interrupt.is_set():
            with self.lock:
                self.device.get_temperature()
                self.current_temp = self.device.current_temp
                self.stop_check.wait(0.5)
        pythoncom.CoUninitialize() 
    
    def check_temperature(self, temp, interrupt):
        pythoncom.CoInitialize()
        while not self.stop_get.is_set() and not interrupt.is_set():
            with self.lock:
                self.device.check_temperature(temp)
                self.isTemperatureReady = self.device.isTemperatureReady
                self.stop_get.wait(0.5)
        pythoncom.CoUninitialize() 
    
    def set_point_and_start_ramp(self, temp):
        return self.device.set_point_and_start_ramp(temp)
    
    def autotune(self, switch):
        return self.device.autotune(switch)

        

  
        

        