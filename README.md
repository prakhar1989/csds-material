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
