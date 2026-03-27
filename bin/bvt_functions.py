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

    #  inicializa COM UMA VEZ por thread
    def _ensure_com(self):
        if not hasattr(self, "initialized"):
            pythoncom.CoInitialize()
            self.uti = win.Dispatch("WinAcquisit.Utilities")
            self.emb = win.Dispatch("WinAcquisit.Embedding")
            self.emb.ShowWindow(self.emb.NORMAL)
            self.bvt_server = win.Dispatch("WinAcquisit.BVT")
            self.initialized = True

    # FINALIZA COM (chamar só no fim da thread!)
    def release_com(self):
        if hasattr(self, "initialized"):
            try:
                del self.emb
                del self.bvt_server
                del self.uti
            except:
                pass
            pythoncom.CoUninitialize()
            del self.initialized

    def start(self, gas_flow, evaporator):
        self.uti = win.Dispatch("WinAcquisit.Utilities")
        self.emb = win.Dispatch("WinAcquisit.Embedding")
        self.emb.ShowWindow(self.emb.NORMAL)
        self.bvt_server = win.Dispatch("WinAcquisit.BVT")
        srv = self.bvt_server
        srv.GasFlow(gas_flow)
        srv.GasFlowOn(True)
        if evaporator:
            srv.EvaporatorOn(True)
            srv.EvaporatorPower(gas_flow)
        srv.HeaterOn(True)
        return

    def set_point_and_start_ramp(self, temp):            
      self.uti = win.Dispatch("WinAcquisit.Utilities")
      self.emb = win.Dispatch("WinAcquisit.Embedding")
      self.emb.ShowWindow(self.emb.NORMAL)
      self.bvt_server = win.Dispatch("WinAcquisit.BVT")
      srv = self.bvt_server
      srv.DesiredTemperature(temp)
      srv.RampGO
      return

    def autotune(self, switch):            
        self.uti = win.Dispatch("WinAcquisit.Utilities")
        self.emb = win.Dispatch("WinAcquisit.Embedding")
        self.emb.ShowWindow(self.emb.NORMAL)
        self.bvt_server = win.Dispatch("WinAcquisit.BVT")
        srv = self.bvt_server
        srv.PIDTuneOn(bool(switch))
        return

    def get_temperature(self, stop_get):
        while not stop_get.is_set():
          self.uti = win.Dispatch("WinAcquisit.Utilities")
          self.emb = win.Dispatch("WinAcquisit.Embedding")
          self.emb.ShowWindow(self.emb.NORMAL)
          self.bvt_server = win.Dispatch("WinAcquisit.BVT")
          self.current_temp = self.bvt_server.GetTemperature
          if self.bvt_server.IsTemperatureOK: #verify if the mesured temperature is the desired temperature 
            self.isTemperatureReady = True
          else:
            self.isTemperatureReady = False
          self.uti = None
          self.emb = None
          self.bvt_server = None

