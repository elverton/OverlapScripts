from os import listdir,system
from sys import exit
from termcolor import colored
import path


# -------------------------------------------------------- #
def output_path(path, to_color=[], color="green"):

    for i,hop in enumerate(path):
        hops_ips_str = " -- ".join(hop) 
        if(hop in to_color or i in to_color):
            print i,colored(hops_ips_str,color)
        else:
            print i,hops_ips_str

# -------------------------------------------------------- #

