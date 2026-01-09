# -*- coding: utf-8 -*-
import os, ast
file_path = os.path.abspath(__file__)
dir_location = os.path.dirname(file_path).replace("\\bin", "")
dir_name = os.path.basename(dir_location + "\\data")

class  Experiment:
    def __init__(self, name, device ,temperatures, waiting_time, pulse_sequence ): #defines a experiment
       self.temperatures = temperatures
       self.pulse_sequence = pulse_sequence
       self.name = name
       self.waiting_time = waiting_time
       self.device=device

    def create_experiment_file(self, name):
        dir_path = dir_location +  "\\"  + "{}".format(dir_name)+ "\\" + "{}".format("Experiments")
        file_path = os.path.join(dir_path, name)
        if not os.path.exists("{}".format(dir_location + "\\" + "{}".format(dir_name))+ "\\" +"{}".format("Experiments")): #ATENÇÂO COM A LOCALIZAÇÂO DO DIRETORIO, VER NO PC DO LAB
           os.makedirs("{}".format(dir_location +"\\" + "{}".format(dir_name))+ "\\" + "{}".format("Experiments"))
        file = open(file_path, "w")
        file.write("{}".format(self.name)+"\n")
        file.write("{}".format(self.device+"\n"))
        file.write("{}".format(self.temperatures)+"\n")
        file.write("{}".format(self.waiting_time)+"\n")
        file.write("{}".format(self.pulse_sequence)+"\n")
        file.close()

    def read_experiment_file():
        file = open("{}".format(dir_location + "\\"  + "{}".format(dir_name))+ "\\" + "{}".format("Experiments"), "r")
        file_content = [l.rstrip("\n") for l in file.readlines()] #returns a list with each line of the file
        return file_content
    
def file_to_experiment(name):
    file = open("{}".format(dir_location + "\\"  + "{}".format(dir_name))+ "\\" + "{}".format("Experiments") + "\\" + "{}".format(name), "r")
    file_content = [l.rstrip("\n") for l in file.readlines()]
    name = file_content[0]
    device = file_content[1]
    temps_str = file_content[2].replace("][","],[") #converting the string in list
    temps = ast.literal_eval(temps_str) #converting the string in list
    waiting_time = ast.literal_eval(file_content[3])
    pulse_sequence = ast.literal_eval(file_content[4])
    experiment = Experiment(name, device, temps, waiting_time, pulse_sequence)
    return experiment   

def gen_application_path(name):
    path = dir_location + "\\"  + "Applications" + "\\" + "{}".format(name)
    return path


