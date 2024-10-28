---
title: "Hugo install"
date: 2024-10-28
description: ""
tags: [homelab, hugo, documentation]
---

## Pre-reqs for Hugo
```bash
## Git
sudo apt install git-all
git config --global user.email jeffreydao7@gmail.com
git config --global user.name 'Jeffrey Dao'
git config --global init.defaultBranch main

## Go https://go.dev/dl/

wget https://go.dev/dl/go1.23.2.linux-amd64.tar.gz
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.23.2.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

go version

## Dart Sass

wget https://github.com/sass/dart-sass/releases/download/1.80.4/dart-sass-1.80.4-linux-x64.tar.gz
sudo rm -rf /usr/local/dart-sass && sudo tar -C /usr/local -xzf dart-sass-1.80.4-linux-x64.tar.gz
export PATH=$PATH:/usr/local/dart-sass
sass --version

## Hugo

wget https://github.com/gohugoio/hugo/releases/download/v0.136.5/hugo_extended_0.136.5_linux-amd64.deb
sudo dpkg -i hugo_0.136.5_linux-amd64.deb
hugo version

or

wget https://github.com/gohugoio/hugo/releases/download/v0.136.5/hugo_extended_0.136.5_linux-amd64.tar.gz
sudo rm -rf /usr/local/bin/hugo && sudo tar -C /usr/local/bin -xzf hugo_extended_0.136.5_linux-amd64.tar.gz
export PATH=$PATH:/usr/local/bin/hugo
hugo version
``` 

## Site Setup

### New Site
```bash
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
```bash
# Make sure the submodule is cloned as well for theme

git submodule init
git submodule update
```

