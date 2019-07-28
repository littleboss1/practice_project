#!/bin/bash
apt-get install ufw
ufw allow from 192.168.0.0/16 to any port 22
ufw default allow
ufw enable
ufw reload
mkdir /data/var/mars
/srv/zabbix/script/add_cron.py "mars checker" "30 01 */1 * * /srv/mars/plan.sh > /dev/null 2>&1 &"
