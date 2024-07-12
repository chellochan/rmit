#!/bin/bash    

hadoop fs -rm -f -r /input
hadoop fs -rm -f -r /task3
hadoop fs -rm -f -r /output/task3

hadoop fs -mkdir /input
hadoop fs -put ./Taxis.txt /input/Taxis.txt
hadoop fs -put ./Trips.txt /input/Trips.txt

# composite keys are taxi & company
# use -k1 as partitioner key which is taxi
hadoop jar ./hadoop-streaming-3.1.4.jar \
-D stream.num.map.output.key.fields=2 \
-D map.output.key.field.separator=, \
-D mapred.text.key.partitioner.options=-k1,1 \
-D mapred.reduce.tasks=3 \
-file ./task3_1_mapper.py \
-mapper ./task3_1_mapper.py \
-file ./task3_1_reducer.py \
-reducer ./task3_1_reducer.py \
-input /input/Trips.txt \
-input /input/Taxis.txt \
-output /task3 \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

# download merged result from part 1 for part 2 input
hadoop fs -getmerge /task3/part* ./task3_join_output.txt
hadoop fs -put ./task3_join_output.txt /input/task3_join_output.txt
hadoop fs -rm -f -r /task3

# only key is company and it is the partition key
# company partition key to make sure same key values are in the same reducer
hadoop jar ./hadoop-streaming-3.1.4.jar \
-D stream.num.map.output.key.fields=1 \
-D map.output.key.field.separator=, \
-D mapred.text.key.partitioner.options=-k1,1 \
-D mapred.reduce.tasks=3 \
-file ./task3_2_mapper.py \
-mapper ./task3_2_mapper.py \
-file ./task3_2_reducer.py \
-reducer ./task3_2_reducer.py \
-input /input/task3_join_output.txt \
-output /output/task3 \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

# for checking result only
#hadoop fs -getmerge /output/task3/part* ./task3_output.txt
#hadoop fs -put ./task3_output.txt /output/task3/task3_output.txt