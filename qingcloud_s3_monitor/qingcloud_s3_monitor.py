#!/usr/bin/env python
#coding=utf-8
#__author__ = "little boss"

import sys
import boto
import random


Rand_num = str(random.random())

def Get_s3server(A,B,C,D):
    conn = boto.connect_s3(aws_access_key_id=A,aws_secret_access_key=B,host=C)
    try:
        if conn.get_bucket(D) is None:
            bucket = conn.create_bucket(D)
        else:
            bucket = conn.get_bucket(D)
        if bucket.get_key('watch_key') is None:
            key = bucket.new_key('watch_key')
            key.set_contents_from_string(Rand_num)
            key_content = key.read().decode()
            key.close()
            conn.close()
        else:
            key = bucket.get_key('watch_key')
            key.set_contents_from_string(Rand_num)
            key_content = key.read().decode()
            key.close()
            conn.close()

        if Rand_num == key_content:
            return 1
        else:
            return 2
    except:
        return 2
        conn.close()


s3_pek3= {"host":"s3.xxx.qingstor.com","ak":"xxx","sk":"xxx","bucket":"xxxbucket"}
s3_gd = {"host":"s3.xxx.qingstor.com","ak":"xxx","sk":"xxx","bucket":"xxxbucket"}


try:
    Argv = sys.argv[1]
except:
    Argv = "stop"

if Argv == "pek3":
    print(Get_s3server(A=s3_pek3['ak'],B=s3_pek3['sk'],C=s3_pek3['host'],D=s3_pek3["bucket"]))
elif Argv == "gd":
    print(Get_s3server(A=s3_gd['ak'],B=s3_gd['sk'],C=s3_gd['host'],D=s3_gd["bucket"]))
else:
    print(2)
