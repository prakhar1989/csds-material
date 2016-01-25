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

Open the terminal in the VM so that you can start running commands. Linux and Mac users can also SSH into the machine by running `ssh training@ip-address` and entering the password - `training`. To get the IP address of the machine, just run `ifconfig` and taking note of the inet addr.

![ip](http://i.imgur.com/VUMJkVy.png)

```
$ cd ~/Desktop
$ git clone https://github.com/prakhar1989/csds-material
```

