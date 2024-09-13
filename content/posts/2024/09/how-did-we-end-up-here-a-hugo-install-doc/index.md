---
title: "How did we end up here? A Hugo install doc"
date: 2024-09-09
description: "Come back and flesh this out or else."
tags: [homelab, hugo, documentation]
---

# High level overview:
- [x] Setup Ubuntu 24.04 LXC
- [x] Setup Hugo + dependencies (Git, Go, and Sass)
- [x] Create the site, and import the theme + any relevant notes/configs
- [x] Using rsync to send the public folder to the Caddy LXC
- [x] Setting up a GitHub repository for the blog
- [ ] Get rich quick using the Chase money glitch


## LXC Setup

```
## Run on PVE host

bash -c "$(wget -qLO - https://github.com/tteck/Proxmox/raw/main/ct/ubuntu.sh)"

# SSH into the LXC

cd .ssh
nano authorized_keys

## Copy and paste your public key

## Generate key-pair to setup ssh with Caddy LXC
ssh-keygen -t rsa -b 4096
nano config 

### Add the Caddy LXC with the following format
Host caddy
    HostName {ip}
    User {user} # root most likely

### On the Caddy LXC copy the public key
nano /root/.ssh/authorized_keys

```

## Pre-reqs for Hugo
```
## Git

apt-get install git-all
git config --global user.email jeffreydao7@gmail.com
git config --global user.name 'Jeffrey Dao'
git config --global init.defaultBranch main

## Go https://go.dev/dl/

wget https://go.dev/dl/go1.23.1.linux-amd64.tar.gz

rm -rf /usr/local/go && tar -C /usr/local -xzf go1.23.1.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

go version

## Dart Sass

wget https://github.com/sass/dart-sass/releases/download/1.78.0/dart-sass-1.78.0-linux-x64.tar.gz

rm -rf /usr/local/dart-sass && tar -C /usr/local -xzf dart-sass-1.78.0-linux-x64.tar.gz

export PATH=$PATH:/usr/local/dart-sass

sass --version

## Hugo

wget https://github.com/gohugoio/hugo/releases/download/v0.134.1/hugo_extended_0.134.1_linux-amd64.tar.gz

rm -rf /usr/local/bin/hugo && tar -C /usr/local/bin -xzf hugo_extended_0.134.1_linux-amd64.tar.gz

export PATH=$PATH:/usr/local/bin/hugo

hugo version

``` 

## Site Setup

### New Site
```
# For a brand new site, you would use

hugo new site quickstart
cd quickstart
git init
cd themes
git submodule add https://github.com/chollinger93/ink-free 

# Then edit the hugo.toml (using the examplesite config.toml as a reference), including social media links, baseURL, page-setup, about.md page and language setting for months

cat > month.yaml << EOF
1: "Jan"
2: "Feb"
3: "Mar"
4: "Apr"
5: "May"
6: "Jun"
7: "Jul"
8: "Aug"
9: "Sep"
10: "Oct"
11: "Nov"
12: "Dec"
EOF
```

## Existing Site
- Simply clone the existing repository into the root folder.
```
# Make sure the submodule is cloned as well for theme

git submodule init
git submodule update
```

- To deploy use `./deploy_hugo.sh` to push any new changes to the Caddy LXC
  - Make sure that the Caddy LXC has rsync installed: 

```
sudo apt update
sudo apt install rsync
```