# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
        # Node R1 configuration
	config.vm.define "hosta" do |hosta|
		hosta.vm.box = "generic/ubuntu1804"
		hosta.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")
		hosta.vm.network "private_network", ip: "10.0.0.2", virtualbox__intnet: "netv4a"
		hosta.vm.network "forwarded_port", guest: 30001, host: 30001
		hosta.vm.network "forwarded_port", guest: 30091, host: 30091
		hosta.vm.provider "virtualbox" do |virtualbox|
			virtualbox.memory = "4096"
			virtualbox.cpus = "2"
			# virtualbox.customize ['modifyvm', :id, '--nictrace2', 'on'] 
			# virtualbox.customize ['modifyvm', :id, '--nictracefile2', 'tracea.pcap']
			virtualbox.customize ['modifyvm', :id, '--cableconnected1', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected2', 'on']
		end
		hosta.vm.provision "shell", path: "config/config_a.sh"
        end

	config.vm.define "hosta1" do |hosta1|
		hosta1.vm.box = "generic/ubuntu1804"
		hosta1.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")
		hosta1.vm.network "private_network", ip: "10.0.0.3", virtualbox__intnet: "netv4a"
		hosta1.vm.provider "virtualbox" do |virtualbox|
			virtualbox.memory = "4096"
			virtualbox.cpus = "2"
			# virtualbox.customize ['modifyvm', :id, '--nictrace2', 'on'] 
			# virtualbox.customize ['modifyvm', :id, '--nictracefile2', 'tracea1.pcap']
			virtualbox.customize ['modifyvm', :id, '--cableconnected1', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected2', 'on']
		end
		hosta1.vm.provision "shell", path: "config/config_a1.sh"
        end
        
	config.vm.define "hostb" do |hostb|
		hostb.vm.box = "generic/ubuntu1804"
		hostb.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")
		hostb.vm.network "private_network", ip: "10.0.1.2", virtualbox__intnet: "netv4b"
		hostb.vm.network "forwarded_port", guest: 30002, host: 30002
		hostb.vm.network "forwarded_port", guest: 30092, host: 30092
		hostb.vm.provider "virtualbox" do |virtualbox|
			virtualbox.memory = "4096"
			virtualbox.cpus = "2"
			# virtualbox.customize ['modifyvm', :id, '--nictrace2', 'on'] 
			# virtualbox.customize ['modifyvm', :id, '--nictracefile2', 'traceb.pcap']
			virtualbox.customize ['modifyvm', :id, '--cableconnected1', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected2', 'on']
		end
		hostb.vm.provision "shell", path: "config/config_b.sh"
        end

	config.vm.define "hostb1" do |hostb1|
		hostb1.vm.box = "generic/ubuntu1804"
		hostb1.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")
		hostb1.vm.network "private_network", ip: "10.0.1.3", virtualbox__intnet: "netv4b"
		hostb1.vm.provider "virtualbox" do |virtualbox|
			virtualbox.memory = "4096"
			virtualbox.cpus = "2"
			# virtualbox.customize ['modifyvm', :id, '--nictrace2', 'on'] 
			# virtualbox.customize ['modifyvm', :id, '--nictracefile2', 'traceb.pcap']
			virtualbox.customize ['modifyvm', :id, '--cableconnected1', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected2', 'on']
		end
		hostb1.vm.provision "shell", path: "config/config_b1.sh"
        end
        
	# Node R1 configuration
	config.vm.define "r1" do |r1|
		r1.vm.box = "generic/ubuntu1804"
		r1.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")

		r1.vm.network "private_network", ip: "2001:10::2",netmask: "64", virtualbox__intnet: "net10"
		r1.vm.network "private_network", ip: "2001:12::1",netmask: "64", virtualbox__intnet: "net12"
		r1.vm.network "private_network", ip: "2001:13::1",netmask: "64", virtualbox__intnet: "net13"

		r1.vm.provider "virtualbox" do |virtualbox|
			virtualbox.memory = "512"
			virtualbox.customize ['modifyvm', :id, '--nictrace2', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile2', './package/trace18.pcap']
			virtualbox.customize ['modifyvm', :id, '--nictrace3', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile3', './package/trace19.pcap']
			virtualbox.customize ['modifyvm', :id, '--nictrace4', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile4', './package/trace110.pcap']
			virtualbox.customize ['modifyvm', :id, '--cableconnected1', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected2', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected3', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected4', 'on']

		end
		r1.vm.provision "shell", path: "config/config_r1.sh"
	end

	# Node R2 configuration
	config.vm.define "r2" do |r2|
		r2.vm.box = "generic/ubuntu1804"
        r2.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")
		r2.vm.network "private_network", ip: "2001:12::2",netmask: "64", virtualbox__intnet: "net12"
		r2.vm.network "private_network", ip: "2001:24::1",netmask: "64", virtualbox__intnet: "net24"
		r2.vm.network "private_network", ip: "2001:25::1",netmask: "64", virtualbox__intnet: "net25"

		r2.vm.provider "virtualbox" do |virtualbox|
			virtualbox.memory = "512"
			virtualbox.cpus = "1"
			virtualbox.customize ['modifyvm', :id, '--nictrace2', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile2', './package/trace28.pcap']
			virtualbox.customize ['modifyvm', :id, '--nictrace3', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile3', './package/trace29.pcap']
			virtualbox.customize ['modifyvm', :id, '--nictrace4', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile4', './package/trace210.pcap']
			virtualbox.customize ['modifyvm', :id, '--cableconnected1', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected2', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected3', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected4', 'on']
		end
		r2.vm.provision "shell", path: "config/config_r2.sh"
	end

        # Node R3 configuration
        config.vm.define "r3" do |r3|
        r3.vm.box = "generic/ubuntu1804"
		r3.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")
		r3.vm.network "private_network", ip: "10.0.0.1", virtualbox__intnet: "netv4a"
        r3.vm.network "private_network", ip: "2001:13::2",netmask: "64", virtualbox__intnet: "net13"
		r3.vm.network "private_network", ip: "2001:35::1",netmask: "64", virtualbox__intnet: "net35"
		r3.vm.provider "virtualbox" do |virtualbox|
			virtualbox.memory = "2048"
			virtualbox.customize ['modifyvm', :id, '--nictrace2', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile2', './package/trace38.pcap']
			virtualbox.customize ['modifyvm', :id, '--nictrace3', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile3', './package/trace39.pcap']
			virtualbox.customize ['modifyvm', :id, '--nictrace4', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile4', './package/trace310.pcap']

			virtualbox.customize ['modifyvm', :id, '--cableconnected1', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected2', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected3', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected4', 'on']

                end
	        r3.vm.provision "shell", path: "config/config_r3.sh"
        end

	# Node R4 configuration
	config.vm.define "r4" do |r4|
		r4.vm.box = "generic/ubuntu1804"
        r4.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")
		r4.vm.network "private_network", ip: "2001:24::2",netmask: "64", virtualbox__intnet: "net24"
		r4.vm.network "private_network", ip: "2001:46::1",netmask: "64", virtualbox__intnet: "net46"

		r4.vm.provider "virtualbox" do |virtualbox|
			virtualbox.memory = "512"
			virtualbox.cpus = "1"
			virtualbox.customize ['modifyvm', :id, '--nictrace2', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile2', './package/trace48.pcap']
			virtualbox.customize ['modifyvm', :id, '--nictrace3', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile3', './package/trace49.pcap']

			virtualbox.customize ['modifyvm', :id, '--cableconnected1', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected2', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected3', 'on']
		end
		r4.vm.provision "shell", path: "config/config_r4.sh"
	end

	# Node R5 configuration
	config.vm.define "r5" do |r5|
		r5.vm.box = "generic/ubuntu1804"
        r5.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")
		r5.vm.network "private_network", ip: "2001:25::2",netmask: "64", virtualbox__intnet: "net25"
		r5.vm.network "private_network", ip: "2001:35::2",netmask: "64", virtualbox__intnet: "net35"
		r5.vm.network "private_network", ip: "2001:56::1",netmask: "64", virtualbox__intnet: "net56"

		r5.vm.provider "virtualbox" do |virtualbox|
			virtualbox.memory = "512"
			virtualbox.cpus = "1"
			virtualbox.customize ['modifyvm', :id, '--nictrace2', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile2', './package/trace58.pcap']
			virtualbox.customize ['modifyvm', :id, '--nictrace3', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile3', './package/trace59.pcap']
			virtualbox.customize ['modifyvm', :id, '--nictrace4', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile4', './package/trace510.pcap']
			virtualbox.customize ['modifyvm', :id, '--cableconnected1', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected2', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected3', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected4', 'on']
		end
		r5.vm.provision "shell", path: "config/config_r5.sh"
	end

	# Node R6 configuration
	config.vm.define "r6" do |r6|
		r6.vm.box = "generic/ubuntu1804"
        r6.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")
		r6.vm.network "private_network", ip: "10.0.1.1", virtualbox__intnet: "netv4b"
		r6.vm.network "private_network", ip: "2001:46::2",netmask: "64", virtualbox__intnet: "net46"
		r6.vm.network "private_network", ip: "2001:56::2",netmask: "64", virtualbox__intnet: "net56"

		r6.vm.provider "virtualbox" do |virtualbox|
			virtualbox.memory = "2048"
			virtualbox.cpus = "1"
			virtualbox.customize ['modifyvm', :id, '--nictrace2', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile2', './package/trace68.pcap']
			virtualbox.customize ['modifyvm', :id, '--nictrace3', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile3', './package/trace69.pcap']
			virtualbox.customize ['modifyvm', :id, '--nictrace4', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile4', './package/trace610.pcap']
			virtualbox.customize ['modifyvm', :id, '--cableconnected1', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected2', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected3', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected4', 'on']
		end
		r6.vm.provision "shell", path: "config/config_r6.sh"
	end

	# Node R0 configuration
	config.vm.define "r0" do |r0|
		r0.vm.box = "generic/ubuntu1804"
        r0.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")
		r0.vm.network "private_network", ip: "10.0.114.1", virtualbox__intnet: "netv4cli"
		r0.vm.network "private_network", ip: "2001:b::1",netmask: "64", virtualbox__intnet: "netv6cli"
		r0.vm.network "private_network", ip: "2001:10::1",netmask: "64", virtualbox__intnet: "net10"

		r0.vm.provider "virtualbox" do |virtualbox|
			virtualbox.memory = "2048"
			virtualbox.cpus = "1"
			virtualbox.customize ['modifyvm', :id, '--nictrace2', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile2', './package/trace08.pcap']
			virtualbox.customize ['modifyvm', :id, '--nictrace3', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile3', './package/trace09.pcap']
			virtualbox.customize ['modifyvm', :id, '--nictrace4', 'on'] 
			virtualbox.customize ['modifyvm', :id, '--nictracefile4', './package/trace010.pcap']
			virtualbox.customize ['modifyvm', :id, '--cableconnected1', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected2', 'on']
			virtualbox.customize ['modifyvm', :id, '--cableconnected3', 'on']
		end
		r0.vm.provision "shell", path: "config/config_r0.sh"
	end

        # client configuration
        config.vm.define "client" do |client|
            client.vm.box = "generic/ubuntu1804"
            client.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")
			client.vm.network "private_network", ip: "10.0.114.2", virtualbox__intnet: "netv4cli"
			
            client.vm.provider "virtualbox" do |virtualbox|
				virtualbox.memory = "1024"
				virtualbox.cpus = "1"
				virtualbox.customize ['modifyvm', :id, '--nictrace2', 'on'] 
				virtualbox.customize ['modifyvm', :id, '--nictracefile2', './package/traceclientv4.pcap']
				virtualbox.customize ['modifyvm', :id, '--cableconnected1', 'on']
				virtualbox.customize ['modifyvm', :id, '--cableconnected2', 'on']
				
			end
	        client.vm.provision "shell", path: "config/config_client.sh"
        end

		# controller configuration
        config.vm.define "controller" do |controller|
            controller.vm.box = "generic/ubuntu1804"
            controller.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")
            controller.vm.network "private_network", ip: "2001:b::2",netmask: "64", virtualbox__intnet: "netv6cli"
			
            controller.vm.provider "virtualbox" do |virtualbox|
				virtualbox.memory = "512"
				virtualbox.cpus = "1"
				virtualbox.customize ['modifyvm', :id, '--nictrace2', 'on'] 
				virtualbox.customize ['modifyvm', :id, '--nictracefile2', './package/tracecontrv6.pcap']
				virtualbox.customize ['modifyvm', :id, '--cableconnected1', 'on']
				virtualbox.customize ['modifyvm', :id, '--cableconnected2', 'on']
			end
	        controller.vm.provision "shell", path: "config/config_ctr.sh"
        end
end
