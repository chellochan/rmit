#!/bin/bash    

hadoop fs -rm -f -r /input
hadoop fs -rm -f -r /output/task1

hadoop fs -mkdir /input
#hadoop fs -put ./Taxis.txt /input/Taxis.txt
hadoop fs -put ./Trips.txt /input/Trips.txt

hadoop jar ./hadoop-streaming-3.1.4.jar \
-D mapred.reduce.tasks=3 \
-file ./task1_mapper.py \
-mapper ./task1_mapper.py \
-file ./task1_reducer.py \
-reducer ./task1_reducer.py \
-input /input/Trips.txt \
-output /output/task1

# for checking result only
#hadoop fs -getmerge /output/task1/part* task1_merged_output.txt
