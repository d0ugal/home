VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu-x64-1204"
  config.vm.provision "shell", path: "bootstrap.sh"
  config.vm.network :private_network, ip: "192.168.200.11"

end
