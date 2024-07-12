#!/bin/bash

################################################################################
# Help                                                                         #
################################################################################
Help()
{
   # Display Help
   echo
   echo "required arguments:"
   echo "k     arg of k-medoid (must be a number) e.g. -k 2"
   echo "v     arg of number of iteration (must be a number)  e.g. -v 10"
   echo
}

num_re='^[0-9]+$'

while getopts k:v: flag
do
    case "${flag}" in
        k)
          k=${OPTARG};;
        v)
          v=${OPTARG};;
        \?) # incorrect option
         echo "Error: Invalid option"
         exit;;
    esac
done

# required arg -k
if  [ -z "$k" ] ; then
  Help
  exit;
fi
# required arg -k with a number
if ! [[ $k =~ $num_re ]] ; then
  Help
  exit;
fi
# required arg -v
if [ -z "$v" ] ; then
  Help
  exit;
fi
# required arg -v with a number
if ! [[ $v =~ $num_re ]] ; then
  Help
  exit;
fi

rm -f .*.crc # handle bugs of hadoop

# for using first k-lines as medoids
#rm -f medoids.txt
#head -$k Trips.txt | awk -F "," '{print $5 ", " $6}' > medoids.txt

hadoop fs -rm -f -r /input
hadoop fs -rm -f -r /output/task2

hadoop fs -mkdir /input
#hadoop fs -put ./Taxis.txt /input/Taxis.txt
hadoop fs -put ./Trips.txt /input/Trips.txt

i=1
while :
do
	hadoop jar ./hadoop-streaming-3.1.4.jar \
    -D mapred.reduce.tasks=3 \
    -D mapred.text.key.partitioner.options=-k1,1 \
    -D stream.num.map.output.key.fields=2 \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
    -D mapred.text.key.comparator.options=-k1,1n \
    -file medoids.txt \
    -file ./task2_mapper.py \
    -mapper ./task2_mapper.py \
    -file ./task2_reducer.py \
    -reducer ./task2_reducer.py \
    -input /input/Trips.txt \
    -output /output/task2/output$i \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

    rm -f .*.crc
    # rename medoid as prev medoids and merge new one from hdfs to master node
    mv medoids.txt medoids_prev.txt
    hadoop fs -getmerge /output/task2/output$i/part-* medoids-tmp.txt

    # to handle infinity loop if results comes from different reducer nodes
    cat medoids-tmp.txt | sort > medoids.txt
    rm medoids-tmp.txt

    # to check metoid is same as previous metoid
    seeiftrue=`python3 task2_reader.py`

  # if metoid is same as previous metoid or loop number greater than $v end program
	if [ $seeiftrue == 1 ] || [ $i -ge $v ]
	then
		break
	fi
	i=$((i+1))
done

