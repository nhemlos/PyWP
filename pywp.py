import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# WordPress Site Configuration
WP_SITE = os.getenv("WP_SITE")
USERNAME = os.getenv("USERNAME")
APP_PASSWORD = os.getenv("APP_PASSWORD")

if not WP_SITE or not USERNAME or not APP_PASSWORD:
    print("❌ Please set WP_SITE, USERNAME, and APP_PASSWORD in the .env file.")
    exit(1)

# Post Details
title = input("Enter the post title: ")
print("Enter your post content. You can paste video URLs (YouTube, TikTok, etc.) to auto-embed them. Type END on a new line to finish:")
lines = []
while True:
    line = input()
    if line.strip().upper() == "END":
        break
    lines.append(line)
content = "\n".join(lines)

excerpt = input("Enter the post excerpt (optional, press Enter to skip): ")
status = input("Enter the post status (publish, draft, future): ").lower()

# Tags and Categories
tags = input("Enter tags (comma-separated, e.g., python, automation): ").split(',')
categories = input("Enter categories (comma-separated, e.g., Tutorials, Python Scripts): ").split(',')

# Featured Image
image_path = input("Enter the path to the local image file (or URL to an image): ")

# Step 1: Get or Create Category IDs
def get_or_create_category(category_names):
    category_ids = []
    for category in category_names:
        category = category.strip()
        response = requests.get(
            f"{WP_SITE}/wp-json/wp/v2/categories",
            auth=HTTPBasicAuth(USERNAME, APP_PASSWORD),
            params={"search": category}
        )
        if response.status_code == 200:
            categories_data = response.json()
            if categories_data:
                category_ids.append(categories_data[0]['id'])
            else:
                create_response = requests.post(
                    f"{WP_SITE}/wp-json/wp/v2/categories",
                    auth=HTTPBasicAuth(USERNAME, APP_PASSWORD),
                    json={"name": category}
                )
                if create_response.status_code == 201:
                    category_ids.append(create_response.json()['id'])
                    print(f"✅ Category '{category}' created.")
                else:
                    print(f"❌ Failed to create category '{category}': {create_response.text}")
        else:
            print(f"❌ Failed to fetch category '{category}': {response.status_code}")
    return category_ids

# Step 2: Get or Create Tag IDs
def get_or_create_tag(tag_names):
    tag_ids = []
    for tag in tag_names:
        tag = tag.strip()
        response = requests.get(
            f"{WP_SITE}/wp-json/wp/v2/tags",
            auth=HTTPBasicAuth(USERNAME, APP_PASSWORD),
            params={"search": tag}
        )
        if response.status_code == 200:
            tags_data = response.json()
            if tags_data:
                tag_ids.append(tags_data[0]['id'])
            else:
                create_response = requests.post(
                    f"{WP_SITE}/wp-json/wp/v2/tags",
                    auth=HTTPBasicAuth(USERNAME, APP_PASSWORD),
                    json={"name": tag}
                )
                if create_response.status_code == 201:
                    tag_ids.append(create_response.json()['id'])
                    print(f"✅ Tag '{tag}' created.")
                else:
                    print(f"❌ Failed to create tag '{tag}': {create_response.text}")
        else:
            print(f"❌ Failed to fetch tag '{tag}': {response.status_code}")
    return tag_ids

# Step 3: Upload Image (if it's a local file)
def upload_image(image_path):
    if os.path.isfile(image_path):
        with open(image_path, 'rb') as img:
            media = {'file': img}
            response = requests.post(
                f"{WP_SITE}/wp-json/wp/v2/media",
                auth=HTTPBasicAuth(USERNAME, APP_PASSWORD),
                files=media,
                headers={"Content-Disposition": f"attachment; filename={os.path.basename(image_path)}"}
            )
            if response.status_code == 201:
                return response.json()['id']
            else:
                print(f"❌ Failed to upload image: {response.text}")
    return None

category_ids = get_or_create_category(categories)
tag_ids = get_or_create_tag(tags)
featured_image_id = upload_image(image_path)

# Prepare the post data
post = {
    "title": title,
    "content": content,
    "excerpt": excerpt,
    "status": status,
    "tags": tag_ids,
    "categories": category_ids
}

if featured_image_id:
    post['featured_media'] = featured_image_id

# Step 4: Create the Post
response = requests.post(
    f"{WP_SITE}/wp-json/wp/v2/posts",
    auth=HTTPBasicAuth(USERNAME, APP_PASSWORD),
    json=post
)

if response.status_code == 201:
    print(f"✅ Post published successfully: {response.json().get('link')}")
else:
    print(f"❌ Failed to publish post: {response.status_code} - {response.text}")
