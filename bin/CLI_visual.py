# -*- coding: utf-8 -*-
import os
from data_management import dir_name, dir_location
import tqdm
import time
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

main_dir_path = dir_location +  "\\"  + "{}".format(dir_name)+ "\\" + "{}".format("Experiments") #ATENÇÂO COM A LOCALIZAÇÂO DO DIRETORIO, VER NO PC DO LAB
files = os.listdir(main_dir_path) #lista os arquivos existentes na pasta Experiments

banner = '''{0} 
███████╗██████╗ ██╗███╗   ██╗████████╗██████╗  █████╗ 
██╔════╝██╔══██╗██║████╗  ██║╚══██╔══╝██╔══██╗██╔══██╗
███████╗██████╔╝██║██╔██╗ ██║   ██║   ██████╔╝███████║
╚════██║██╔═══╝ ██║██║╚██╗██║   ██║   ██╔══██╗██╔══██║
███████║██║     ██║██║ ╚████║   ██║   ██║  ██║██║  ██║
╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
                                                        ''' . format(CYAN)


def gen_selection(options, final_option):
  text = ""
  for i in range(len(options)):
    text = text + "{1}"+str(i+1)+". "+"{0}"+str(options[i] + "      ")
  text = text +"{1}" + str(len(options)+1)+ "." + " " + "{0}" + final_option
  return text.format(WHITE, GREEN)



#def gen_experiment_selection_menu(list_of_existent_files):
  experiment_selection_menu = ""
  for i in range(len(list_of_existent_files)):
    experiment_selection_menu = experiment_selection_menu  + "{1}"+ str(i+1) + "." + " " + "{0}" + str(list_of_existent_files[i] + "      " )
  experiment_selection_menu = experiment_selection_menu  +"{1}" + str(len(list_of_existent_files)+1)+ "." + " " + "{0}" + "Back"
  return experiment_selection_menu.format(WHITE, GREEN)





   
    
