# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "docker-sandbox" do |sandbox|
    
    sandbox.vm.box = "bento/ubuntu-24.04"
    sandbox.vm.box_version = "202510.26.0"
    sandbox.vm.network "forwarded_port", guest: 3000, host: 3000

    sandbox.vm.provider "virtualbox" do |vb|
      vb.name = "docker-sandbox"
      vb.memory = "2048"
      vb.cpus = 2
    end

    sandbox.vm.provision "shell", path: "scripts/setup_docker.sh"
  end
end