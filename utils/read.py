from os import listdir
from sys import exit
import path
from collections import defaultdict


# -------------------------------------------------------- #
def read_detection_file(detection_file):
    detections_by_id = dict()
    for line in open(detection_file,"r"):
        line_parts = line.strip().split(" ")
        id_ = int(line_parts[0].split(" ")[0])
        detections_by_id[id_] = read_detection(line.strip())

    return detections_by_id

# -------------------------------------------------------- #
def read_detection_id(detection_file, id_target):
    for line in open(detection_file,"r"):
        line_parts = line.strip().split(" ")
        id_ = int(line_parts[0].split(" ")[0])
        if(id_ == id_target):
            return read_detection(line.strip())
    return []

# -------------------------------------------------------- #
def read_path_file(paths_file):
    paths_by_id = dict()
    for line in open(paths_file,"r"):
        line_parts = line.strip().split(" ")
        id_ = int(line_parts[0])
        paths_by_id[id_] = read_path(line.strip())

    return paths_by_id

# -------------------------------------------------------- #
def read_path_id(paths_file, id_target):
    for line in open(paths_file,"r"):
        line_parts = line.strip().split(" ")
        id_ = int(line_parts[0])
        if(id_ == id_target):
            return read_path(line.strip())
    return []

# -------------------------------------------------------- #
def read_detection(detection_str):
    
    detection_tokens = detection_str.split(" ")

    changes_old = []
    if(detection_tokens[10] != "empty"):
        changes_old = [x.strip(",").split(",") for x in \
            detection_tokens[10].split("#") if x] 

    changes_new = []
    if(detection_tokens[12] != "empty"):
        changes_new = [x.strip(",").split(",") for x in \
            detection_tokens[12].split("#") if x] 

    
    overlap_dsts = []
    if(detection_tokens[5] != "empty"):
        overlap_dsts.extend(detection_tokens[5].split(","))
    if(detection_tokens[6] != "empty"):
        overlap_dsts.extend(detection_tokens[6].split(","))


    detection_info = dict()
    detection_info["id"] = int(detection_tokens[0])
    detection_info["src"] = detection_tokens[3]
    detection_info["dst"] = detection_tokens[4]
    detection_info["overlap"] = overlap_dsts
    detection_info["oldpath"] = path.path_fromstr(detection_tokens[7])
    detection_info["newpath"] = path.path_fromstr(detection_tokens[8])
    detection_info["changes_old"] = changes_old
    detection_info["changes_new"] = changes_new

    return detection_info

# -------------------------------------------------------- #

def read_path(path_str):

    path_tokens = path_str.split(" ")
    
    path_info = dict()
    path_info["id"] = int(path_tokens[0])
    path_info["from_id"] = int(path_tokens[1])
    path_info["src"] = path_tokens[4]
    path_info["dst"] = path_tokens[5]
    path_info["path"] = path.path_fromstr(path_tokens[7])

    if(len(path_info) == 9):
        path_info["tstamp"] = path_tokens[8]

    return path_info

# -------------------------------------------------------- #

def read_intersectionpp_file(intersectionpp_file):

    intersectionpp_by_ids = defaultdict(lambda: \
        defaultdict(lambda:list()))
    for line in open(intersectionpp_file,"r"):
        line = line.strip().split(" ")

        intersections = line[3].split("#")
        oldpath_overlap = path.path_fromstr(line[7])
        
        for intersection in intersections:
            old_detection,new_detection,intersect = intersection.split(";")
            # freedom_level ZERO for now. Create a function to allow others
            if(old_detection == intersect):
                hops = path.hops_fromstr(intersect)
                for hop in hops:
                    ttl = path.path_recover_ttl(oldpath_overlap,hop)
                    intersectionpp_by_ids[",".join(line[0:3])]["ttls"].append(ttl) 

    return intersectionpp_by_ids

# -------------------------------------------------------- #
# -------------------------------------------------------- #
# -------------------------------------------------------- #















