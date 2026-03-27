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
        if not hasattr(self._tls, "initialized"):
            pythoncom.CoInitialize()
            self._tls.uti = win.Dispatch("WinAcquisit.Utilities")
            self._tls.emb = win.Dispatch("WinAcquisit.Embedding")
            self._tls.emb.ShowWindow(self._tls.emb.NORMAL)
            time.sleep(2)
            self._tls.bvt_server = win.Dispatch("WinAcquisit.BVT")
            self._tls.initialized = True

    # FINALIZA COM (chamar só no fim da thread!)
    def release_com(self):
        if hasattr(self._tls, "initialized"):
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

    def set_point_and_start_ramp(self, temp):
        self._ensure_com()
        srv = self._tls.bvt_server

        srv.DesiredTemperature(temp)
        srv.RampGO

    def autotune(self, switch):
        self._ensure_com()
        srv = self._tls.bvt_server

        srv.PIDTuneOn(bool(switch))

    def get_temperature(self):
        self._ensure_com()
        try:
            self.current_temp = self._tls.bvt_server.GetTemperature
        except Exception as e:
            print("ERROR READING BVT TEMPERATURES:", e)
        try:
            if self.current_temp is not None:
                self.isTemperatureReady = bool(self._tls.bvt_server.IsTemperatureOK)
        except Exception as e:
            print("ERROR CHECKING TEMPERATURE:", e)

