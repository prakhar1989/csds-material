#CSDS Assignment 2 (Prof. Sahu)

In the previous assignment you worked with the Hadoop, HDFS and Hive environments to perform simple map-reduce and basic operations like loading data in HDFS and querying on a small Hive database. Now we shall see and learn how to work with actual big data. In this assignment you shall write your own map-reduce programs to perform more sophisticated tasks. Further you will create your own Hive database given the dataset in raw form and run few queries on it.

This assignment can be performed on the same cloudera virtual machine that was used for the previous assignment. No further setup or installation will be needed. You are free to use any language of your choice for this assignment.

##About the Dataset (editing of technical details might be needed)

**File Name** - server-logz.gz (300 Mb)

**Size** - The total size of the dataset is roughly 1GB after uncompressing the .gz file. 

**Description** - The given data set contains Apache Logs gathered by NASA's server in the months of July-October, 1995.

The logs are line separated, each line consisting of: </br>

**Source IP - Timestamp - HTTP Method - Requested URL - HTTP Protocol - Status Code - Response Bytes**
**Sample : 129.188.154.200 - - [01/Jul/1995:00:03:14 -0400] "GET /images/launchpalms-small.gif HTTP/1.0" 200 11473**


Download and uncompress the dataset from ________. Go through the dataset to get a good idea of all the data and fields present. 

##Part a : Hive (50 points)

1. (Optional) Create a schema for the dataset in Hive. You will have to create a concrete structure describing all the required fields. (* @Prakhar please elaborate this a bit more *)

2. Find the number of 200 status code in the response in the month of August. (10)

3. Find the number of unique source IPs that have made requests to the NASA server for the month of September. (10)

4. Which was the most requested URL in the year 1995. (10)

5. Make a simpe plot depicting the number of requests made in a day for every day in the month of October. You are free to choose any visualization tool for this part. (20)

##Part b : MapReduce (50 points)

1. Enumerate all HTTP status codes and give counts of each (25)

  **Output sample:**  
  200 - 32476  
  404 - 34846  
  500 - 1234  
  
  The counts for each of the status codes are only an example and may vary from the actual counts. Write a mapper and a      reducer to obtain this output.

2. Find the total bandwidth that was sent by the Nasa webserver in the month of July 1995. (25)

##Submission Instructions:

- Create a folder with the source code for both parts and the outputs (screenshots or text file).
- Create a zip file named uni_hw2.zip. 
- Upload this file only on courseworks. 


Any and all doubts are welcome, feel free to ask on Piazza.
