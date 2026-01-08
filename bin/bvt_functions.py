import win32com.client as win

class BVT:
  def __init__(self, threshold):
    self.isTemperatureReady = False
    self.current_temp = None
    self.threshold = threshold

  def init_com_server(self): #COM objects are not thread safe #PROBLEM HERE
    self.emb = win.Dispatch("WinAcquisit.Embedding")
    self.emb.ShowWindow(self.emb.NORMAL)
    self.bvt_server = win.Dispatch("WinAcquisit.BVT")
    self.uti = win.Dispatch("WinAcquisit.Utilities")

  def start(self, gas_flow, evaporator):
    self.init_com_server()
    self.bvt_server.GasFlow(gas_flow)
    self.bvt_server.GasFlowOn(True)
    if evaporator:
      self.bvt_server.EvaporatorOn(True)
      self.bvt_server.EvaporatorPower(gas_flow)
    self.bvt_server.HeaterOn(True)
    return

  def set_point_and_start_ramp(self, temp):
    self.init_com_server()
    self.bvt_server.DesiredTemperature(temp)
    self.bvt_server.RampGO
    return 

  def autotune(self, switch):
    self.init_com_server()
    if switch == True:
      self.bvt_server.PIDTuneOn(True)
    if switch == False:
      self.bvt_server.PIDTuneOn(False)
    return
    
  def get_temperature(self):
    self.init_com_server()
    try:
        self.current_temp  = self.bvt_server.GetTemperature #saves the temperature read
    except Exception as e:
        print("ERROR IN READING TEMPERATURES", e)

  def check_temperature(self, temp): #thread function
    self.init_com_server()
    if self.current_temp is not None:
        if self.bvt_server.IsTemperatureOK: #verify if the mesured temperature is the desired temperature 
            self.isTemperatureReady = True
        else:
            self.isTemperatureReady = False


