# Data Processing

*Assigned: *

*Due:  (just before class)*


In this lab, you will use various types of tools -- from command line tools like `sed` and `awk` to high-level tools like Data Wrangler -- to perform data parsing and extraction from data encoded into a text file.  The goal of this lab is simply to gain experience with these tools and compare and contrast their usage.


# Setup

See the [setup instructions](./SETUP.md)

The `lab` directory contains two datasets that you will work with:

1. A dataset of all the movies in 2013 from January to March (`2013films.txt`). It contains Movie name, Production house, Genre, Publisher and some other details.

1. The second dataset (`worldcup.txt`) is a snippet of the following Wikipedia webpage on [FIFA (Soccer) World Cup](http://en.wikipedia.org/wiki/FIFA_World_Cup).
Specifically it is a partially cleaned-up wiki source for the table toward the end of the page that lists teams finishing in the top 4. 


# Wrangler

Go to the [Data Wrangler website](http://vis.stanford.edu/wrangler/app/).  Load both of the datasets (we recommend cutting out a small subset -- 100~ lines) into Data Wrangler and try playing with the tool.


Some tips using Wrangler:

* Wrangler responds to mouse highlights and clicks on the displayed table cells by suggesting operations on the left sidebar.  
* Hovering over each element shows the result in the table view.  
* Clicking adds the operation.  
* Clear the sidebar by clicking the colored row above the schema row

## Tasks:

Use Data Wrangler for the following two datasets.  

### 2013films.txt

Use the tool to generate output as follows, i.e., Movie name, Production/Distribtuion house, Director, Genre and publisher. 

        'A dark truth, Magnolia Pictures, Damian Lee, Action,ComingSoon.net
         Table No. 21, Eros International, Aditya Datt, Thriller, BoxOfficeMojo.com
         ...
        
For the purpose of explanation columns are separated by ||. You can choose any pattern to extract information. 

1. Movie name can be identified as first column in every line formatted as ''[[ <movie name> ]]''  
1. Production/Distribution house is the following column that is formatted as [[< Production house>]]  
1. Director name can be identified with "(director)" tag that follows the name  
1. Genre is present in the next column but make sure to extract only second part that is separated by | operator. For eg. in [Action film|Action] relevant information is Action  
1. Publisher name can be identified in the last column with format "publisher=<publisher name>"  

It may help to skip first few lines that contains html code, so that you process actual records.

**note**: `lab3/wrangler` contains a modified python wrangler module, which you should use for this lab.  This means that the python scripts that you export when using Data Wrangler should be run in the `lab3/` folder.


#### Questions

1. Export the Python version of the wrangler script and save it to a file.  
1. Use the script to clean the data, then determine which Production/Distribution house produced maximum movies.

### worldcup.txt

Use the tool to generate output as follows, i.e., each line in the output contains a country, a year, and the position of the county in that year (if within top 4).

        BRA, 1962, 1
        BRA, 1970, 1
        BRA, 1994, 1
        BRA, 2002, 1
        BRA, 1958, 1
        BRA, 1998, 2
        BRA, 1950, 2
        ...

It may help to 

1. Skip the first 20 or so rows of table headers and other text, so that the data wrangler works with are "record text".  
2. Delete the rows that are clearly HTML formatting content
3. Extract the relevant data from the remaining column into new columns
4. Use the fill operation

#### Questions

1. According to the dataset, how often has each country won the world cup?



# Grep, Sed & Awk

The set of three UNIX tools, `sed`, `awk`, and `grep`, can be very useful for quickly cleaning up and transforming data for further analysis
(and have been around since the inception of UNIX). 
In conjunction with other unix utilities like `sort`, `uniq`, `tail`, `head`, etc., you can accomplish many simple data parsing and cleaning 
tasks with these tools. 
You are encouraged to play with these tools and familiarize yourselves with the basic usage of these tools.


As an example, the following sequence of commands can be used to answer the third question from the [lab 2](../lab2/) ("Find the five uids that have tweeted the most").

    grep "created\_at" twitter.json | sed 's/"user":{"id":\([0-9]*\).*/XXXXX\1/' | sed 's/.*XXXXX\([0-9]*\)$/\1/' | sort | uniq -c | sort -n | tail -5

The first command (`grep`) discards the deleted tweets, the `sed` commands extract the first "user-id" from each line, `sort` sorts the user ids, and `uniq -c` counts the unique entries (i.e., user ids). The final `sort -n | tail -5` return the top 5 uids.
Note that, combining the two `sed` commands as follows does not do the right thing -- we will let you figure out why.

    grep "created\_at" twitter.json | sed 's/.*"user":{"id":\([0-9]*\).*/\1/' | sort | uniq -c | sort -n | tail -5"

To get into some details:

## grep

The basic syntax for `grep` is: 

     grep 'regexp' filename

or equivalently (using UNIX pipelining):

    cat filename | grep 'regexp'

The output contains only those lines from the file that match the regular expression. Two options to grep are useful: `grep -v` will output those lines that
*do not* match the regular expression, and `grep -i` will ignore case while matching. See the manual (`man grep`) (or online resources) for more details.

## sed
Sed stands for _stream editor_. Basic syntax for `sed` is:

    sed 's/regexp/replacement/g' filename

For each line in the intput, the portion of the line that matches _regexp_ (if any) is replaced with _replacement_. Sed is quite powerful within the limits of
operating on single line at a time. You can use \\( \\) to refer to parts of the pattern match. In the first sed command above, the sub-expression within \\( \\)
extracts the user id, which is available to be used in the _replacement_ as \1. 


## awk 

Finally, `awk` is a powerful scripting language (not unlike perl). The basic syntax of `awk` is: 

    awk -F',' 'BEGIN{commands} /regexp1/ {command1} /regexp2/ {command2} END{commands}' 

For each line, the regular expressions are matched in order, and if there is a match, the corresponding command is executed (multiple commands may be executed
for the same line). BEGIN and END are both optional. The `-F','` specifies that the lines should be _split_ into fields using the separator "_,_", and those fields are available to the regular
expressions and the commands as $1, $2, etc. See the manual (`man awk`) or online resources for further details. 



## Examples 

A few examples to give you a flavor of the tools and what one can do with them.

1. Perform the equivalent of _wrap_ on `labor.csv` (i.e., merge consecutive groups of lines referring to the same record)

        cat labor.csv | awk '/^Series Id:/ {print combined; combined = $0} 
                            !/^Series Id:/ {combined = combined", "$0;}
                            END {print combined}'

1. On  `crime-clean.txt`, the following command does a _fill_ (first row of output: "Alabama, 2004, 4029.3".

        cat crime-clean.txt | grep -v '^,$' | awk '/^[A-Z]/ {state = $4} !/^[A-Z]/ {print state, $0}'
    
1. On `crime-clean.txt`, the following script cleans the data as was done in the Wrangler demo in class. The following works assuming perfectly homogenous data (as the example on the Wrangler wbesite is).

        cat crime-clean.txt | grep -v '^,$' | sed 's/,$//g; s/Reported crime in //; s/[0-9]*,//' | 
            awk -F',' 'BEGIN {printf "State, 2004, 2005, 2006, 2007, 2008"} 
                /^[A-Z]/ {print c; c=$0}  
                !/^[A-Z]/ {c=c", "$0;}    
                END {print c}'

1. On `crime-unclean.txt` the follow script perfroms the same cleaning as above, but
allows incomplete information (e.g., some years may be missing).

        cat crime-unclean.txt | grep -v '^,$' | sed 's/Reported crime in //;' | 
                awk -F',' 'BEGIN {printf "State, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008"} 
                           /^[A-Z]/ || /^$/ {if(state) {
                                        printf(state); 
                                        for(i = 2000; i <= 2008; i++) {
                                               if(array[i]) {printf("%s,", array[i])} else {printf("0,")}
                                        }; printf("\n");} 
                                     state=$0; 
                                     delete array} 
                          !/^[A-Z]/ {array[$1] = $2}'

We provided the last example to show how powerful `awk` can be. However if you need to write a long command like this, you may be better
off using a proper scripting language like `perl` or `python`!

    
## Tasks:

Perform the above cleaning tasks using these tools. Hints:

1. Use the "split" function, and "for loop" constructs (e.g., [here](http://www.math.utah.edu/docs/info/gawk_12.html)).

2. For World Cup data, start with this command that cleans up the data a little bit.

        cat worldcup.txt | sed 's/\[\[\([0-9]*\)[^]]*\]\]/\1/g; s/.*fb|\([A-Za-z]*\)}}/\1/g; s/<sup><\/sup>//g; s/|bgcolor[^|]*//g; s/|align=center[^|]*//g'

Perform the above cleaning tasks using these tools.   No need to re-answer the questions in the Wrangler section, but recompute them to ensure your answers are consistent.

#### Questions

1. Submit the scripts you wrote to perform the cleaning tasks.
2. From your experience, briefly discuss the pro and cons between using Data Wrangler as compared to lower levels tools like sed/awk?
3. What additional operations would have made using Data Wrangler "easier"?


### Handing in your work

1. Create a PDF file containing: 
  * your name 
  * the results of the tasks in Wrangler section  
  * the brief responses to the reflection questions 
2. Create a folder that has all the code that **you've** written (AWK, SED) and wrangler generated python scripts. Please don't upload the same files that we've provided for this assignment.
3. Create a zip containing the PDF and the code folder 
4. Submit on Courseworks.


### Feedback (optional, but valuable)

If you have any comments about this lab, or any thoughts about the
class so far, we would greatly appreciate them.  Your comments will
be strictly used to improve the rest of the labs and classes and have
no impact on your grade. 

Some questions that would be helpful:

* Is the lab too difficult or too easy?  
* Did you look forward to any exercise that the lab did not cover?
* Which parts of the lab were interesting or valuable towards understanding the material?
* How is the pace of the course so far?

