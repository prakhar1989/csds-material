# Data Lab: Entity Resolution

*Due:  12:59 PM (just before class)*

In this lab, you will take two datasets that describe the same
entities, and identify which entity in one dataset is the same as an
entity in the other dataset.  Our datasets were provided by Foursquare
and Locu, and contain descriptive information about various venues
such as venue names and phone numbers.  

Rather than have you compete against yourself, we've turned this lab
into a competition: students will submit their best matching
algorihtms and try to beat one-another on a leaderboard to identify
the best algorithm.  You may enter this competition yourself or as a
team of up to 3 students.  We will give a nice prize to the winning
team or teams.

This lab uses several files for you to test your entity resolution algorithms on:
 * [locu_train.json](datasets/locu_train_hard.json)
 * [foursquare_train.json](datasets/foursquare_train_hard.json)
 * [matches_train.csv](datasets/matches_train_hard.csv)

The `json` files contain a json-encoded list of venue attribute
dictionaries.  The `csv` file contains two columns, `locu_id` and
`foursquare_id`, which reference the venue `id` fields that match in
each dataset.

Your job is to write a script that will load both datasets and
identify matching venues in each dataset.  Measure the [precision,
recall, and F1-score](https://en.wikipedia.org/wiki/F-score) of your
algorithm against the ground truth in `matches_train.csv`.  Once
you're satisfied with an algorithm that has high values for these
training data points, move on to the two test files:
 * [locu_test.json](datasets/locu_test_hard.json)
 * [foursquare_test.json](datasets/foursquare_test_hard.json)

Your job is to generate `matches_test.csv`, a mapping that looks like `matches_train.csv` but with mappings for the new test listings.  Here are a few notes:
 * The schemas for these datasets are aligned, but this was something that Locu and Foursquare engineers had to do ahead of time when we initially matched our datasets.
 * The two datasets don't have the same exact formatting for some fields: check out the `phone` field in each dataset as an example.  You'll have to normalize some of your datasets.
 * You might notice matches in matches_train.csv that you disagree with.  That's fair: our data comes from matching algorithms and crowds, both of which can be imperfect.  If you feel it makes your algorithm's training process better, feel free to blacklist (programmatically) certain training values.
 * There are many different features that can suggest venue similarity. Field equality is a good one: if the names or phone numbers of venues are equal, the venues might be equal.  But this is a relatively high-precision, low-recall feature (`Bob's Pizza` and `Bob's Pizzeria` aren't equal), and so you'll have to add other ones.  For example, [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) between two strings offers finer granularity of how similar two strings are.  At Locu we have many tens of features, ranging from field equality to more esoteric but useful ones (e.g., "Does the first numeric value in the address field match?").
 * Since there are many features, you need some way to combine them.  A simple weighted average of values, where more important values (similar names) are weighed more highly will get you quite far.  In practice, you'd want to build a classifier that takes these features and learns the weights based on the training data.  If you're using Python and want to build a classifier, check out [scikit-learn](http://scikit-learn.org/).  We've seen good results with the decision tree ensemble/random forest techniques.  Note that this step will take time, so only do it if you've hand-rolled your own reasonable matcher already.
 * It's possible to be near 1 for precision/recall/F1 with enough training data and good enough machine learning models, but this took Locu engineers several months to get right.
 * These datasets aren't too large, but in practice require matching several million venues across datasets.  Performing an `O(N^2)` comparison on all venues would take too long in those cases so some heuristics are needed to narrow down the likely candidates.
* There is no longer a one to one mapping (bijection) between entities in the Locu / foursquare data sets.  Some entities may have no matches.


# Submission Instructions

## Development Environment

For this lab, we've partnered with [Instabase](https://www.instabase.com/) to provide you with a hosted IPython environment. To get started, create an account on the [website](https://www.instabase.com/account/register) - make sure you sign up with your columbia email. After you've signed up, login and follow the steps below - 

1. Create a new repository. Give it a name / description of your liking and set the visibility to private.
2. Once the repo is created, click on the "collaborators" button on the sidebar and add `Prakhar` as a collaborator.
3. Lastly, create a new IPython notebook. For the purposes of this assignment, the datasets have already been uploaded on [Instabase](https://www.instabase.com/Prakhar/er-assignment/fs/Instabase%20Drive/files/datasets/).

To use the dataset in your notebook, you can use the following snippet of code - 

```python
import json

PATH = "Prakhar/er-assignment/fs/Instabase%20Drive/files/datasets/"
FILES = {
    "foursquare_test": "foursquare_test_hard.json",
    "locu_test": "locu_test_hard.json",
    "matches": "matches_train_hard.csv",
    "foursquare_train": "foursquare_train_hard.json",
    "locu_train": "locu_train_hard.json"
}

foursquare_test = json.loads(ib.open(PATH + FILES["foursquare_test"]).read())
print "total records:", len(foursquare_test)
```

**Installing packages**
The instabase platform already comes installed with the popular data-science and machine learning packages. To get the complete list, you can interact with the `bash` like so in your IPython notebook
```
%%bash
pip freeze
```
If you want to install a certain package that doesn't exist, you can install it on your own
```
%%bash
pip install requests
```
[Here's](https://www.instabase.com/user/Prakhar-nb/notebooks/Prakhar/er-assignment/fs/Instabase%20Drive/notebooks/hello-instabase/getting-started.ipynb) a sample IPython that shows you how can start on Instabase.

## Upload your best results to the leaderboard

To compete in the challenge, you should go to
[instabase leadearboard app](http://ec2-52-87-156-152.compute-1.amazonaws.com/). Once you have registered for an account, you can upload your results and also see the results of other students so that you can improve your algorithm and compete for the grand prize!

On the website, you will need to submit your result file (`matches_test.csv`) and the script/program that outputs this file. The format of the `matches_test.csv` should be exactly same as that of the given `matches_train_hard.csv` file. The script/program should be runnable from inside a directory containing the files `locu_train.json`, `foursquare_train.json`, `matches_train.csv`, `locu_test.json`,  and `foursquare_test.json`, and should output `matches_test.csv` based on these files. We will run your program against a set of hidden test data (that we have not provided) as a final test of the top few students' code.

*While we'll use `matches_test.csv` to identify the most promising submissions, only programs that run on the data and emit the best `matches_test.csv` on our machine will be considered for a prize.*

## Write up Instructions

In addition to competing in the challenge, please write a detailed explanation of what you have done in the IPython notebook itself (use the [markdown cell](http://jupyter-notebook.readthedocs.org/en/latest/examples/Notebook/rstversions/Working%20With%20Markdown%20Cells.html))

The write up should contain:

1. Your user name and registered email address on the competition site.
1. Answers to the following questions:
 * Describe your entity resolution technique, as well as its precision, recall, and F1 score.
 * What were the most important features that powered your technique?
 * How did you avoid pairwise comparison of all venues across both datasets?
