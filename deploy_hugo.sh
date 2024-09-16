#!/bin/bash

# Step 1: Run Hugo to generate the site
cd /root/jeffdao-blog
hugo --cleanDestinationDir --minify

# Step 2: Use rsync to copy the public directory to Caddy LXC
rsync -avzh --delete /root/jeffdao-blog/public caddy:/var/blog/

# Optional: Print a message when done
echo "Site deployed to Caddy LXC!"
