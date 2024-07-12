# s3939713
# Wing Hang Chan
# COSC 2637/2633 Big Data Processing
# Assignment 3 – HDFS Monitoring via Spark Streaming

## Initialization
1. Copy and paste the jar file to master node
scp s3939713_BDP_A3.jar jumphost:~/
scp s3939713_BDP_A3.jar hadoop:~/

2. Prepare a plain HDFS file path

## Run spark-submit with input & output path in hadoop master node
spark-submit --class streaming.WordCount --master yarn --deploy-mode client s3939713_BDP_A3.jar <input_filepath_hdfs> <output_filepath_hdfs>

e.g.
spark-submit --class streaming.WordCount --master yarn --deploy-mode client s3939713_BDP_A3.jar hdfs:///input/ hdfs:///output/

spark-submit --class streaming.WordCount --master yarn --conf "spark.driver.extraJavaOptions=-Dlog4j.configuration=log4j-spark.properties" --conf "spark.executor.extraJavaOptions=-Dlog4j.configuration=log4j-spark.properties" --deploy-mode client assg3.jar hdfs:///input/ hdfs:///output/

## Testing
Upload any text file to hdfs input path
e.g.
hadoop fs -put test.txt /input/

Check with output
hadoop fs -cat /output/task*-*/part*