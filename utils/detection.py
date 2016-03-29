from os import listdir
from sys import exit
from termcolor import colored
from sys import exit

# -------------------------------------------------------- #
def detection_branch_joins(detection):

    branch_joins = list() 
    for change in detection["changes_old"]:
        branch_ttl = int(change[0])
        join_ttl = int(change[-1])
 
        if(int(branch_ttl) < 0):
            branch_hop =  [detection["src"]]
        else:
            branch_hop = detection["oldpath"][branch_ttl]

        if(len(detection["oldpath"]) >= int(join_ttl)):
            join_hop = [detection["dst"]]
        else:
            join_hop = detection["oldpath"][join_ttl]
        
        branch_joins.append((branch_hop,join_hop))
    
    return branch_joins
        
# -------------------------------------------------------- #
    



