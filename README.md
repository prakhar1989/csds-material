Hadoop
===

This is a quick guide on getting your feet wet with Hadoop. It'll teach you how to setup a single-node hadoop cluster, run jobs in Java/Python and lastly, explore the results.

#### Getting Hadoop

The easiest way to try out Hadoop locally as a developer is by running a preconfigured-VM.

1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) for your Operating System.
2. For the VM, we'll be using Cloudera's VM that they made available for Udacity. Unlike the official Cloudera Hadoop distribution (CHD) this is a more stripped down version (1.7 GB). Download the file from [here](http://content.udacity-data.com/courses/ud617/Cloudera-Udacity-Training-VM-4.1.1.c.zip) and unzip it. If you are on a Windows machine you will likely need to use WinRAR to open this .zip file because other methods fail to open the unzipped file (which exceeds the maximum specified 4GB for a .zip file).
3. Open Virtualbox and click on "New".
4. Give a name "Hadoop", Type as "Linux" and Version as "Ubuntu (64-bit)"
5. Drag the slider to select a memory of 2048 MB
6. In the hard disk section, click the radio button "Use an existing virtual hard disk file", browse to your download directory and select the `Cloudera-Training-VM-4.1.1.c.vmdk` file.
7. Now you should see a "hadoop" machine in the sidebar. Select it and click on Settings.
8. Choose network from the top panel, and change the "Attached to" to Bridged Adapter.
9. You can now select the machine, and click on "Start".
10. Your machine will now boot up.

![img](http://i.imgur.com/N0GS3b1.jpg)

#### Running Jobs

Before we start running MapReduce jobs, we first need to get the code. When the VM first starts, the terminal should already be open. Get started by cloning this repository.

```
$ cd ~/Desktop
$ git clone https://github.com/prakhar1989/csds-material
$ cd csds-material
```

Linux and Mac users can also SSH into the machine by running `ssh training@ip-address` and entering the password - `training`. To get the IP address of the machine, just run `ifconfig` and taking note of the inet addr.

![ip](http://i.imgur.com/VUMJkVy.png)

The `csds-material` directory has an input folder which describes the input on which we'll running our MapReduce jobs. To view the contents, just type the following -

```
$ cat input/*
Hello World Bye World
Hello Hadoop Goodbye Hadoop
```

The job that we're going to run is the canonical wordcount example - it counts the number of words in a file (set of files).

#### HDFS
HDFS or Hadoop FileSystem is the filesystem where Hadoop expects the input files to be. When a job completes, HDFS is also where the final result will be placed by Hadoop. So the first thing we need to do, is to move our input files into HDFS. 
```
$ hadoop fs -ls /user/
drwxr-xr-x   - hue      supergroup          0 2013-09-05 20:08 /user/hive
drwxr-xr-x   - hue      hue                 0 2013-09-10 10:37 /user/hue
drwxr-xr-x   - training supergroup          0 2013-10-04 18:58 /user/training

$ hadoop fs -mkdir /user/csds
$ hadoop fs -copyFromLocal input /user/csds/
$ hadoop fs -ls /user/csds/input
Found 2 items
-rw-r--r--   1 training supergroup         22 2016-01-25 23:06 /user/csds/input/file1
-rw-r--r--   1 training supergroup         28 2016-01-25 23:06 /user/csds/input/file2
```

Great! Now that we have our data residing in HDFS, lets run our mapreduce job!


##### Java

To run the java job, we'll first create a jar and then tell `hadoop` to run it.

```
$ cd java-example
$ export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar
$ hadoop com.sun.tools.javac.Main WordCount.java
$ jar cf wc.jar WordCount*.class
```
When this is done, we'll have a `wc.jar` in our directory which we'll use to run a MapReduce job. 

```
$ hadoop jar wc.jar WordCount /user/csds/input /user/csds/output
16/01/25 23:09:47 WARN mapred.JobClient: Use GenericOptionsParser for parsing the arguments. Applications should implement Tool for the same.
16/01/25 23:09:47 INFO input.FileInputFormat: Total input paths to process : 2
16/01/25 23:09:47 WARN snappy.LoadSnappy: Snappy native library is available
16/01/25 23:09:47 INFO snappy.LoadSnappy: Snappy native library loaded
16/01/25 23:09:47 INFO mapred.JobClient: Running job: job_201601252122_0010
16/01/25 23:09:48 INFO mapred.JobClient:  map 0% reduce 0%
16/01/25 23:09:53 INFO mapred.JobClient:  map 100% reduce 0%
16/01/25 23:09:55 INFO mapred.JobClient:  map 100% reduce 100%
16/01/25 23:09:56 INFO mapred.JobClient: Job complete: job_201601252122_0010
16/01/25 23:09:56 INFO mapred.JobClient: Counters: 32
16/01/25 23:09:56 INFO mapred.JobClient:   File System Counters
16/01/25 23:09:56 INFO mapred.JobClient:     FILE: Number of bytes read=79
16/01/25 23:09:56 INFO mapred.JobClient:     FILE: Number of bytes written=544598
16/01/25 23:09:56 INFO mapred.JobClient:     FILE: Number of read operations=0
16/01/25 23:09:56 INFO mapred.JobClient:     FILE: Number of large read operations=0
16/01/25 23:09:56 INFO mapred.JobClient:     FILE: Number of write operations=0
16/01/25 23:09:56 INFO mapred.JobClient:     HDFS: Number of bytes read=262
16/01/25 23:09:56 INFO mapred.JobClient:     HDFS: Number of bytes written=41
16/01/25 23:09:56 INFO mapred.JobClient:     HDFS: Number of read operations=4
16/01/25 23:09:56 INFO mapred.JobClient:     HDFS: Number of large read operations=0
16/01/25 23:09:56 INFO mapred.JobClient:     HDFS: Number of write operations=1
16/01/25 23:09:56 INFO mapred.JobClient:   Job Counters
16/01/25 23:09:56 INFO mapred.JobClient:     Launched map tasks=2
16/01/25 23:09:56 INFO mapred.JobClient:     Launched reduce tasks=1
16/01/25 23:09:56 INFO mapred.JobClient:     Rack-local map tasks=2
16/01/25 23:09:56 INFO mapred.JobClient:     Total time spent by all maps in occupied slots (ms)=7528
16/01/25 23:09:56 INFO mapred.JobClient:     Total time spent by all reduces in occupied slots (ms)=2476
16/01/25 23:09:56 INFO mapred.JobClient:     Total time spent by all maps waiting after reserving slots (ms)=0
16/01/25 23:09:56 INFO mapred.JobClient:     Total time spent by all reduces waiting after reserving slots (ms)=0
16/01/25 23:09:56 INFO mapred.JobClient:   Map-Reduce Framework
16/01/25 23:09:56 INFO mapred.JobClient:     Map input records=2
16/01/25 23:09:56 INFO mapred.JobClient:     Map output records=8
16/01/25 23:09:56 INFO mapred.JobClient:     Map output bytes=82
16/01/25 23:09:56 INFO mapred.JobClient:     Input split bytes=212
16/01/25 23:09:56 INFO mapred.JobClient:     Combine input records=8
16/01/25 23:09:56 INFO mapred.JobClient:     Combine output records=6
16/01/25 23:09:56 INFO mapred.JobClient:     Reduce input groups=5
16/01/25 23:09:56 INFO mapred.JobClient:     Reduce shuffle bytes=85
16/01/25 23:09:56 INFO mapred.JobClient:     Reduce input records=6
16/01/25 23:09:56 INFO mapred.JobClient:     Reduce output records=5
16/01/25 23:09:56 INFO mapred.JobClient:     Spilled Records=12
16/01/25 23:09:56 INFO mapred.JobClient:     CPU time spent (ms)=890
16/01/25 23:09:56 INFO mapred.JobClient:     Physical memory (bytes) snapshot=348463104
16/01/25 23:09:56 INFO mapred.JobClient:     Virtual memory (bytes) snapshot=1163071488
16/01/25 23:09:56 INFO mapred.JobClient:     Total committed heap usage (bytes)=337780736
```
Our job has now run! To see the output, we can view the `/user/csds/output/` directory.

```
$ hadoop fs -ls /user/csds/output
Found 3 items
-rw-r--r--   1 training supergroup          0 2016-01-25 23:09 /user/csds/output/_SUCCESS
drwxr-xr-x   - training supergroup          0 2016-01-25 23:09 /user/csds/output/_logs
-rw-r--r--   1 training supergroup         41 2016-01-25 23:09 /user/csds/output/part-r-00000

$ hadoop fs -cat /user/csds/output/part-r-00000
Bye	1
Goodbye	1
Hadoop	2
Hello	2
World	2
```
Awesome! Our hadoop job ran correctly.

##### Python

Hadoop, by default, only supports Java for writing MR jobs. However, its [streaming](http://hadoop.apache.org/docs/r1.2.1/streaming.html) API allows us to provide any shell executable program to be the mapper and the reducer. The `python-example` folder has the corresponding code for `mapper` and `reducer`.

Since our `input` folder already exists in HDFS, we will not need to create the folder again. Let's directly run the MR job

```
$ cd python-example
$ hs mapper.py reducer.py /user/csds/input/* /user/csds/outputpy
packageJobJar: [mapper.py, reducer.py, /tmp/hadoop-training/hadoop-unjar6628549512020884250/] [] /tmp/streamjob6598847338247804626.jar tmpDir=null
16/01/26 00:29:26 WARN mapred.JobClient: Use GenericOptionsParser for parsing the arguments. Applications should implement Tool for the same.
16/01/26 00:29:26 WARN snappy.LoadSnappy: Snappy native library is available
16/01/26 00:29:26 INFO snappy.LoadSnappy: Snappy native library loaded
16/01/26 00:29:26 INFO mapred.FileInputFormat: Total input paths to process : 2
16/01/26 00:29:27 INFO streaming.StreamJob: getLocalDirs(): [/var/lib/hadoop-hdfs/cache/training/mapred/local]
16/01/26 00:29:27 INFO streaming.StreamJob: Running job: job_201601260027_0001
16/01/26 00:29:27 INFO streaming.StreamJob: To kill this job, run:
16/01/26 00:29:27 INFO streaming.StreamJob: UNDEF/bin/hadoop job  -Dmapred.job.tracker=0.0.0.0:8021 -kill job_201601260027_0001
16/01/26 00:29:27 INFO streaming.StreamJob: Tracking URL: http://0.0.0.0:50030/jobdetails.jsp?jobid=job_201601260027_0001
16/01/26 00:29:28 INFO streaming.StreamJob:  map 0%  reduce 0%
16/01/26 00:29:32 INFO streaming.StreamJob:  map 100%  reduce 0%
16/01/26 00:29:35 INFO streaming.StreamJob:  map 100%  reduce 100%
16/01/26 00:29:36 INFO streaming.StreamJob: Job complete: job_201601260027_0001
16/01/26 00:29:36 INFO streaming.StreamJob: Output: /user/csds/outputpy

$ hadoop fs -ls /user/csds/outputpy
Found 3 items
-rw-r--r--   1 training supergroup          0 2016-01-26 00:29 /user/csds/outputpy/_SUCCESS
drwxr-xr-x   - training supergroup          0 2016-01-26 00:29 /user/csds/outputpy/_logs
-rw-r--r--   1 training supergroup         41 2016-01-26 00:29 /user/csds/outputpy/part-00000

$ hadoop fs -cat /user/csds/outputpy/part-00000
Bye	1
Goodbye	1
Hadoop	2
Hello	2
World	2
```

##### Tracking jobs
Hadoop provides a simple interface to track the status of MR jobs. To view it, you first need to get the VM ip using `ifconfig`. Then note the `inet addr` address. Finally, open `http://ip:50030/jobtracker.jsp` on your local machine. Alternatively, you can also open Firefox in the VM and browse to `http://localhost:50030/jobtracker.jsp` to view the jobs.

![img](http://i.imgur.com/vAxP024.png)


### AWS EMR

In this section, we'll see how we can use [AWS Elastic Mapreduce](https://aws.amazon.com/elasticmapreduce/) (EMR) to run our MapReduce job. To follow along, make sure you have a functioning AWS account.

AWS EMR reads and writes data to [AWS S3](https://aws.amazon.com/s3/) so the first step is to upload our application code and input to S3. Head over to the [console](https://console.aws.amazon.com/s3/home?region=us-east-1), create a new bucket (with a unique bucket name) and upload `python-example/mapper.py`, `python-example/reducer.py` and `aws_emr/aws.txt`.

We can now begin configuring our MR job. Head over to the [EMR console](https://console.aws.amazon.com/elasticmapreduce/home?region=us-east-1) and click on **Create Cluster**. See the screen below for the options to configure -

![img](http://i.imgur.com/NAbeCpj.png)

AWS will then go ahead and follow that up with the cluster creation screen -

![img](http://i.imgur.com/eF4pPVK.png)

The next step is to add a MR step. Click on **Add Step** and fill in the details as shown below. Be sure to change these paths for your S3 bucket.

![img](http://i.imgur.com/AuXphLo.png)

When done, the status of the cluster will change from *Waiting* to *Running*. After a few minutes, your job should be complete. This is indicated by the status of the cluster again going back to *Waiting*. You can now head over to the S3 bucket and see the output being generated.

![img](http://i.imgur.com/U2XYgJr.png)

And that's it! This is how your run MR jobs on AWS EMR!

Hive
====

This section teaches you how to try out [Hive](https://en.wikipedia.org/wiki/Apache_Hive) on the VM. The Hive data warehouse facilitates querying and managing large datasets residing in distributed storage. Hive provides a mechanism to project structure onto this data and query the data using a SQL-like language called HiveQL. At the same time this language also allows traditional map/reduce programmers to plug in their custom mappers and reducers when it is inconvenient or inefficient to express this logic in HiveQL.

In this section, we'll see how to use Hive to query a dataset of Shopping Mall purchases. The dataset is located in the `hive/purchases.txt`. Hive is already installed and setup on your VM, so getting started is just a command away. Type the following in the terminal -

```
$ hive
Logging initialized using configuration in file:/etc/hive/conf.dist/hive-log4j.properties
Hive history file=/tmp/training/hive_job_log_training_201602010336_645327107.txt
hive> 
```

Let's use the `SHOW TABLES` command to see if any tables exist. Interacting with Hive is exactly like any relational database - so if you've worked with MySQL or PostgreSQL before you'll feel right at home.
```
hive> SHOW TABLES;
OK
Time taken: 2.028 seconds
```
Since no tables exist, we see a blank list. Now let's go ahead and create a table. 

```
hive> CREATE TABLE test_tables;
FAILED: SemanticException [Error 10043]: Either list of columns or a custom serializer should be specified

hive> CREATE TABLE test_tables (some_text STRING);
OK
Time taken: 0.713 seconds

hive> SHOW TABLES;
OK
test_tables
Time taken: 0.053 seconds

hive> select * from test_tables;
OK
Time taken: 0.161 seconds
```

Press `Ctrl-D` to exit from the Hive console. So we created the `test_tables` above, but the first command failed because we didn't provide any schema. Every table that you wish to create must have a schema. In the subsequent command, we provide a dummy column name - `some_text` of the `STRING` type to make the command succeed. Once the table is created, `SHOW TABLES` correctly lists our table. However, since our table has no data, the `select` query returns a blank list.

Now we know how to create a table in Hive, we'll create a table and add real data. But before we do that, let us inspect the data that we're going to put in. This will be required for coming up with a schema for our database.

```
$ head purchases.txt
2012-07-20 09:59:00,Corpus Christi,CDs,327.91,Cash
2012-03-11 17:29:00,Durham,Books,115.09,Discover
2012-07-31 11:43:00,Rochester,Toys,332.07,MasterCard
2012-06-18 14:47:00,Garland,Computers,31.99,Visa
2012-03-27 11:40:00,Tulsa,CDs,452.18,Discover
2012-05-31 10:57:00,Pittsburgh,Garden,492.25,Amex
2012-08-22 14:35:00,Richmond,Consumer Electronics,346,Amex
2012-09-23 16:45:00,Scottsdale,CDs,21.58,Cash
2012-10-17 11:29:00,Baton Rouge,Computers,226.26,Cash
2012-07-03 11:05:00,Virginia Beach,Women's Clothing,23.47,Cash
```

We can see above that our data has 5 columns, each separated by a comma. The first column is a timestamp indicating the time and date of the sale. The second column indicates the store location where the sale occured, followed by the category of the product. The last two columns indicate the price and the mode of payment associated with the sale respectively.

Let's log into `hive` and load this data into HDFS. We'll start by first creating a new table.

```
hive> CREATE TABLE purchases (
  `sales_date` TIMESTAMP,
  `store_location` STRING,
  `category` STRING,
  `price` FLOAT,
  `card` STRING 
) row format delimited fields terminated by ',' stored as textfile;
OK
Time taken: 0.177 seconds
```
In the above command, we create a new table called `purchases` with the appropriate schema shown above. The `row format ...` command tells Hive that we'll be loading in data from a [csv](https://en.wikipedia.org/wiki/Comma-separated_values) file eventually. The next step is to move our data into HDFS so that we can import it in Hive. Exit from hive and run the following command from the `csds-material` directory.

```
$ hadoop fs -copyFromLocal hive/purchases.txt /user/csds/input
$ hadoop fs -ls /user/csds/input
Found 1 items
-rw-r--r--   1 training supergroup      53755 2016-02-01 04:29 /user/csds/input/purchases.txt
```
Now we have everything in place to load data in Hive. Log back into the `hive` console and run the following -
```
hive> LOAD DATA INPATH '/user/csds/input/purchases.txt' INTO TABLE purchases;
Loading data to table default.purchases
OK
Time taken: 2.436 seconds
```
Great our data is now loaded. Now let's explore the data 
```
hive> show tables;
OK
purchases
test_tables
Time taken: 0.133 seconds

hive> select * from purchases limit 10;
OK
2012-07-20 09:59:00	Corpus Christi	CDs	327.91	Cash
2012-03-11 17:29:00	Durham	Books	115.09	Discover
2012-07-31 11:43:00	Rochester	Toys	332.07	MasterCard
2012-06-18 14:47:00	Garland	Computers	31.99	Visa
2012-03-27 11:40:00	Tulsa	CDs	452.18	Discover
2012-05-31 10:57:00	Pittsburgh	Garden	492.25	Amex
2012-08-22 14:35:00	Richmond	Consumer Electronics	346.0	Amex
2012-09-23 16:45:00	Scottsdale	CDs	21.58	Cash
2012-10-17 11:29:00	Baton Rouge	Computers	226.26	Cash
2012-07-03 11:05:00	Virginia Beach	Women's Clothing	23.47	Cash
Time taken: 0.155 seconds

hive> select sum(price) from purchases where card = "Cash";
Total MapReduce jobs = 1
Launching Job 1 out of 1
Number of reduce tasks determined at compile time: 1
In order to change the average load for a reducer (in bytes):
  set hive.exec.reducers.bytes.per.reducer=<number>
In order to limit the maximum number of reducers:
  set hive.exec.reducers.max=<number>
In order to set a constant number of reducers:
  set mapred.reduce.tasks=<number>
Starting Job = job_201602010237_0001, Tracking URL = http://0.0.0.0:50030/jobdetails.jsp?jobid=job_201602010237_0001
Kill Command = /usr/lib/hadoop/bin/hadoop job  -Dmapred.job.tracker=0.0.0.0:8021 -kill job_201602010237_0001
Hadoop job information for Stage-1: number of mappers: 1; number of reducers: 1
2016-02-01 04:36:15,505 Stage-1 map = 0%,  reduce = 0%
2016-02-01 04:36:17,537 Stage-1 map = 100%,  reduce = 0%, Cumulative CPU 0.57 sec
2016-02-01 04:36:18,558 Stage-1 map = 100%,  reduce = 0%, Cumulative CPU 0.57 sec
2016-02-01 04:36:19,565 Stage-1 map = 100%,  reduce = 100%, Cumulative CPU 1.23 sec
2016-02-01 04:36:20,582 Stage-1 map = 100%,  reduce = 100%, Cumulative CPU 1.23 sec
MapReduce Total cumulative CPU time: 1 seconds 230 msec
Ended Job = job_201602010237_0001
MapReduce Jobs Launched:
Job 0: Map: 1  Reduce: 1   Cumulative CPU: 1.23 sec   HDFS Read: 0 HDFS Write: 0 SUCCESS
Total MapReduce CPU Time Spent: 1 seconds 230 msec
OK
55199.32992255688
Time taken: 9.002 seconds
```
In this last query, we ran a simple query to calculate the total price of all the products that were paid in cash. We can see that our query got mapped to MapReduce tasks and got run by Hadoop. Finally at the end, we see the answer to our query - $55199 and also the total time taken.

So this is how you can use Hive and the power of SQL to analyse your big data that is already stored on an HDFS cluster. For more practice, try running your own queries and see what you can uncover. If you're feeling adventurous, try to formuate the queries for answering the questions below -

1. What is the average price of the products that were purchased via Mastercard?
2. Which date recorded the highest total sales?
3. What is the minimum value of a product under the Computers category?
4. How many distinct categories of products are there?
5. Which store location had the lowest total sales?

If you need help with HiveQL, [this](https://docs.treasuredata.com/articles/hive) documentation should be useful.


