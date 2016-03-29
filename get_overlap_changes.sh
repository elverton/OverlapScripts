TARGET_DATE=20160127_ignore_lb
for i in `cat config/nodelist.txt | grep -v "#"`;
do
    echo $i;
    python normalize_overlap_path.py process_output/$TARGET_DATE/intersections.$i > temp;
    ./path_diff_list temp > temp2;
    paste -d " " process_output/$TARGET_DATE/intersections.$i temp2 > temp3;
    mv temp3 process_output/$TARGET_DATE/intersections_with_changes.$i;
    rm temp temp2;

done
