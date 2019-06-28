#!/usr/bin/env python
# coding: utf-8

import sys
from rediscluster import StrictRedisCluster

def conn_redis_cluster():
    redis_nodes = [
            {'host':'192.168.100.8','port':6379},
            {'host':'192.168.100.9','port':6380}]
    try:
        redisconn = StrictRedisCluster(startup_nodes=redis_nodes)
    except Exception as e:
        print('error',e)
        sys.exit()

    print(redisconn.get('name1'))
    print(redisconn.get('name2'))



print("start connect redis cluster")
conn_redis_cluster()
