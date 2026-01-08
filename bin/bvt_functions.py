import win32com.client as win
import pythoncom
import threading

class BVT:
  def __init__(self, threshold):
    self.isTemperatureReady = False
    self.current_temp = None
    self.threshold = threshold
    self._tls = threading.local()

  def _ensure_com(self):
    if not hasattr(self._tls, "initialized"):
        pythoncom.CoInitialize()
        self._tls.emb = win.Dispatch("WinAcquisit.Embedding")
        self._tls.bvt_server = win.Dispatch("WinAcquisit.BVT")
        self._tls.uti = win.Dispatch("WinAcquisit.Utilities")
        self._tls.initialized = True

  def _release_com(self):
    if hasattr(self._tls, "initialized"):
        del self._tls.emb
        del self._tls.bvt_server
        del self._tls.uti
        pythoncom.CoUninitialize()
        del self._tls.initialized

  def start(self, gas_flow, evaporator):
    self._ensure_com()
    self._tls.bvt_server.GasFlow(gas_flow)
    self._tls.bvt_server.GasFlowOn(True)
    if evaporator:
      self._tls.bvt_server.EvaporatorOn(True)
      self._tls.bvt_server.EvaporatorPower(gas_flow)
    self._tls.bvt_server.HeaterOn(True)
    self._release_com()
    return

  def set_point_and_start_ramp(self, temp):
    self._ensure_com()
    self._tls.bvt_server.DesiredTemperature(temp)
    self._tls.bvt_server.RampGO
    self._release_com()
    return 

  def autotune(self, switch):
    self._ensure_com()
    if switch == True:
      self._tls.bvt_server.PIDTuneOn(True)
    if switch == False:
      self._tls.bvt_server.PIDTuneOn(False)
    self._release_com()
    return
    
  def get_temperature(self):
    self._ensure_com()
    try:
        self.current_temp  = self._tls.bvt_server.GetTemperature #saves the temperature read
    except Exception as e:
        print("ERROR IN READING TEMPERATURES", e)
    self._release_com()

  def check_temperature(self, temp): #thread function
    self._ensure_com()
    if self.current_temp is not None:
        if self._tls.bvt_server.IsTemperatureOK: #verify if the mesured temperature is the desired temperature 
            self.isTemperatureReady = True
        else:
            self.isTemperatureReady = False
    self._release_com()


