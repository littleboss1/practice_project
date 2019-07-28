#!/usr/bin/env bash
###删除日志文件
find /data/var/mars/ -type f -mtime +7 -exec rm -f {} \;
echo "" >/data/var/mars/ufw_add.log

###切换目录
cd /data/var/mars/;
###备份日志
File="deny_address.log_"`date +"%Y-%m-%d"`
cat deny_address.log > $File 
