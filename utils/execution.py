from os import listdir
from sys import exit
import read
import path
import statistical
from os.path import exists
from collections import defaultdict

# --------------------------------------------------------------- #
def get_ids_by_dst(paths_by_id):
    ids_by_dst = defaultdict(lambda: list())
    for id_,path in paths_by_id.items():
        ids_by_dst[path["dst"]].append(id_)

    for dst,ids in ids_by_dst.items():
        ids.sort()
    return ids_by_dst

    
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
    o1 = open(infos["output_dir"]+"/detection_overlaps." +\
            infos["node"],"w")
    o1.close()

    o2 = open(infos["output_dir"]+"/log_ids."+\
            infos["node"],"w")

    ids_by_dst = get_ids_by_dst(paths_by_id)

    detection_ids = detections_by_id.keys()
    detection_ids.sort()
    for detection_id in detection_ids:
        detection = detections_by_id[detection_id]
        
        print >> o2, detection_id

        if(detection["changes_old"] == []):
            continue
        
        try: 
            statistical.statistical(detection, paths_by_id, ids_by_dst, infos)
        except Exception as exception:
            print >> infos["log"], "execution problem ", detection_id, exception


    o2.close()
# --------------------------------------------------------------- #

