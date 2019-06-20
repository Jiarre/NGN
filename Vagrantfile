# -*- mode: ruby -*-
# vi: set ft=ruby :
# About: Vagrant file for the development environment

###############
#  Variables  #
###############

CPUS = 2
RAM = 2048

# Bento: Packer templates for building minimal Vagrant baseboxes
# The bento/ubuntu-18.04 is a small image of 500 MB, fast to download
BOX = "bento/ubuntu-18.04"
BOX_VER = "201906.18.0"
VM_NAME = "ubuntu-18.04-comnetsemu"

######################
#  Provision Script  #
######################

# Common bootstrap
$bootstrap= <<-SCRIPT
# Install dependencies
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y git pkg-config gdb tmux sudo make
sudo apt-get install -y bash-completion htop dfc
sudo apt-get install -y iperf iperf3
sudo apt-get install -y python3-pip
SCRIPT

$setup_x11_server= <<-SCRIPT
sudo apt-get install -y xorg
sudo apt-get install -y openbox
SCRIPT

####################
#  Vagrant Config  #
####################

if Vagrant.has_plugin?("vagrant-vbguest")
  config.vbguest.auto_update = false
end


Vagrant.configure("2") do |config|

  config.vm.define "comnetsemu" do |comnetsemu|

    comnetsemu.vm.hostname = "comnetsemu"
    comnetsemu.vm.box = BOX
    comnetsemu.vm.box_version = BOX_VER
    comnetsemu.vm.box_check_update = true

    # Sync ./ to home dir of vagrant to simplify the install script
    comnetsemu.vm.synced_folder ".", "/vagrant", disabled: true
    comnetsemu.vm.synced_folder ".", "/home/vagrant/comnetsemu"

    # Workaround for vbguest plugin issue
    comnetsemu.vm.provision "shell", run: "always", inline: <<-WORKAROUND
    modprobe vboxsf || true
    WORKAROUND

    comnetsemu.vm.provision :shell, inline: $bootstrap, privileged: false
    comnetsemu.vm.provision :shell, inline: $setup_x11_server, privileged: false

    comnetsemu.vm.provision "shell",privileged: false,inline: <<-SHELL
      cd /home/vagrant/comnetsemu/util || exit
      PYTHON=python3 ./install.sh -a

      cd /home/vagrant/comnetsemu/ || exit
      # setup.py develop installs the package (typically just a source folder)
      # in a way that allows you to conveniently edit your code after it’s
      # installed to the (virtual) environment, and have the changes take
      # effect immediately. Convinient for development
      sudo make develop

      # Build images for Docker hosts
      cd /home/vagrant/comnetsemu/test_containers || exit
      bash ./build.sh
    SHELL

    # Enable X11 forwarding
    comnetsemu.ssh.forward_agent = true
    comnetsemu.ssh.forward_x11 = true

    # VirtualBox-specific configuration
    comnetsemu.vm.provider "virtualbox" do |vb|
      vb.name = VM_NAME
      vb.memory = RAM
      vb.cpus = CPUS
      # MARK: The CPU should enable SSE3 or SSE4 to compile DPDK
      vb.customize ["setextradata", :id, "VBoxInternal/CPUM/SSE4.1", "1"]
      vb.customize ["setextradata", :id, "VBoxInternal/CPUM/SSE4.2", "1"]
    end
  end

end
