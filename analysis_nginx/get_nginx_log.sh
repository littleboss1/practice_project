#!/bin/bash
cat /etc/hosts | grep web | awk '{print $2}' >log_host
dd=`date +"%Y_%m_%d"`
log_time=`date +"%Y_%m_%d %H:%M:%S"`
echo " " >total_utl.txt
#access.2019_01_14.log.gz
log_file=`echo "access.$dd.log.gz"`
for machi in $(cat log_host)
do
    echo "$log_time get host $machi" >>/tmp/backup_nginx.log
    scp $machi:/data/log/tengine/$log_file /data/auto_log/data_log/.
    mv data_log/$log_file data_log/$machi-$log_file
    zcat data_log/$machi-$log_file | awk -F "\t" '{print $5,$14}'| awk -v OFS='\t' '{print $2,$1}' >>total_utl.txt
done

echo "delete old  log"
#find data_log/ -mtime +2 -exec rm -rf {} \ ;
./ENV/bin/python clear_ngx_log.py

echo "sen dmail"
./ENV/bin/python sendmail.py > /tmp/sendmail.txt 2>&1
