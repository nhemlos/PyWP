# PyWP
Easily create and publish WordPress blog posts via the REST API using Python.  This script lets you automate blog publishing with features like:  ✅ Category &amp; tag creation ✅ Featured image upload ✅ Auto-embed YouTube/TikTok links ✅ Post statuses (publish/draft/scheduled) ✅ .env support for secure credentials
📝 WordPress Auto Poster (Python Script)
This Python script allows you to automatically post articles to your WordPress site using the WordPress REST API. It supports:

1. Category and tag creation

2. Rich post content with embedded video links (YouTube, TikTok, etc.)

3. Featured image uploads (local or URL)

4. Status options (publish, draft, scheduled)

.env file support for credentials

📦 Requirements
Python 3.x

A WordPress site with Application Passwords enabled

.env file with credentials

The following Python packages:

pip install requests python-dotenv
📁 .env File Format
Create a .env file in the same directory as your script and add the following:

WP_SITE=https://your-wordpress-site.com
USERNAME=your_wp_username
APP_PASSWORD=your_app_password
🚀 How to Use
Run the script:

python PyWP.py
Follow the prompts:

Enter the post title

Paste your content (type END on a new line to finish)

Provide an excerpt (optional)

Choose post status (publish, draft, future)

Input tags and categories (comma-separated)

Specify an image path (local file or image URL)

Done!

If successful, the script will display the link to the published post.
📌 Notes
Image uploads only work for local files, not direct URLs.

Make sure your WordPress user has proper permissions to create posts/media.

Application Password must be generated under your user’s Profile → Application Passwords section.
