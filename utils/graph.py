from os import listdir
from collections import defaultdict
import path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import sys
import evaluation
import statistical
import tests
import read

# ----------------------------------------------------------------- #
def transform_interval(intersect):
    if(intersect <= 0.201 and intersect > 0.0):
        return 0
    elif(intersect <= 0.401 and intersect > 0.201):
        return 1
    elif(intersect <= 0.601 and intersect > 0.401):
        return 2
    elif(intersect <= 0.801 and intersect > 0.601):
        return 3
    elif(intersect <= 1.001 and intersect > 0.801):
        return 4

    return 10

# ---------------------------------------------------------------- #
"""
The goal of this graph is to know better how the overlapping route
LCZs fits in a intersection
"""
def graph_cdf_changed_overlap_cut_bj(infos):
    
    intersectionpp_files = [x for x in listdir(infos["output_dir"])
        if x.find("intersections_with") != -1]

    intersect_num = 0
    changed_overlap = list()
   
    print "graph_cdf_changed_overlap_cut_bj"
    for f in intersectionpp_files:
        
        print f
        infos["node"] = f.split(".",1)[1]
        out_ids_intersect = open("ids/ids_cdf_changed_overlap_cut_bj."+infos["node"] ,"w")
        
        for line in open(infos["output_dir"]+"/"+f,"r"):

            line_parts = line.split(" ")

            overlap_oldpath = path.path_fromstr(line_parts[7])
            overlap_newpath = path.path_fromstr(line_parts[11])

            lczs_detection_old = [path.hops_fromstr(x.split(";")[0]) \
                    for x in line_parts[3].split("#")]
           
            intersections = [x.split(";")[2] \
                    for x in line_parts[3].split("#") ]

            overlap_changes_old_str = line_parts[13]
            overlap_changes_new_str = line_parts[15]

            overlap_changes_old = []
            overlap_changes_new = []
            if overlap_changes_old_str != "empty":
                overlap_changes_old = [x.strip(",").split(",") for x in \
                    overlap_changes_old_str.split("#") if x]
                overlap_changes_new = [x.strip(",").split(",") for x in \
                    overlap_changes_new_str.split("#") if x]


            statistical.fix_branch_join(overlap_oldpath,overlap_newpath,\
                    overlap_changes_old, overlap_changes_new)
           
            for j,intersection in enumerate(intersections):
                lcz_detection_old = lczs_detection_old[j]
                
                branch_detection = lcz_detection_old[0]
                join_detection = lcz_detection_old[-1]
                intersection_hops = path.hops_fromstr(intersection)

                intersection_hops = [x for x in intersection_hops \
                    if x != ["255.255.255.255"] and x != branch_detection \
                        and x != join_detection]
               
                if(not intersection_hops):
                    continue

                total_coverage = set()
                for i,change_zone_old in enumerate(overlap_changes_old):

                    change_zone_old_hops = path.path_get_subpath(overlap_oldpath,\
                        change_zone_old[1:-1])
                    coverage_change_zone = statistical.list_intersection(\
                        change_zone_old_hops, intersection_hops, ignore_lb=False)
                    
                    if(coverage_change_zone):
                        set_2 = set([",".join(x) for x in coverage_change_zone]) 
                        total_coverage |= set_2
                
                set_intersect = set([",".join(x) for x in intersection_hops]) 
                v = float(len(total_coverage)) / len(set_intersect)
                changed_overlap.append(v)
                intersect_num += 1
        
                if(v > 0):
                    print >> out_ids_intersect, ",".join(line_parts[0:3]),\
                        len(total_coverage), len(set_intersect), ">0"
                else:
                    print >> out_ids_intersect, ",".join(line_parts[0:3]),\
                        len(total_coverage), len(set_intersect), "=0"

               
        out_ids_intersect.close()

    uniq_values = list(set(changed_overlap))
    x = uniq_values
    x.sort()
    y = [changed_overlap.count(i)/float(intersect_num) for i in x]
    cdf = np.cumsum(y)

    o1 = open("dots/out_cdf_changed_overlap_cut_bj.txt","w")
    for i in range(len(x)):
        print >> o1, x[i],y[i]
    o1.close()

    o2 = open("dots/dots_cdf_changed_overlap_cut_bj.txt","w")
    for i in changed_overlap:
        print >> o2, i
    o2.close()
    
    plt.step(x,cdf, where="post")

    plt.xlabel("% of the intersect that has a LCZD",fontsize=16)
    plt.ylabel("CDF of all intersects on detections",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)
    plt.savefig('out_cdf_changed_overlap_cut_bj.pdf')
    plt.clf()

# ----------------------------------------------------------- #
"""
The goal of this graph is to know better how the overlap size have
influence into locate a change or not.
"""
def graph_prob_change_in_old_cut_bj(infos):
    
    intersectionpp_files = [x for x in listdir(infos["output_dir"])
        if x.find("intersections_with") != -1]

    intersect_num = 0
    changes_in_old = defaultdict(lambda: defaultdict(lambda: 0))
    
    print "graph_prob_change_in_old_cut_bj"
    for f in intersectionpp_files:
        
        print f
        infos["node"] = f.split(".",1)[1]
        out_ids_intersect = open("ids/ids_prob_change_in_old_cut_bj."+infos["node"] ,"w")
        
        for line in open(infos["output_dir"]+"/"+f,"r"):
            infos["node"] = f.split(".",1)[1]

            line_parts = line.split(" ")

            overlap_oldpath = path.path_fromstr(line_parts[7])
            overlap_newpath = path.path_fromstr(line_parts[11])

            lczs_detection_old = [path.hops_fromstr(x.split(";")[0]) \
                    for x in line_parts[3].split("#")]
           
            intersections = [x.split(";")[2] \
                    for x in line_parts[3].split("#") ]

            overlap_changes_old_str = line_parts[13]
            overlap_changes_new_str = line_parts[15]

            overlap_changes_old = []
            overlap_changes_new = []
            if overlap_changes_old_str != "empty":
                overlap_changes_old = [x.strip(",").split(",") for x in \
                    overlap_changes_old_str.split("#") if x]
                overlap_changes_new = [x.strip(",").split(",") for x in \
                    overlap_changes_new_str.split("#") if x]


            statistical.fix_branch_join(overlap_oldpath,overlap_newpath,\
                    overlap_changes_old,overlap_changes_new)
           
            for j,intersection in enumerate(intersections):
               
                lcz_detection_old = lczs_detection_old[j]
                
                branch_detection = lcz_detection_old[0]
                join_detection = lcz_detection_old[-1]
                intersection_hops = path.hops_fromstr(intersection)
                
                intersection_hops = [x for x in intersection_hops \
                    if x != ["255.255.255.255"] and x != branch_detection \
                        and x != join_detection]
               
                if(not intersection_hops):
                    continue

                has_change = False
                for i,change_zone_old in enumerate(overlap_changes_old):

                    change_zone_old_hops = path.path_get_subpath(overlap_oldpath,\
                        change_zone_old[1:-1])
                    coverage_change_zone = statistical.list_intersection(\
                        change_zone_old_hops, intersection_hops, ignore_lb=False)
      
                    if(coverage_change_zone):
                        has_change = True
                
                set_1 = set([",".join(x) for x in lczs_detection_old[j][1:-1]])
                set_2 = set([",".join(x) for x in intersection_hops])
                intersect = float(len(set_2)) / len(set_1)
                intersect = transform_interval(intersect)
               
                if(intersect == 10):
                    print >> out_ids_intersect, "not ok", ",".join(line_parts[0:3])
                    continue

                intersect_num += 1
                if(has_change):
                    changes_in_old[intersect]["changed"] += 1 
                    print >> out_ids_intersect, ",".join(line_parts[0:3])
                else:
                    changes_in_old[intersect]["not_changed"] += 1 

        out_ids_intersect.close()    
    
    print intersect_num
    x = changes_in_old.keys()
    x.sort()
    x = np.asarray(x)
    y = [float(changes_in_old[i]["changed"])/(changes_in_old[i]["changed"]\
        +changes_in_old[i]["not_changed"]) for i in x]

    o1 = open("dots/out_prob_change_in_old_cut_bj.txt","w")
    for i in range(len(x)):
        print >> o1, x[i],y[i]
    o1.close()

    o2 = open("dots/dots_prob_change_in_old_cut_bj.txt","w")
    for i,j in changes_in_old.items():
        print >> o2, i,j
    o2.close()
 
    bar_width = 0.35
    plt.bar(x, y, bar_width, color="#81DAF5")

    plt.xticks(x, ('1-20', '21-40', '41-60', '61-80',\
        '81-100'))

    plt.xlabel("% of all overlaps in detections",fontsize=16)
    plt.ylabel("P(change)",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.savefig('out_prob_change_cut_bj.pdf')
    plt.clf()


# ----------------------------------------------------------- #
"""
The goal of this graph is to know better how the overlapping route
LCZs fits in a intersection
"""
def graph_cdf_changed_overlap_cut_b(infos):
    
    intersectionpp_files = [x for x in listdir(infos["output_dir"])
        if x.find("intersections_with") != -1]

    intersect_num = 0
    changed_overlap = list()
   
    print "graph_cdf_changed_overlap_cut_b"
    for f in intersectionpp_files:
        
        print f
        infos["node"] = f.split(".",1)[1]
        out_ids_intersect = open("ids/ids_cdf_changed_overlap_cut_b."+infos["node"] ,"w")
        
        for line in open(infos["output_dir"]+"/"+f,"r"):

            line_parts = line.split(" ")

            overlap_oldpath = path.path_fromstr(line_parts[7])
            overlap_newpath = path.path_fromstr(line_parts[11])

            lczs_detection_old = [path.hops_fromstr(x.split(";")[0]) \
                    for x in line_parts[3].split("#")]
           
            intersections = [x.split(";")[2] \
                    for x in line_parts[3].split("#") ]

            overlap_changes_old_str = line_parts[13]
            overlap_changes_new_str = line_parts[15]

            overlap_changes_old = []
            overlap_changes_new = []
            if overlap_changes_old_str != "empty":
                overlap_changes_old = [x.strip(",").split(",") for x in \
                    overlap_changes_old_str.split("#") if x]
                overlap_changes_new = [x.strip(",").split(",") for x in \
                    overlap_changes_new_str.split("#") if x]


            statistical.fix_branch_join(overlap_oldpath,overlap_newpath,\
                    overlap_changes_old, overlap_changes_new)
           
            for j,intersection in enumerate(intersections):
                lcz_detection_old = lczs_detection_old[j]
                
                branch_detection = lcz_detection_old[0]
                join_detection = lcz_detection_old[-1]
                intersection_hops = path.hops_fromstr(intersection)

                intersection_hops = [x for x in intersection_hops \
                    if x != ["255.255.255.255"] and x != branch_detection]
                      #  and x != join_detection]
               
                if(not intersection_hops):
                    continue

                total_coverage = set()
                for i,change_zone_old in enumerate(overlap_changes_old):

                    change_zone_old_hops = path.path_get_subpath(overlap_oldpath,\
                        change_zone_old[1:-1])
                    coverage_change_zone = statistical.list_intersection(\
                        change_zone_old_hops, intersection_hops, ignore_lb=False)
                    
                    if(coverage_change_zone):
                        set_2 = set([",".join(x) for x in coverage_change_zone]) 
                        total_coverage |= set_2
                
                set_intersect = set([",".join(x) for x in intersection_hops]) 
                v = float(len(total_coverage)) / len(set_intersect)
                changed_overlap.append(v)
                intersect_num += 1
                
                if(v > 0):
                    print >> out_ids_intersect, ",".join(line_parts[0:3]),\
                        len(total_coverage), len(set_intersect), ">0"
                else:
                    print >> out_ids_intersect, ",".join(line_parts[0:3]),\
                        len(total_coverage), len(set_intersect), "=0"

        out_ids_intersect.close()

    uniq_values = list(set(changed_overlap))
    x = uniq_values
    x.sort()
    y = [changed_overlap.count(i)/float(intersect_num) for i in x]
    cdf = np.cumsum(y)

    o1 = open("dots/out_cdf_changed_overlap_cut_bj.txt","w")
    for i in range(len(x)):
        print >> o1, x[i],y[i]
    o1.close()

    o2 = open("dots/dots_cdf_changed_overlap_cut_bj.txt","w")
    for i in changed_overlap:
        print >> o2, i
    o2.close()
    
    plt.step(x,cdf, where="post")

    plt.xlabel("% of the intersect that has a LCZD",fontsize=16)
    plt.ylabel("CDF of all intersects on detections",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)
    plt.savefig('out_cdf_changed_overlap_cut_bj.pdf')
    plt.clf()

# ----------------------------------------------------------- #
"""
The goal of this graph is to know better how the overlapping route
LCZs fits in a intersection
"""
def graph_cdf_changed_overlap_only_j(infos):
    
    intersectionpp_files = [x for x in listdir(infos["output_dir"])
        if x.find("intersections_with") != -1]

    intersect_num = 0
    changed_overlap = list()
   
    print "graph_cdf_changed_overlap_only_j"
    for f in intersectionpp_files:
        
        infos["node"] = f.split(".",1)[1]
        if(infos["node"] != "planetlab-n2.wand.net.nz"):
            continue
        print f
        out_ids_intersect = open("ids/ids_cdf_changed_overlap_only_j."+infos["node"] ,"w")
        
        for line in open(infos["output_dir"]+"/"+f,"r"):

            line_parts = line.split(" ")

            overlap_oldpath = path.path_fromstr(line_parts[7])
            overlap_newpath = path.path_fromstr(line_parts[11])

            lczs_detection_old = [path.hops_fromstr(x.split(";")[0]) \
                    for x in line_parts[3].split("#")]
           
            intersections = [x.split(";")[2] \
                    for x in line_parts[3].split("#") ]

            overlap_changes_old_str = line_parts[13]
            overlap_changes_new_str = line_parts[15]

            overlap_changes_old = []
            overlap_changes_new = []
            if overlap_changes_old_str != "empty":
                overlap_changes_old = [x.strip(",").split(",") for x in \
                    overlap_changes_old_str.split("#") if x]
                overlap_changes_new = [x.strip(",").split(",") for x in \
                    overlap_changes_new_str.split("#") if x]


            statistical.fix_branch_join(overlap_oldpath,overlap_newpath,\
                    overlap_changes_old, overlap_changes_new)
           
            for j,intersection in enumerate(intersections):
                lcz_detection_old = lczs_detection_old[j]
                
                branch_detection = lcz_detection_old[0]
                join_detection = lcz_detection_old[-1]
                intersection_hops = path.hops_fromstr(intersection)

                intersection_hops = [x for x in intersection_hops if x != ["255.255.255.255"] 
                    and x == join_detection]
    
                if(not intersection_hops):
                    continue

                total_coverage = set()
                for i,change_zone_old in enumerate(overlap_changes_old):

                    change_zone_old_hops = path.path_get_subpath(overlap_oldpath,\
                        change_zone_old[1:-1])
                    coverage_change_zone = statistical.list_intersection(\
                        change_zone_old_hops, intersection_hops, ignore_lb=False)
                    
                    if(coverage_change_zone):
                        set_2 = set([",".join(x) for x in coverage_change_zone]) 
                        total_coverage |= set_2
                
                set_intersect = set([",".join(x) for x in intersection_hops]) 
                v = float(len(total_coverage)) / len(set_intersect)
                changed_overlap.append(v)
                intersect_num += 1
     
                if(v > 0):
                    print >> out_ids_intersect, ",".join(line_parts[0:3]),\
                        len(total_coverage), len(set_intersect), ">0"
                else:
                    print >> out_ids_intersect, ",".join(line_parts[0:3]),\
                        len(total_coverage), len(set_intersect), "=0"

        out_ids_intersect.close()

    uniq_values = list(set(changed_overlap))
    x = uniq_values
    x.sort()
    y = [changed_overlap.count(i)/float(intersect_num) for i in x]
    cdf = np.cumsum(y)

    o1 = open("dots/out_cdf_changed_overlap_only_j.txt","w")
    for i in range(len(x)):
        print >> o1, x[i],y[i]
    o1.close()

    o2 = open("dots/dots_cdf_changed_overlap_only_j.txt","w")
    for i in changed_overlap:
        print >> o2, i
    o2.close()
    
    plt.step(x,cdf, where="post")

    plt.xlabel("% of the intersect that has a LCZD",fontsize=16)
    plt.ylabel("CDF of all intersects on detections",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)
    plt.savefig('out_cdf_changed_overlap_only_j.pdf')
    plt.clf()




# ----------------------------------------------------------- #
"""
The goal of this graph is to know better how the overlapping route
LCZs fits in a intersection
"""
def graph_cdf_changed_overlap_only_b(infos):
    
    intersectionpp_files = [x for x in listdir(infos["output_dir"])
        if x.find("intersections_with") != -1]

    intersect_num = 0
    changed_overlap = list()
   
    print "graph_cdf_changed_overlap_only_b"
    for f in intersectionpp_files:
        
        print f
        infos["node"] = f.split(".",1)[1]
        out_ids_intersect = open("ids/ids_cdf_changed_overlap_only_b."+infos["node"] ,"w")
        
        for line in open(infos["output_dir"]+"/"+f,"r"):

            line_parts = line.split(" ")

            overlap_oldpath = path.path_fromstr(line_parts[7])
            overlap_newpath = path.path_fromstr(line_parts[11])

            lczs_detection_old = [path.hops_fromstr(x.split(";")[0]) \
                    for x in line_parts[3].split("#")]
           
            intersections = [x.split(";")[2] \
                    for x in line_parts[3].split("#") ]

            overlap_changes_old_str = line_parts[13]
            overlap_changes_new_str = line_parts[15]

            overlap_changes_old = []
            overlap_changes_new = []
            if overlap_changes_old_str != "empty":
                overlap_changes_old = [x.strip(",").split(",") for x in \
                    overlap_changes_old_str.split("#") if x]
                overlap_changes_new = [x.strip(",").split(",") for x in \
                    overlap_changes_new_str.split("#") if x]


            statistical.fix_branch_join(overlap_oldpath,overlap_newpath,\
                    overlap_changes_old, overlap_changes_new)
           
            for j,intersection in enumerate(intersections):
                lcz_detection_old = lczs_detection_old[j]
                
                branch_detection = lcz_detection_old[0]
                join_detection = lcz_detection_old[-1]
                intersection_hops = path.hops_fromstr(intersection)

                intersection_hops = [x for x in intersection_hops if x != ["255.255.255.255"] 
                    and x == branch_detection]
                      
                if(not intersection_hops):
                    continue

                total_coverage = set()
                for i,change_zone_old in enumerate(overlap_changes_old):

                    change_zone_old_hops = path.path_get_subpath(overlap_oldpath,\
                        change_zone_old[1:-1])
                    coverage_change_zone = statistical.list_intersection(\
                        change_zone_old_hops, intersection_hops, ignore_lb=False)
                    
                    if(coverage_change_zone):
                        set_2 = set([",".join(x) for x in coverage_change_zone]) 
                        total_coverage |= set_2
                
                set_intersect = set([",".join(x) for x in intersection_hops]) 
                v = float(len(total_coverage)) / len(set_intersect)
                changed_overlap.append(v)
                intersect_num += 1
                
                if(v > 0):
                    print >> out_ids_intersect, ",".join(line_parts[0:3]),\
                        len(total_coverage), len(set_intersect), ">0"
                else:
                    print >> out_ids_intersect, ",".join(line_parts[0:3]),\
                        len(total_coverage), len(set_intersect), "=0"


        out_ids_intersect.close()

    uniq_values = list(set(changed_overlap))
    x = uniq_values
    x.sort()
    y = [changed_overlap.count(i)/float(intersect_num) for i in x]
    cdf = np.cumsum(y)

    o1 = open("dots/out_cdf_changed_overlap_only_b.txt","w")
    for i in range(len(x)):
        print >> o1, x[i],y[i]
    o1.close()

    o2 = open("dots/dots_cdf_changed_overlap_only_b.txt","w")
    for i in changed_overlap:
        print >> o2, i
    o2.close()
    
    plt.step(x,cdf, where="post")

    plt.xlabel("% of the intersect that has a LCZD",fontsize=16)
    plt.ylabel("CDF of all intersects on detections",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)
    plt.savefig('out_cdf_changed_overlap_only_b.pdf')
    plt.clf()

# ----------------------------------------------------------- #
# ----------------------------------------------------------- #
"""
The goal of this graph is to know better how the overlapping route
LCZs fits in a intersection
"""
def graph_cdf_changed_overlap_only_j_add(infos):
    
    intersectionpp_files = [x for x in listdir(infos["output_dir"])
        if x.find("intersections_with") != -1]

    intersect_num = 0
    changed_overlap = list()
   
    print "graph_cdf_changed_overlap_only_j_add"
    for f in intersectionpp_files:
        
        infos["node"] = f.split(".",1)[1]
        print f
        out_ids_intersect = open("ids/ids_cdf_changed_overlap_only_j_add."+infos["node"] ,"w")
        
        for line in open(infos["output_dir"]+"/"+f,"r"):

            line_parts = line.split(" ")

            overlap_oldpath = path.path_fromstr(line_parts[7])
            overlap_newpath = path.path_fromstr(line_parts[11])

            lczs_detection_old = [path.hops_fromstr(x.split(";")[0]) \
                    for x in line_parts[3].split("#")]
           
            intersections = [x.split(";")[2] \
                    for x in line_parts[3].split("#") ]

            overlap_changes_old_str = line_parts[13]
            overlap_changes_new_str = line_parts[15]

            overlap_changes_old = []
            overlap_changes_new = []
            if overlap_changes_old_str != "empty":
                overlap_changes_old = [x.strip(",").split(",") for x in \
                    overlap_changes_old_str.split("#") if x]
                overlap_changes_new = [x.strip(",").split(",") for x in \
                    overlap_changes_new_str.split("#") if x]


            statistical.fix_branch_join(overlap_oldpath,overlap_newpath,\
                    overlap_changes_old, overlap_changes_new)
           
            for j,intersection in enumerate(intersections):
                lcz_detection_old = lczs_detection_old[j]
                
                branch_detection = lcz_detection_old[0]
                join_detection = lcz_detection_old[-1]
                intersection_hops = path.hops_fromstr(intersection)

                intersection_hops = [x for x in intersection_hops if x != ["255.255.255.255"] 
                    and x == join_detection]
               
                if(not intersection_hops):
                    continue

                total_coverage = set()
                for i,change_zone_old in enumerate(overlap_changes_old):

                    if len(change_zone_old) != 2:
                        continue

                    change_zone_old_hops = path.path_get_subpath(overlap_oldpath,\
                        change_zone_old[1:])
                    coverage_change_zone = statistical.list_intersection(\
                        change_zone_old_hops, intersection_hops, ignore_lb=False)
                    
                    if(coverage_change_zone):
                        set_2 = set([",".join(x) for x in coverage_change_zone]) 
                        total_coverage |= set_2
                
                set_intersect = set([",".join(x) for x in intersection_hops]) 
                v = float(len(total_coverage)) / len(set_intersect)
                changed_overlap.append(v)
                intersect_num += 1
                
                if(v > 0):
                    print >> out_ids_intersect, ",".join(line_parts[0:3]),\
                        len(total_coverage), len(set_intersect), ">0"
                else:
                    print >> out_ids_intersect, ",".join(line_parts[0:3]),\
                        len(total_coverage), len(set_intersect), "=0"

        out_ids_intersect.close()

    uniq_values = list(set(changed_overlap))
    x = uniq_values
    x.sort()
    y = [changed_overlap.count(i)/float(intersect_num) for i in x]
    cdf = np.cumsum(y)

    o1 = open("dots/out_cdf_changed_overlap_only_j_add.txt","w")
    for i in range(len(x)):
        print >> o1, x[i],y[i]
    o1.close()

    o2 = open("dots/dots_cdf_changed_overlap_only_j_add.txt","w")
    for i in changed_overlap:
        print >> o2, i
    o2.close()
    
    plt.step(x,cdf, where="post")

    plt.xlabel("% of the intersect that has a LCZD",fontsize=16)
    plt.ylabel("CDF of all intersects on detections",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)
    plt.savefig('out_cdf_changed_overlap_only_j_add.pdf')
    plt.clf()



# ----------------------------------------------------------- #
