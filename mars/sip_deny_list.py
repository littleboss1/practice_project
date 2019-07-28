#!/usr/bin/env python
#!coding=utf-8

import re
import time
import logging
import subprocess

File="/data/var/mars/deny_address.log"
logging.basicConfig(filename=File,level = logging.INFO,format = '%(asctime)s %(name)s  %(levelname)s  %(message)s')

whilte_list = []
with open('conf/whilte_address.txt','r') as whilte:
    for line in whilte:
        line = line.split('\n')[0]
        whilte_list.append(line)


def add_deny_ip(log_path):
    black_set = set(())
    point = 0
    init_time = time.time()
    while True:
        ips = []
        try:
            with open(log_path) as fs_log:
                fs_log.seek(point)
                for line in fs_log:
                    ip = re.findall(r"Can't find user.* from ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})",line)
                    if ip:
                        ips.append(ip[0])
                        if ips.count(ip[0]) > 20 and ip[0] not in black_set and ip[0] not in whilte_list:
                            black_set.add(ip[0])
                            result = subprocess.check_call("ufw deny from %s to any" % ip[0], shell=True,stdout=open('/data/var/mars/ufw_add.log','a+'))
                            if result == 0:
                                logging.info("将 %s 添加到黑名单列表" % (ip[0]))
                            else:
                                logging.info("将 %s 添加到黑名单列表失败" % (ip[0]))
                point = fs_log.tell()
                #logging.info("当前point是%s" % (point))
                time.sleep(60)
                if len(ips) > 500:
                    ips = []
                    black_set = set(())
        except IOError as e:
            logging.error("发生%s错误" % (e))
            time.sleep(300)
        except KeyboardInterrupt as e:
            logging.warning("黑名单程序退出(exit)")
            break


add_deny_ip("/data/log/freeswitch/freeswitch.log")
