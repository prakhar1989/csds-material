These are setup instructions for the [data structuring lab](./README.md)

You can either setup a local virtual machine, or run a virtual machine in Amazon EC2.

### Option 1: Local setup

Start by installing [Vagrant](https://www.vagrantup.com/downloads.html) and [Virtualbox](https://www.virtualbox.org/wiki/Downloads). If you've done the Hadoop homeworks, you should already have Virtualbox installed.

Once Vagrant is installed, check your installation by running `vagrant -v` on the command line. 
```
$ vagrant -v
Vagrant 1.7.4
```
The next step is to clone this repository on your computer.
```
$ git clone -b ewu-csds https://github.com/prakhar1989/csds-material 
```

**Starting the VM**

Now that we have everything, we can start the VM.

```
$ cd csds-material
$ vagrant up
```
You will see a stream of text run by on you on your screen. Vagrant will download the VM and install the required packages. If everything works as expected, you should now be able to `ssh` into your VM using `vagrant ssh` (Windows users will need to install a ssh client, e.g. Putty, to ssh into the VM. `vagrant ssh` command will provide you all the details, e.g. the IP, Port, Private key location etc. that you will have to manually enter in Putty). Remember, always `cd` into the directory containing the `Vagrantfile` for the Vagrant commands to work.

```
$ vagrant ssh
Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-generic x86_64)

 * Documentation:  https://help.ubuntu.com/
New release '14.04.4 LTS' available.
Run 'do-release-upgrade' to upgrade to it.

Welcome to your Vagrant-built virtual machine.
Last login: Fri Sep 14 06:23:18 2012 from 10.0.2.2

vagrant@precise64:~$  cd /vagrant

vagrant@precise64:/vagrant$ ls
createdb.py  encode.py  README.md  twitter.db  twitter.ddl  twitter.json.gz  twitter.pb  twitter_pb2.py  twitter_pb2.pyc  twitter.proto  Vagrantfile
```
Now that you're into the VM, the way to access the data that's on your host machine is via the `/vagrant` folder. By default, Vagrant will automatically enable sharing of the `/vagrant` folder between the guest and the host. `CD`ing into the `/vagrant` folder will show all your files.

You can now get started on working through the assignment.

**Stopping the VM** 

Once you are done with using the VM, disconnect from the VM (by hitting `Ctrl+D`), and then run `vagrant halt` to turn it off. Later when you want to resume work, just run `vagrant up` to start the VM from the directory that has the `Vagrantfile`.

### Option 2: EC2 setup

By using EC2 you can avoid potential local issues with vagrant and VirtualBox (like having to enable virtualization in the Windows BIOS or version mismatch errors). By using a small instance type, you can do this HW in the AWS cloud for free.

**Launch an EC2 instance**

In the AWS console, choose EC2. Click the "Launch Instance" button. In the Quick Start tab there will be an Ubutu image (Ubuntu Server 14.04 LTS (HVM), SSD Volume Type) that is labeled as "Free tier eligible". Select this instance type. Proceed to create the instance with all the other default options.

When click the "Launch" button, you will be given the create a new key pair and name it hw3. Download the key file to somewhere convenient on your machine.

**Connecting to the instance**

In a shell with an ssh client (the terminal works fine on a Mac), `cd` to the directory where the `.pem` file is saved. Run these commands to ssh to your EC2 instance:

```
$ chmod 400 hw3.pem
$ ssh -i "hw3.pem" ubuntu@YOUR_PUBLIC_DNS 
```
Your public DNS should look something like `ec2-11-111-11-11.us-west-2.compute.amazonaws.com`. AWS tells you this name when you create the instance, and you can subsequently find it in the Instances tab after selecting EC2 in the AWS console.

**Setting up tools on your instance**

From within your EC2 instance, run these commands to install the tools needed to complete the lab:

```
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
$ echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
$ sudo apt-get update
$ sudo apt-get -yqq install python-pip python-dev protobuf-compiler sqlite3 mongodb-org
$ sudo pip install protobuf sqlalchemy
$ sudo apt-get install git
$ git clone -b ewu-csds https://github.com/prakhar1989/csds-material
$ cd csds-material
```

**Shutting down the instance**

While there is no financial cost for leaving the instance running indefinitely, you'll probably want to shut it down when you're done. To terminate the instance, select EC2 in the AWS console, select the Instances tab, expand the Actions dropdown, and select Instance State > Terminate. (This cannot be undone!)
