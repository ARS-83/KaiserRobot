#!/bin/bash

sudo apt update && apt upgrade -y 
sudo apt install python3
sudo apt install pip
sudo apt install git 
git clone https://github.com/ARS-83/KaiserRobot.git

sudo apt-get install nginx

read -p "Please Enter Your Domain : " server_name
output_file="/etc/nginx/sites-enabled/${server_name}"

cat <<EOL > "$output_file"
server {
    listen 80;
    server_name $server_name;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
EOL

output_file="/etc/nginx/sites-available/${server_name}"
cat <<EOL > "$output_file"
...
server_name $server_name;
...
EOL

sudo nginx -t

sudo systemctl reload nginx

sudo ufw status

sudo ufw allow 'Nginx Full'

sudo ufw delete allow 'Nginx HTTP'

sudo certbot --nginx -d $server_name 

sudo certbot renew --dry-run

currentDir=$(basename "$PWD")
cd "/$currentDir/KaiserRobot"
pip install -r requirements.txt
serviceDir="/etc/systemd/system/Kaiser.service"

python_path=$(which python3)
python_version=$($python_path --version 2>&1)
echo "Using Python version: $python_version"

cat <<EOL > "$serviceDir"
[Unit]
Description=Kaiser Telegram Xui Robot
After=multi-user.target
[Service]
Type=simple
Restart=always
WorkingDirectory=/$currentDir/KaiserRobot
ExecStart=$python_path /$currentDir/KaiserRobot/__main__.py
[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable Kaiser.service
sudo systemctl start Kaiser.service
