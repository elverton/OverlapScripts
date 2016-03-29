import path
import read
import random
import output
from os import system
from collections import defaultdict

# ------------------------------------------------------- #
def test_output(intersection_line, infos):
    path_file = infos["database_dir"] + "/path." + infos["node"]
    detection_file = infos["database_dir"] + "/changes." + \
        infos["node"]

    intersection_line_parts = intersection_line.split(" ")
    detection_id = int(intersection_line_parts[0])
    overlap_old_id = int(intersection_line_parts[1])
    overlap_new_id = int(intersection_line_parts[2])

    detection = read.read_detection_id(detection_file,detection_id)
    overlap_old = read.read_path_id(path_file,overlap_old_id)
    overlap_new = read.read_path_id(path_file,overlap_new_id)

    for intersection in intersection_line_parts[3].split("#"):
        intersection_parts = intersection.split(";")
        detection_change_zone_old = path.hops_fromstr(intersection_parts[0])
        detection_change_zone_new = path.hops_fromstr(intersection_parts[1])
        detection_overlap_intersect = path.hops_fromstr(intersection_parts[2])
    

        print "-----------------"
        print "OVERLAP_OLD"
        if(intersection_line_parts[-4] == "empty"):
            output.output_path(overlap_old["path"],[],"red")
        else:
            output.output_path(overlap_old["path"],[int(x) for y in\
                intersection_line_parts[-4].split("#") for x in y.split(",") if x],"red")
        print "-----------------"
        print "OVERLAP_NEW"
        if(intersection_line_parts[-2] == "empty"):
            output.output_path(overlap_new["path"],[],"red")
        else:
            output.output_path(overlap_new["path"],[int(x) for y in\
                intersection_line_parts[-2].split("#") for x in y.split(",") if x],"red")
        raw_input()
        print "DETECTION_OLD"
        output.output_path(detection["oldpath"],detection_change_zone_old)
        print "-----------------"
        print "DETECTION_NEW"
        output.output_path(detection["newpath"],detection_change_zone_new)
        print "-----------------"
        print "OVERLAP_OLD INTERSECTION"
        output.output_path(overlap_old["path"],detection_change_zone_old)
        print "-----------------"
        output.output_path(detection_overlap_intersect,detection_overlap_intersect)
        raw_input()

