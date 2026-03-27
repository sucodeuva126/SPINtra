import win32com.client as win
import pythoncom
import threading

class BVT:
  def __init__(self, threshold):
    self.isTemperatureReady = False
    self.current_temp = None
    self.threshold = threshold

#COM objects are not thread safe #PROBLEM HERE

  def start(self, gas_flow, evaporator):
    self.emb = win.Dispatch("WinAcquisit.Embedding")
    self.emb.ShowWindow(self.emb.NORMAL)
    self.bvt_server = win.Dispatch("WinAcquisit.BVT")
    self.uti = win.Dispatch("WinAcquisit.Utilities")
    self.bvt_server.GasFlow(gas_flow)
    self.bvt_server.GasFlowOn(True)
    if evaporator:
      self.bvt_server.EvaporatorOn(True)
      self.bvt_server.EvaporatorPower(gas_flow)
    self.bvt_server.HeaterOn(True)
    self.emb = None
    self.bvt_server = None
    self.uti = None
    return

  def set_point_and_start_ramp(self, temp):
    self.bvt_server = win.Dispatch("WinAcquisit.BVT")
    self.bvt_server.DesiredTemperature(temp)
    self.bvt_server.RampGO
    self.bvt_server = None
    return 

  def autotune(self, switch):
    self.bvt_server = win.Dispatch("WinAcquisit.BVT")
    if switch == True:
      self.bvt_server.PIDTuneOn(True)
    if switch == False:
      self.bvt_server.PIDTuneOn(False)
    self.bvt_server = None
    return
    
  def get_temperature(self):
    self.bvt_server = win.Dispatch("WinAcquisit.BVT")
    try:
        self.current_temp  = self.bvt_server.GetTemperature #saves the temperature read
        self.bvt_server = None
    except Exception as e:
        self.bvt_server = None
        print("ERROR READING BVT TEMPERATURES", e)
    

  def check_temperature(self, temp): #thread function
    self.bvt_server = win.Dispatch("WinAcquisit.BVT")
    if self.current_temp is not None:
        if self.bvt_server.IsTemperatureOK: #verify if the mesured temperature is the desired temperature 
            self.isTemperatureReady = True
        else:
            self.isTemperatureReady = False
    self.bvt_server = None


