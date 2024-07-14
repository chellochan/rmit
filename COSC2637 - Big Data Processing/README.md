# Big Data Processing

The course covers Big Data Fundamentals, including the characteristics of Big Data, the sources Big Data (such as social media, sensor data, and geospatial data), as well as the challenges imposed around information management, data analytics, as well as platforms and architectures.

The course aims to keep a balance between algorithmic and systematic issues. The algorithms discussed in this course involve methods of organising big data for efficient complex computation. In addition, we consider Big Data platforms (such as Hadoop) to present practical applications of the algorithms covered in the course.

## Assg 1 - MapReduce Programming

This assignment helps students to build up an understanding on fundamental MapReduce program principles. 

> Spec: `assg1/Assignment 1 formatted-v4.pdf`

### Usage
> Under hadoop platform
```bash
sh assg1/s3939713/task1_run.sh;
sh assg1/s3939713/task2_run.sh;
sh assg1/s3939713/task3_run.sh;
```




## Assg 2 - Big Data Processing with High-level language
## Handling Big Data with Apache Pig

This assignment is featured by big data processing with high-level language based on the Hadoop platform. 

> Spec: `assg2/Assignment 2 formatted - Pig - 2023.pdf`

### Usage
> Under hadoop platform
```bash
pig -x local -4 assg2/nolog.conf

pig -x local assg2/s3939713_BDP_A2/task1.pig 
```

## Assg 3 - Spark Problem Solving 
## HDFS Monitoring via Spark Streaming

This assignment gives students the chance to understand the Spark program principles and to develop advanced problem-solving skills by working on a challenging big data analysis task. 

> Spec: `assg3/Assignment 3 - formatted - 2023Y-1.pdf`

### Initialization
1. Copy and paste the jar file to master node
```bash
scp s3939713_BDP_A3.jar jumphost:~/
scp s3939713_BDP_A3.jar hadoop:~/
```

2. Prepare a plain HDFS file path

### Run spark-submit with input & output path in hadoop master node
```bash
spark-submit --class streaming.WordCount --master yarn --deploy-mode client s3939713_BDP_A3.jar <input_filepath_hdfs> <output_filepath_hdfs>
```

e.g.
```bash
spark-submit --class streaming.WordCount --master yarn --deploy-mode client s3939713_BDP_A3.jar hdfs:///input/ hdfs:///output/
```

### Testing
Upload any text file to hdfs input path
e.g.
```bash
hadoop fs -put test.txt /input/
```

Check with output
```bash
hadoop fs -cat /output/task*-*/part*
```
