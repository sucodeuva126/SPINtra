# -*- coding: utf-8 -*-
from data_management import dir_name, dir_location
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"


banner = '''{0} 
   _____  ____   ____ _   __ __              
  / ___/ / __ \ /  _// | / // /_ _____ ____ _
  \__ \ / /_/ / / / /  |/ // __// ___// __ `/
 ___/ // ____/_/ / / /|  // /_ / /   / /_/ / 
/____//_/    /___//_/ |_/ \__//_/    \__,_/  ''' . format(CYAN)


def gen_selection(options, final_option):
  text = ""
  for i in range(len(options)):
    text = text + "{1}"+str(i+1)+". "+"{0}"+str(options[i] + "      ")
  text = text +"{1}" + str(len(options)+1)+ "." + " " + "{0}" + final_option
  return text.format(WHITE, GREEN)






   
    
