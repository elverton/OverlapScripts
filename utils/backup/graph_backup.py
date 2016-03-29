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

# ---------------------------------------------------------------- #
"""
The goal of this graph is to show where the LCZ of changed routes that
intersect a detection are located and where the detections have more 
coverage in these LCZs.
The first result shows that the LCZs are likely to be in any part of
the path but the detections have a better coverage on LCZs that are on
the beginning of the path.
"""
def graph_cumulative_bins(infos):
    
    evaluation_2_files = [x for x in listdir(infos["output_dir"])
        if x.find("evaluation_2") != -1]

    cumulative_lcz = 10*[0]
    coverage_lcz = 10*[0]
    for f in evaluation_2_files:
        print f
        for line in open(infos["output_dir"]+"/"+f,"r"):
            line = line.strip().split(" ")
            bins = [int(x) for x in line[-1].split(",")]
            for i,b in enumerate(bins):
                if(b == 1 or b == 2):
                    cumulative_lcz[i] += 1
                if(b == 2):
                    coverage_lcz[i] += 1

    x = np.arange(10)
    y = [z for z in cumulative_lcz]

    bar_width = 0.35
    plt.bar(x, y, bar_width,label='changed routes that intersect\na detection',color="#2E64FE")

    x = np.arange(10)
    y = [z for z in coverage_lcz]

    plt.bar(x+bar_width, y, bar_width,label='changed routes that intersect\na detection' +\
        ' and\nhave a coverage', color="#81DAF5")

    plt.xticks(x+bar_width, ('0-10', '10-20', '20-30', '30-40',\
        '40-50','50-60','60-70','70-80','80-90','90-100'))
    plt.xlabel('path range (%)')
    plt.ylabel('# of overlapping changed routes')

    plt.legend(bbox_to_anchor=(1.1, 1.05))
    plt.savefig('out_bins.pdf')
    plt.clf()

# ---------------------------------------------------------------- #
"""
The goal of this graph is to show the size of the LCZ of the 
overlapping changed routes in detections. We need this to better
understand the problem.
"""
def graph_generate_cdf_lcz_size(infos):
    
    evaluation_2_files = [x for x in listdir(infos["output_dir"])
        if x.find("evaluation_2") != -1]
    covered_dist = defaultdict(lambda: 0)
    uncovered_dist = defaultdict(lambda: 0)
    all_dist = defaultdict(lambda: 0)
    
    covered_number = 0
    uncovered_number = 0
    all_number = 0

    for f in evaluation_2_files:
        print f
        for line in open(infos["output_dir"]+"/"+f,"r"):
            line = line.strip().split(" ")
            if(line[3] == "0,0"):
                continue
            lcz_stats = line[3].split(";")
            lcz_ttls = line[4].split(";")
            for i,stat in enumerate(lcz_stats):
                lcz_size,lcz_intersect = stat.split(",")
                lcz_size = int(lcz_size)
                lcz_intersect = int(lcz_intersect)
                if(lcz_intersect > 0):
                    covered_dist[lcz_size] += 1
                    covered_number += 1
                else:
                    uncovered_dist[lcz_size] += 1
                    uncovered_number += 1
                all_dist[lcz_size] += 1
                all_number += 1
    
    x = [z for z in covered_dist.keys()]
    x.sort()
    y = [covered_dist[i]/float(covered_number) for i in x]
    cdf = np.cumsum(y)

    plt.step(x,cdf,label="covered LCZ", where="post")

    x = [z for z in uncovered_dist.keys()]
    x.sort()
    y = [uncovered_dist[i]/float(uncovered_number) for i in x]
    cdf = np.cumsum(y)
    
    plt.step(x,cdf,label="uncovered LCZ", where="post")
    
    x = [z for z in all_dist.keys()]
    x.sort()
    y = [all_dist[i]/float(all_number) for i in x]
    cdf = np.cumsum(y)
    
    plt.step(x,cdf,linestyle="--",label="all LCZ", where="post")


    plt.xlabel("LCZ Size",fontsize=16)
    plt.ylabel("CDF of LCZ in overlapping changed routes",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.legend(loc='lower right')
    plt.savefig('out_cdf_lcz_size.pdf')
    plt.clf()

# ---------------------------------------------------------------- #
"""
This graph has the goal to calculate the distance of the LCZs of
overlapping changed routes in detection from beginning. We separate
the LCZs in two groups: one that has, at least, one intersection with
detection and another with no intersection. 
"""
def graph_cdf_lcz_distance_from_start(infos):
    
    evaluation_2_files = [x for x in listdir(infos["output_dir"])
        if x.find("evaluation_2") != -1]
    covered_dist = defaultdict(lambda: 0)
    uncovered_dist = defaultdict(lambda: 0)
    all_dist = defaultdict(lambda: 0)

    covered_number = 0
    uncovered_number = 0
    all_number = 0
    for f in evaluation_2_files:
        print f
        for line in open(infos["output_dir"]+"/"+f,"r"):
            line = line.strip().split(" ")
            if(line[3] == "0,0"):
                continue
            lcz_stats = line[3].split(";")
            lcz_ttls = [x.split(",") for x in line[4].split(";")]
            for i,stat in enumerate(lcz_stats):
                lcz_size,lcz_intersect = stat.split(",")
                lcz_size = int(lcz_size)
                lcz_intersect = int(lcz_intersect)
                distance = int(lcz_ttls[i][0])
                if(lcz_intersect > 0):
                    covered_dist[distance] += 1
                    covered_number += 1
                else:
                    uncovered_dist[distance] += 1
                    uncovered_number += 1
                all_dist[distance] += 1
                all_number += 1
    
    x = [z for z in covered_dist.keys()]
    x.sort()
    y = [covered_dist[i]/float(covered_number) for i in x]
    cdf = np.cumsum(y)

    plt.step(x,cdf,label="covered LCZ", where="post")

    x = [z for z in uncovered_dist.keys()]
    x.sort()
    y = [uncovered_dist[i]/float(uncovered_number) for i in x]
    cdf = np.cumsum(y)
    
    plt.step(x,cdf,label="uncovered LCZ", where="post")

    x = [z for z in all_dist.keys()]
    x.sort()
    y = [all_dist[i]/float(all_number) for i in x]
    cdf = np.cumsum(y)
    
    plt.step(x,cdf,linestyle="--",label="all LCZ", where="post")

    plt.xlabel("# hops from source",fontsize=16)
    plt.ylabel("CDF of LCZ in overlapping changed routes",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.legend(loc='lower right')
    plt.savefig('out_cdf_distance_from_start.pdf')
    plt.clf()

# ---------------------------------------------------------------- #
"""
This graph has the goal to calculate the distance of the LCZs of
overlapping changed routes in detection from end. We separate
the LCZs in two groups: one that has, at least, one intersection with
detection and another with no intersection. 
"""

def graph_cdf_lcz_distance_from_end(infos):
    
    evaluation_2_files = [x for x in listdir(infos["output_dir"])
        if x.find("evaluation_2") != -1]
    covered_dist = defaultdict(lambda: 0)
    uncovered_dist = defaultdict(lambda: 0)
    all_dist = defaultdict(lambda: 0)

    covered_number = 0
    uncovered_number = 0
    all_number = 0
    for f in evaluation_2_files:
        print f
        for line in open(infos["output_dir"]+"/"+f,"r"):
            line = line.strip().split(" ")
            if(line[3] == "0,0"):
                continue
            lcz_stats = line[3].split(";")
            lcz_ttls = [x.split(",") for x in line[4].split(";")]
            path_length = int(line[6])
            for i,stat in enumerate(lcz_stats):
                lcz_size,lcz_intersect = stat.split(",")
                lcz_size = int(lcz_size)
                lcz_intersect = int(lcz_intersect)
                distance = path_length - int(lcz_ttls[i][-1])
                if(lcz_intersect > 0):
                    covered_dist[distance] += 1
                    covered_number += 1
                else:
                    uncovered_dist[distance] += 1
                    uncovered_number += 1
                all_dist[distance] += 1
                all_number += 1

    x = [z for z in covered_dist.keys()]
    x.sort()
    y = [covered_dist[i]/float(covered_number) for i in x]
    cdf = np.cumsum(y)

    plt.step(x,cdf,label="covered LCZ", where="post")

    x = [z for z in uncovered_dist.keys()]
    x.sort()
    y = [uncovered_dist[i]/float(uncovered_number) for i in x]
    cdf = np.cumsum(y)
    
    plt.step(x,cdf,label="uncovered LCZ", where="post")

    x = [z for z in all_dist.keys()]
    x.sort()
    y = [all_dist[i]/float(all_number) for i in x]
    cdf = np.cumsum(y)
    
    plt.step(x,cdf,linestyle="--",label="all LCZ", where="post")

    plt.xlabel("# hops from end",fontsize=16)
    plt.ylabel("CDF of all LCZ in overlapping changed routes",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.legend(loc='lower right')
    plt.savefig('out_cdf_distance_from_end.pdf')
    plt.clf()

# ---------------------------------------------------------------- #
# ---------------------------------------------------------------- #
"""
Just basis statistics to get an overview of the database.
"""
def graph_generate_basic(infos):
    
    evaluation_2_files = [x for x in listdir(infos["output_dir"])
        if x.find("evaluation_2") != -1]

    number_of_detections = 0
    number_of_intersects = 0
    number_of_lcz_in_intersects = 0 
    size_of_lcz = defaultdict(lambda: 0)
    
    for f in evaluation_2_files:
        uniq_detections = set()
        for line in open(infos["output_dir"]+"/"+f,"r"):
            
            number_of_intersects += 1
            
            line_parts = line.strip().split(" ")
            uniq_detections.add(line_parts[0])
            if(line_parts[3] == "0,0"):
                continue
            for lcz_info in line_parts[3].split(";"):
                lcz_size,lcz_coverage = lcz_info.split(",")
                lcz_size = int(lcz_size)
                size_of_lcz[lcz_size] += 1
                number_of_lcz_in_intersects += 1
        
        number_of_detections += len(uniq_detections)
    
    print "number_of_intersects: ",number_of_intersects
    print "number_of_detections: ",number_of_detections
    print "number_of_lcz_in_intersects: ", number_of_lcz_in_intersects

    x = [z for z in size_of_lcz.keys()]
    x.sort()
    y = [size_of_lcz[i]/float(number_of_lcz_in_intersects)\
        for i in x]
    cdf = np.cumsum(y)

    plt.step(x,cdf,label="CDF of LCZ size", where="post")

    plt.xlabel("LCZ size",fontsize=16)
    plt.ylabel("CDF of all LCZ in overlapping changed routes",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.legend(loc='lower right')
    plt.savefig('basic_1.pdf')
    plt.clf()

    uniq_size_of_lcz = defaultdict(lambda: 0)
    uniq_number_of_lcz_in_intersects = 0
    uniq_number_of_intersects = 0
    for f in evaluation_2_files:
        overlap_change_ids = set()
        for line in open(infos["output_dir"]+"/"+f,"r"):
            

            line_parts = line.strip().split(" ")
            overlap_change_id = line_parts[1] + " " + line_parts[2]
            if overlap_change_id in overlap_change_ids:
                continue
            overlap_change_ids.add(overlap_change_id)
            
            uniq_number_of_intersects += 1
            if(line_parts[3] == "0,0"):
                continue
            
            for lcz_info in line_parts[3].split(";"):
                if(not lcz_info):
                    continue
                lcz_size,lcz_coverage = lcz_info.split(",")
                lcz_size = int(lcz_size)
                uniq_size_of_lcz[lcz_size] += 1
                uniq_number_of_lcz_in_intersects += 1
    
    print "uniq_number_of_lcz_in_intersects", uniq_number_of_lcz_in_intersects
    print "uniq_number_of_intersects", uniq_number_of_intersects
    x = [z for z in uniq_size_of_lcz.keys()]
    x.sort()
    y = [uniq_size_of_lcz[i]/float(uniq_number_of_lcz_in_intersects)\
        for i in x]
    cdf = np.cumsum(y)

    plt.step(x,cdf,label="CDF of LCZ size", where="post")

    plt.xlabel("LCZ size",fontsize=16)
    plt.ylabel("CDF of all uniq LCZ in overlapping changed routes",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.legend(loc='lower right')
    plt.savefig('basic_2.pdf')
    plt.clf()


# ---------------------------------------------------------------- #
"""
The goal of this graph is to know better the intersection between
detection and the routes overlapping its LCZs.
"""
def graph_cdf_lcz_intersect_relation(infos):
    
    intersectionpp_files = [x for x in listdir(infos["output_dir"])
        if x.find("intersectionspp") != -1]

    relation = list()
    intersect_null = 0
    for f in intersectionpp_files:
        print f
        for line in open(infos["output_dir"]+"/"+f,"r"):
            
            line_parts = line.split(" ")
            for lcz in line_parts[3].split("#"):
                lcz_old, lcz_new, intersect = lcz.split(";")
                if(intersect == ""):
                    intersect_null += 1
                    continue
                lcz_old = set([",".join(x) for x in path.hops_fromstr(lcz_old)]) 
                intersect = set([",".join(x) for x in path.hops_fromstr(intersect)]) 
                lcz_old -= set(["255.255.255.255"])
                intersect -= set(["255.255.255.255"])
                len_lcz_old = len(lcz_old)
                len_lcz_intersect = len(intersect)
                relation.append(float(len_lcz_intersect)/len_lcz_old)

    total_values = float(len(relation))
    uniq_values = list(set(relation))
    uniq_values.sort()
    x = uniq_values
    y = [relation.count(i)/total_values for i in x]
    cdf = np.cumsum(y)

    plt.step(x,cdf, where="post")

    plt.xlabel("intersect_size/detection_lcz_old",fontsize=16)
    plt.ylabel("CDF of all overlap between detection and routes",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)
    plt.savefig('out_lcz_intersect_relation.pdf')
    plt.clf()

# ---------------------------------------------------------------- #
"""
The goal of this graph is to know better how the intersection between
detection and the routes overlapping its LCZs can help we send probes
smartly.
"""
def graph_cdf_lcz_intersect_jaccard(infos):
    
    intersectionpp_files = [x for x in listdir(infos["output_dir"])
        if x.find("intersectionspp") != -1]

    relation = list()
    intersect_null = 0
    jaccard_indexes = list()

    for f in intersectionpp_files:
        print f
        for line in open(infos["output_dir"]+"/"+f,"r"):
            infos["node"] = f.split(".",1)[1]

            line_parts = line.split(" ")

            overlap_oldpath = path.path_fromstr(line_parts[7])
            overlap_newpath = path.path_fromstr(line_parts[11])

            lczs_detection_new = [path.hops_fromstr(x.split(";")[1]) \
                    for x in line_parts[3].split("#")]
           
            intersections = [x.split(";")[2] \
                    for x in line_parts[3].split("#")]

            changes_old_str = line_parts[13]
            changes_new_str = line_parts[15]

            changes_old = []
            changes_new = []
            if changes_old_str != "empty":
                changes_old = [x.strip(",").split(",") for x in \
                    changes_old_str.split("#") if x]
                changes_new = [x.strip(",").split(",") for x in \
                    changes_new_str.split("#") if x]
            else:
                continue

            statistical.fix_branch_join(overlap_oldpath,overlap_newpath,\
                    changes_old,changes_new)

            for i,change_zone_old in enumerate(changes_old):
                change_zone_new = changes_new[i]

                change_zone_old_hops = path.path_get_subpath(overlap_oldpath,\
                    change_zone_old)
                change_zone_new_hops = path.path_get_subpath(overlap_newpath,\
                    change_zone_new)

                for j,intersection in enumerate(intersections):

                    intersection_hops = path.hops_fromstr(intersection)
                    coverage_change_zone_old = statistical.list_intersection(\
                        change_zone_old_hops,intersection_hops)
                    # stars does not make intersections
                    coverage_change_zone = [x for x in coverage_change_zone_old \
                        if x != ["255.255.255.255"]]
                    if(coverage_change_zone):
                        
                        set_1 = set([",".join(x) for x in change_zone_new_hops])
                        set_2 = set([",".join(x) for x in lczs_detection_new[j]])
                        intersection = len(set_1.intersection(set_2))
                        union = len(set_1.union(set_2))
                        jaccard_indexes.append(float(intersection)/union)
   
    total_values = float(len(jaccard_indexes))
    uniq_values = list(set(jaccard_indexes))
    uniq_values.sort()
    x = uniq_values
    y = [jaccard_indexes.count(i)/total_values for i in x]
    cdf = np.cumsum(y)

    plt.step(x,cdf, where="post")

    plt.xlabel("jaccard index (detection new, overlap new)",fontsize=16)
    plt.ylabel("CDF of all LCZ in overlapping changed routes\nthat intersect "+\
        "detection",fontsize=12)

    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)
    plt.savefig('out_lcz_jaccard22.pdf')
    plt.clf()


# ---------------------------------------------------------------- #
"""
The goal of this graph is to show how many lczs exists on overlapping
changed routes in detections.
"""
def graph_cdf_lcz_number(infos):
    
    evaluation_2_files = [x for x in listdir(infos["output_dir"])
        if x.find("evaluation_2") != -1]

    all_dist = defaultdict(lambda: 0)
    covered_dist = defaultdict(lambda: 0)
    uncovered_dist = defaultdict(lambda: 0)

    all_dist_number = 0
    covered_dist_number = 0
    uncovered_dist_number = 0
    for f in evaluation_2_files:
        print f
        for line in open(infos["output_dir"]+"/"+f,"r"):
            line = line.strip().split(" ")
            if(line[3] == "0,0"):
                continue
            lcz_stats = line[3].split(";")
            all_dist[len(lcz_stats)] += 1        
            all_dist_number += 1
            has_coverage = False
            for stat in lcz_stats:
                lcz_size,lcz_coverage = stat.split(",")
                lcz_coverage = int(lcz_coverage)
                if(lcz_coverage > 0):
                    has_coverage = True
            if(has_coverage):
                covered_dist[len(lcz_size)] += 1
                covered_dist_number += 1
            else:
                uncovered_dist[len(lcz_size)] += 1
                uncovered_dist_number += 1

    bar_width = 0.25
    x = [z for z in all_dist.keys()]
    x.sort()
    x = np.asarray(x)
    y = [all_dist[i]/float(all_dist_number) for i in x]

    plt.bar(x, y, bar_width,label="all routes",color="#000066")

    x = [z for z in covered_dist.keys()]
    x.sort()
    x = np.asarray(x)
    y = [covered_dist[i]/float(all_dist_number) for i in x]

    plt.bar(x+bar_width, y, bar_width, label="covered routes", color="#3366ff")
    
    x = [z for z in uncovered_dist.keys()]
    x.sort()
    x = np.asarray(x)
    y = [uncovered_dist[i]/float(all_dist_number) for i in x]

    plt.bar(x+2*bar_width, y, bar_width, label="uncovered routes", color="#33ccff")

    plt.xlabel("# of LCZs",fontsize=16)
    plt.ylabel("% of all overlapping changed routes",fontsize=16)

    plt.legend(loc='upper right')
    plt.savefig('out_cdf_lcz_number.pdf')
    plt.clf()

# ---------------------------------------------------------------- #
"""
Worth send probes to changed overlapping routes?
"""

def graph_cdf_route_coverage(infos):
    
    evaluation_2_files = [x for x in listdir(infos["output_dir"])
        if x.find("evaluation_2") != -1]
    all_dist = list()

    all_number = 0
    routes_num = 0
    for f in evaluation_2_files:
        print f
        for line in open(infos["output_dir"]+"/"+f,"r"):
            line = line.strip().split(" ")
            if(line[3] == "0,0"):
                #all_dist.append(1.0)
                continue
            routes_num += 1
            lcz_stats = line[3].split(";")
           
            covered = 0
            for i,stat in enumerate(lcz_stats):
                lcz_size,lcz_intersect = stat.split(",")
                lcz_size = int(lcz_size)
                lcz_intersect = int(lcz_intersect)
                if(lcz_intersect > 0):
                    covered += 1
            all_dist.append(float(covered)/len(lcz_stats))
    
    uniq_values = list(set(all_dist))
    uniq_values.sort()
    x = uniq_values
    y = [all_dist.count(i)/float(routes_num) for i in x]
    cdf = np.cumsum(y)


    plt.step(x,cdf, where="post")

    plt.xlabel("% LCZ Covered",fontsize=16)
    plt.ylabel("CDF of all overlapping changed routes",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.savefig('out_cdf_route_coverage.pdf')
    plt.clf()


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
"""
The goal of this graph is to know better how the overlap size have
influence into locate a change or not.
"""
def graph_prob_change_in_old(infos):
    
    intersectionpp_files = [x for x in listdir(infos["output_dir"])
        if x.find("intersectionspp") != -1]

    intersect_num = 0
    changes_in_old = defaultdict(lambda: defaultdict(lambda: 0))
    
    for f in intersectionpp_files:
        print f
        for line in open(infos["output_dir"]+"/"+f,"r"):
            infos["node"] = f.split(".",1)[1]

            line_parts = line.split(" ")

            overlap_oldpath = path.path_fromstr(line_parts[7])
            overlap_newpath = path.path_fromstr(line_parts[11])

            lczs_detection_old = [path.hops_fromstr(x.split(";")[0]) \
                    for x in line_parts[3].split("#")]

            lczs_detection_new = [path.hops_fromstr(x.split(";")[1]) \
                    for x in line_parts[3].split("#")]
           
            intersections = [x.split(";")[2] \
                    for x in line_parts[3].split("#") ]

            changes_old_str = line_parts[13]
            changes_new_str = line_parts[15]

            changes_old = []
            changes_new = []
            if changes_old_str != "empty":
                changes_old = [x.strip(",").split(",") for x in \
                    changes_old_str.split("#") if x]
                changes_new = [x.strip(",").split(",") for x in \
                    changes_new_str.split("#") if x]

            statistical.fix_branch_join(overlap_oldpath,overlap_newpath,\
                    changes_old,changes_new)
           
            for j,intersection in enumerate(intersections):
                intersection_hops = path.hops_fromstr(intersection)
                intersection_hops = [x for x in intersection_hops \
                    if x != ["255.255.255.255"]]
               
                if(not intersection_hops):
                    continue

                has_change = False
                for i,change_zone_old in enumerate(changes_old):

                    change_zone_old_hops = path.path_get_subpath(overlap_oldpath,\
                        change_zone_old)
                    coverage_change_zone = statistical.list_intersection(\
                        change_zone_old_hops, intersection_hops)
      
                    if(coverage_change_zone):
                        has_change = True
                
                set_1 = set([",".join(x) for x in lczs_detection_old[j]])
                set_2 = set([",".join(x) for x in intersection_hops])
                intersect = float(len(set_2)) / len(set_1)
                intersect = transform_interval(intersect)
               
                if(intersect == 10):
                    print "not ok"
                    continue

                intersect_num += 1
                if(has_change):
                    changes_in_old[intersect]["changed"] += 1 
                else:
                    changes_in_old[intersect]["not_changed"] += 1 

    print changes_in_old
    x = changes_in_old.keys()
    x.sort()
    x = np.asarray(x)
    print x
    y = [float(changes_in_old[i]["changed"])/(intersect_num) for i in x]

    bar_width = 0.35
    plt.bar(x, y, bar_width, color="#81DAF5")

    plt.xticks(x, ('1-10', '11-20', '21-30', '31-40',\
        '41-50','51-60','61-70','71-80','81-90','91-100'))

    plt.xlabel("% of all overlaps in detections",fontsize=16)
    plt.ylabel("P(change)",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.savefig('out_lcz_overlap_in_old.pdf')
    plt.clf()


# --------------------------------------------------------------- #
def list_intersectionX(list_1,list_2):

    intersection = list()
    for l1 in list_1:
        l1_set = set(l1)
        for l2 in list_2:
            l2_set = set(l2)
            if(l1_set.intersection(l2_set)):
                intersection.append(l2)
    return intersection
"""
The goal of this graph is to know better how the overlapping route
LCZs fits in a intersection
"""
def graph_cdf_changed_overlap(infos):
    
    intersectionpp_files = [x for x in listdir(infos["output_dir"])
        if x.find("intersectionspp") != -1]

    intersect_num = 0
    changed_overlap = list()
   
    print "correct"
    num_overlapping = 0
    for f in intersectionpp_files:
        print f
        for line in open(infos["output_dir"]+"/"+f,"r"):
            infos["node"] = f.split(".",1)[1]

            line_parts = line.split(" ")

            overlap_oldpath = path.path_fromstr(line_parts[7])
            overlap_newpath = path.path_fromstr(line_parts[11])

            lczs_detection_old = [path.hops_fromstr(x.split(";")[0]) \
                    for x in line_parts[3].split("#")]

            lczs_detection_new = [path.hops_fromstr(x.split(";")[1]) \
                    for x in line_parts[3].split("#")]
           
            intersections = [x.split(";")[2] \
                    for x in line_parts[3].split("#") ]

            changes_old_str = line_parts[13]
            changes_new_str = line_parts[15]

            changes_old = []
            changes_new = []
            if changes_old_str != "empty":
                changes_old = [x.strip(",").split(",") for x in \
                    changes_old_str.split("#") if x]
                changes_new = [x.strip(",").split(",") for x in \
                    changes_new_str.split("#") if x]

            statistical.fix_branch_join(overlap_oldpath,overlap_newpath,\
                    changes_old,changes_new)
           
            for j,intersection in enumerate(intersections):
                intersection_hops = path.hops_fromstr(intersection)
                intersection_hops = [x for x in intersection_hops \
                    if x != ["255.255.255.255"]]
               
                if(not intersection_hops):
                    continue

                total_coverage = set()
                for i,change_zone_old in enumerate(changes_old):

                    change_zone_old_hops = path.path_get_subpath(overlap_oldpath,\
                        change_zone_old)
                    coverage_change_zone = statistical.list_intersection(\
                        change_zone_old_hops, intersection_hops)
                    
                    if(coverage_change_zone):
                        set_2 = set([",".join(x) for x in coverage_change_zone]) 
                        total_coverage |= set_2
                
                set_intersect = set([",".join(x) for x in intersection_hops]) 
                v = float(len(total_coverage)) / len(set_intersect)
                changed_overlap.append(v)
                num_overlapping += 1
    
    print num_overlapping
    print len(changed_overlap.count(0))
    uniq_values = list(set(changed_overlap))
    x = uniq_values
    x.sort()
    y = [changed_overlap.count(i)/float(num_overlapping) for i in x]
    cdf = np.cumsum(y)


    plt.step(x,cdf, where="post")

    plt.xlabel("% overlap changed",fontsize=16)
    plt.ylabel("CDF of all overlaps in overlapping routes",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.savefig('out_cdf_changed_overlapZZZXXX.pdf')
    plt.clf()


# ------------------------------------------------------ #
def list_intersection(list_1,list_2):

    intersection = list()
    for l1 in list_1:
        l1_set = set(l1)
        for l2 in list_2:
            l2_set = set(l2)
            if(l1_set.intersection(l2_set)):
                intersection.append(l1)
    return intersection
"""
The goal of this graph is to know better how the overlap size have
influence into locate a change or not.
"""
def graph_prob_change_in_old_2(infos):
    
    intersectionpp_files = [x for x in listdir(infos["output_dir"])
        if x.find("intersectionspp") != -1]

    intersect_num = 0
    changes_in_old = defaultdict(lambda: defaultdict(lambda: 0))
    
    for f in intersectionpp_files:
        print f
        for line in open(infos["output_dir"]+"/"+f,"r"):
            infos["node"] = f.split(".",1)[1]

            line_parts = line.split(" ")

            overlap_oldpath = path.path_fromstr(line_parts[7])
            overlap_newpath = path.path_fromstr(line_parts[11])

            lczs_detection_old = [path.hops_fromstr(x.split(";")[0]) \
                    for x in line_parts[3].split("#")]

            lczs_detection_new = [path.hops_fromstr(x.split(";")[1]) \
                    for x in line_parts[3].split("#")]
           
            intersections = [x.split(";")[2] \
                    for x in line_parts[3].split("#") ]

            changes_old_str = line_parts[13]
            changes_new_str = line_parts[15]

            changes_old = []
            changes_new = []
            if changes_old_str != "empty":
                changes_old = [x.strip(",").split(",") for x in \
                    changes_old_str.split("#") if x]
                changes_new = [x.strip(",").split(",") for x in \
                    changes_new_str.split("#") if x]

            statistical.fix_branch_join(overlap_oldpath,overlap_newpath,\
                    changes_old,changes_new)
           
            for j,intersection in enumerate(intersections):
                intersection_hops = path.hops_fromstr(intersection)
                intersection_hops = [x for x in intersection_hops \
                    if x != ["255.255.255.255"]]
               
                if(not intersection_hops):
                    continue

                has_change = False
                has_change_2 = False
                for i,change_zone_old in enumerate(changes_old):

                    change_zone_old_hops = path.path_get_subpath(overlap_oldpath,\
                        change_zone_old)
                    coverage_change_zone = list_intersection(\
                        change_zone_old_hops, intersection_hops)
      
                    if(coverage_change_zone):
                        has_change = True
                    
                    coverage_change_zone = statistical.list_intersection(\
                        change_zone_old_hops, intersection_hops)
                    if(coverage_change_zone):
                        has_change_2 = True
                    
                if(has_change != has_change_2):
                    print line_parts[0:3]
                    raw_input()

                set_1 = set([",".join(x) for x in lczs_detection_old[j]])
                set_2 = set([",".join(x) for x in intersection_hops])
                intersect = float(len(set_2)) / len(set_1)
                intersect = transform_interval(intersect)
               
                intersect_num += 1
                if(has_change):
                    changes_in_old[intersect]["changed"] += 1 
                else:
                    changes_in_old[intersect]["not_changed"] += 1 

    print changes_in_old
    x = changes_in_old.keys()
    x.sort()
    x = np.asarray(x)
    print x
    y = [float(changes_in_old[i]["changed"])/(changes_in_old[i]["changed"]\
        +changes_in_old[i]["not_changed"]) for i in x]

    bar_width = 0.35
    plt.bar(x, y, bar_width, color="#81DAF5")

    plt.xticks(x, ('1-20', '21-40', '41-60', '61-80',\
        '81-100'))

    plt.xlabel("% of overlaps in detections with overlap X",fontsize=16)
    plt.ylabel("P(change) (in X domain)",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.savefig('out_lcz_overlap_in_old_XXXXX.pdf')
    plt.clf()

# ------------------------------------------------------ #
def graph_cdf_num_overlap_routes_detection(infos):

    overlaps_in_detection = defaultdict(lambda: 0)
    num_detection = 0
    
    for node in infos["nodes"]:
        print node
        detection_file = infos["database_dir"] + "/changes." + node
        detections_by_id = read.read_detection_file(detection_file)
        
        for detection_id,detection in detections_by_id.items():

            if(detection["changes_old"] == []):
                continue

            overlaps_in_detection[len(detection["overlap"])] += 1
            num_detection += 1

    x = overlaps_in_detection.keys() 
    x.sort()
    y = [overlaps_in_detection[i]/float(num_detection) for i in x]
    x_norm = [(z/1000.00) for z in x]
    cdf = np.cumsum(y)

    plt.step(x_norm,cdf, where="post")

    plt.xlabel("Fraction of paths that overlap the detection",fontsize=16)
    plt.ylabel("CDF of number of detections",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.savefig('out_cdf_num_overlap.pdf')
    plt.clf()

# ----------------------------------------------------------- #   
"""
The goal of this graph is to know better how the overlapping route
LCZs fits in a intersection
"""
def graph_cdf_changed_overlap_2(infos):
    
    intersectionpp_files = [x for x in listdir(infos["output_dir"])
        if x.find("intersectionspp") != -1]

    intersect_num = 0
    changed_overlap = list()
    
    num_overlapping = 0
    for f in intersectionpp_files:
        print f
        for line in open(infos["output_dir"]+"/"+f,"r"):
            infos["node"] = f.split(".",1)[1]

            line_parts = line.split(" ")

            overlap_oldpath = path.path_fromstr(line_parts[7])
            overlap_newpath = path.path_fromstr(line_parts[11])

            lczs_detection_old = [path.hops_fromstr(x.split(";")[0]) \
                    for x in line_parts[3].split("#")]

            lczs_detection_new = [path.hops_fromstr(x.split(";")[1]) \
                    for x in line_parts[3].split("#")]
           
            intersections = [x.split(";")[2] \
                    for x in line_parts[3].split("#") ]

            changes_old_str = line_parts[13]
            changes_new_str = line_parts[15]

            changes_old = []
            changes_new = []
            if changes_old_str != "empty":
                changes_old = [x.strip(",").split(",") for x in \
                    changes_old_str.split("#") if x]
                changes_new = [x.strip(",").split(",") for x in \
                    changes_new_str.split("#") if x]

            statistical.fix_branch_join(overlap_oldpath,overlap_newpath,\
                    changes_old,changes_new)
           
            for j,intersection in enumerate(intersections):
                intersection_hops = path.hops_fromstr(intersection)
                intersection_hops = [x for x in intersection_hops \
                    if x != ["255.255.255.255"]]
               
                if(not intersection_hops):
                    continue

                total_coverage = set()
                for i,change_zone_old in enumerate(changes_old):

                    change_zone_old_hops = path.path_get_subpath(overlap_oldpath,\
                        change_zone_old)
                    coverage_change_zone = statistical.list_intersection(\
                        change_zone_old_hops, intersection_hops)
      
                    if(coverage_change_zone):
                        total_coverage = set([",".join(x) for x in coverage_change_zone]) 
                        break

                set_intersect = set([",".join(x) for x in intersection_hops]) 
                v = float(len(total_coverage)) / len(set_intersect)
                changed_overlap.append(v)
                num_overlapping += 1
                break
    
    uniq_values = list(set(changed_overlap))
    x = uniq_values
    x.sort()
    y = [changed_overlap.count(i)/float(num_overlapping) for i in x]
    cdf = np.cumsum(y)


    plt.step(x,cdf, where="post")

    plt.xlabel("% overlap changed",fontsize=16)
    plt.ylabel("CDF of all overlaps in overlapping routes",fontsize=16)

    plt.ylim(0.0, 1.0)
    plt.savefig('out_cdf_changed_overlap_Y2.pdf')
    plt.clf()








