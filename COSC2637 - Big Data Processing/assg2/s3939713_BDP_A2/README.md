# s3939713
# Wing Hang Chan
# COSC 2637/2633 Big Data Processing
# COSC 2637/2633 Big Data Processing Assignment 2 – Handling Big Data with Apache Pig

## Initialization
1.) Assume the 2 csv files are in HDFS and placed into /input
2.) Assume there are no /output/taskX folders

unzip s3939713_BDP_A2.zip
cd ./s3939713_BDP_A2/

Can run below commands to reset. Assume csv files placed in parent directory.
hadoop fs -rm -f -r /input
hadoop fs -mkdir /input
hadoop fs -put ../cust_order.csv /input/cust_order.csv
hadoop fs -put ../order_line.csv /input/order_line.csv
hadoop fs -rm -f -r /output/task1
hadoop fs -rm -f -r /output/task2

## Run .pig script in hadoop master node
### Task 1
pig -x mapreduce task1.pig

### Task 2
pig -x mapreduce task2.pig
