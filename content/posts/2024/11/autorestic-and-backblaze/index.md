---

title: "Autorestic and Backblaze"

date: 2024-11-19

description: "RAID is not a backup."

tags: [backup]

---

## 3-2-1

This boils down to having an on-site backup and an off-site backup. For some time, I put off having an off-site backup, which back fired horribly. Since then, I got a NAS which provides a layer of redundancy using SHR-1 (RAID 5 equivalent), but this still leaves me vulnerable in the event something happens to my home.

## Current backup strategy

This strategy is not set in stone, and there are things I want to revisit later. If I were to rate my confidence in this solution, I would place it at a 8/10. While I'm confident of the setup, I want to ensure that I'm ready to restore when necessary and protect myself from ransomware attacks.
### Proxmox Backup Server

Running Proxmox as my hypervisor meant that Proxmox Backup Server was a natural first choice. This currently runs on my Synology NAS within a VM. Previously, I had it installed as a LXC, but you can also run this on baremetal. I do not keep a ton of backups at this time, but my pruning rules are to keep the last 7 daily backups, and 4 weekly backups. I don't see myself going that far back for backups, although I may reconsider this because it doesn't hurt to do so.

The backups run everyday during off hours (1am) for all of my VMs and containers. They take about 1 minute to complete the backup, and handle deduplication well resulting in a 24.20 deduplication factor. Notifications are sent via SMTP to my email, which provides visibility on the status of the backups. 

Restoring from this is as simple as adding the PBS server to the Proxmox host, and using the UI to selectively restore what VMs/LXCs you want to restore. Overall, this process is good, but I had a hard time figuring out how I'd like to keep this backed up off-site. This ultimately led me to Restic.
### Restic/Autorestic

Restic is up there in terms of backup solutions on GitHub, and after getting it set up, I believe for good reason. To get it setup I used their documentation which is very thorough and easy to follow. Essentially, you setup a repository, which is similar to a datastore in PBS. Your backups are encrypted using a password defined upon creation. From there, deduplication and pruning are similar.

After getting the basics of Restic down, I integrated Autorestic because I liked the concept of having a config file and its integration of docker volume backups. It also provides a cron job feature, but I am not currently using it. Related to the docker volume feature, I was hoping to use their hooks feature to stop the docker containers with a named volume before backing them up. Since hooks are bonded to the location (directory path) that is backed up, backing up Planka for example would involve restarting the container 4 times since the docker volumes are separated. I ended up using a bash script which stops all docker containers with named volumes, then runs a restic backup, then restarts those containers.

### On-site: Synology

So far, I am happy with the Synology DS923+ I got. It was straight forward to get set up, and has been fairly stable. With 36TB of usable space, I have plenty of room for hoarding. This includes media, documents, and homelab related data. While there have been some concerns recently about security, this is not accessible from outside my network.

### Off-site: Backblaze B2

Backblaze B2 was an attractive options since its integrated in a lot of backup applications, and the prices are reasonable ($6/TB/month) compared to S3. They previously charged more for egress, but now you have free 3x monthly egress. The only thing I have to look out for is pruning which can include a lot of downloads.

## Going forward

Documentation is always a goal, and I intend to go back and create a cheatsheet I can refer to and rely on because all these commands are not memorable. I also need to go back and automate the check and prune functions for Restic. Lastly, I plan to backup more personal data, like my Obsidian vault, in the event iCloud decides to do something less than ideal.
