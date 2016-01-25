Hadoop
===

This is a quick guide on getting your feet wet with Hadoop. It'll teach you how to setup a single-node hadoop cluster, run jobs in Java/Python and lastly, explore the results.

#### Getting Hadoop

The easiest way to try out Hadoop locally as a developer is by running a preconfigured-VM. 

1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) for your Operating System.
2. For the VM, we'll be using Cloudera's VM that they made available for Udacity. Unlike the official Cloudera Hadoop distribution (CHD) this is a more stripped down version (1.7 GB). Download the file from [here](http://content.udacity-data.com/courses/ud617/Cloudera-Udacity-Training-VM-4.1.1.c.zip) and unzip it.
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

Before we start running MapReduce jobs, we first need to get the code. Get started by cloning this repository.

```
$ cd ~/Desktop
$ git clone https://github.com/prakhar1989/csds-material
```

Open the terminal in the VM so that you can start running commands. Linux and Mac users can also SSH into the machine by running `ssh training@ip-address` and entering the password - `training`. To get the IP address of the machine, just run `ifconfig` and taking note of the inet addr.

![ip](http://i.imgur.com/VUMJkVy.png)

The `csds-material` directory has an input folder which describes the input on which we'll running our MapReduce jobs. To view the contents, just type the following -

```
$ cat input/*
Hello World Bye World
Hello Hadoop Goodbye Hadoop
```

The job that we're going to run is the canonical wordcount example - it counts the number of words in a file (set of files).

**Java**
To run the java job, we'll first create a jar and then tell `hadoop` to run it.

```
$ cd java-example
$ export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar
$ hadoop com.sun.tools.javac.Main WordCount.java
$ jar cf wc.jar WordCount*.class
```
When this is done, we'll have a `wc.jar` in our directory which we'll use to run a MapReduce job. But before we run our jobs, we need to make sure that the input data is available in HDFS. Let's now copy the `input` directory from our local machine to a location called `/user/csds/`

```
$ cd ../
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

```
$ cd java-example
$ $ hadoop jar wc.jar WordCount /user/csds/input /user/csds/output
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
