# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  # config.vm.box = "base"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Disable the default share of the current code directory. Doing this
  # provides improved isolation between the vagrant box and your host
  # by making sure your Vagrantfile isn't accessible to the vagrant box.
  # If you use this you may want to enable additional shared subfolders as
  # shown above.

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
  #
  #
  
  config.vm.synced_folder ".", "/vagrant", disabled: true
  
  config.vm.box = "ubuntu/jammy64"
  config.vm.box_version = "20241002.0.0"
  load_env(".env")
  # --- INVENTORY SERVICE ---
  config.vm.define "inventory-vm" do |inventory|
    inventory.vm.network "private_network", ip: "192.168.56.10"

    inventory.vm.synced_folder "./srcs/inventory-app", "/home/vagrant/inventory-app",
      type: "rsync",
      rsync__exclude: [".venv/", ".env"]
    
    inventory.vm.provision "shell" do |sh|
      sh.path = "scripts/provision_inventory.sh"
      sh.env = {
        "INVENTORY_HOST": ENV['INVENTORY_HOST'],
        "INVENTORY_PORT": ENV['INVENTORY_PORT'],
        "INVENTORY_DEBUG": ENV['INVENTORY_DEBUG'],
        "INVENTORY_MOVIES_DATABASE_URL": ENV['INVENTORY_MOVIES_DATABASE_URL'],
        "GATEWAY_IP": ENV['GATEWAY_IP'],
      }
    end
  end

  # --- BILLING SERVICE ---
  config.vm.define "billing-vm" do |billing|
    billing.vm.network "private_network", ip: "192.168.56.11"

    billing.vm.synced_folder "./srcs/billing-app", "/home/vagrant/billing-app",
      type: "rsync",
      rsync__exclude: [".venv/", ".env"]
    
    billing.vm.provision "shell" do |sh|
      sh.path = "scripts/provision_billing.sh"
      sh.env = {
        "BILLING_HOST": ENV['BILLING_HOST'],
        "BILLING_PORT": ENV['BILLING_PORT'],
        "BILLING_DEBUG": ENV['BILLING_DEBUG'],
        "GATEWAY_IP": ENV['GATEWAY_IP'],
        "RABBITMQ_HOST": ENV['RABBITMQ_HOST'],
        "RABBITMQ_PORT": ENV['RABBITMQ_PORT'],
        "RABBITMQ_USER": ENV['RABBITMQ_USER'],
        "RABBITMQ_PASS": ENV['RABBITMQ_PASS'],
        "RABBITMQ_QUEUE": ENV['RABBITMQ_QUEUE'],
        "BILLING_DATABASE_URL": ENV['BILLING_DATABASE_URL']
      }
    end
  end

  # --- GATEWAY SERVICE ---
  config.vm.define "gateway-vm" do |gateway|
    gateway.vm.network "private_network", ip: "192.168.56.12"
    gateway.vm.network "forwarded_port", guest: "5000", host: "5000"

    gateway.vm.synced_folder "./srcs/api-gateway", "/home/vagrant/api-gateway",
      type: "rsync",
      rsync__exclude: [".venv/", ".env"]

    gateway.vm.provision "shell" do |sh|
      sh.path = "scripts/provision_gateway.sh"
      sh.env = {
        "GATEWAY_HOST": ENV['GATEWAY_HOST'],
        "GATEWAY_PORT": ENV['GATEWAY_PORT'],
        "GATEWAY_DEBUG": ENV['GATEWAY_DEBUG'],
        "INVENTORY_IP": ENV['INVENTORY_IP'],
        "INVENTORY_PORT": ENV['INVENTORY_PORT'],
        "BILLING_IP": ENV['BILLING_IP'],
        "BILLING_PORT": ENV['BILLING_PORT'],
        "INVENTORY_SERVICE_URL": ENV['INVENTORY_SERVICE_URL'],
        "BILLING_SERVICE_URL": ENV['BILLING_SERVICE_URL'],
        "RABBITMQ_HOST": ENV['RABBITMQ_HOST'],
        "RABBITMQ_PORT": ENV['RABBITMQ_PORT'],  
        "RABBITMQ_USER": ENV['RABBITMQ_USER'],
        "RABBITMQ_PASS": ENV['RABBITMQ_PASS'],
        "RABBITMQ_QUEUE": ENV['RABBITMQ_QUEUE']
      }
    end
  end
end


def load_env(file_path = ".env")
  variables = {}
  if File.exist?(file_path)
    File.foreach(file_path) do |line|
      next if line.strip.empty? || line.strip.start_with?("#")
      
      key, value = line.strip.split('=', 2)
      
      if key && value
        clean_value = value.gsub(/^["']|["']$/, '')
        variables[key] = clean_value
        
        ENV[key] = clean_value
      end
    end
  else
    puts "Warning: #{file_path} not found. Using default settings."
  end
  variables
end