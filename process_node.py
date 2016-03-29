from config import process_config
from utils import execution, statistical
from sys import argv,exit
from os.path import exists
from os import makedirs

node = argv[1]

infos = dict()
infos["database_dir"] = process_config.database_dir
infos["node"] = node

if(not exists(process_config.output_dir)):
    makedirs(process_config.output_dir)
infos["output_dir"] = process_config.output_dir

infos["log"] = open(process_config.output_dir+"/log."+node,"w")
execution.execute(infos)
infos["log"].close()

