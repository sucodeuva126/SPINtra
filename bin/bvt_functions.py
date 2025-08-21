import win32com.client as win


class BVT:
  def __init__(self, threshold):
    self.isTemperatureReady = False
    self.current_temp = None
    self.threshold = threshold
    self.bvt_server = win.Dispatch("WinAcquisit.BVT")
    self.emb = win.Dispatch("WinAcquisit.Embedding")
    self.uti = win.Dispatch("WinAcquisit.Utilities")

  def start(self, gas_flow, evaporator):
    self.bvt_server = win.Dispatch("WinAcquisit.BVT") #the COM object is not thread safe, so it needs to be initialized here again
    self.emb = win.Dispatch("WinAcquisit.Embedding")
    self.uti = win.Dispatch("WinAcquisit.Utilities")
    self.bvt_server.GasFlow(gas_flow)
    self.bvt_server.GasFlowOn(True)
    if evaporator:
      self.bvt_server.EvaporatorOn(True)
      self.bvt_server.EvaporatorPower(gas_flow)
    self.bvt_server.HeaterOn(True)
    return

  def set_point_and_start_ramp(self, temp):
    self.bvt_server = win.Dispatch("WinAcquisit.BVT") #the COM object is not thread safe, so it needs to be initialized here again
    self.emb = win.Dispatch("WinAcquisit.Embedding")
    self.uti = win.Dispatch("WinAcquisit.Utilities")
    self.bvt_server.DesiredTemperature(temp)
    self.bvt_server.RampGO
    return 

  def autotune(self, switch):
    self.bvt_server = win.Dispatch("WinAcquisit.BVT") #the COM object is not thread safe, so it needs to be initialized here again
    self.emb = win.Dispatch("WinAcquisit.Embedding")
    self.uti = win.Dispatch("WinAcquisit.Utilities")
    if switch == True:
      self.bvt_server.PIDTuneOn(True)
    if switch == False:
      self.bvt_server.PIDTuneOn(False)
    return
    
  def get_temperature(self):
    self.bvt_server = win.Dispatch("WinAcquisit.BVT") #the COM object is not thread safe, so it needs to be initialized here again
    self.emb = win.Dispatch("WinAcquisit.Embedding")
    self.uti = win.Dispatch("WinAcquisit.Utilities")
    try:
        self.current_temp  = self.bvt_server.GetTemperature #saves the temperature read
    except Exception as e:
        print("ERROR IN READING TEMPERATURES", e)

  def check_temperature(self, temp): #thread function
    self.bvt_server = win.Dispatch("WinAcquisit.BVT") #the COM object is not thread safe, so it needs to be initialized here again
    self.emb = win.Dispatch("WinAcquisit.Embedding")
    self.uti = win.Dispatch("WinAcquisit.Utilities")
    if self.current_temp is not None:
        if self.bvt_server.IsTemperatureOK: #verify if the mesured temperature is the desired temperature 
            self.isTemperatureReady = True
        else:
            self.isTemperatureReady = False


