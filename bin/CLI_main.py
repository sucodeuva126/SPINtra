# -*- coding: utf-8 -*-
import os
import sys
import time
import CLI_visual
from CLI_visual import WHITE, GREEN, RED, YELLOW, CYAN
from data_management import Experiment, dir_name, file_to_experiment, dir_location
import win32com.client as win
from devices import Device
import threading
import colorama
import signal
from tqdm import tqdm

interrupt = threading.Event()
def handle_keyboard_interrupt(signum, frame):
    print("INTERRUPTED!!!!")
    interrupt.set()

signal.signal(signal.SIGINT, handle_keyboard_interrupt)


class CLI:
  def __init__(self):
    colorama.init()
    self.version = "1.0"
    self.experiments_dir_path = "{}".format(dir_location)+  "\\"  + "{}".format(dir_name)+ "\\" + "{}".format("Experiments") #ATENÇÂO COM A LOCALIZAÇÂO DO DIRETORIO, VER NO PC DO LAB
    self.experiments_files = os.listdir(self.experiments_dir_path) #lists existent experiment files in the Experiments directory
    self.applications_dir_path = "{}".format(dir_location)+  "\\"  + "{}".format(dir_name)+ "\\" + "{}".format("Applications")
    self.applications_files = [f for f in os.listdir(self.applications_dir_path) if f.endswith(".app")] #lists existent application files in the Applications directory
    self.exeperiment_running = False
    self.selected_experiment = None
    self.selected_device = None
    self.current_waiting = None
    self.current_app = None
    self.current_temp = None
    self.scans_to_do = None
    self.scans_done = None
    self.scans_bar = None
    self.lock = threading.Lock()
    self.stop_run_screen = threading.Event()
    self.start_menu()

  def clean_screen_and_print_header(self):
      os.system("cls")
      print(CLI_visual.banner + "{}".format(self.version))
      print("Spectroscopy Intelligent Thermal Assistant")
      print('by L.A.R.M.M.O.R.')
      print("\n")
      if self.selected_experiment != None: #checks if there is an selected experiment to show to the user
        print("{0}Selected experiment:". format(RED)+ " " +"{}".format(self.selected_experiment))
        print("\n")
      if self.selected_device != None: #checks if there is an selected thermal device to show to the user
        print("{0}Selected thermal control device:". format(YELLOW)+ " " +"{}".format(self.selected_device))
        print("\n")
      return None

  def start_menu(self):
      self.clean_screen_and_print_header()
      options = ["Start experiment", "Select existent experiment", "Create new experiment", "Select thermal device", "Thermal devices operations"]
      print(CLI_visual.gen_selection(options=options, final_option="Exit"))
      selection = input("{0}Enter Selection > ".format(WHITE))
      if selection == 1:
        if self.selected_experiment != None:
          self.run_experiment()
          return
        else:
          print("Please, select an experiment first.")
          time.sleep(1.5)
          self.start_menu()
          return
      elif selection == 2:
        self.experiment_selection_menu()
        return
      elif selection == 3:
        self.creation_menu()
        return
      elif selection == 4:
        self.device_selection_menu()
        return
      elif selection == 5:
        self.device_ops_menu()
        return
      elif selection == 6:
        exit()
      else:
        print("This option doesn't exist, returning...")
        time.sleep(1.5)
        self.start_menu()
        return
      return None

  def device_selection_menu(self):
    self.clean_screen_and_print_header()
    options = ["BVT", "KM3P"]
    print("{0}Select the thermal device:".format(WHITE))
    print(CLI_visual.gen_selection(options=options, final_option="Back"))
    selection = input("{0}Enter Selection > ".format(WHITE))
    if selection == 1:
      self.selected_device = options[0]
      print("Device" +" " +"\"" + "{}".format(options[0])+ "\"" + " " + " has been selected.")
      self.start_menu()
      return
    elif selection == 2:
      self.selected_device = options[1]
      print("Device" +" " +"\"" + "{}".format(options[1])+ "\"" + " " + " has been selected.")
      self.start_menu()
      return
    elif selection == 3:
      print("Returning to menu in 1s...")
      time.sleep(1)
      self.start_menu()
      return
    else:
      print("This option doesn't exist, returning to menu in 1s...")
      time.sleep(1)
      self.start_menu()
      return

  def device_ops_menu(self):
    options = ["BVT", "KM3P"]
    temp_dim = ["K", "°C"]
    methods = ["Start autotunning","Set Point and start ramp"]
    print(CLI_visual.gen_selection(options=options, final_option="Back"))
    device_selection = int(input("Enter selection > "))
    device = Device(options[device_selection-1], tolerance=1)
    if device_selection == 1:
      print(CLI_visual.gen_selection(options=methods, final_option="Back"))
      selection = input("{0}Enter Selection > ".format(WHITE))
      if selection == 1:
        device.autotune(switch=True)
        self.device_ops_menu()
      if selection == 2:
        point = float(input("Set point("+"{}"+") >".format(temp_dim[device_selection - 1])))
        device.set_point_and_start_ramp(point)
        self.device_ops_menu()
    elif device_selection == 2:  
      print(CLI_visual.gen_selection(options=methods, final_option="Back"))
      selection = input("{0}Enter Selection > ".format(WHITE))
    elif device_selection == 3:
      print("Returning to menu in 1s...")
      time.sleep(1)
      self.start_menu() 
      return
    else:
      print("This option doesn't exist, returning to menu in 1s...")
      time.sleep(1)
      self.start_menu()
      return
    return

  def experiment_selection_menu(self):
    self.experiment_files = os.listdir(self.experiments_dir_path) #update the existent experiment_files in the Experiments directory, in case something has been added.
    self.clean_screen_and_print_header() 
    print("{0}Select one already existent experiment:".format(WHITE))
    print(CLI_visual.gen_selection(self.experiment_files, final_option="Back"))
    option = input("{0}Enter Selection >" . format(WHITE))
    if option not in (range(len(self.experiment_files)+2)): #checks if the option is not between the shown
      print("This option doesn't exist, returning to menu in 1s...")
      time.sleep(1)
      self.start_menu()
      return
    if option == len(self.experiment_files) + 1: #checks if the option is "Back"
      print("Returning to menu in 1s...")
      time.sleep(1)
      self.start_menu()
      return    
    if option in range(len(self.experiment_files)+1): #checks if the option is between the shown
      self.selected_experiment = self.experiment_files[int(option) - 1] #atributes one experiment from the experiment_files to be the selected 
      print("Experiment" +" " +"\"" + "{}".format(self.selected_experiment)+ "\"" + " " + " has been selected.")
      self.start_menu()
      return
    return None

  def creation_menu(self):
    self.clean_screen_and_print_header()
    name = raw_input("Experiment name >") #raw doesn't need "" for strings inputs
    print("{0}Select the thermal device for this experiment:".format(WHITE))
    print(CLI_visual.gen_selection(options=["BVT", "KM3P"], final_option="Back"))
    selection = int(input("Enter selection"))
    if selection == 1:
      device = "BVT"
    elif selection == 2:
      device = "KM3P"
    else:
      print("This option doesn't exist, returning to menu in 2s...")
      time.sleep(2)
      self.start_menu()
    temps = []
    waiting_times = []
    number_of_temps_intervals = int(input("How many temperatures intervals? > "))
    for i in range(number_of_temps_intervals):
      interval = []
      step = float(input("Temperature step for interval" + " " +"{}".format(i+1) +" >" ))
      initial_limit = float(input("Initial temperature of interval" + " " +"{}".format(i+1) +" >"))
      final_limit = float(input("Final temperature of interval" + " " +"{}".format(i+1) +" >"))
      waiting = float(input("Thermalization waiting time for interval (seconds)" + " " +"{}".format(i+1)+" >"))
      waiting_times.append(waiting)
      interval.append(initial_limit)
      t = initial_limit
      if final_limit > initial_limit: 
        while t < final_limit:
          t = t + step
          interval.append(t)
      else:
        while t > final_limit:
          t = t - step
          interval.append(t)
      temps.append(interval)
    print(CLI_visual.gen_selection(self.applications_files, final_option="Back"))
    pulse_sequences = []
    number_of_pulse_sequences = int(input("How many pulse sequences? >")) #ADD BACK OPTION
    for i in range(number_of_pulse_sequences):
      ask = int(input("Pulse sequence"  +" "+"{}".format(i+1) + " >"))
      pulse_sequences.append(self.applications_files[ask-1])
    experiment = Experiment(name, device, temps, waiting_times, pulse_sequences)
    experiment.create_experiment_file(name)
    print("Experiment" + " " +"\"" + "{}".format(name) + "\"" + " " + "has been created, returning to menu in 2s...")
    time.sleep(2)
    self.start_menu()
    return None

  def exit(self):
    sys.exit()
    return

  def current_experiment_screen(self, device, interrupt):
    while not self.stop_run_screen.is_set() and not interrupt.is_set():
        with self.lock:
          if device.isTemperatureReady:
            color = GREEN
          else:
            color = YELLOW
          sys.stdout.write("\r{0}Current temperature: {2}{3}   |   {0}Current pulse sequence: {1}{4}   |   {0}Current waiting time for thermalization: {1}{5}".format(CYAN, WHITE, color, device.current_temp, self.current_app, self.current_waiting))
          sys.stdout.flush()
          time.sleep(0.1)
 
  def run_experiment(self):
    self.experiment_running = True
    temp_tolerance = 1
    current_experiment = file_to_experiment(self.selected_experiment)
    current_experiment_path = self.experiments_dir_path + "\\" + "{}".format(self.selected_experiment)
    temps = current_experiment.temperatures #matrix with intervals(lines) and temperatures(columns)
    pulse_sequences = current_experiment.pulse_sequence
    waiting_times = current_experiment.waiting_time
    get_thread = None
    check_thread = None
    screen_thread = None
    current_app_path = []
    for p in range(len(pulse_sequences)):
      current_app_path.append(self.applications_dir_path + "\\" + "{}".format(pulse_sequences[p]))
    pnmr = win.Dispatch("theMinispec.PNMR")
    pnmr.ConfigWakeUp([0,pnmr.MAXIMIZED, 1, 0, 0, 0])
    pnmr.OpenPNMR()
    serial_number= pnmr.GetInstrumentSerialNumber
    pnmr.ConnectInstrument(serial_number)
    if not pnmr.IsInstrumentConnected:
      print("ERROR CONNECTING TO THE MINISPEC")
    device = Device(self.selected_device, temp_tolerance)
    if self.selected_device == "BVT":
      a = raw_input("Turn on the evaporator?[y/n] ")
      g = float(input("Gas flow(l/h)> "))
      if a == "y":
        ev = True
      else:
        ev = False
      device.start(gas_flow = g, evaporator = ev) #works only for the bvt
    self.stop_run_screen.clear()
    screen_thread = threading.Thread(target=self.current_experiment_screen, args=(device, interrupt,))
    screen_thread.start() 
    try:
      for i in range(len(temps)):
        wait = float(waiting_times[i])
        for j in range(len(temps[i])):
          device.set_point_and_start_ramp(float(temps[i][j]))
          device.stop_get.clear()  # reset stop flags
          device.stop_check.clear()
          get_thread = threading.Thread(target=device.get_temperature, args=(interrupt,)) #start monitoring threads
          check_thread = threading.Thread(target=device.check_temperature, args=(float(temps[i][j]),interrupt,)) #checks if the current temperature is the desired, yes it needs the final comma
          get_thread.start()
          check_thread.start()
          while not device.isTemperatureReady and not interrupt.is_set():
            time.sleep(1)
          self.current_waiting = wait
          time.sleep(wait)
          self.current_waiting = None
          for p in range(len(pulse_sequences)):
            pnmr.ReleaseApplication
            self.current_app = pulse_sequences[p]
            pnmr.LoadApplication(current_app_path[p])
            if not pnmr.IsApplicationLoaded:
              print("ERROR LOADING APPLICATION")
            pnmr.RunApplication()
            while pnmr.IsApplicationRunning and not interrupt.is_set():
              time.sleep(1)
          pnmr.ReleaseApplication
          device.stop_get.set()
          device.stop_check.set()
          self.stop_run_screen.set()
          get_thread.join()
          check_thread.join()
          screen_thread.join() #end
    
    except KeyboardInterrupt:
      if check_thread is not None:
        device.stop_check.set()
        check_thread.join()
      if get_thread is not None:
        device.stop_get.set()
        get_thread.join()
      if screen_thread is not None:
        self.stop_run_screen.set()
        screen_thread.join()
      pnmr = None
      device = None
      
    finally:
      if self.selected_device == "BVT":
        device.set_point_and_start_ramp(300)
      if self.selected_device == "KM3P":
        device.set_point_and_start_ramp(27)
      if check_thread is not None:
        device.stop_check.set()
        check_thread.join()
      if get_thread is not None:
        device.stop_get.set()
        get_thread.join()
      if screen_thread is not None:
        self.stop_run_screen.set()
        screen_thread.join()
      pnmr = None
      device = None
      self.experiment_running = False
      self.selected_experiment = None
      self.selected_device = None
      print("\n")
      print("Experiment "+ "{}". format(current_experiment.name)  +" has finished...")
      r = raw_input("{} Would you like to return to main menu?[y/n] ".format(WHITE))
      if r == "y":
        self.start_menu()
      elif r == "n":
        self.exit()
      else:
        print("This option doesn't exist, quiting...")
        time.sleep(1.5)
        self.exit()
    return

if __name__ == "__main__":
  cli=CLI()
