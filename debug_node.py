from config import process_config
from utils import execution, statistical,tests
from sys import argv,exit
from os.path import exists
from os import makedirs

node = argv[1]

output_file = "/mnt/data2/elverton/TopoMap/experiments/"+\
    "processed/20160127_consider_lb/" +\
    "intersections_with_changes." + node

infos = dict()
infos["database_dir"] = process_config.database_dir
infos["node"] = node

ids = ""
if(len(argv) > 2):
    ids = argv[2].replace(","," ")

for line in open(output_file,"r"):
    line = line.strip()
    if(ids):
        if(line.find(ids) != -1):
            tests.test_output(line,infos)
    else:
        tests.test_output(line,infos)
