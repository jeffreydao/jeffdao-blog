---

title: "Emergency Preparedness: Learning from Mistakes"

date: 2024-11-04

description: "There's a first time for everything"

tags: [homelab, backup]

---

  

## Failing drives

For whatever reason, disaster struck last month. All of a sudden, both my NVMe drive and my WD Elements external HDD decided they had enough. This was only discovered after an Xfinity outage, the trusty Optiplex 7050 refused to boot. The NVMe drive was where all of the Proxmox and VM related data was, while the WD Elements had all of my media.

  

## Emergency preparedness, or lack thereof

My backup solution isn't compliant with the 3-2-1 strategy, but it was luckily enough. `Proxmox Backup Server` is the heart of it all, and it was running as an LXC on the same machine. While this goes against recommendations, it was sufficient at the time because it was stored on the WD Elements drive. I also repurposed a Sandisk Extreme portable SSD and had switched PBS to use that instead.

While rebuilding the homelab core infra wasn't hard, it would have been nice to have done a restore drill beforehand. First, replacing the storage for the Optiplex included two drives:

1. SATA SSD Boot Drive: [TEAMGROUP Vulcan Z 256GB](https://www.amazon.com/dp/B0B6ZCMSQ3?_encoding=UTF8&th=1)
2. NVMe VM Storage Drive: [TEAMGROUP MP44L 1TB](https://a.co/d/dEL8998)

While separating the boot and VM drives wasn't exactly necessary, it would have been nice to not have to reinstall Proxmox when the time came. Once I was back up and running, all it came down to was creating a new PBS container, and restoring the data. Turns out PBS does not like adding existing datastores all that much, so what worked for me was creating a new datastore, deleting the folder where it was, and then moving my existing datastore into that folder, which worked. From there, Proxmox Backup Server took care of the rest.
## Synology DS923+: 36~TB usable

The WD Elements was never meant to be the main storage device, but it was the cheapest and lowest effort way to lots of storage for cheap. There was no redundancy with this since I had only one drive, which led me to where I was. Luckily, the Synology DS923+ was on sale recently at B&H Photos, and refurbished drives from [serverpartdeals.com](https://serverpartdeals.com/) are always available.

- Synology DS923+: $519.59
- 4 x Western Digital Ultrastar DC HC530: $584.51
- Total Cost: *$1,104.1*

I would've loved to go down the path of getting a workstation like the HP Z640 or Dell T7820. Getting the Synology setup, however, I understand the appeal of having something that just works. I must give [Derek Seaman's guide on setting up PBS on a Synology VM](https://www.derekseaman.com/2023/04/how-to-setup-synology-nfs-for-proxmox-backup-server-datastore.html) credit, since PBS is finicky with permissions...
## Going forward: cloud backups

The backup strategy still does not meet the 3-2-1 rule of 3 copies (original + 2 copies), 2 types of media, and 1 copy off-site. The missing piece to the puzzle is setting up a cloud storage solution, which I'm exploring Backblaze B2 + Restic as a solution. I'm lucky the external drive saved the day this time, but having an off-site copy for PBS + other items on my NAS would be ideal in case all hell breaks loose.
