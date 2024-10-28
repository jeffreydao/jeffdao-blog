#!/bin/bash

# Step 1: Run Hugo to generate the site
cd ~/jeffdao-blog
hugo --cleanDestinationDir --minify

# Step 2: Use rsync to copy the public directory to Caddy LXC
rsync -avzh --delete ~/jeffdao-blog/public jeff@10.0.0.26:/home/jeff/docker/caddy/site
