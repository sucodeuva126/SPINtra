# -*- coding: utf-8 -*-
import win32com.client as win
import pythoncom
import threading
import time

class BVT:
    def __init__(self, threshold):
        self.isTemperatureReady = False
        self.current_temp = None
        self.threshold = threshold
        self._tls = threading.local()

    #  inicializa COM UMA VEZ por thread
    def _ensure_com(self):
        if not hasattr(self, "initialized"):
            pythoncom.CoInitialize()
            self._tls.uti = win.Dispatch("WinAcquisit.Utilities")
            self._tls.emb = win.Dispatch("WinAcquisit.Embedding")
            self._tls.emb.ShowWindow(self.emb.NORMAL)
            self._tls.bvt_server = win.Dispatch("WinAcquisit.BVT")
            self._tls.initialized = True

    # FINALIZA COM (chamar só no fim da thread!)
    def _release_com(self):
        if hasattr(self, "initialized"):
            try:
                del self._tls.emb
                del self._tls.bvt_server
                del self._tls.uti
            except:
                pass
            pythoncom.CoUninitialize()
            del self._tls.initialized

    def start(self, gas_flow, evaporator):
        self._ensure_com()
        srv = self._tls.bvt_server
        srv.GasFlow(gas_flow)
        srv.GasFlowOn(True)
        if evaporator:
            srv.EvaporatorOn(True)
            srv.EvaporatorPower(gas_flow)
        srv.HeaterOn(True)
        return
    
    def end(self):
        self._release_com()
        return

    def set_point_and_start_ramp(self, temp):            
      srv = self._tls.bvt_server
      srv.DesiredTemperature(temp)
      srv.RampGO
      return

    def autotune(self, switch):            
        srv = self._tls.bvt_server
        srv.PIDTuneOn(bool(switch))
        return

    def get_temperature(self):
        self.current_temp = self._tls.bvt_server.GetTemperature
        if self.bvt_server.IsTemperatureOK: #verify if the mesured temperature is the desired temperature 
            self.isTemperatureReady = True
        else:
            self.isTemperatureReady = False


