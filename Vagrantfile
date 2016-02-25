# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "hashicorp/precise64"
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get -yqq install python-pip python-dev protobuf-compiler sqlite3
    sudo pip install protobuf sqlalchemy
  SHELL
end
