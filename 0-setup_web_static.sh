<<<<<<< HEAD
#!/usr/bin/env bash
# Script sets up your web servers for the deployment of web_static

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
index_content="<html>
    <head>
    </head>
    <body>
    Holberton School
    </body>
</html>"


# Create or update the index.html page
echo "$index_content" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# create symbolic link
sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Configure Nginx
nginx_config="server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$HOSTNAME;
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
}"

# Update the Nginx configuration using the provided block
echo "$nginx_config" | sudo tee /etc/nginx/sites-available/default > /dev/null

# Test Nginx configuration for syntax errors
sudo nginx -t

# Restart Nginx to apply the changes
=======
#!/usr/bin/env/bash
# Script that sets up your web servers for the deployment of web_static

sudo apt-get update
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sudo sed -i '42i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Restart nginx
>>>>>>> d96a6a9 (task 0)
sudo service nginx restart
