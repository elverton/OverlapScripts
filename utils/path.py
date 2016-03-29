from os import listdir
from sys import exit
from termcolor import colored

# -------------------------------------------------------- #
def path_fromstr(path_str):
    
    path_hops_str = path_str.split("|")

    path = list()
    for hop in path_hops_str:
        subparts = hop.split(";")
        hop_ips = list()
        for subpart in subparts:
            ip = subpart.split(":")[0]
            hop_ips.append(ip)
        hop_ips.sort()
        path.append(hop_ips)
    
    return path

# -------------------------------------------------------- #
def path_get_subpath(path,ttls):
    
    subpath = list()
    path_length = len(path)
    for ttl in ttls:
        ttl = int(ttl)
        if ttl < 0 or ttl >= path_length:
            continue
        subpath.append(path[ttl])

    return subpath

# -------------------------------------------------------- #
def hops_tostr(hops):
    ifaces_str = [",".join(x) for x in hops]
    hops_str = "|".join(ifaces_str)

    return hops_str
# -------------------------------------------------------- #
def hops_fromstr(hops_str):
    hops = list()
    for hopstr in hops_str.split("|"):
        hop = hopstr.split(",")
        if(hop == ['']):
            continue
        hop.sort()
        hops.append(hop)

    return hops

# -------------------------------------------------------- #
def path_tostr(hops):

    path_str_normalized = ""
    for hop in hops:
        for iface in hop:
            path_str_normalized += iface+":0:0.0,0.0,0.0,0.0:0;"
        path_str_normalized = path_str_normalized.strip(";")
        path_str_normalized += "|"
    path_str_normalized = path_str_normalized.strip("|")

    return path_str_normalized

# -------------------------------------------------------- #
def path_recover_ttl(path,target_hop):
    for i,hop in enumerate(path):
        if(target_hop == hop):
            return i
# -------------------------------------------------------- #
