---
title: "Hugo Install"
date: 2024-10-28
description: "Initial setup and notes for Hugo install"
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

## Syncing with Caddy

### Create SSH keypair

- Copy this over to the Ansible host
```bash
ssh-keygen -t ed25519 -C "jeffreydao7@gmail.com"
```

### Syncing changes to Caddy
./deploy_hugo.sh

### Update Caddy

```
blog.jeffdao.com {
    root * /srv/public
    file_server
}
```

## Ansible Playbook
```yaml
---
- name: Install Hugo
  hosts: private-loco  # Replace with your target host or group
  become: true  # Use sudo for installation
  tasks:
    - name: Ensure required packages are installed
      apt:
        name:
          - curl
          - tar
          - git-all
        state: present
        update_cache: yes

    - name: Configure Git user email
      git_config:
        name: user.email
        value: "jeffreydao7@gmail.com"

    - name: Configure Git user name
      git_config:
        name: user.name
        value: "Jeffrey Dao"

    - name: Configure Git default branch name
      git_config:
        name: init.defaultBranch
        value: "main"

    - name: Get the latest Dart Sass release information
      uri:
        url: https://api.github.com/repos/sass/dart-sass/releases/latest
        return_content: yes
      register: dart_sass_release

    - name: Set download URL for the latest Linux x64 Dart Sass
      set_fact:
        dart_sass_url: "{{ (dart_sass_release.json.assets | selectattr('name', 'match', 'dart-sass-.*-linux-x64.tar.gz') | first).url }}"

    - name: Download Dart Sass
      get_url:
        url: "{{ dart_sass_url }}"
        dest: /tmp/dart-sass-linux-x64.tar.gz
        headers:
          Accept: application/octet-stream  # To get the raw file

    - name: Remove existing Dart Sass directory
      file:
        path: /usr/local/dart-sass
        state: absent

    - name: Extract Dart Sass
      unarchive:
        src: /tmp/dart-sass-linux-x64.tar.gz
        dest: /usr/local
        remote_src: yes

    - name: Add Dart Sass to PATH
      lineinfile:
        path: /etc/profile.d/dart-sass.sh
        line: 'export PATH=$PATH:/usr/local/dart-sass'
        create: yes

    - name: Clean up
      file:
        path: /tmp/dart-sass-linux-x64.tar.gz
        state: absent

    - name: Get the latest Go release information
      uri:
        url: https://go.dev/dl/
        return_content: yes
      register: go_release_page

    - name: Set download URL for the latest Go version
      set_fact:
        go_url: "https://go.dev{{ (go_release_page.content | regex_search('/dl/go[0-9]+\\.[0-9]+\\.[0-9]+\\.linux-amd64\\.tar\\.gz')) }}"
  
    - name: Debug Go URL
      debug:
        var: go_url  # Display the extracted URL

    - name: Download Go
      get_url:
        url: "{{ go_url }}"
        dest: /tmp/go.linux-amd64.tar.gz
        headers:
          Accept: application/octet-stream  # To get the raw file

    - name: Remove existing Go directory
      file:
        path: /usr/local/go
        state: absent

    - name: Extract Go
      unarchive:
        src: /tmp/go.linux-amd64.tar.gz
        dest: /usr/local
        remote_src: yes

    - name: Add Go to PATH
      lineinfile:
        path: /etc/profile.d/go.sh
        line: 'export PATH=$PATH:/usr/local/go/bin'
        create: yes

    - name: Clean up
      file:
        path: /tmp/go.linux-amd64.tar.gz
        state: absent

    - name: Get the latest Hugo release from GitHub API
      uri:
        url: https://api.github.com/repos/gohugoio/hugo/releases/latest
        return_content: yes
      register: hugo_release

    - name: Set download URL for Hugo extended
      set_fact:
        hugo_download_url: "{{ (hugo_release.json.assets | selectattr('name', 'match', 'hugo_extended_.*_Linux-64bit.tar.gz') | first).browser_download_url }}"

    - name: Debug Hugo URL
      debug:
        var: hugo_download_url  # Display the extracted URL

    - name: Download Hugo
      get_url:
        url: "{{ hugo_download_url }}"
        dest: /tmp/hugo_extended_linux-amd64.tar.gz
        headers:
          Accept: application/octet-stream  # To get the raw file

    - name: Remove existing Hugo directory
      file:
        path: /usr/local/bin/hugo
        state: absent

    - name: Extract Hugo
      unarchive:
        src: /tmp/hugo_extended_linux-amd64.tar.gz
        dest: /usr/local/bin
        remote_src: yes
        
    - name: Update PATH
      lineinfile:
        path: /etc/profile
        line: 'export PATH=$PATH:/usr/local/bin/hugo'
        state: present
    - name: Clean up
      file:
        path: /tmp/hugo_extended_linux-amd64.tar.gz
        state: absent
```
