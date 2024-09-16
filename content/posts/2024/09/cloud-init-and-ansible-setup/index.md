---
title: "Cloud-init and Ansible Setup"
date: 2024-09-16
description: "Step 1 of trying to automate things so a catastrophic failure does not ruin us."
tags: [documentation, ansible]
---
## Overview
1. Cloud-init can be used to create templates for VM's. This simplifies the OS part of creating a VM, allows you to import public keys, and define default resources
2. Ansible can be used to further setup the VM configuration wise. In this doc, Ansible is responsible for installing Docker, its dependencies, and other packages possibly needed

Inspiration from Techno Tim and Jim's Garage's videos:

{{< youtube id="shiIi38cJe4" title="Techno Tim's video on Cloud-Init" >}}

{{< youtube id="Kv6-_--y5CM" title="Jim Garage's video on Cloud-Init" >}}


## Creating the VM:
1. Download ISO: [noble-server-cloudimg-amd64.img](https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img)
2. Create VM via CLI
```bash
qm create 200 --memory 4096 --core 2 --name ubuntu-cloud --net0 virtio,bridge=vmbr0
cd /var/lib/vz/template/iso/
qm importdisk 200 noble-server-cloudimg-amd64.img local-zfs
qm set 200 --scsihw virtio-scsi-pci --scsi0 local-zfs:vm-200-disk-0
qm set 200 --ide2 local-zfs:cloudinit
qm set 200 --boot c --bootdisk scsi0
qm set 200 --serial0 socket --vga serial0
```
3. Configure the VM via GUI: memory ballooning off, 32gb storage, CPU host type, 32gb storage (add 28.5gb from 3.5 storage default)
4. Cloud-init settings: user, password, ssh public key, and network DHCP
5. Turn the VM into a template, and then you can full-clone it to make new machines

## Ansible Setup:
*(Revisit for setting up Ansible from scratch again)*
### setup.yaml
```yaml
---
- name: Set up Docker on Ubuntu
  hosts: all
  become: true
  tasks:
    - name: Update apt package index
      ansible.builtin.apt:
        update_cache: yes

    - name: Install dependencies for Docker
      ansible.builtin.apt:
        name:
          - qemu-guest-agent
          - build-essential
          - apt-transport-https
          - ca-certificates
          - curl
          - software-properties-common
        state: present

    - name: Add Docker GPG key
      ansible.builtin.apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
        state: present

    - name: Add Docker repository
      ansible.builtin.apt_repository:
        repo: "deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ ansible_lsb.codename }} stable"
        state: present

    - name: Install Docker CE
      ansible.builtin.apt:
        name: docker-ce
        state: present
        update_cache: yes
    
    - name: Add user to docker group
      ansible.builtin.user:
        name: "{{ ansible_user }}"
        groups: docker
        append: yes

    - name: Ensure Docker is started and enabled at boot
      ansible.builtin.systemd:
        name: docker
        enabled: yes
        state: started

    - name: Reboot the VM
      ansible.builtin.reboot:
        msg: "Reboot initiated by Ansible playbook for Docker setup."
        reboot_timeout: 300  # Timeout in seconds to wait for the reboot

```
### inventory.yaml
```yaml
ubuntu_vms:
  hosts:
    docker-dev:
      ansible_host: {ip_address}
      ansible_user: {user}
      ansible_ssh_private_key_file: ~/.ssh/id_rsa
      ansible_become: true
      ansible_become_method: sudo
```

### Running the playbook
```bash
ssh-keyscan -H {ip_address} >> ~/.ssh/known_hosts
ansible-playbook -i inventory.yaml setup.yaml --ask-pass --ask-become-pass
```
- ssh-keyscan will add the new VM's fingerprint so it avoids the initial host-key verification popup

## Updates to the general ecosystem

1. A smaller VM id 113 (docker-v3) with 2 cores / 4gb ram, and 32gb storage comes into the mix, running `Actual + IT-Tools`
2. Original VM id 102 (docker) with 4 cores, 32gb ram, and 128gb storage remains, focused on other services (`*arr stack, sabznbd <--- resource hog, and changedetection`)
3. Other services still run on seperate LXCs, which I want to look into how to backup and restore that gracefully outside of PBS