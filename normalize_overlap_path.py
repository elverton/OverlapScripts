from sys import argv
from utils import path


f = open(argv[1],"r")
for line in f:
    line = line.strip().split(" ")
    oldpath = line[4]+" "+line[5]+" "+line[6]+" "+line[7]
    newpath = line[8]+" "+line[9]+" "+line[10]+" "+line[11]
    print oldpath+"@"+newpath


