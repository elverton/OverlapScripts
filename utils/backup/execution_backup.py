from os import listdir
from sys import exit
import read
import path
import statistical
from os.path import exists

# --------------------------------------------------------------- #
def execute(infos):

    path_file = infos["database_dir"] + "/path." + infos["node"]
    detection_file = infos["database_dir"] + "/changes." + infos["node"]
    
    paths_by_id = read.read_path_file(path_file)
    detections_by_id = read.read_detection_file(detection_file)
    
    global_correct = 0
    global_incorrect = 0

    o1 = open(infos["output_dir"]+"/intersections." +\
            infos["node"],"w")
    o1.close()

    o2 = open(infos["output_dir"]+"/log_ids."+\
            infos["node"],"w")

    for detection_id,detection in detections_by_id.items():
        print >> o2, detection_id

        if(detection["changes_old"] == []):
            continue
        try: 
            correct,incorrect = statistical.statistical(\
                detection, paths_by_id, infos)
        except:
            print >> infos["log"], "execution problem ", detection_id

        global_correct += correct
        global_incorrect += incorrect 

    o2.close()
    print >> infos["log"], "FINAL"
    print >> infos["log"], global_correct, global_incorrect
# --------------------------------------------------------------- #

