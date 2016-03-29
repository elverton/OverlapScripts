from sys import argv
from config.process_config import LIMIT, database_dir, INTERVAL
import subprocess
from time import sleep


if(len(argv) == 1):
    print "python process_all.py"

nodes = [x.strip() for x in open(database_dir+"/nodelist.txt","r") if x.find("#") == -1] 

active_processes = list()
selector = lambda x: x.poll() == None

node_count = 0
total_nodes = len(nodes)
while (nodes or active_processes):

    while (len(nodes) > 0) and (len(active_processes) < LIMIT):
        node = nodes.pop(0)
        new_process = subprocess.Popen(["python","process_node.py",node])
        if(new_process):
            active_processes.append(new_process)
            print "Processing (" + str(node_count) + "/" + \
                str(total_nodes) + "): " + node + " | PID "+str(new_process.pid)
        else:
            print "Problem in " + node
        node_count += 1

    sleep(INTERVAL)
    active_processes = filter(selector, active_processes)
