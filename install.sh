#!/bin/bash
GREEN='\033[0;32m' 
RED='\033[0;31m' 
NC='\033[0m' # No Color

if [ $(id -u) -ne 0 ]; then
  echo -e "${RED}Please run this script as root or use sudo.${NC}"
  exit 1
fi

sudo apt update && sudo apt upgrade -y 

sudo apt install python3-pip -y

sudo apt install git -y

currentDir=$(basename "$PWD")

ls "$currentDir/KaiserRobot"
if [ $? != 0 ]; then
        echo -e "${RED}Directory KaiserRobot already exists! If installed in your device please update"
        exit 1;
fi


git clone https://github.com/ARS-83/KaiserRobot.git

sudo apt-get install nginx -y

clear


cd "$currentDir/KaiserRobot"

echo -e """${GREEN}
    _    ____  ____  
   / \  |  _ \/ ___| 
  / _ \ | |_) \___ \ 
 / ___ \|  _ < ___) |
/_/   \_\_| \_\____/ 
                     
- - - - - - - - - - -                     
${NC}"""
pip3 install -r requirements.txt

echo -e "${GREEN}Please Enter Your Domain:${NC}"
read -e server_name

echo -e "${GREEN}Please Enter Your UserId Admin:${NC}"
read -e userId

re='^[0-9]+$'
if ! [[ $userId =~ $re ]] ; then
   echo -e "${RED} error: Not a number${NC}" >&2
   exit 1
fi

echo -e "${GREEN}Please Enter Your Bot Token:${NC}"
read -e token

echo -e "${GREEN} Configuration Nginx ... ${NC}"


output_file="/etc/nginx/sites-available/${server_name}"

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

ln -s "/etc/nginx/sites-available/${server_name}" "/etc/nginx/sites-enabled/"

sudo apt install certbot python3-certbot-nginx -y

sudo nginx -t

sudo systemctl reload nginx

sudo ufw status

sudo ufw allow 'Nginx Full'

sudo ufw delete allow 'Nginx HTTP'

sudo certbot --nginx -d $server_name 

sudo certbot renew --dry-run

echo -e "${GREEN} Done.${NC}"

echo -e "${GREEN} Configuration Robot ...${NC}"

cat <<EOL > "$currentDir/KaiserRobot/Config/Config.json" 
{"ownerId": $userId, "SendingPublicMessage": 0, "NumberConfig": 0, "offset": 0,"bot_token" : "$token"}
EOL

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
WorkingDirectory=$currentDir/KaiserRobot
ExecStart=$python_path $currentDir/KaiserRobot/__main__.py
[Install]
WantedBy=multi-user.target
EOL

echo -e "${GREEN} Running Robot ... ${NC}"
sudo systemctl daemon-reload
sudo systemctl enable Kaiser.service
sudo systemctl start Kaiser.service

sudo nohup gunicorn -w 4 -b 127.0.0.1:8000 SubscribeHandler:app & 

clear 
echo -e "${GREEN} Done. Your Robot Is Running ${NC}"
