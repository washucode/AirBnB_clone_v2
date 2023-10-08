#!/usr/bin/env bash
# Script sets up your web servers for the deployment of web_static
#   Install Nginx if it not already installed
#   Create folder /data/web_static/releases/test/ if it doesn’t already exist
#   Create folder /data/web_static/shared/ if it doesn’t already exist
#   Create a fake HTML file /data/web_static/releases/test/index.html 
#           (with simple content, to test your Nginx configuration)
#   Create a symbolic link /data/web_static/current linked to the
#           /data/web_static/releases/test/ folder. If the symbolic
#           link already exists, it should be deleted and recreated
#           every time the script is ran.
#   Give ownership of the /data/ folder to the ubuntu user AND group 
#           (you can assume this user and group exist). This should be
#           recursive; everything inside should be created/owned by this user/group.
#   Update the Nginx configuration to serve the content of /data/web_static/current/
#           to hbnb_static (ex: https://mydomainname.tech/hbnb_static).

# install nginx if not already installed
if ! dpkg -l | grep -q nginx; then
    sudo apt-get -y update
    sudo apt-get -y upgrade
    sudo apt-get -y install nginx
fi

# create folders if they don't exist
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
# give ownership of /data/ to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Define the test index.html content
index_content="This a test page for html file."

# Create or update the index.html page
echo "$index_content" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# create symbolic link
rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# configure nginx
printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4&ab_channel=NyanCat;
    }

    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}" > /etc/nginx/sites-available/default

# Test Nginx configuration for syntax errors
sudo nginx -t

# Restart Nginx to apply the changes
sudo service nginx restart
