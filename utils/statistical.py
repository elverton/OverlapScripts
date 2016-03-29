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
            oldchanges[i].append(join_old)
            newchanges[i].append(join_new)

# ------------------------------------------------------------------------ #
def list_intersection(list_1, list_2, ignore_lb=False):
    intersection = list()
    
    if(ignore_lb):
        for l1 in list_1:
            set_1 = set(l1)
            for l2 in list_2:
                set_2 = set(l2)
                intersect = list(set_1.intersection(set_2))
                if(intersect):
                    intersection.append(intersect)
        return intersection
    else:
        for l1 in list_1:
            if l1 in list_2:
                intersection.append(l1)
        return intersection

# ------------------------------------------------------------------------ #
def update_ids_by_dst(ids_by_dst,dst,limiar):
    last_id = -1
    newlist = list()
    for id_ in ids_by_dst[dst]:
        if(id_ > limiar):
            newlist.append(id_)
        else:
            last_id = id_
    if(last_id != -1):
        newlist.insert(0,last_id)
    ids_by_dst[dst] = newlist

# ------------------------------------------------------------------------ #
def statistical(detection, paths_by_id, ids_by_dst, infos):

    o1 = open(infos["output_dir"]+"/intersections." + infos["node"],"a")

    fix_branch_join(detection["oldpath"],detection["newpath"],detection["changes_old"],\
        detection["changes_new"])

    """
    has_overlap = False
    for change_zone_old in detection["changes_old"]:
        if(change_zone_old[1:-1]):
            has_overlap = True

    if(not has_overlap):
        return
    """

    detection_oldpath = detection["oldpath"]
    detection_newpath = detection["newpath"]

    limiar = detection["id"]
    dst_overlap_set = set()
    
    for dst in detection["overlap"]: 

        update_ids_by_dst(ids_by_dst, dst, limiar)
        
        if(dst not in ids_by_dst or len(ids_by_dst[dst]) < 2):
            print >> infos["log"], detection["id"],\
                "dst " + dst + " does not have old or new path!" 
            continue
     
        if(ids_by_dst[dst][0] > detection["id"]):
            print >> infos["log"], detection["id"], \
            ",".join([str(x) for x in ids_by_dst[dst]]),\
                "dst do not have an oldpath"
            continue
        overlap_oldpath = paths_by_id[ids_by_dst[dst][0]]["path"]
        overlap_newpath = paths_by_id[ids_by_dst[dst][1]]["path"]
        
        output_str = str(detection["id"]) + " "
        output_str += str(ids_by_dst[dst][0]) + " "
        output_str += str(ids_by_dst[dst][1]) + " "

        has_intersection = False
        for change_zone_id,change_zone_old in enumerate(detection["changes_old"]):

            change_zone_new = detection["changes_new"][change_zone_id]

            # TODO ignoring branch and join
            detection_oldpath_subpath = path.path_get_subpath(detection_oldpath,\
                    change_zone_old)
            detection_newpath_subpath = path.path_get_subpath(detection_newpath,\
                    change_zone_new)
           
            intersection = list_intersection(overlap_oldpath,\
                    detection_oldpath_subpath)

            intersection = [x for x in intersection if x != ["255.255.255.255"]]
            if(intersection):
                dst_overlap_set.add(dst + ";" + str(ids_by_dst[dst][1]))
                has_intersection = True
    
            output_str += path.hops_tostr(detection_oldpath_subpath) + ";"
            output_str += path.hops_tostr(detection_newpath_subpath) + ";"
            
            output_str += path.hops_tostr(intersection) + "#"

        if(not has_intersection):
            print >> infos["log"],detection["id"],\
                ids_by_dst[dst][0],\
                ids_by_dst[dst][1],\
                " does not have an intersection"
            continue

        src_overlap = paths_by_id[ids_by_dst[dst][0]]["src"] 
        dst_overlap = paths_by_id[ids_by_dst[dst][0]]["dst"] 
        prefix = src_overlap + " " + dst_overlap + " 1 "
        output_str = output_str.strip("#") + " "
        output_str += prefix + path.path_tostr(overlap_oldpath) + " "
        output_str += prefix + path.path_tostr(overlap_newpath) 

        print >> o1, output_str

    o1.close()

    o2 = open(infos["output_dir"]+"/detection_overlaps." + infos["node"],"a")
    print >> o2, detection["id"], ",".join(list(dst_overlap_set)) 
    o2.close()
# -------------------------------------------------------- #

