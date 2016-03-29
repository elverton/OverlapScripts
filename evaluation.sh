TARGET_DATE=20160127
for i in `cat config/nodelist.txt | grep -v "#"`; do echo $i; python evaluate_node.py $i; done
