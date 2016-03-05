These are setup instructions for the [data structuring lab](./README.md)


### Setup

To setup the tools required for this lab, you'll be running a preconfigured VM that has been made especially for this lab.
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
You will see a stream of text run by on you on your screen. Vagrant will download the VM and install the required packages. If everything works as expected, you should now be able to `ssh` into your VM using `vagrant ssh`. Remember, always `cd` into the directory containing the `Vagrantfile` for the Vagrant commands to work.

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


