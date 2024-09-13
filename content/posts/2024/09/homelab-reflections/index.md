---
title: "Homelab reflections"
date: 2024-09-06
description: "Computers. Time. Learning."
tags: [homelab, hugo]
---

## Introduction: High ceiling hobbies
This self-hosting journey started last year with a tiny Dell Optiplex 7050 Micro and a dream. Before that, my Plex setup was literally running on my Macbook Pro. Obviously 4k files would wreak havoc on my puny non-upgradeable SSD, so a Sandisk Extreme Portable SSD was soon added into the mix. Eventually, I got tired of this, because it just felt silly.

That summer, I browsed r/homelab and found a semi-expensive hobby to add to my list (cycling, cooking, etc.). Now, I’ve always seen huge rack servers, but that’s obviously impractical because where the hell am I suppose to put that, and how am I going to pay for the electricity needed to keep it runnning?

## Micro PCs
![Amazon - Optiplex](https://m.media-amazon.com/images/I/51muPv+cJzL._AC_UF894,1000_QL80_.jpg)


Pretty much everyone on r/homelab is a micro PC megacluster-er or has a datacenter inside of place of residence. Either way, I leaned towards micro PCs since it only took about $400 to get started. This included:

- Dell Optiplex 7050 Micro (i5 6500t, 16gb, 512gb SSD): $150
- WD Elements 16tb External HDD: $250

Nothing ever stays that cheap however! Ever since I started working as a GRA, I needed to upgrade to 64gb of RAM since loading the NPI registry would OOM the machine quickly. Also, quickly realized the 6500t was not going to be capable of HW transcsoding 4k HEVC, so a 7500t came into the picture. This brings up the running cost to:

- 2x32gb RAM: $120
- i5 7500t: $40
- Current total: $580
Not bad!

What are we hosting?
## Phase 1 - Media
- Proxmox
- Plex
- Sonarr
- Radarr
- SABnzbd

I could not be more creative than this: the dream really starting with the *arrs, Plex, and SABnzbd because the primary goal was always a media server. Flashback to 2016: I remember using seedboxes and getting a dedi hosted on OVH or Hetzner from andy10gbit :) good times.

## Phase 2 - Life?
- Acutal Budget
- Stirling-PDF
- Dashy
- DuckDNS
- Gotify
- InfluxDB
- Grafana
- Prometheus[^1]
- Proxmox Backup Server
- Caddy

Phase 2 was a deviation from the media server function, but in a good way. Actual Budget is an amazing YNAB alternative, and helps me keep track of my spending in a proactive manner. Stirling-PDF came in handy when I needed to fix some of the accounting slides (to be honest, don’t use this THAT much but it’s nice to have).

{{< youtube 85ME8i4Ry6A >}}

Moving onto the monitoring part, I was inspired by a video by Techno Tim where he went over how to setup alerts because a hard drive failed for him. Now that was setup, Proxmox Backup Server came into the picture since the idea of losing ALL of my progress setting things up would be terrible!

Gotify was an easy cop-out of a notification server (which was intended to server PBS, Radarr, and Sonarr notifcations), but honestly I do not find myself checking it that much. Having PBS send emails to a gmail account setup for it has been more useful.

Grafana, at its current implementation state, is superfluous since it’s a prettier version of Proxmox’s current dashboard.

Caddy was a surprising one for me since I thought reverse proxies for a long time were hard to implmeent, but now that I’m the proud owner of jeffdao.com I can say that’s not the case anymore.

## Phase 3: Hugo???
BOY it shouldn’t have been this hard to setup. Why didn’t Snap work that well in a LXC without nesting, FUSE, and being priveleged? I don’t know honestly, but even when it worked snap was just annoying to use with Hugo so I scrapped that idea.

I’m still wrapping my head around how exactly this blog is going to work into my current flow of consciousness but one thing I need to do is work on standardizing deployment of services because if I ever have to redeploy this entire server, it will take some time.

## What now?
Well first things first, Hugo most likely won’t stay on this LXC its on forever, and I need to get it pointed towards blog.jeffdao.com via Caddy. Probably worth learning how exactly Hugo’s workflow would look like from creation to publishing.

Second, locking down the server since I have Caddy setup now is up there in terms of priorities, most likely using Authelia

Third, I need to standardize deployments beyond Tteck scripts, as much as I love them. Setting up Hugo was a HUGE pain in the ass, and making sure those steps are repeatable is crucial for my sanity.

[^1]: Still have yet to set this up, since InfluxDB –> Proxmox metric server integrates well.