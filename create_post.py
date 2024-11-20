import os
import datetime
import argparse

# Function to create a new Hugo post
def create_post(title, description, base_path="content/posts", images=False):
    # Get the current year and month
    now = datetime.datetime.now()
    year = str(now.year)
    month = f"{now.month:02d}"  # Zero-padded month (e.g., 01, 11)

    # Define the post folder path
    post_path = os.path.join(base_path, year, month, title.lower().replace(" ", "-"))

    # Create the folder structure
    os.makedirs(post_path, exist_ok=True)

    # Create an images folder if required
    if images:
        os.makedirs(os.path.join(post_path, "images"), exist_ok=True)

    # Define YAML front matter
    front_matter = f"""---
title: "{title}"
description: "{description}"
date: "{now.strftime('%Y-%m-%d')}"
tags: []
---
"""

    # Write the index.md file
    with open(os.path.join(post_path, "index.md"), "w") as f:
        f.write(front_matter)

    print(f"Post '{title}' created at: {post_path}")

# Parse command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new Hugo post.")
    parser.add_argument("title", help="The title of the post.")
    parser.add_argument("description", help="The description of the post.")
    parser.add_argument("--base", default="content/posts", help="The base folder for posts.")
    parser.add_argument("--images", action="store_true", help="Include an images folder.")
    args = parser.parse_args()

    create_post(args.title, args.description, args.base, args.images)

# Example usage: python3 create_post.py "My Post Title" "A brief description of my post." --images