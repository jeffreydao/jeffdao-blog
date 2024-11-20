---
title: "Hugo Cheatsheet"
description: "My memory isn't the same as it used to be."
date: "2024-11-20"
tags: [hugo]
---

| **Action**               | **Command**                                                                                                        | **Description**                                                                                           |
|--------------------------|--------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| **Creating New Post**     | `python3 create_post.py "{Title}" "{Description}" --images`                                                         | Creates a new post with the specified title, description, and images.                                      |
| **Deploying Hugo**        | `./deploy_hugo.sh`                                                                                                 | Tells Hugo to generate the site and uses `rsync` to send it to the Caddy host.                            |
| **Shortcode - Images**    | `![{alt text}](images/{image file path} "{caption}\|{caption 2}")`                                                   | Embeds an image with specified alt text, file path, and captions.                                          |
| **Shortcode - YouTube**   | `{{</* youtube id="{youtube link id}" title="{caption}" */>}}`                                                          | Embeds a YouTube video with the provided video ID and caption.                                             |
| **Shortcode - Linking Posts** | `[caption]({{</* ref "/posts/{path to post}" */>}})`                                                                  | Creates a link to another post using the specified path.                                                  |

