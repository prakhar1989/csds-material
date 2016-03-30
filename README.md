## Spark Mini-Homework

This will be a quick guide to get you introduced with one of the most popular and effective tools used for working with big data. Apache Spark is a cluster computing platform designed to be fast and general-purpose. On the speed side, Spark extends the popular MapReduce model to efficiently suport more types of computations, including interactive queries and stream processing.

### Getting Spark

- Unlike Hadoop, it is very easy to get Spark installed and running on your computer locally. But we have provided a pre-configured VM to get Spark and IPython notebook running quickly on your machine.
- A VagrantFile is provided in the repository which will instantiate an Ubuntu virtual machine for you. The steps for running a vagrant VM has been explained in the previous assignment.
- Once we have the machine up and running and you have ssh-ed into it, you will see a file `spark-notebook.py` in `/home/vagrant` directory.
- Simply run this script using the command `python spark_notebook.py`. This will launch PySpark with IPython notebook. The server will be listening on port 8001.
- Open your browser and enter the url `http://localhost:8001`. This will open Jupyter in your browser, following which you can create a notebook and run PySpark commands from it.

### Loading Data
- In this mini homework you will be using the data from the first Hadoop-Hive assignment, but this time you will be writing your own code.
- To get the data loaded into your VM you can clone the repository and copy-paste it into the vagrant folder locally. This will load the data in your VM at the location `/vagrant`. 
- To get this into your home directory in the VM, simply run the command `cp -avr /vagrant/csds-material/ /home/vagrant/`
- Now you can use this data in your notebook.

### Running Jobs
- Create a notebook in the csds-material folder and open in.
- You can use Spark using the SparkContext which is available in the variable `sc`. Simply enter `sc` in a cell and run the cell to see if you have everything working correctly till now.

![img](http://i.imgur.com/mvGM4VY.png)

#### RDD : Resilient Distributed Dataset
- This is where the magic lies and is the backbone of Spark (hence, we strongly recommend you read the original paper on RDD).
- In Spark you only deal with RDDs, whether it's a 1kb dataset or a 1gb dataset, it will all be stored in RDDs. 
- To get any work done, all you need to know are two basic operations:
  1. **Transformations**: This basically transforms an RDD to another RDD by applying modifications to it.
  2. **Actions**: They are the operations that return a final value to the driver program or write data to an external storage system. 

#### Loading Data Into an RDD
- Let us first start by loading the contents of a file into an RDD.
- Spark provides really vast standard library functions that get most basic jobs done with much ease.
- Here we will use the `sc.textFile("filename")` function to read the contents of text file.

![img](http://i.imgur.com/x1mJI4c.png)

#### Total Word Count
- In Hadoop we performed the traditional Map-Reduce operation to obtain the word count for the file, but for Spark we will use transformations and actions to get the job done.
- First we observe that the RDD stores lines of the text file as entries. So we split each line on spaces to obtain an array of words.
- Then we use the flatmap function to flatten the entries so then now every entry holds a single word.
- This entire step is what we call a *Transformation* operation.
- Now we perform an *Action* on the resultant RDD to obtain the count of the entries in the RDD (which is effectively the number of words in the file). The `count` function does this for us.
- Thus we have obtained the count of total number of words in our file.

*Note: Even though we are talking about Transformations and Actions, beneath the surface Spark performs Map-Reduce operations only do all the processing.*

![img](http://i.imgur.com/qjvpx02.png)

### Problem 1
- Similar to what we did above, you now have to compute the counts of each word in the files, file1 and file2 combined in the input folder.
- Your solution should look something like the following

```
World   : <count>
Bye     : <count>
Hello   : <count>
Goodbye : <count>
Hadoop  : <count>
```
- You can start by looking into the spark function `wholeTextFiles`
- Do explore all the transformation and action functions provided in the standard library of spark. You will find it very useful.

### Spark SQL and DataFrames
- In this section you will learn how to use the equivalent of Hive on Spark, i.e. SparkSQL
- SparkSQL provides an SQL interface to query data stored in an DataFrames.
- A DataFrame is a distributed collection of data organized into named columns. 
- It is conceptually equivalent to a table in a relational database or a data frame in R/Python, but with richer optimizations under the hood. 
- For more information about SparkSQL and DataFrame check out their [documentation](http://spark.apache.org/docs/latest/sql-programming-guide.html).
- We will be using the Shopping Mall purchases dataset for the following problem.

### Problem 2.
1. Load the `purchases.txt` file into an RDD

2. create a DataFrame from the RDD by adhering to the following steps-

  - convert each entry of the RDD into a tuple containing values of each field in correct format.
  - encode the schema into an array called `fields`containing the following fields:
    `timestamp: string, location: string, category: string, price: float, card: string`.
  - apply the schema to the RDD, thus converting it into a DataFrame.
  - register the DataFrame as a table called `purchases`.

3. formuate the queries for answering the questions below -
  1. What is the average price of the products that were purchased via Mastercard?
  2. Which date recorded the highest total sales?
  3. What is the minimum value of a product under the Computers category?
  4. How many distinct categories of products are there?
  5. Which store location had the lowest total sales?

- You will not need to rewrite the queries again, SparkSQL queries look exactly like the SQL queries you wrote for the Hive Assignment. The only tricky part here is creating the Schema.

### Problem 3. (Alternative | Optional)
- Another neat way of dealing with relational data (or tables) is by doing a direct conversion from RDD to DataFrame using the `toDF` function and not registering it as an SQL table.

![img](http://i.imgur.com/lQjxlxi.png)

- Following this you can directly solve the queries by using functions provided by Spark DataFrames standard library like filter, select, groupBy, agg etc.
- Let's try the first query from Problem 2. 

![img](http://i.imgur.com/bsUOS5O.png)

- Similar to above, you can try solving the rest of the queries.

### Submission Instructions
All your content should be in the IPython notebook which should be directly submitted (`.ipynb` file) on Courseworks. Please name the file as `<uni>.ipynb`.
