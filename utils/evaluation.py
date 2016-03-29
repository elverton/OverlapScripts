import path
import statistical
import read

# -------------------------------------------------------- #
def evaluation_fix_branch_join(oldpath,newpath,oldchanges,newchanges):
     
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

   

# -------------------------------------------------------- #
def evaluation_change_zones_coverage(infos):
    intersectionpp_file = infos["output_dir"]+"intersectionspp."+\
        infos["node"] 
    output_file = open(infos["output_dir"]+"evaluation_1."+infos["node"],"r")

    for line in open(intersectionpp_file,"r"):
        line_parts = line.strip().split(" ")
        overlap_oldpath = path.path_fromstr(line_parts[7])
        overlap_newpath = path.path_fromstr(line_parts[11])
        intersections = [x.split(";")[2] \
                for x in line_parts[3].split("#")]
        changes_old_str = line_parts[13]
        changes_new_str = line_parts[15]
        
        output_str = " ".join(line_parts[0:3]) + " "
        changes_old = []
        changes_new = []
        if changes_old_str != "empty":
            changes_old = [x.strip(",").split(",") for x in \
                changes_old_str.split("#") if x]
            changes_new = [x.strip(",").split(",") for x in \
                changes_new_str.split("#") if x]
            
        else:
            print output_str + "0,0"
            continue

        output_changes = ""
        output_coverage = ""

        evaluation_fix_branch_join(overlap_oldpath,overlap_newpath,\
                changes_old,changes_new)
        for i,change_zone in enumerate(changes_old):
            
            output_changes += ",".join(change_zone) + ";"
            change_zone_hops = path.path_get_subpath(overlap_oldpath,\
                change_zone)
            output_str += str(len(change_zone_hops)) + ","
            total_coverage = 0
            
            for intersection in intersections:
                intersection_hops = path.hops_fromstr(intersection)
                coverage_change_zone = statistical.list_intersection(\
                    change_zone_hops,intersection_hops)
                # stars does not make intersections
                coverage_change_zone = [x for x in coverage_change_zone \
                    if x != ["255.255.255.255"]]
                if(coverage_change_zone):
                    total_coverage += len(coverage_change_zone)
                    for coverage in coverage_change_zone:
                        output_coverage += str(path.path_recover_ttl(\
                            overlap_oldpath,coverage)) + ","
            output_str += str(total_coverage) + ";"
      
        output_str = output_str.strip(";")
        output_changes = output_changes.strip(";")
        output_coverage = output_coverage.strip(",")
        
        print >> output_file, output_str + " " + output_changes + " " + \
            output_coverage + " " + str(len(overlap_oldpath))
         
    output_file.close()

# -------------------------------------------------------- #
def evaluate_coverage_bins(infos,num_bins=10):
    
    evaluation_1_file = infos["output_dir"]+"evaluation_1."+\
        infos["node"]

    output_file = open(infos["output_dir"]+"evaluation_2."+\
        infos["node"],"w")
    
    for line in open(evaluation_1_file,"r"):

        line = line.strip()
        line_parts = line.strip().split(" ")
        if(len(line_parts) < 7):
            print >> output_file, line + " " + ",".join(10*["0"])
            continue

        local_change_zones = [int(y) for x in line_parts[-3].split(";")\
            for y in x.split(",")]
        local_change_zones = list(set(local_change_zones))
        coverage = list(set([int(x) for x in line_parts[-2].split(",") if x]))
        
        oldpath_len = int(line_parts[-1]) * 10
        step = oldpath_len/num_bins
        path_pos = step
        bins = list()
        while(path_pos <= oldpath_len): 
            bin_mark = "0"
            for ttl in local_change_zones:
                if(ttl*10 < path_pos and ttl*10 >= path_pos - step):
                    bin_mark = "1"
                    if(ttl in coverage):
                        bin_mark = "2" 
            bins.append(bin_mark)
            path_pos += step
       
        print >> output_file, line + " " + ",".join(bins)

    output_file.close()


# -------------------------------------------------------- #
# -------------------------------------------------------- #
# -------------------------------------------------------- #










