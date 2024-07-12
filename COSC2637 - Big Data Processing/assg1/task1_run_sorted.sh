#!/bin/bash    

hadoop fs -rm -f -r /input
hadoop fs -rm -f -r /output/task1

hadoop fs -mkdir /input
hadoop fs -put .Taxis.txt /input/Taxis.txt
hadoop fs -put .Trips.txt /input/Trips.txt

# specify sort by integer with KeyFieldBasedComparator -n : numeric sort, -r : reverse sort
# ref: https://stackoverflow.com/questions/13331722/how-to-sort-numerically-in-hadoops-shuffle-sort-phase
hadoop jar .hadoop-streaming-3.1.4.jar \
-D mapred.reduce.tasks=3 \
-D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
-D  mapred.text.key.comparator.options=-n \
-file ./task1-mapper.py \
-mapper ./task1-mapper.py \
-file ./task1-reducer.py \
-reducer ./task1-reducer.py \
-input /input/Trips.txt \
-output /output/task1

hadoop fs -getmerge /output/task1/part* task1_merged_output.txt

