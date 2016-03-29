from os import listdir
from sys import exit
import path
import read
import detection as u_detection

# ------------------------------------------------------------------------ #
def fix_branch_join(oldpath,newpath,oldchanges,newchanges):

    for i,change_zone in enumerate(oldchanges):
        branch_old = int(oldchanges[i][0])   
        branch_new = int(newchanges[i][0])   
        if(branch_old < 0 or branch_new < 0):
            break
        while(oldpath[branch_old] != newpath[branch_new]):
            branch_old -= 1                      
            branch_new -= 1                      
            if(branch_old < 0 or branch_new < 0):
                break
            oldchanges[i].insert(0,str(branch_old))
            newchanges[i].insert(0,str(branch_new))

    len_oldpath = len(oldpath)                  
    len_newpath = len(newpath)                  
    for i,change_zone in enumerate(oldchanges): 
        join_old = int(oldchanges[i][-1])                      
        join_new = int(newchanges[i][-1])                      
        if(join_old >= len_oldpath or join_new >= len_newpath):
            break
        while(oldpath[join_old] != newpath[join_new]):
            join_old += 1                                          
            join_new += 1                                          
            if(join_old >= len_oldpath or join_new >= len_newpath):
                break
            oldchanges[i].insert(0,str(branch_old))
            newchanges[i].insert(0,str(branch_new))

# ------------------------------------------------------------------------ #
def list_intersection(list_1, list_2):
    intersection = list()
    for x in list_1:
        if x in list_2:
            intersection.append(x)
    return intersection

# ------------------------------------------------------------------------ #
def get_oldpath(dict_1, limiar):
   
    keys_sorted = dict_1.keys()
    keys_sorted.sort()

    keys_valid = [x for x in keys_sorted if x < limiar]
    keys_valid.reverse()

    paths_old = dict()
    for key_valid in keys_valid:
        dst = dict_1[key_valid]["dst"]
        if dst not in paths_old:
            paths_old[dst] = dict_1[key_valid]

    return paths_old

# ------------------------------------------------------------------------ #
def get_newpath(dict_1, limiar):
    
    keys_sorted = dict_1.keys() 
    keys_sorted.sort()          

    keys_valid = [x for x in keys_sorted if x > limiar]

    paths_new = dict()
    for key_valid in keys_valid:
        dst = dict_1[key_valid]["dst"]
        if dst not in paths_new:
            paths_new[dst] = dict_1[key_valid]

    return paths_new

# ------------------------------------------------------------------------ #
def statistical(detection, paths_by_id, infos):

    correct = 0
    incorrect = 0

    o1 = open(infos["output_dir"]+"/intersections." + infos["node"],"a")

    fix_branch_join(detection["oldpath"],detection["newpath"],detection["changes_old"],\
        detection["changes_new"])

    detection_oldpath = detection["oldpath"]
    detection_newpath = detection["newpath"]

    paths_old = get_oldpath(paths_by_id, detection["id"])
    paths_new = get_newpath(paths_by_id, detection["id"])

    for dst in detection["overlap"]: 

        if(dst not in paths_old or dst not in paths_new):
            print >> infos["log"], detection["id"],\
                "dst " + dst + " not present!" 
            continue
        
        overlap_oldpath = paths_old[dst]["path"]
        overlap_newpath = paths_new[dst]["path"]
        
        output_str = str(detection["id"]) + " "
        output_str += str(paths_old[dst]["id"]) + " "
        output_str += str(paths_new[dst]["id"]) + " "

        has_intersection = False
        for change_zone_id,change_zone_old in enumerate(detection["changes_old"]):

            change_zone_new = detection["changes_new"][change_zone_id]

            detection_oldpath_subpath = path.path_get_subpath(detection_oldpath,\
                    change_zone_old)
            detection_newpath_subpath = path.path_get_subpath(detection_newpath,\
                    change_zone_new)
           
            intersection = list_intersection(overlap_oldpath,\
                    detection_oldpath_subpath)

            intersection = [x for x in intersection if x != ["255.255.255.255"]]
            if(intersection):
                has_intersection = True

            output_str += path.hops_tostr(detection_oldpath_subpath) + ";"
            output_str += path.hops_tostr(detection_newpath_subpath) + ";"

            output_str += path.hops_tostr(intersection) + "#"

        if(not has_intersection):
            print >> infos["log"],detection["id"],\
                paths_old[dst]["id"],\
                paths_new[dst]["id"],\
                " does not have an intersection"
            continue

        prefix = "1.1.1.1 2.2.2.2 1 "
        output_str = output_str.strip("#") + " "
        output_str += prefix + path.path_tostr(paths_old[dst]["path"]) + " "
        output_str += prefix + path.path_tostr(paths_new[dst]["path"]) 

        print >> o1, output_str

    return correct,incorrect

# -------------------------------------------------------- #

