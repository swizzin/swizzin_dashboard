#!/bin/bash

master=$(cut -d: -f1 < /root/.master.info)

apt-get -y -q install python3-venv git
mkdir -p /opt/swizzin/
python3 -m venv /opt/swizzin/venv
git clone https://github.com/liaralabs/swizzin_dashboard.git /opt/swizzin/swizzin
/opt/swizzin/venv/bin/pip install -r /opt/swizzin/swizzin/requirements.txt
useradd -r swizzin
chown -R swizzin: /opt/swizzin
mkdir -p /etc/nginx/apps

if [[ -f /install/.deluge.lock ]]; then
  touch /install/.delugeweb.lock
fi

if [[ $master == $(id -nu 1000) ]]; then
  :
else
  echo "ADMIN_USER = '$master'" >> /opt/swizzin/swizzin/swizzin.cfg
fi

cat > /etc/nginx/apps/panel.conf <<'EON'
location / {
  #rewrite ^/panel/(.*) /$1 break;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Host $host;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_set_header Origin "";
  proxy_pass http://127.0.0.1:8333;
  proxy_http_version 1.1;
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection "Upgrade";
}
EON

cat > /etc/systemd/system/panel.service <<EOS
[Unit]
Description=swizzin panel service
After=nginx.service

[Service]
Type=simple
User=swizzin

ExecStart=/opt/swizzin/venv/bin/python swizzin.py
WorkingDirectory=/opt/swizzin/swizzin
Restart=on-failure
TimeoutStopSec=300

[Install]
WantedBy=multi-user.target
EOS

cat > /etc/sudoers.d/panel <<EOSUD
#Defaults  env_keep -="HOME"
Defaults:swizzin !logfile
Defaults:swizzin !syslog
Defaults:swizzin !pam_session

Cmnd_Alias   CMNDS = /usr/bin/quota, /bin/systemctl

swizzin     ALL = (ALL) NOPASSWD: CMNDS
EOSUD

systemctl reload nginx
systemctl enable --now panel

