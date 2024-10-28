---
title: "Proxmox Template for Cloud-init"
date: 2024-10-28
description: "Maybe VM's aren't so bad after all"
tags: [documentation, cloud-init]
---
## Overview
1. Cloud-init can be used to create templates for VM's. This simplifies the OS part of creating a VM, allows you to import public keys, and define default resources

Inspiration from Techno Tim and Jim's Garage's videos:

{{< youtube id="shiIi38cJe4" title="Techno Tim's video on Cloud-Init" >}}

{{< youtube id="Kv6-_--y5CM" title="Jim Garage's video on Cloud-Init" >}}


## Creating the VM:
1. Download ISO: [noble-server-cloudimg-amd64.img](https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img)
2. Create VM via CLI
```bash
cd /var/lib/vz/template/iso
wget https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img

qm create 9000 --memory 4096 --core 2 --name ubuntu-cloud --net0 virtio,bridge=vmbr0
cd /var/lib/vz/template/iso
qm disk import 9000 noble-server-cloudimg-amd64.img nvme
qm set 9000 --cpu host
qm set 9000 --scsihw virtio-scsi-pci --scsi0 nvme:vm-9000-disk-0,ssd=1
qm set 9000 --ide2 nvme:cloudinit
qm set 9000 --boot c --bootdisk scsi0
qm set 9000 --serial0 socket --vga serial0
qm set 9000 --agent enabled=1,fstrim_cloned_disks=1
qm set 9000 --ipconfig0 ip6=auto,ip=dhcp
qm set 9000 --ciuser jeff
qm disk resize 9000 scsi0 32G
```
3. Add in your SSH public keys for the Ansible host and Macbook
4. Right click and create a template using this VM